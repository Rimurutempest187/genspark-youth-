# Church Community Bot - Complete Documentation
**Created by: PINLON-YOUTH**

## Table of Contents
1. [Quick Start Guide](#quick-start-guide)
2. [Detailed Setup](#detailed-setup)
3. [Command Reference](#command-reference)
4. [Admin Guide](#admin-guide)
5. [User Guide](#user-guide)
6. [Troubleshooting](#troubleshooting)

---

## Quick Start Guide

### Step 1: Get Your Bot Token
1. Open Telegram
2. Search for `@BotFather`
3. Send `/newbot`
4. Choose a name for your bot (e.g., "My Church Bot")
5. Choose a username (must end with 'bot', e.g., "mychurch_bot")
6. Copy the token provided

### Step 2: Get Your User ID
1. Search for `@userinfobot` on Telegram
2. Send any message
3. Copy your User ID (numbers only)

### Step 3: Install and Run
```bash
# Install dependencies
pip install -r requirements.txt

# Run setup
python setup.py

# Or manually create .env file
cp .env.example .env
nano .env  # Add your BOT_TOKEN and ADMIN_IDS

# Start the bot
python bot.py
```

---

## Detailed Setup

### Requirements
- Python 3.8 or higher
- pip (Python package manager)
- Internet connection
- Telegram account

### Installation Methods

#### Method 1: Automated Setup (Recommended)
```bash
# Linux/Mac
chmod +x start.sh
./start.sh

# Windows
start.bat
```

#### Method 2: Manual Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env file
cp .env.example .env

# 3. Edit .env file with your credentials
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
ADMIN_IDS=123456789,987654321

# 4. Run the bot
python bot.py
```

#### Method 3: Interactive Setup
```bash
python setup.py
# Follow the prompts to enter your bot token and admin IDs
```

---

## Command Reference

### User Commands

| Command | Description | Usage Example |
|---------|-------------|---------------|
| `/start` | Start the bot and see welcome message | `/start` |
| `/about` | View church information | `/about` |
| `/contact` | View contact numbers | `/contact` |
| `/verse` | Get daily Bible verse | `/verse` |
| `/events` | View upcoming events | `/events` |
| `/birthday` | View this month's birthdays | `/birthday` |
| `/pray` | Submit prayer request | `/pray Please pray for my family` |
| `/quiz` | Take a Bible quiz | `/quiz` |
| `/tops` | View quiz leaderboard | `/tops` |
| `/report` | Report an issue | `/report The verse command is not working` |

### Admin Commands

| Command | Description | Usage Example |
|---------|-------------|---------------|
| `/edit` | View admin command list | `/edit` |
| `/edabout` | Edit church information | `/edabout` |
| `/edcontact` | Add contact numbers | `/edcontact` |
| `/edverse` | Add Bible verses | `/edverse` |
| `/edevents` | Add events | `/edevents` |
| `/edbirthday` | Add birthdays | `/edbirthday` |
| `/edquiz` | Add quizzes | `/edquiz` |
| `/praylist` | View prayer requests | `/praylist` |
| `/set` | Set quiz threshold | `/set 10` |
| `/broadcast` | Send message to all groups | `/broadcast` |
| `/stats` | View bot statistics | `/stats` |
| `/backup` | Backup bot data | `/backup` |
| `/restore` | Restore bot data | `/restore` |
| `/delete` | Delete specific data | `/delete verse 1` |
| `/allclear` | Clear all data | `/allclear` |

---

## Admin Guide

### Adding Church Information
```
Command: /edabout

Then type your church information:

ကျွန်ုပ်တို့၏အသင်းတော်သည် ၁၉၉၅ ခုနှစ်တွင် တည်ထောင်ခဲ့ပြီး 
လူငယ်များအား ယေရှုခရစ်တော်နှင့် ပိုမိုနီးကပ်စေရန် ရည်ရွယ်ပါသည်။

Send and the information will be saved.
```

### Adding Multiple Contacts
```
Command: /edcontact

Format: Name - Phone Number (one per line)

ဦးအောင်အောင် - 09123456789
မမမမ - 09987654321
ဦးသန်းသန်း - 09456789123

Send all at once.
```

### Adding Bible Verses
```
Command: /edverse

Format: Verse - Reference (one per line)

တရားတော်သည် ငါ့ခြေ၌ မီးခွက်ဖြစ်၍ - ဆာလံ ၁၁၉:၁၀၅
သင်တို့သည် ငါ့ကိုခေါ်၍ ဆုတောင်းသောအခါ - ယေရမိ ၂၉:၁၂

Send all at once.
```

### Adding Quizzes
```
Command: /edquiz

Format (separate each quiz with a blank line):

လောကကို ဖန်ဆင်းခဲ့သူမှာ မည်သူနည်း?
A) မောရှေ
B) ယေရှု
C) ဘုရားသခင်
D) အာဗြဟံ
အဖြေ: C

ကယ်တင်ရှင်မည်သူနည်း?
A) ယောန
B) ဒါဝိဒ်
C) ယေရှုခရစ်တော်
D) ပေတရု
အဖြေ: C

