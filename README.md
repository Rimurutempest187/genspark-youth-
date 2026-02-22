# Church Community Telegram Bot

**Created by: PINLON-YOUTH**

A comprehensive Telegram bot for managing church community activities, including events, birthdays, prayers, Bible verses, and interactive quizzes.

## Features

### User Commands
- `/start` - စတင်အသုံးပြုခြင်းနှင့် နှုတ်ခွန်းဆက်လွှာ
- `/about` - အသင်းတော်အကြောင်း
- `/contact` - တာဝန်ခံများ၏ ဖုန်းနံပါတ်များ
- `/verse` - ယနေ့အတွက် ကျမ်းချက် (Random Auto)
- `/events` - လာမည့်အစီအစဉ်များ
- `/birthday` - ယခုလမွေးနေ့များ
- `/pray <text>` - ဆုတောင်းခံချက်ပို့ရန်
- `/quiz` - ကျမ်းစာ Quiz ဖြေရန်
- `/tops` - Quiz အမှတ်အများဆုံးစာရင်း
- `/report <text>` - အကြောင်းကြားရန်

### Admin Commands
- `/edit` - Admin commands စာရင်းကြည့်ရန်
- `/edabout` - အသင်းတော်အကြောင်းပြင်ဆင်ရန်
- `/edcontact` - ဆက်သွယ်ရန်အချက်အလက်များထည့်ရန်
- `/edverse` - ကျမ်းချက်များထည့်ရန်
- `/edevents` - အစီအစဉ်များထည့်ရန်
- `/edbirthday` - မွေးနေ့များထည့်ရန်
- `/edquiz` - Quiz များထည့်ရန်
- `/praylist` - ဆုတောင်းခံချက်စာရင်း
- `/set <number>` - Auto quiz drop threshold သတ်မှတ်ရန်
- `/broadcast` - Group များထံ သတင်းပို့ရန်
- `/stats` - Bot statistics
- `/backup` - Data backup လုပ်ရန်
- `/restore` - Data ပြန်ယူရန်
- `/delete <type> <number>` - Data တစ်ခုချင်းဖျက်ရန်
- `/allclear` - Data အားလုံးဖျက်ရန်

## Installation

### 1. Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### 2. Setup Steps

```bash
# Clone or download the bot files
cd church_bot

# Install required packages
pip install -r requirements.txt

# Create .env file from example
cp .env.example .env

# Edit .env file with your credentials
nano .env
```

### 3. Configuration

Edit the `.env` file:

```env
BOT_TOKEN=your_bot_token_here
ADMIN_IDS=123456789,987654321
```

**How to get Bot Token:**
1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Copy the token provided

**How to get your User ID:**
1. Search for `@userinfobot` on Telegram
2. Send any message
3. Copy your User ID
4. Add it to ADMIN_IDS in .env file

### 4. Run the Bot

```bash
python bot.py
```

## Usage Examples

### Adding Bible Verses (Admin)
```
/edverse

တရားတော်သည် ငါ့ခြေ၌ မီးခွက်ဖြစ်၍ ငါ့လမ်း၌ အလင်းဖြစ်၏။ - ဆာလံ ၁၁၉:၁၀၅
သင်တို့သည် ငါ့ကိုခေါ်၍ ဆုတောင်းသောအခါ ငါနားထောင်မည်။ - ယေရမိ ၂၉:၁၂
```

### Adding Quizzes (Admin)
```
/edquiz

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
```

### Adding Contacts (Admin)
```
/edcontact

ဦးအောင်အောင် - 09123456789
မမမမ - 09987654321
ဦးသန်းသန်း - 09456789123
```

### Adding Events (Admin)
```
/edevents

2024-12-25 - ခရစ္စမတ်ပွဲတော်
2024-12-31 - နှစ်သစ်ကူးဆုတောင်းပွဲ
2025-01-15 - လူငယ်စခနး်
```

### Adding Birthdays (Admin)
```
/edbirthday

1-15 - မောင်မောင်
3-20 - မမမ
6-10 - ကိုကို
12-25 - စုစု
```

### Setting Auto Quiz
```
/set 10
```
Quiz will automatically appear after 10 messages in the group.

### Prayer Requests (Users)
```
/pray ကျွန်တော့်မိသားစုအတွက် ကျန်းမာရေးကောင်းမွန်ပါစေ
```

### Broadcasting (Admin)
```
/broadcast

Then send your message (text or photo with caption)
```

## Features Details

### Auto Quiz System
- Quiz automatically drops after a set number of messages
- Multiple choice questions (A, B, C, D)
- Score tracking system
- Leaderboard with top scorers

### Daily Bible Verse
- Random verse selection
- Morning/Evening greetings
- Burmese language support

### Birthday Reminders
- Automatic monthly birthday list
- Easy birthday management

### Prayer Request System
- Users can submit prayer requests
- Admin can view all requests with usernames
- Timestamped entries

### Data Management
- JSON-based storage
- Backup and restore functionality
- Selective deletion
- Complete data wipe option

## File Structure

```
church_bot/
├── bot.py              # Main bot script
├── requirements.txt    # Python dependencies
├── .env.example       # Environment variables template
├── .env               # Your configuration (create this)
├── bot_data.json      # Data storage (auto-created)
└── README.md          # This file
```

## Troubleshooting

### Bot not responding
- Check if BOT_TOKEN is correct in .env file
- Ensure bot is running (python bot.py)
- Check internet connection

### Commands not working
- Verify you have admin privileges (check ADMIN_IDS)
- Make sure you're using the correct command format
- Check if bot has required permissions in group

### Data loss
- Use `/backup` regularly
- Keep backup files safe
- Use `/restore` with backup file to recover data

## Security Notes

1. **Keep your .env file secret** - Never share your bot token
2. **Admin IDs** - Only add trusted users as admins
3. **Group permissions** - Give bot appropriate admin rights in groups
4. **Regular backups** - Use `/backup` command regularly

## Support

For issues or questions:
- Create an issue in the repository
- Contact: PINLON-YOUTH

## License

Created by: **PINLON-YOUTH**

---

**God Bless! 🙏**
