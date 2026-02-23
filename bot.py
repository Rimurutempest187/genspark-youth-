#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Church Community Telegram Bot
Created by: PINLON-YOUTH
"""

import os
import json
import random
import logging
from datetime import datetime, time
from typing import Dict, List, Optional
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)
from telegram.constants import ParseMode
import pytz

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_IDS = [int(id.strip()) for id in os.getenv('ADMIN_IDS', '').split(',') if id.strip()]
DATA_FILE = 'bot_data.json'
TIMEZONE = pytz.timezone('Asia/Yangon')

# Conversation states
EDIT_ABOUT, EDIT_CONTACT, EDIT_VERSE, EDIT_EVENTS, EDIT_BIRTHDAY, EDIT_QUIZ = range(6)
BROADCAST_TEXT, BROADCAST_PHOTO = range(6, 8)

# Data structure
class BotData:
    def __init__(self):
        self.about = ""
        self.contacts = []
        self.verses = []
        self.events = []
        self.birthdays = []
        self.prayers = []
        self.quizzes = []
        self.quiz_scores = {}
        self.message_count = {}
        self.quiz_threshold = 10
        self.users = set()
        self.groups = set()
        
    def to_dict(self):
        return {
            'about': self.about,
            'contacts': self.contacts,
            'verses': self.verses,
            'events': self.events,
            'birthdays': self.birthdays,
            'prayers': self.prayers,
            'quizzes': self.quizzes,
            'quiz_scores': self.quiz_scores,
            'message_count': self.message_count,
            'quiz_threshold': self.quiz_threshold,
            'users': list(self.users),
            'groups': list(self.groups)
        }
    
    @classmethod
    def from_dict(cls, data):
        bot_data = cls()
        bot_data.about = data.get('about', '')
        bot_data.contacts = data.get('contacts', [])
        bot_data.verses = data.get('verses', [])
        bot_data.events = data.get('events', [])
        bot_data.birthdays = data.get('birthdays', [])
        bot_data.prayers = data.get('prayers', [])
        bot_data.quizzes = data.get('quizzes', [])
        bot_data.quiz_scores = data.get('quiz_scores', {})
        bot_data.message_count = data.get('message_count', {})
        bot_data.quiz_threshold = data.get('quiz_threshold', 10)
        bot_data.users = set(data.get('users', []))
        bot_data.groups = set(data.get('groups', []))
        return bot_data

# Global data storage
bot_data = BotData()

# Utility functions
def save_data():
    """Save bot data to JSON file"""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(bot_data.to_dict(), f, ensure_ascii=False, indent=2)
        logger.info("Data saved successfully")
        return True
    except Exception as e:
        logger.error(f"Error saving data: {e}")
        return False

def load_data():
    """Load bot data from JSON file"""
    global bot_data
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                bot_data = BotData.from_dict(data)
            logger.info("Data loaded successfully")
            return True
    except Exception as e:
        logger.error(f"Error loading data: {e}")
    return False

def is_admin(user_id: int) -> bool:
    """Check if user is admin"""
    return user_id in ADMIN_IDS

def get_current_month_birthdays():
    """Get birthdays for current month"""
    current_month = datetime.now(TIMEZONE).month
    monthly_birthdays = [b for b in bot_data.birthdays if b.get('month') == current_month]
    return monthly_birthdays

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    chat = update.effective_chat
    
    # Track users and groups
    if chat.type == 'private':
        bot_data.users.add(user.id)
    else:
        bot_data.groups.add(chat.id)
    save_data()
    
    welcome_text = f"""
🙏 ကြိုဆိုပါတယ် {user.first_name}!

Church Community Bot မှ ကြိုဆိုပါတယ်။

📜 အသုံးပြုနိုင်သော Commands များ:

/about - အသင်းတော်အကြောင်း
/contact - ဆက်သွယ်ရန်ဖုန်းနံပါတ်များ
/verse - ယနေ့အတွက် ကျမ်းချက်
/events - လာမည့်အစီအစဉ်များ
/birthday - ယခုလမွေးနေ့များ
/pray - ဆုတောင်းခံချက်ပို့ရန်
/quiz - ကျမ်းစာ Quiz ဖြေရန်
/tops - Quiz အမှတ်အများဆုံး
/report - အကြောင်းကြားရန်