Send all at once.
```

### Adding Events
```
Command: /edevents

Format: YYYY-MM-DD - Event Name (one per line)

2024-12-25 - ခရစ္စမတ်ပွဲတော်
2024-12-31 - နှစ်သစ်ကူးဆုတောင်းပွဲ
2025-01-15 - လူငယ်စခန်း

Send all at once.
```

### Adding Birthdays
```
Command: /edbirthday

Format: M-D - Name (one per line)

1-15 - မောင်မောင်
3-20 - မမမ
6-10 - ကိုကို
12-25 - စုစု

Send all at once.
```

### Setting Auto Quiz Threshold
```
Command: /set 10

The quiz will automatically appear after 10 messages in the group.
You can set any number you want.
```

### Broadcasting Messages
```
Command: /broadcast

Then send either:
1. Text message
2. Photo with caption

The message will be sent to all groups where the bot is present.
```

### Viewing Prayer Requests
```
Command: /praylist

Shows the last 20 prayer requests with:
- Username
- Prayer text
- Date and time
```

### Data Management

#### Backup Data
```
Command: /backup

Sends you a JSON file with all bot data.
Save this file safely!
```

#### Restore Data
```
Command: /restore

Then send the backup JSON file.
All data will be restored from the file.
```

#### Delete Specific Data
```
Commands:
/delete verse 1    - Delete 1st verse
/delete quiz 2     - Delete 2nd quiz
/delete event 3    - Delete 3rd event
/delete contact 1  - Delete 1st contact
/delete birthday 2 - Delete 2nd birthday

Numbers start from 1.
```

#### Clear All Data
```
Command: /allclear

WARNING: This will delete ALL data!
Confirmation button will appear before deletion.
```

---

## User Guide

### Getting Started
1. Find your church bot on Telegram
2. Send `/start` to begin
3. You'll see a welcome message with available commands

### Reading Daily Verse
```
/verse

The bot will send a random Bible verse.
Morning: 🌅 မင်္ဂလာနံနက်ခင်းပါ
Evening: 🌙 မင်္ဂလာညပါ
```

### Submitting Prayer Requests
```
/pray Your prayer request here

Example:
/pray ကျွန်တော့်မိသားစုအတွက် ကျန်းမာရေးကောင်းမွန်ပါစေ

You'll receive a confirmation message.
```

### Taking Quizzes
```
Method 1: Manual
/quiz - Take a quiz anytime

Method 2: Automatic
Quiz appears automatically after X messages in the group
(X is set by admin with /set command)

How to answer:
- Click A, B, C, or D button
- Immediate feedback
- Score is tracked automatically
```

### Viewing Leaderboard
```
/tops

Shows top 10 quiz scorers:
🥇 1st place
🥈 2nd place
🥉 3rd place
4. and below
```

### Reporting Issues
```
/report Your issue description

Example:
/report The quiz feature is not working properly

