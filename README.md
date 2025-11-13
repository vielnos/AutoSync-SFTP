🔥 AutoSync – SFTP Auto Sync \& File Change Tracker



AutoSync is a lightweight, configurable Python tool that automates SFTP → Local folder syncing, detects new or modified files, generates an Excel audit report, and sends a notification email — all without manual effort.



This tool is perfect for:



Audit \& compliance teams



Data engineering



DevOps



Financial operations



Anyone managing recurring SFTP file downloads



🚀 Features



🔄 Automatically sync files from SFTP → Local (via WinSCP)



📁 Detect new files vs previous sync



📝 Generate Excel reports:



New Data



Old Data



New Files



✉️ Send email notifications with attached Excel report



⚙️ Fully configurable using config.json



🔒 Credentials stored externally (never in code)



🪶 Lightweight and easy to deploy



📂 Folder Structure

Sync/

│

├── SFTP Auto Sync Tool.py   # Main script

├── README.md                # Documentation

├── .gitignore               # Prevents secret file upload

├── config.json              # Local configuration (ignored by Git)

└── config.json.example      # Safe template for GitHub



⚙️ Installation

1\) Clone the repository

git clone https://github.com/<your-username>/AutoSync.git

cd AutoSync



2\) Install dependencies

pip install pandas openpyxl



3\) Install WinSCP



Download here:

https://winscp.net/eng/download.php



Then update the path in config.json → winscp\_path.



🛠 Configuration



The tool uses config.json for all credentials \& settings.

This file MUST exist in the same folder as the Python script.



⚠️ Never upload config.json to GitHub. Only upload config.json.example.



👉 Example: config.json.example (safe for GitHub)

{

&nbsp; "sftp": {

&nbsp;   "host": "your-sftp-host",

&nbsp;   "port": 22,

&nbsp;   "username": "your-username",

&nbsp;   "password": "your-password",

&nbsp;   "remote\_directory": "/remote/folder/path"

&nbsp; },

&nbsp; "local": {

&nbsp;   "local\_directory": "C:/SyncFolder",

&nbsp;   "winscp\_path": "C:/Program Files (x86)/WinSCP/WinSCP.com",

&nbsp;   "report\_name": "sync\_report.xlsx"

&nbsp; },

&nbsp; "email": {

&nbsp;   "sender": "sender@gmail.com",

&nbsp;   "receiver": "receiver@example.com",

&nbsp;   "password": "your-gmail-app-password"

&nbsp; }

}





Users should copy this file, rename to config.json, and fill real credentials.



▶️ How to Run

python "SFTP Auto Sync Tool.py"





The system will:



Connect to the SFTP server



Sync all files to local folder



Compare old vs new data



Generate an Excel audit report



Email the results



📊 Excel Report Output

Sheet: New Data



| Folder Path | File Name | Last Modified | Matched | Match Time |



Sheet: Old Data



| Folder Path | File Name | Last Modified | Matched |



Sheet: New Files



(New files detected since previous sync)



🧱 Architecture Diagram (ASCII)

&nbsp;          ┌──────────────────────┐

&nbsp;          │      SFTP Server     │

&nbsp;          └──────────┬───────────┘

&nbsp;                     │

&nbsp;            (Synchronize via WinSCP)

&nbsp;                     │

&nbsp;                     ▼

&nbsp;          ┌──────────────────────┐

&nbsp;          │   Local Sync Folder  │

&nbsp;          └──────────┬───────────┘

&nbsp;                     │

&nbsp;              (File Scanner)

&nbsp;                     │

&nbsp;                     ▼

&nbsp;          ┌──────────────────────┐

&nbsp;          │   Change Detector     │

&nbsp;          └──────────┬───────────┘

&nbsp;                     │

&nbsp;            (Generate Excel Report)

&nbsp;                     │

&nbsp;                     ▼

&nbsp;          ┌──────────────────────┐

&nbsp;          │ Email Notification   │

&nbsp;          └──────────────────────┘



📅 Roadmap

v1.0



✔ SFTP sync

✔ File comparison

✔ Excel report generation

✔ Email alerts

✔ Config-driven



v1.1 (Planned)



⬜ OneDrive / Google Drive sync

⬜ Logging system (logs folder)

⬜ CLI commands

⬜ GUI version

⬜ Scheduled sync (cron).



📜 License



MIT License — free to use \& modify.



⭐ Support



If you find this tool useful, please star ⭐ the repository!