━━━━━━━━━━━━━━━
✨ Created by: PINLON-YOUTH
"""
    
    await update.message.reply_text(welcome_text)

async def edit_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /edit command - Admin only"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⚠️ သင်သည် Admin မဟုတ်ပါ။")
        return
    
    admin_text = """
🔧 Admin Commands:

/edabout - အသင်းတော်အကြောင်းပြင်ဆင်ရန်
/edcontact - ဆက်သွယ်ရန်အချက်အလက်များထည့်ရန်
/edverse - ကျမ်းချက်များထည့်ရန်
/edevents - အစီအစဉ်များထည့်ရန်
/edbirthday - မွေးနေ့များထည့်ရန်
/edquiz - Quiz များထည့်ရန်
/praylist - ဆုတောင်းခံချက်စာရင်း
/set - Quiz ကျမည့်အကြိမ်သတ်မှတ်ရန်
/broadcast - သတင်းစကားများပို့ရန်
/stats - အသုံးပြုသူများစာရင်း
/backup - Data ကို Backup လုပ်ရန်
/restore - Data ပြန်ယူရန်
/delete - Data များဖျက်ရန်
/allclear - Data အားလုံးဖျက်ရန်

━━━━━━━━━━━━━━━
✨ Created by: PINLON-YOUTH
"""
    await update.message.reply_text(admin_text)

async def edabout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /edabout command"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⚠️ သင်သည် Admin မဟုတ်ပါ။")
        return ConversationHandler.END
    
    await update.message.reply_text(
        "📝 အသင်းတော်၏ သမိုင်းကြောင်းနှင့် ရည်ရွယ်ချက်ကို ရေးသားပါ:\n\n"
        "ပယ်ဖျက်ရန် /cancel"
    )
    return EDIT_ABOUT

async def receive_about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive about text"""
    bot_data.about = update.message.text
    save_data()
    await update.message.reply_text("✅ အသင်းတော်အကြောင်း သိမ်းဆည်းပြီးပါပြီ။")
    return ConversationHandler.END

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /about command"""
    if bot_data.about:
        await update.message.reply_text(
            f"ℹ️ **အသင်းတော်အကြောင်း**\n\n{bot_data.about}\n\n"
            f"━━━━━━━━━━━━━━━\n✨ Created by: PINLON-YOUTH",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await update.message.reply_text("📝 အချက်အလက်များ မရှိသေးပါ။")

async def edcontact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /edcontact command"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⚠️ သင်သည် Admin မဟုတ်ပါ။")
        return ConversationHandler.END
    
    await update.message.reply_text(
        "📞 ဆက်သွယ်ရန်အချက်အလက်များထည့်ပါ:\n\n"
        "Format: အမည် - ဖုန်းနံပါတ်\n"
        "ဥပမာ:\n"
        "မောင်မောင် - 09123456789\n"
        "မမမ - 09987654321\n\n"
        "တစ်ကြောင်းချင်းစီ ရေးပါ။ ပယ်ဖျက်ရန် /cancel"
    )
    return EDIT_CONTACT

async def receive_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive contact info"""
    contacts = update.message.text.strip().split('\n')
    for contact in contacts:
        if contact.strip():
            bot_data.contacts.append(contact.strip())
    save_data()
    await update.message.reply_text(f"✅ ဆက်သွယ်ရန်အချက်အလက် {len(contacts)} ခု ထည့်ပြီးပါပြီ။")
    return ConversationHandler.END

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /contact command"""
    if bot_data.contacts:
        contact_text = "📞 **ဆက်သွယ်ရန်**\n\n"
        for idx, contact in enumerate(bot_data.contacts, 1):
            contact_text += f"{idx}. {contact}\n"
        contact_text += "\n━━━━━━━━━━━━━━━\n✨ Created by: PINLON-YOUTH"
        await update.message.reply_text(contact_text, parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.reply_text("📝 ဆက်သွယ်ရန်အချက်အလက် မရှိသေးပါ။")

async def edverse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /edverse command"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⚠️ သင်သည် Admin မဟုတ်ပါ။")
        return ConversationHandler.END
    
    await update.message.reply_text(
        "📖 ကျမ်းချက်များထည့်ပါ:\n\n"
        "Format: ကျမ်းချက် - အကိုးအကား\n"
        "ဥပမာ:\n"
        "ငါ့ကို လမ်းပြပါ အမှန်တရားသို့။ - ဆာလံ ၂၅:၅\n\n"
        "တစ်ကြောင်းချင်းစီ ရေးပါ။ ပယ်ဖျက်ရန် /cancel"
    )
    return EDIT_VERSE

async def receive_verse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive verse"""
    verses = update.message.text.strip().split('\n')
    count = 0
    for verse in verses:
        if verse.strip():
            bot_data.verses.append(verse.strip())
            count += 1
    save_data()
    await update.message.reply_text(f"✅ ကျမ်းချက် {count} ခု ထည့်ပြီးပါပြီ။")
    return ConversationHandler.END