Admin will receive your report with your username and user ID.
```

---

## Troubleshooting

### Bot Not Responding

**Problem:** Bot doesn't reply to commands

**Solutions:**
1. Check if bot is running:
   ```bash
   # Should show bot.py process
   ps aux | grep bot.py
   ```

2. Check .env file:
   ```bash
   cat .env
   # Verify BOT_TOKEN is correct
   ```

3. Check bot logs:
   ```bash
   python bot.py
   # Look for error messages
   ```

4. Restart the bot:
   ```bash
   # Stop (Ctrl+C) and restart
   python bot.py
   ```

### Commands Not Working for Admin

**Problem:** Admin commands show "You are not admin"

**Solutions:**
1. Verify your User ID:
   - Message @userinfobot on Telegram
   - Copy your User ID

2. Check .env file:
   ```bash
   cat .env
   # Should show: ADMIN_IDS=123456789,987654321
   ```

3. Update .env if needed:
   ```bash
   nano .env
   # Add your User ID to ADMIN_IDS
   ```

4. Restart bot after changing .env

### Quiz Not Auto-Dropping

**Problem:** Quiz doesn't appear automatically

**Solutions:**
1. Check threshold setting:
   ```
   /set 10
   ```

2. Verify quizzes exist:
   ```
   /stats (admin only)
   # Check "Quizzes: X"
   ```

3. Add quizzes if none exist:
   ```
   /edquiz
   ```

4. Reset message count:
   - Send /allclear (clears everything)
   - Or manually edit bot_data.json

### Data Lost

**Problem:** All data disappeared

**Solutions:**
1. Check if bot_data.json exists:
   ```bash
   ls -la bot_data.json
   ```

2. Restore from backup:
   ```
   /restore
   # Then send backup file
   ```

3. If no backup:
   - Data is permanently lost
   - Start fresh with /edabout, /edverse, etc.
   - Remember to backup regularly with /backup

### Broadcast Not Working

**Problem:** Messages not sent to groups

**Solutions:**
1. Check if bot is admin in groups:
   - Go to each group
   - Check bot permissions
   - Make bot admin

2. Check if groups are tracked:
   ```
   /stats
   # Check "Groups: X"
   ```

3. If groups not tracked:
   - Have someone in the group send /start
   - Or any command to the bot

### Permission Errors

**Problem:** "Bot was kicked from group" or similar

**Solutions:**
1. Re-add bot to group:
   - Remove bot from group
   - Add bot back
   - Make bot admin

2. Grant necessary permissions:
   - Send messages
   - Read messages
   - Delete messages (optional)

### Installation Issues

**Problem:** pip install fails

**Solutions:**
1. Update pip:
   ```bash
   pip install --upgrade pip
   ```

2. Use pip3 instead:
   ```bash
   pip3 install -r requirements.txt
   ```

3. Install with user flag:
   ```bash
   pip install --user -r requirements.txt
   ```

4. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

### Python Version Issues

**Problem:** "Python version not supported"

**Solutions:**
1. Check Python version:
   ```bash
   python --version
   # or
   python3 --version
   ```

2. Install Python 3.8+:
   - Visit python.org
   - Download Python 3.8 or higher
   - Install with pip included

3. Use python3 explicitly:
   ```bash
   python3 bot.py
   ```

---

## Best Practices

### For Admins

1. **Regular Backups**
   - Use `/backup` weekly
   - Save backup files safely
   - Label with dates

2. **Content Management**
   - Add varied Bible verses
   - Update events regularly
   - Keep contact list current

3. **Quiz Management**
   - Create diverse questions
   - Check for typos
   - Test answers are correct

4. **Prayer Requests**
   - Check `/praylist` regularly
   - Respond to requests
   - Delete old requests if needed

5. **Group Management**
   - Make bot admin in all groups
   - Monitor bot performance
   - Check `/stats` weekly

### For Users

1. **Prayer Requests**
   - Be specific but concise
   - Use respectful language
   - Don't spam requests

2. **Quizzes**
   - Read questions carefully
   - Learn from wrong answers
   - Have fun and grow spiritually!

3. **Reporting Issues**
   - Be descriptive
   - Include error messages
   - Be patient for fixes

---

## Advanced Configuration

### Running Bot as Service (Linux)

Create systemd service file:

```bash
sudo nano /etc/systemd/system/church-bot.service
```

Add content:
```ini
[Unit]
Description=Church Community Telegram Bot
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/path/to/church_bot
ExecStart=/usr/bin/python3 /path/to/church_bot/bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable church-bot
sudo systemctl start church-bot
sudo systemctl status church-bot
```

### Running with Docker

Create Dockerfile:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
```

Build and run:
```bash
docker build -t church-bot .
docker run -d --name church-bot --restart always church-bot
```

---

## FAQ

**Q: Can I use this bot in multiple groups?**
A: Yes! The bot works in unlimited groups simultaneously.

**Q: Is the data secure?**
A: Data is stored locally in bot_data.json. Keep backups safe and secure your server.

**Q: Can I customize the bot messages?**
A: Yes! Edit bot.py to customize any messages.

**Q: How do I add more admin users?**
A: Add their User IDs to ADMIN_IDS in .env file (comma-separated).

**Q: Can users see other users' prayer requests?**
A: No, only admins can see all prayer requests with /praylist.

**Q: How many verses/quizzes can I add?**
A: Unlimited! Add as many as you want.

**Q: Does the bot work 24/7?**
A: Yes, as long as the script is running on your server.

**Q: Can I host this on free hosting?**
A: Yes! Use platforms like Heroku, Replit, or PythonAnywhere.

---

## Support & Contribution

**Created by: PINLON-YOUTH**

### Getting Help
- Read this documentation thoroughly
- Check Troubleshooting section
- Review code comments in bot.py

### Contributing
- Report bugs
- Suggest features
- Improve documentation
- Share with other churches

---

**God Bless Your Church Community! 🙏**
