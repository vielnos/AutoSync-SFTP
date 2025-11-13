#!/usr/bin/env python
# coding: utf-8

# In[9]:


import os
import subprocess
import pandas as pd
from datetime import datetime
import smtplib
import json

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

# --------------------------------------------------
# Load configuration from external JSON file
# --------------------------------------------------
CONFIG_PATH = "config.json"

if not os.path.exists(CONFIG_PATH):
    raise Exception("❌ config.json not found. Please create it before running the script.")

with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

# -----------------------------
# 🔹 Config Values
# -----------------------------
host = config["sftp"]["host"]
port = config["sftp"]["port"]
username = config["sftp"]["username"]
password = config["sftp"]["password"]
remote_directory = config["sftp"]["remote_directory"]

local_directory = config["local"]["local_directory"]
winscp_path = config["local"]["winscp_path"]
report_excel = os.path.join(local_directory, config["local"]["report_name"])

sender_email = config["email"]["sender"]
receiver_email = config["email"]["receiver"]
email_password = config["email"]["password"]

os.makedirs(local_directory, exist_ok=True)

# --------------------------------------------------
# Function: Send email with Excel attachment
# --------------------------------------------------
def send_email(filepath, new_files_count, total_files, old_count):
    subject = f"Sync Report – {datetime.now().strftime('%d-%b-%Y %H:%M')}"
    body = f"""
Hello,

Your automated SFTP sync has been completed successfully.

📁 Synced Folder: {local_directory}
📊 Report: {os.path.basename(filepath)}
🕒 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📈 Previous File Count: {old_count}
📈 Current File Count: {total_files}
🆕 New Files Added: {new_files_count}

Best regards,
AutoSync System
"""

    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Attach Excel report
        with open(filepath, "rb") as file:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(file.read())

        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f'attachment; filename="{os.path.basename(filepath)}"')
        msg.attach(part)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, email_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())

        print("📧 Email sent successfully.")
    except Exception as e:
        print("⚠️ Email sending failed:", e)

# --------------------------------------------------
# STEP 1: Load Old Sync Data
# --------------------------------------------------
df_old = pd.DataFrame(columns=["Folder Path", "File Name", "Last Modified", "Matched"])

if os.path.exists(report_excel):
    try:
        xl = pd.ExcelFile(report_excel)

        if "New Data" in xl.sheet_names:
            df_old = xl.parse("New Data")
            df_old.columns = df_old.columns.astype(str).str.strip()

        elif "Old Data" in xl.sheet_names:
            df_old = xl.parse("Old Data")

        print("✔ Loaded baseline (Old Data).")

    except Exception as e:
        print("⚠️ Error reading existing report. Starting fresh:", e)

old_count = len(df_old)

# --------------------------------------------------
# STEP 2: Sync using WinSCP
# --------------------------------------------------
winscp_script = f"""
option batch on
option confirm off
option transfer binary
open sftp://{username}:{password}@{host}:{port}/
synchronize local "{local_directory}" "{remote_directory}"
exit
"""

with open("sync_script.txt", "w") as f:
    f.write(winscp_script)

print("⬇️ Running WinSCP sync...")
subprocess.run(f'"{winscp_path}" /script="sync_script.txt"', shell=True)
print("✅ SFTP sync completed.")

# --------------------------------------------------
# STEP 3: Scan synced files
# --------------------------------------------------
synced_files = []

for root, dirs, files in os.walk(local_directory):
    for file in files:
        full_path = os.path.join(root, file)
        last_modified = datetime.fromtimestamp(os.path.getmtime(full_path)).strftime("%Y-%m-%d %H:%M:%S")

        synced_files.append({
            "Folder Path": root,
            "File Name": file,
            "Last Modified": last_modified
        })

df = pd.DataFrame(synced_files)

if df.empty:
    print("⚠ No files found after sync.")
    exit()

# Internal keys for matching
df["File Path Key"] = (df["Folder Path"] + "\\" + df["File Name"]).str.lower()
df_old["File Path Key"] = (df_old["Folder Path"] + "\\" + df_old["File Name"]).str.lower()

df["key_full"] = df["File Path Key"] + "||" + df["Last Modified"]
df_old["key_full"] = df_old["File Path Key"] + "||" + df_old["Last Modified"]

# --------------------------------------------------
# STEP 4: Compare Old vs New
# --------------------------------------------------
old_paths = set(df_old["File Path Key"])
old_keys = set(df_old["key_full"])

df["Matched"] = df["File Path Key"].apply(lambda x: "False" if x not in old_paths else "True")
df["Match Time"] = df["key_full"].apply(lambda x: "TRUE" if x in old_keys else "FALSE")

new_files_count = (df["Matched"] == "False").sum()
total_files = len(df)

df_new = df[df["Matched"] == "False"]

# --------------------------------------------------
# CLEAN OUTPUT — Only Export User-Friendly Columns
# --------------------------------------------------
safe_columns = ["Folder Path", "File Name", "Last Modified", "Matched", "Match Time"]

df_export = df[safe_columns].copy()
df_old_export = df_old[["Folder Path", "File Name", "Last Modified", "Matched"]].copy()
df_new_export = df_new[["Folder Path", "File Name", "Last Modified", "Matched"]].copy()

# --------------------------------------------------
# STEP 5: Write Excel Report
# --------------------------------------------------
with pd.ExcelWriter(report_excel, engine="openpyxl", mode="w") as writer:
    df_export.to_excel(writer, index=False, sheet_name="New Data")
    df_old_export.to_excel(writer, index=False, sheet_name="Old Data")
    if not df_new_export.empty:
        df_new_export.to_excel(writer, index=False, sheet_name="New Files")

print("📄 Excel report generated.")
print(f"📈 Previous: {old_count}, Current: {total_files}, New: {new_files_count}")

# --------------------------------------------------
# STEP 6: Email Report
# --------------------------------------------------
send_email(report_excel, new_files_count, total_files, old_count)
print("✅ Process Complete.")