async def verse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /verse command"""
    if bot_data.verses:
        random_verse = random.choice(bot_data.verses)
        now = datetime.now(TIMEZONE)
        greeting = "🌅 မင်္ဂလာနံနက်ခင်းပါ" if now.hour < 12 else "🌙 မင်္ဂလာညပါ"
        
        await update.message.reply_text(
            f"{greeting}\n\n"
            f"📖 **ယနေ့အတွက် ကျမ်းချက်**\n\n"
            f"{random_verse}\n\n"
            f"━━━━━━━━━━━━━━━\n✨ Created by: PINLON-YOUTH",
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await update.message.reply_text("📝 ကျမ်းချက်များ မရှိသေးပါ။")

async def edevents(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /edevents command"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⚠️ သင်သည် Admin မဟုတ်ပါ။")
        return ConversationHandler.END
    
    await update.message.reply_text(
        "📅 အစီအစဉ်များထည့်ပါ:\n\n"
        "Format: ရက်စွဲ - အစီအစဉ်အမည်\n"
        "ဥပမာ:\n"
        "2024-03-15 - နှစ်သစ်ကူးပွဲတော်\n"
        "2024-04-01 - လူငယ်စခန်း\n\n"
        "တစ်ကြောင်းချင်းစီ ရေးပါ။ ပယ်ဖျက်ရန် /cancel"
    )
    return EDIT_EVENTS

async def receive_events(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive events"""
    events = update.message.text.strip().split('\n')
    count = 0
    for event in events:
        if event.strip():
            bot_data.events.append(event.strip())
            count += 1
    save_data()
    await update.message.reply_text(f"✅ အစီအစဉ် {count} ခု ထည့်ပြီးပါပြီ။")
    return ConversationHandler.END

