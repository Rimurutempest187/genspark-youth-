# Church Community Telegram Bot - Project Structure

## Files Overview

```
church_bot/
│
├── bot.py                  # Main bot application (33 KB)
│   └── Complete bot logic with all features
│
├── requirements.txt        # Python dependencies
│   ├── python-telegram-bot==20.7
│   ├── python-dotenv==1.0.0
│   └── pytz==2023.3
│
├── .env.example           # Environment variables template
│   └── Template for BOT_TOKEN and ADMIN_IDS
│
├── README.md              # Quick start guide (6.5 KB)
│   └── Installation and basic usage
│
├── DOCUMENTATION.md       # Complete documentation (12.8 KB)
│   └── Detailed guide for admins and users
│
├── setup.py              # Interactive setup script
│   └── Automated configuration helper
│
├── start.sh              # Linux/Mac startup script
│   └── Automated installation and startup
│
├── start.bat             # Windows startup script
│   └── Automated installation and startup
│
├── .gitignore            # Git ignore rules
│   └── Excludes .env, bot_data.json, etc.
│
└── bot_data.json         # Data storage (auto-created)
    └── Stores all bot data in JSON format

```

## File Descriptions

### Core Files

**bot.py** (33 KB)
- Main application with all bot logic
- Handles all commands and features
- Includes conversation handlers
- Auto-saves data to JSON
- Ready to run out of the box

**requirements.txt** (60 bytes)
- Python dependencies list
- Compatible with pip
- Minimal dependencies

### Configuration Files

**.env.example** (266 bytes)
- Template for environment variables
- Copy to .env and fill in values
- Contains BOT_TOKEN and ADMIN_IDS

**.env** (not included)
- Your actual configuration
- Created from .env.example
- MUST be created before running

### Documentation Files

**README.md** (6.5 KB)
- Quick start guide
- Installation instructions
- Command reference
- Basic troubleshooting

**DOCUMENTATION.md** (12.8 KB)
- Complete user guide
- Detailed admin guide
- Advanced configuration
- Comprehensive troubleshooting
- FAQ section
- Best practices

### Setup Files

**setup.py** (3.4 KB)
- Interactive setup script
- Prompts for configuration
- Creates initial data file
- Python script for all platforms

**start.sh** (1.5 KB)
- Linux/Mac startup script
- Checks dependencies
- Installs requirements
- Starts the bot
- Executable: chmod +x start.sh

**start.bat** (1.2 KB)
- Windows startup script
- Checks Python installation
- Installs dependencies
- Starts the bot
- Double-click to run

### Other Files

**.gitignore** (681 bytes)
- Git ignore rules
- Excludes sensitive files
- Excludes generated files
- Safe for version control

**bot_data.json** (auto-created)
- JSON data storage
- Created on first run
- Contains all bot data
- Backed up with /backup command

## Installation Methods

### Method 1: Quick Start (Recommended)
```bash
# Linux/Mac
chmod +x start.sh
./start.sh

# Windows
start.bat
```

### Method 2: Interactive Setup
```bash
python setup.py
python bot.py
```

### Method 3: Manual Setup
```bash
pip install -r requirements.txt
cp .env.example .env
nano .env  # Add credentials
python bot.py
```

## Features Checklist

✅ User Commands
- [x] /start - Welcome message
- [x] /about - Church information
- [x] /contact - Contact numbers
- [x] /verse - Daily Bible verse
- [x] /events - Upcoming events
- [x] /birthday - Monthly birthdays
- [x] /pray - Submit prayer requests
- [x] /quiz - Take Bible quiz
- [x] /tops - Quiz leaderboard
- [x] /report - Report issues

✅ Admin Commands
- [x] /edit - Admin menu
- [x] /edabout - Edit church info
- [x] /edcontact - Add contacts
- [x] /edverse - Add verses
- [x] /edevents - Add events
- [x] /edbirthday - Add birthdays
- [x] /edquiz - Add quizzes
- [x] /praylist - View prayers
- [x] /set - Set quiz threshold
- [x] /broadcast - Send to all groups
- [x] /stats - Bot statistics
- [x] /backup - Backup data
- [x] /restore - Restore data
- [x] /delete - Delete specific data
- [x] /allclear - Clear all data

✅ Features
- [x] Auto quiz on message count
- [x] Random daily verses
- [x] Quiz scoring system
- [x] Prayer request tracking
- [x] Birthday reminders
- [x] Event management
- [x] Multi-group support
- [x] Data persistence
- [x] Backup/Restore
- [x] Broadcast messaging
- [x] User tracking
- [x] Admin controls
- [x] Burmese language support
- [x] Interactive buttons
- [x] Conversation handlers

## System Requirements

- **Python**: 3.8 or higher
- **RAM**: 128 MB minimum
- **Disk**: 10 MB minimum
- **Network**: Internet connection
- **OS**: Linux, Mac, or Windows

## Dependencies

```
python-telegram-bot==20.7  # Telegram Bot API
python-dotenv==1.0.0       # Environment variables
pytz==2023.3               # Timezone support
```

## Data Storage

All data is stored in `bot_data.json`:
- Church about information
- Contact numbers
- Bible verses
- Events
- Birthdays
- Prayer requests
- Quizzes and answers
- Quiz scores
- Message counts
- User IDs
- Group IDs

## Security Notes

🔒 **Important:**
- Never share .env file
- Keep backup files secure
- Only add trusted admins
- Regular backups recommended
- Bot data contains user information

## Support

**Created by: PINLON-YOUTH**

For help:
1. Read README.md
2. Check DOCUMENTATION.md
3. Review troubleshooting section
4. Check code comments

## License

Free to use for church communities.
Created by: PINLON-YOUTH

---

**God Bless! 🙏**