async def events(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /events command"""
    if bot_data.events:
        events_text = "📅 **လာမည့်အစီအစဉ်များ**\n\n"
        for idx, event in enumerate(bot_data.events, 1):
            events_text += f"{idx}. {event}\n"
        events_text += "\n━━━━━━━━━━━━━━━\n✨ Created by: PINLON-YOUTH"
        await update.message.reply_text(events_text, parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.reply_text("📝 အစီအစဉ်များ မရှိသေးပါ။")

async def edbirthday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /edbirthday command"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⚠️ သင်သည် Admin မဟုတ်ပါ။")
        return ConversationHandler.END
    
    await update.message.reply_text(
        "🎂 မွေးနေ့များထည့်ပါ:\n\n"
        "Format: လ-ရက် - အမည်\n"
        "ဥပမာ:\n"
        "3-15 - မောင်မောင်\n"
        "4-20 - မမမ\n\n"
        "တစ်ကြောင်းချင်းစီ ရေးပါ။ ပယ်ဖျက်ရန် /cancel"
    )
    return EDIT_BIRTHDAY

async def receive_birthday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive birthdays"""
    birthdays = update.message.text.strip().split('\n')
    count = 0
    for birthday in birthdays:
        if birthday.strip() and '-' in birthday:
            try:
                date_part, name = birthday.split('-', 2)[0:2], birthday.split('-', 2)[2]
                month, day = map(int, date_part[0].split('-'))
                bot_data.birthdays.append({
                    'month': month,
                    'day': day,
                    'name': name.strip()
                })
                count += 1
            except:
                continue
    save_data()
    await update.message.reply_text(f"✅ မွေးနေ့ {count} ခု ထည့်ပြီးပါပြီ။")
    return ConversationHandler.END

async def birthday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /birthday command"""
    monthly_birthdays = get_current_month_birthdays()
    
    if monthly_birthdays:
        current_month = datetime.now(TIMEZONE).strftime('%B')
        birthday_text = f"🎂 **{current_month} လ မွေးနေ့များ**\n\n"
        for bd in sorted(monthly_birthdays, key=lambda x: x['day']):
            birthday_text += f"• {bd['month']}/{bd['day']} - {bd['name']}\n"
        birthday_text += "\n━━━━━━━━━━━━━━━\n✨ Created by: PINLON-YOUTH"
        await update.message.reply_text(birthday_text, parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.reply_text("🎂 ယခုလတွင် မွေးနေ့များ မရှိပါ။")

async def pray(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /pray command"""
    if not context.args:
        await update.message.reply_text(
            "🙏 ဆုတောင်းခံချက်ပို့ရန်:\n\n"
            "/pray သင့်ဆုတောင်းခံချက်"
        )
        return
    
    prayer_text = ' '.join(context.args)
    user = update.effective_user
    
    prayer_entry = {
        'user_id': user.id,
        'username': user.username or user.first_name,
        'prayer': prayer_text,
        'date': datetime.now(TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')
    }
    
    bot_data.prayers.append(prayer_entry)
    save_data()
    
    await update.message.reply_text(
        "✅ သင့်ဆုတောင်းခံချက်ကို လက်ဝယ်ရရှိပြီး ဆုတောင်းပေးပါမည်။\n\n"
        "━━━━━━━━━━━━━━━\n✨ Created by: PINLON-YOUTH"
    )

async def praylist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /praylist command - Admin only"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⚠️ သင်သည် Admin မဟုတ်ပါ။")
        return
    
    if bot_data.prayers:
        prayer_text = "🙏 **ဆုတောင်းခံချက်စာရင်း**\n\n"
        for idx, prayer in enumerate(bot_data.prayers[-20:], 1):  # Last 20
            prayer_text += f"{idx}. @{prayer['username']}\n"
            prayer_text += f"   {prayer['prayer']}\n"
            prayer_text += f"   📅 {prayer['date']}\n\n"
        await update.message.reply_text(prayer_text, parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.reply_text("📝 ဆုတောင်းခံချက်များ မရှိသေးပါ။")

async def set_quiz_threshold(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /set command"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⚠️ သင်သည် Admin မဟုတ်ပါ။")
        return
    
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text(
            "⚙️ Quiz ကျမည့် message အရေအတွက်သတ်မှတ်ရန်:\n\n"
            f"/set နံပါတ်\n\n"
            f"လက်ရှိ: {bot_data.quiz_threshold} messages"
        )
        return
    
    bot_data.quiz_threshold = int(context.args[0])
    save_data()
    await update.message.reply_text(
        f"✅ Quiz threshold ကို {bot_data.quiz_threshold} messages သို့ သတ်မှတ်ပြီးပါပြီ။"
    )

async def edquiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /edquiz command"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⚠️ သင်သည် Admin မဟုတ်ပါ။")
        return ConversationHandler.END
    
    await update.message.reply_text(
        "❓ Quiz များထည့်ပါ:\n\n"
        "Format:\n"
        "မေးခွန်း?\n"
        "A) ရွေးချယ်စရာ ၁\n"
        "B) ရွေးချယ်စရာ ၂\n"
        "C) ရွေးချယ်စရာ ၃\n"
        "D) ရွေးချယ်စရာ ၄\n"
        "အဖြေ: A\n\n"
        "Quiz တစ်ခုချင်းစီကို ကွက်လပ်တစ်ကြောင်းခြားပါ။\n"
        "ပယ်ဖျက်ရန် /cancel"
    )
    return EDIT_QUIZ

async def receive_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive quizzes"""
    quiz_blocks = update.message.text.strip().split('\n\n')
    count = 0
    
    for block in quiz_blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 6:
            quiz = {
                'question': lines[0],
                'choices': {
                    'A': lines[1].replace('A)', '').strip(),
                    'B': lines[2].replace('B)', '').strip(),
                    'C': lines[3].replace('C)', '').strip(),
                    'D': lines[4].replace('D)', '').strip()
                },
                'answer': lines[5].replace('အဖြေ:', '').strip().upper()
            }
            bot_data.quizzes.append(quiz)
            count += 1
    
    save_data()
    await update.message.reply_text(f"✅ Quiz {count} ခု ထည့်ပြီးပါပြီ။")
    return ConversationHandler.END

async def track_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Track messages for auto quiz"""
    chat_id = str(update.effective_chat.id)
    
    if chat_id not in bot_data.message_count:
        bot_data.message_count[chat_id] = 0
    
    bot_data.message_count[chat_id] += 1
    
    if bot_data.message_count[chat_id] >= bot_data.quiz_threshold and bot_data.quizzes:
        bot_data.message_count[chat_id] = 0
        save_data()
        await send_quiz(update, context)

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /quiz command"""
    await send_quiz(update, context)

async def send_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random quiz"""
    if not bot_data.quizzes:
        await update.message.reply_text("📝 Quiz များ မရှိသေးပါ။")
        return
    
    quiz = random.choice(bot_data.quizzes)
    quiz_id = bot_data.quizzes.index(quiz)
    
    quiz_text = f"❓ **Quiz Time!**\n\n{quiz['question']}\n\n"
    quiz_text += f"A) {quiz['choices']['A']}\n"
    quiz_text += f"B) {quiz['choices']['B']}\n"
    quiz_text += f"C) {quiz['choices']['C']}\n"
    quiz_text += f"D) {quiz['choices']['D']}\n"
    
    keyboard = [
        [
            InlineKeyboardButton("A", callback_data=f"quiz_{quiz_id}_A"),
            InlineKeyboardButton("B", callback_data=f"quiz_{quiz_id}_B"),
            InlineKeyboardButton("C", callback_data=f"quiz_{quiz_id}_C"),
            InlineKeyboardButton("D", callback_data=f"quiz_{quiz_id}_D")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(quiz_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def quiz_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle quiz answer callback"""
    query = update.callback_query
    await query.answer()
    
    data = query.data.split('_')
    quiz_id = int(data[1])
    user_answer = data[2]
    
    if quiz_id >= len(bot_data.quizzes):
        await query.edit_message_text("❌ Quiz မရှိတော့ပါ။")
        return
    
    quiz = bot_data.quizzes[quiz_id]
    user_id = str(query.from_user.id)
    username = query.from_user.username or query.from_user.first_name
    
    if user_id not in bot_data.quiz_scores:
        bot_data.quiz_scores[user_id] = {'name': username, 'score': 0}
    
    if user_answer == quiz['answer']:
        bot_data.quiz_scores[user_id]['score'] += 1
        bot_data.quiz_scores[user_id]['name'] = username
        save_data()
        
        result_text = f"✅ **မှန်ကန်ပါသည်!**\n\n"
        result_text += f"အဖြေ: {quiz['answer']}) {quiz['choices'][quiz['answer']]}\n\n"
        result_text += f"🏆 သင့်ရမှတ်: {bot_data.quiz_scores[user_id]['score']}"
    else:
        result_text = f"❌ **မှားယွင်းနေပါသည်။**\n\n"
        result_text += f"မှန်ကန်သောအဖြေ: {quiz['answer']}) {quiz['choices'][quiz['answer']]}\n\n"
        result_text += f"🏆 သင့်ရမှတ်: {bot_data.quiz_scores[user_id]['score']}"
    
    await query.edit_message_text(result_text, parse_mode=ParseMode.MARKDOWN)

import html
async def tops(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /tops command"""
    
    # ၁။ Score ရှိမရှိ စစ်ဆေးခြင်း
    if not bot_data.quiz_scores:
        await update.message.reply_text("🏆 Quiz အမှတ်များ မရှိသေးပါ။")
        return
    
    try:
        # ၂။ Score အများဆုံးသူကို အစဉ်လိုက် စီခြင်း
        sorted_scores = sorted(
            bot_data.quiz_scores.items(), 
            key=lambda x: x[1].get('score', 0), 
            reverse=True
        )
        
        # ၃။ HTML format ဖြင့် စာသားတည်ဆောက်ခြင်း
        tops_text = "<b>🏆 Quiz Top Scores</b>\n\n"
        
        for idx, (user_id, data) in enumerate(sorted_scores[:10], 1):
            # ပထမ၊ ဒုတိယ၊ တတိယကို ရွှေ၊ ငွေ၊ ကြေး ဆုတံဆိပ်ပြောင်းခြင်း
            medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx}."
            
            # နာမည်ထဲမှာ ပါနိုင်တဲ့ special characters တွေကို HTML အဖြစ်ပြောင်းလဲခြင်း
            safe_name = html.escape(str(data.get('name', 'Unknown')))
            score = data.get('score', 0)
            
            tops_text += f"{medal} {safe_name} - <b>{score}</b> points\n"
        
        tops_text += "\n━━━━━━━━━━━━━━━\n✨ Created by: <b>PINLON-YOUTH</b>"
        
        # ၄။ ParseMode.HTML ကို သုံးပြီး message ပို့ခြင်း
        await update.message.reply_text(tops_text, parse_mode=ParseMode.HTML)

    except Exception as e:
        # အမှားတစ်ခုခုတက်ရင် log ထုတ်ကြည့်ရန်
        print(f"Error in tops command: {e}")
        await update.message.reply_text("❌ Ranking ပြသရာတွင် အမှားအယွင်း တစ်ခုရှိနေပါသည်။")

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /broadcast command"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⚠️ သင်သည် Admin မဟုတ်ပါ။")
        return ConversationHandler.END
    
    await update.message.reply_text(
        "📢 Broadcast Message ပို့ရန်:\n\n"
        "စာသားတစ်ခု သို့မဟုတ် ပုံတစ်ပုံ (caption ပါ) ပို့ပါ။\n\n"
        "ပယ်ဖျက်ရန် /cancel"
    )
    return BROADCAST_TEXT

async def receive_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive and send broadcast message"""
    sent_count = 0
    failed_count = 0
    
    # Send to all groups
    for group_id in bot_data.groups:
        try:
            if update.message.photo:
                await context.bot.send_photo(
                    chat_id=group_id,
                    photo=update.message.photo[-1].file_id,
                    caption=update.message.caption or ""
                )
            else:
                await context.bot.send_message(
                    chat_id=group_id,
                    text=update.message.text
                )
            sent_count += 1
        except Exception as e:
            logger.error(f"Failed to send to {group_id}: {e}")
            failed_count += 1
    
    await update.message.reply_text(
        f"✅ Broadcast ပို့ပြီးပါပြီ။\n\n"
        f"အောင်မြင်: {sent_count}\n"
        f"မအောင်မြင်: {failed_count}"
    )
    return ConversationHandler.END

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats command"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⚠️ သင်သည် Admin မဟုတ်ပါ။")
        return
    
    stats_text = "📊 **Bot Statistics**\n\n"
    stats_text += f"👥 Users: {len(bot_data.users)}\n"
    stats_text += f"👨‍👩‍👧‍👦 Groups: {len(bot_data.groups)}\n"
    stats_text += f"📖 Verses: {len(bot_data.verses)}\n"
    stats_text += f"❓ Quizzes: {len(bot_data.quizzes)}\n"
    stats_text += f"🙏 Prayers: {len(bot_data.prayers)}\n"
    stats_text += f"🎂 Birthdays: {len(bot_data.birthdays)}\n"
    stats_text += f"📅 Events: {len(bot_data.events)}\n"
    stats_text += f"📞 Contacts: {len(bot_data.contacts)}\n"
    
    await update.message.reply_text(stats_text, parse_mode=ParseMode.MARKDOWN)

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /report command"""
    if not context.args:
        await update.message.reply_text(
            "📝 အကြောင်းကြားရန်:\n\n"
            "/report သင့်အကြောင်းအရာ"
        )
        return
    
    report_text = ' '.join(context.args)
    user = update.effective_user
    
    # Send to admins
    for admin_id in ADMIN_IDS:
        try:
            await context.bot.send_message(
                chat_id=admin_id,
                text=f"📝 **New Report**\n\n"
                     f"From: @{user.username or user.first_name}\n"
                     f"User ID: {user.id}\n\n"
                     f"{report_text}",
                parse_mode=ParseMode.MARKDOWN
            )
        except:
            pass
    
    await update.message.reply_text("✅ သင့်အကြောင်းကြားချက်ကို လက်ဝယ်ရရှိပြီးပါပြီ။")

async def backup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /backup command"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⚠️ သင်သည် Admin မဟုတ်ပါ။")
        return
    
    if save_data():
        with open(DATA_FILE, 'rb') as f:
            await update.message.reply_document(
                document=f,
                filename=f"backup_{datetime.now(TIMEZONE).strftime('%Y%m%d_%H%M%S')}.json",
                caption="✅ Data Backup လုပ်ပြီးပါပြီ။"
            )
    else:
        await update.message.reply_text("❌ Backup လုပ်ရာတွင် အမှားအယွင်းဖြစ်ပေါ်ခဲ့သည်။")

async def restore(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /restore command"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⚠️ သင်သည် Admin မဟုတ်ပါ။")
        return
    
    await update.message.reply_text(
        "📁 Data file ကို ပို့ပါ (.json file):\n\n"
        "ပယ်ဖျက်ရန် /cancel"
    )

async def receive_restore_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive restore file"""
    if not update.message.document:
        return
    
    if not is_admin(update.effective_user.id):
        return
    
    try:
        file = await update.message.document.get_file()
        await file.download_to_drive(DATA_FILE)
        
        if load_data():
            await update.message.reply_text("✅ Data ကို ပြန်လည်ရယူပြီးပါပြီ။")
        else:
            await update.message.reply_text("❌ Data file မှားယွင်းနေပါသည်။")
    except Exception as e:
        logger.error(f"Restore error: {e}")
        await update.message.reply_text("❌ ပြန်လည်ရယူရာတွင် အမှားအယွင်းဖြစ်ပေါ်ခဲ့သည်။")

async def delete_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /delete command"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⚠️ သင်သည် Admin မဟုတ်ပါ။")
        return
    
    if not context.args:
        await update.message.reply_text(
            "🗑️ Data ဖျက်ရန်:\n\n"
            "/delete verse နံပါတ်\n"
            "/delete quiz နံပါတ်\n"
            "/delete event နံပါတ်\n"
            "/delete contact နံပါတ်\n"
            "/delete birthday နံပါတ်"
        )
        return
    
    data_type = context.args[0].lower()
    
    if len(context.args) < 2 or not context.args[1].isdigit():
        await update.message.reply_text("⚠️ နံပါတ်ထည့်ပါ။")
        return
    
    index = int(context.args[1]) - 1
    
    try:
        if data_type == 'verse' and 0 <= index < len(bot_data.verses):
            deleted = bot_data.verses.pop(index)
            save_data()
            await update.message.reply_text(f"✅ ကျမ်းချက် ဖျက်ပြီးပါပြီ။")
        elif data_type == 'quiz' and 0 <= index < len(bot_data.quizzes):
            deleted = bot_data.quizzes.pop(index)
            save_data()
            await update.message.reply_text(f"✅ Quiz ဖျက်ပြီးပါပြီ။")
        elif data_type == 'event' and 0 <= index < len(bot_data.events):
            deleted = bot_data.events.pop(index)
            save_data()
            await update.message.reply_text(f"✅ အစီအစဉ် ဖျက်ပြီးပါပြီ။")
        elif data_type == 'contact' and 0 <= index < len(bot_data.contacts):
            deleted = bot_data.contacts.pop(index)
            save_data()
            await update.message.reply_text(f"✅ ဆက်သွယ်ရန် ဖျက်ပြီးပါပြီ။")
        elif data_type == 'birthday' and 0 <= index < len(bot_data.birthdays):
            deleted = bot_data.birthdays.pop(index)
            save_data()
            await update.message.reply_text(f"✅ မွေးနေ့ ဖျက်ပြီးပါပြီ။")
        else:
            await update.message.reply_text("❌ မှားယွင်းသော အမျိုးအစား သို့မဟုတ် နံပါတ်။")
    except Exception as e:
        logger.error(f"Delete error: {e}")
        await update.message.reply_text("❌ ဖျက်ရာတွင် အမှားအယွင်းဖြစ်ပေါ်ခဲ့သည်။")

async def allclear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /allclear command"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("⚠️ သင်သည် Admin မဟုတ်ပါ။")
        return
    
    keyboard = [
        [
            InlineKeyboardButton("✅ Yes, Clear All", callback_data="clear_confirm"),
            InlineKeyboardButton("❌ Cancel", callback_data="clear_cancel")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "⚠️ **သတိပေးချက်!**\n\n"
        "Data အားလုံးကို ဖျက်ပစ်မှာ သေချာပါသလား?\n"
        "ဤလုပ်ဆောင်ချက်ကို နောက်ပြန်ဆုတ်၍မရနိုင်ပါ။",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )

async def allclear_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle allclear confirmation"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "clear_confirm":
        global bot_data
        bot_data = BotData()
        save_data()
        await query.edit_message_text("✅ Data အားလုံးကို ဖျက်ပြီးပါပြီ။")
    else:
        await query.edit_message_text("❌ ပယ်ဖျက်လိုက်ပါပြီ။")

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel conversation"""
    await update.message.reply_text("❌ ပယ်ဖျက်လိုက်ပါပြီ။")
    return ConversationHandler.END

def main():
    """Main function"""
    # Load data
    load_data()
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Conversation handlers
    about_handler = ConversationHandler(
        entry_points=[CommandHandler('edabout', edabout)],
        states={
            EDIT_ABOUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_about)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    contact_handler = ConversationHandler(
        entry_points=[CommandHandler('edcontact', edcontact)],
        states={
            EDIT_CONTACT: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_contact)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    verse_handler = ConversationHandler(
        entry_points=[CommandHandler('edverse', edverse)],
        states={
            EDIT_VERSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_verse)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    events_handler = ConversationHandler(
        entry_points=[CommandHandler('edevents', edevents)],
        states={
            EDIT_EVENTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_events)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    birthday_handler = ConversationHandler(
        entry_points=[CommandHandler('edbirthday', edbirthday)],
        states={
            EDIT_BIRTHDAY: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_birthday)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    quiz_handler = ConversationHandler(
        entry_points=[CommandHandler('edquiz', edquiz)],
        states={
            EDIT_QUIZ: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_quiz)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    broadcast_handler = ConversationHandler(
        entry_points=[CommandHandler('broadcast', broadcast)],
        states={
            BROADCAST_TEXT: [MessageHandler((filters.TEXT | filters.PHOTO) & ~filters.COMMAND, receive_broadcast)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    # Add handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('edit', edit_menu))
    application.add_handler(about_handler)
    application.add_handler(CommandHandler('about', about))
    application.add_handler(contact_handler)
    application.add_handler(CommandHandler('contact', contact))
    application.add_handler(verse_handler)
    application.add_handler(CommandHandler('verse', verse))
    application.add_handler(events_handler)
    application.add_handler(CommandHandler('events', events))
    application.add_handler(birthday_handler)
    application.add_handler(CommandHandler('birthday', birthday))
    application.add_handler(CommandHandler('pray', pray))
    application.add_handler(CommandHandler('praylist', praylist))
    application.add_handler(CommandHandler('set', set_quiz_threshold))
    application.add_handler(quiz_handler)
    application.add_handler(CommandHandler('quiz', quiz))
    application.add_handler(CallbackQueryHandler(quiz_callback, pattern='^quiz_'))
    application.add_handler(CommandHandler('tops', tops))
    application.add_handler(broadcast_handler)
    application.add_handler(CommandHandler('stats', stats))
    application.add_handler(CommandHandler('report', report))
    application.add_handler(CommandHandler('backup', backup))
    application.add_handler(CommandHandler('restore', restore))
    application.add_handler(MessageHandler(filters.Document.ALL, receive_restore_file))
    application.add_handler(CommandHandler('delete', delete_data))
    application.add_handler(CommandHandler('allclear', allclear))
    application.add_handler(CallbackQueryHandler(allclear_callback, pattern='^clear_'))
    
    # Message tracker for auto quiz
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, track_messages), group=1)
    
    # Start bot
    logger.info("Bot started...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
