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
import asyncio

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
    ConversationHandler
)
from telegram.constants import ParseMode

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
WAITING_ABOUT, WAITING_CONTACT, WAITING_VERSE, WAITING_EVENTS = range(4)
WAITING_BIRTHDAY, WAITING_QUIZ, WAITING_BROADCAST, WAITING_SET = range(4, 8)

# Data file
DATA_FILE = "church_bot_data.json"

# Admin IDs (ထည့်သွင်းရန်)
ADMIN_IDS = [1812962224]  # သင့် Admin Telegram ID ကို ဒီမှာထည့်ပါ

class ChurchBot:
    def __init__(self):
        self.data = {
            "about": "",
            "contacts": [],
            "verses": [],
            "events": [],
            "birthdays": [],
            "prayers": [],
            "quizzes": [],
            "quiz_scores": {},
            "message_count": {},
            "quiz_trigger": 10,
            "users": set(),
            "groups": set()
        }
        self.load_data()
    
    def load_data(self):
        """Load data from JSON file"""
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)
                    # Convert lists back to sets for users and groups
                    if 'users' in loaded_data:
                        loaded_data['users'] = set(loaded_data['users'])
                    if 'groups' in loaded_data:
                        loaded_data['groups'] = set(loaded_data['groups'])
                    self.data.update(loaded_data)
                logger.info("Data loaded successfully")
        except Exception as e:
            logger.error(f"Error loading data: {e}")
    
    def save_data(self):
        """Save data to JSON file"""
        try:
            save_data = self.data.copy()
            # Convert sets to lists for JSON serialization
            save_data['users'] = list(self.data['users'])
            save_data['groups'] = list(self.data['groups'])
            
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            logger.info("Data saved successfully")
        except Exception as e:
            logger.error(f"Error saving data: {e}")
    
    def backup_data(self) -> str:
        """Create backup file"""
        try:
            backup_file = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            save_data = self.data.copy()
            save_data['users'] = list(self.data['users'])
            save_data['groups'] = list(self.data['groups'])
            
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            return backup_file
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            return None

# Initialize bot instance
bot_data = ChurchBot()

def is_admin(user_id: int) -> bool:
    """Check if user is admin"""
    return user_id in ADMIN_IDS

def track_user(update: Update):
    """Track users and groups"""
    if update.effective_chat.type == "private":
        bot_data.data['users'].add(update.effective_user.id)
    else:
        bot_data.data['groups'].add(update.effective_chat.id)
    bot_data.save_data()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    track_user(update)
    
    welcome_message = """
🙏 ကြိုဆိုပါတယ်! Church Community Bot မှ နှုတ်ခွန်းဆက်လွှာ ပါ။

📋 **အသုံးပြုနိုင်သော Commands များ:**

/about - အသင်းတော်အကြောင်း
/contact - တာဝန်ခံများ၏ ဆက်သွယ်ရန်
/verse - ယနေ့အတွက် ကျမ်းချက်
/events - လာမည့်အစီအစဉ်များ
/birthday - ယခုလမွေးနေ့များ
/pray - ဆုတောင်းခံချက်ပို့ရန်
/quiz - Quiz ဖြေရန်
/tops - Quiz အမှတ်များဆုံး
/report - တင်ပြလိုသောအကြောင်းအရာ

✨ Create by: PINLON-YOUTH
"""
    
    keyboard = [
        [KeyboardButton("📖 About"), KeyboardButton("📞 Contact")],
        [KeyboardButton("📜 Verse"), KeyboardButton("📅 Events")],
        [KeyboardButton("🎂 Birthday"), KeyboardButton("🙏 Pray")],
        [KeyboardButton("❓ Quiz"), KeyboardButton("🏆 Tops")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(welcome_message, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def edit_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /edit command - Admin only"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ ဤ command သည် Admin များသာ အသုံးပြုနိုင်ပါသည်။")
        return
    
    admin_message = """
🔧 **Admin Commands:**

/edabout - အကြောင်းအရာပြင်ဆင်ရန်
/edcontact - ဆက်သွယ်ရန်အချက်အလက်ပြင်ဆင်ရန်
/edverse - ကျမ်းချက်များထည့်ရန်
/edevents - အစီအစဉ်များထည့်ရန်
/edbirthday - မွေးနေ့များထည့်ရန်
/edquiz - Quiz များထည့်ရန်
/praylist - ဆုတောင်းခံချက်စာရင်း
/set - Quiz trigger သတ်မှတ်ရန်
/broadcast - Group များသို့ message ပို့ရန်
/stats - စာရင်းအင်းကြည့်ရန်
/backup - Data backup လုပ်ရန်
/restore - Data ပြန်ယူရန်
/allclear - Data အားလုံးရှင်းရန်
/delete - တစ်ခုချင်းဖျက်ရန်
"""
    await update.message.reply_text(admin_message, parse_mode=ParseMode.MARKDOWN)

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /about command"""
    track_user(update)
    about_text = bot_data.data.get('about', 'အသင်းတော်အကြောင်း အချက်အလက်များ မရှိသေးပါ။')
    await update.message.reply_text(f"📖 **အသင်းတော်အကြောင်း**\n\n{about_text}\n\n✨ Create by: PINLON-YOUTH", parse_mode=ParseMode.MARKDOWN)

async def edabout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /edabout command - Admin only"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ ဤ command သည် Admin များသာ အသုံးပြုနိုင်ပါသည်။")
        return
    
    await update.message.reply_text("📝 အသင်းတော်အကြောင်း သမိုင်းကြောင်းနှင့် ရည်ရွယ်ချက်ကို ရေးပါ:")
    return WAITING_ABOUT

async def receive_about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive about text"""
    bot_data.data['about'] = update.message.text
    bot_data.save_data()
    await update.message.reply_text("✅ အသင်းတော်အကြောင်း သိမ်းဆည်းပြီးပါပြီ။")
    return ConversationHandler.END

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /contact command"""
    track_user(update)
    contacts = bot_data.data.get('contacts', [])
    
    if not contacts:
        await update.message.reply_text("📞 ဆက်သွယ်ရန် အချက်အလက်များ မရှိသေးပါ။")
        return
    
    contact_text = "📞 **တာဝန်ခံများ၏ ဆက်သွယ်ရန်:**\n\n"
    for contact in contacts:
        contact_text += f"👤 {contact}\n"
    
    contact_text += "\n✨ Create by: PINLON-YOUTH"
    await update.message.reply_text(contact_text, parse_mode=ParseMode.MARKDOWN)

async def edcontact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /edcontact command - Admin only"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ ဤ command သည် Admin များသာ အသုံးပြုနိုင်ပါသည်။")
        return
    
    await update.message.reply_text("📝 တာဝန်ခံများ၏ အမည်နှင့် ဖုန်းနံပါတ်များကို ရေးပါ (တစ်ကြောင်းချင်း):\n\nဥပမာ:\nကိုယောဟန် - 09123456789\nမနာမ - 09987654321")
    return WAITING_CONTACT

async def receive_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive contact info"""
    contacts = update.message.text.strip().split('\n')
    bot_data.data['contacts'].extend(contacts)
    bot_data.save_data()
    await update.message.reply_text(f"✅ ဆက်သွယ်ရန် {len(contacts)} ခု ထည့်သွင်းပြီးပါပြီ။")
    return ConversationHandler.END

async def verse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /verse command"""
    track_user(update)
    verses = bot_data.data.get('verses', [])
    
    if not verses:
        await update.message.reply_text("📜 ကျမ်းချက်များ မရှိသေးပါ။")
        return
    
    # Get random verse
    random_verse = random.choice(verses)
    current_hour = datetime.now().hour
    
    if current_hour < 12:
        greeting = "🌅 နံနက်ခင်းအတွက် ကျမ်းချက်"
    else:
        greeting = "🌙 ညနေခင်းအတွက် ကျမ်းချက်"
    
    await update.message.reply_text(f"{greeting}\n\n📜 {random_verse}\n\n✨ Create by: PINLON-YOUTH")

async def edverse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /edverse command - Admin only"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ ဤ command သည် Admin များသာ အသုံးပြုနိုင်ပါသည်။")
        return
    
    await update.message.reply_text("📝 ကျမ်းချက်များကို ထည့်ပါ (တစ်ကြောင်းချင်း):\n\nဥပမာ:\nယောဟန် ၃:၁၆ - ဘုရားသခင်သည် လောကီသားတို့ကို...")
    return WAITING_VERSE

async def receive_verse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive verse"""
    verses = update.message.text.strip().split('\n')
    bot_data.data['verses'].extend(verses)
    bot_data.save_data()
    await update.message.reply_text(f"✅ ကျမ်းချက် {len(verses)} ခု ထည့်သွင်းပြီးပါပြီ။")
    return ConversationHandler.END

async def events(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /events command"""
    track_user(update)
    events = bot_data.data.get('events', [])
    
    if not events:
        await update.message.reply_text("📅 လာမည့်အစီအစဉ်များ မရှိသေးပါ။")
        return
    
    events_text = "📅 **လာမည့်အစီအစဉ်များ:**\n\n"
    for event in events:
        events_text += f"🔹 {event}\n"
    
    events_text += "\n✨ Create by: PINLON-YOUTH"
    await update.message.reply_text(events_text, parse_mode=ParseMode.MARKDOWN)

async def edevents(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /edevents command - Admin only"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ ဤ command သည် Admin များသာ အသုံးပြုနိုင်ပါသည်။")
        return
    
    await update.message.reply_text("📝 အစီအစဉ်များကို ထည့်ပါ (တစ်ကြောင်းချင်း):\n\nဥပမာ:\n၂၀၂၆ ဇန်နဝါရီ ၁၀ - ဝိညာဉ်ရေးခရီး\n၂၀၂၆ ဇန်နဝါရီ ၂၅ - လူငယ်စခန်း")
    return WAITING_EVENTS

async def receive_events(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive events"""
    events = update.message.text.strip().split('\n')
    bot_data.data['events'].extend(events)
    bot_data.save_data()
    await update.message.reply_text(f"✅ အစီအစဉ် {len(events)} ခု ထည့်သွင်းပြီးပါပြီ။")
    return ConversationHandler.END

async def birthday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /birthday command"""
    track_user(update)
    birthdays = bot_data.data.get('birthdays', [])
    
    if not birthdays:
        await update.message.reply_text("🎂 ယခုလမွေးနေ့စာရင်း မရှိသေးပါ။")
        return
    
    birthday_text = "🎂 **ယခုလမွေးနေ့များ:**\n\n"
    for birthday in birthdays:
        birthday_text += f"🎉 {birthday}\n"
    
    birthday_text += "\n✨ Create by: PINLON-YOUTH"
    await update.message.reply_text(birthday_text, parse_mode=ParseMode.MARKDOWN)

async def edbirthday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /edbirthday command - Admin only"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ ဤ command သည် Admin များသာ အသုံးပြုနိုင်ပါသည်။")
        return
    
    await update.message.reply_text("📝 မွေးနေ့များကို ထည့်ပါ (တစ်ကြောင်းချင်း):\n\nဥပမာ:\nဇန်နဝါရီ ၁၀ - ကိုယောဟန်\nဇန်နဝါရီ ၂၅ - မနာမ")
    return WAITING_BIRTHDAY

async def receive_birthday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive birthdays"""
    birthdays = update.message.text.strip().split('\n')
    bot_data.data['birthdays'].extend(birthdays)
    bot_data.save_data()
    await update.message.reply_text(f"✅ မွေးနေ့ {len(birthdays)} ခု ထည့်သွင်းပြီးပါပြီ။")
    return ConversationHandler.END

async def pray(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /pray command"""
    track_user(update)
    
    if context.args:
        prayer_text = ' '.join(context.args)
        username = update.effective_user.username or update.effective_user.first_name
        prayer_entry = {
            "username": username,
            "prayer": prayer_text,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        bot_data.data['prayers'].append(prayer_entry)
        bot_data.save_data()
        await update.message.reply_text("✅ သင့်ဆုတောင်းခံချက်ကို လက်ခံပြီးပါပြီ။ ဆုတောင်းပေးပါမည်။ 🙏")
    else:
        await update.message.reply_text("🙏 ဆုတောင်းပေးစေလိုသော အချက်အလက်ကို ရေးပါ:\n\nဥပမာ: /pray ကျန်းမာရေး အတွက်")

async def praylist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /praylist command - Admin only"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ ဤ command သည် Admin များသာ အသုံးပြုနိုင်ပါသည်။")
        return
    
    prayers = bot_data.data.get('prayers', [])
    
    if not prayers:
        await update.message.reply_text("🙏 ဆုတောင်းခံချက်များ မရှိသေးပါ။")
        return
    
    prayer_text = "🙏 **ဆုတောင်းခံချက်စာရင်း:**\n\n"
    for idx, prayer in enumerate(prayers, 1):
        prayer_text += f"{idx}. @{prayer['username']} ({prayer['date']})\n   📝 {prayer['prayer']}\n\n"
    
    await update.message.reply_text(prayer_text, parse_mode=ParseMode.MARKDOWN)

async def set_quiz_trigger(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /set command - Admin only"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ ဤ command သည် Admin များသာ အသုံးပြုနိုင်ပါသည်။")
        return
    
    if context.args and context.args[0].isdigit():
        trigger_count = int(context.args[0])
        bot_data.data['quiz_trigger'] = trigger_count
        bot_data.save_data()
        await update.message.reply_text(f"✅ Quiz trigger ကို {trigger_count} messages သို့ သတ်မှတ်ပြီးပါပြီ။")
    else:
        await update.message.reply_text("❌ အသုံးပြုပုံ: /set <နံပါတ်>\n\nဥပမာ: /set 10")

async def track_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Track messages for quiz trigger"""
    if update.effective_chat.type == "private":
        return
    
    chat_id = update.effective_chat.id
    
    if chat_id not in bot_data.data['message_count']:
        bot_data.data['message_count'][str(chat_id)] = 0
    
    bot_data.data['message_count'][str(chat_id)] += 1
    
    if bot_data.data['message_count'][str(chat_id)] >= bot_data.data['quiz_trigger']:
        bot_data.data['message_count'][str(chat_id)] = 0
        bot_data.save_data()
        
        # Trigger quiz
        await send_random_quiz(update, context)

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /quiz command"""
    track_user(update)
    await send_random_quiz(update, context)

async def send_random_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send random quiz"""
    quizzes = bot_data.data.get('quizzes', [])
    
    if not quizzes:
        await update.message.reply_text("❓ Quiz များ မရှိသေးပါ။")
        return
    
    quiz = random.choice(quizzes)
    
    keyboard = [
        [InlineKeyboardButton(f"A. {quiz['a']}", callback_data=f"quiz_A_{quiz['answer']}")],
        [InlineKeyboardButton(f"B. {quiz['b']}", callback_data=f"quiz_B_{quiz['answer']}")],
        [InlineKeyboardButton(f"C. {quiz['c']}", callback_data=f"quiz_C_{quiz['answer']}")],
        [InlineKeyboardButton(f"D. {quiz['d']}", callback_data=f"quiz_D_{quiz['answer']}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    quiz_text = f"❓ **Quiz Time!**\n\n{quiz['question']}"
    await update.message.reply_text(quiz_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

async def quiz_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle quiz answer callback"""
    query = update.callback_query
    await query.answer()
    
    data_parts = query.data.split('_')
    user_answer = data_parts[1]
    correct_answer = data_parts[2]
    
    user_id = str(update.effective_user.id)
    username = update.effective_user.username or update.effective_user.first_name
    
    if user_id not in bot_data.data['quiz_scores']:
        bot_data.data['quiz_scores'][user_id] = {"name": username, "score": 0}
    
    if user_answer == correct_answer:
        bot_data.data['quiz_scores'][user_id]['score'] += 1
        bot_data.save_data()
        await query.edit_message_text(f"✅ မှန်ကန်ပါသည်! 🎉\n\nမှန်ကန်သော အဖြေ: {correct_answer}\nသင့်ရမှတ်: {bot_data.data['quiz_scores'][user_id]['score']}")
    else:
        await query.edit_message_text(f"❌ မှားပါသည်။\n\nမှန်ကန်သော အဖြေ: {correct_answer}\nသင့်ရမှတ်: {bot_data.data['quiz_scores'][user_id]['score']}")

async def edquiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /edquiz command - Admin only"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ ဤ command သည် Admin များသာ အသုံးပြုနိုင်ပါသည်။")
        return
    
    await update.message.reply_text("""📝 Quiz များကို အောက်ပါ format နှင့် ထည့်ပါ:

Q: မေးခွန်း
A: အဖြေ A
B: အဖြေ B
C: အဖြေ C
D: အဖြေ D
ANS: A

(Quiz များစွာထည့်လိုပါက Q: နဲ့ခွဲပါ)""")
    return WAITING_QUIZ

async def receive_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive quiz"""
    quiz_text = update.message.text.strip()
    quiz_blocks = quiz_text.split('Q:')
    
    added_count = 0
    for block in quiz_blocks:
        if not block.strip():
            continue
        
        lines = [line.strip() for line in block.strip().split('\n') if line.strip()]
        if len(lines) < 6:
            continue
        
        quiz_data = {
            "question": lines[0],
            "a": lines[1].replace('A:', '').strip(),
            "b": lines[2].replace('B:', '').strip(),
            "c": lines[3].replace('C:', '').strip(),
            "d": lines[4].replace('D:', '').strip(),
            "answer": lines[5].replace('ANS:', '').strip()
        }
        
        bot_data.data['quizzes'].append(quiz_data)
        added_count += 1
    
    bot_data.save_data()
    await update.message.reply_text(f"✅ Quiz {added_count} ခု ထည့်သွင်းပြီးပါပြီ။")
    return ConversationHandler.END

async def tops(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /tops command"""
    track_user(update)
    scores = bot_data.data.get('quiz_scores', {})
    
    if not scores:
        await update.message.reply_text("🏆 Quiz အမှတ်စာရင်း မရှိသေးပါ။")
        return
    
    # Sort by score
    sorted_scores = sorted(scores.items(), key=lambda x: x[1]['score'], reverse=True)
    
    tops_text = "🏆 **Quiz Top Scorers:**\n\n"
    for idx, (user_id, data) in enumerate(sorted_scores[:10], 1):
        medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else "🏅"
        tops_text += f"{medal} {idx}. {data['name']} - {data['score']} points\n"
    
    tops_text += "\n✨ Create by: PINLON-YOUTH"
    await update.message.reply_text(tops_text, parse_mode=ParseMode.MARKDOWN)

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /broadcast command - Admin only"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ ဤ command သည် Admin များသာ အသုံးပြုနိုင်ပါသည်။")
        return
    
    await update.message.reply_text("📢 Group များသို့ ပို့လိုသော message ကို ရေးပါ (သို့မဟုတ်) ပုံပို့ပါ:")
    return WAITING_BROADCAST

async def receive_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive and send broadcast message"""
    groups = list(bot_data.data.get('groups', set()))
    
    success_count = 0
    fail_count = 0
    
    for group_id in groups:
        try:
            if update.message.photo:
                # Send photo with caption
                await context.bot.send_photo(
                    chat_id=group_id,
                    photo=update.message.photo[-1].file_id,
                    caption=update.message.caption or ""
                )
            else:
                # Send text message
                await context.bot.send_message(
                    chat_id=group_id,
                    text=update.message.text
                )
            success_count += 1
            await asyncio.sleep(0.5)  # Avoid rate limiting
        except Exception as e:
            logger.error(f"Error sending to {group_id}: {e}")
            fail_count += 1
    
    await update.message.reply_text(f"✅ Broadcast ပို့ပြီးပါပြီ။\n\nအောင်မြင်: {success_count}\nမအောင်မြင်: {fail_count}")
    return ConversationHandler.END

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats command - Admin only"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ ဤ command သည် Admin များသာ အသုံးပြုနိုင်ပါသည်။")
        return
    
    users_count = len(bot_data.data.get('users', set()))
    groups_count = len(bot_data.data.get('groups', set()))
    prayers_count = len(bot_data.data.get('prayers', []))
    quizzes_count = len(bot_data.data.get('quizzes', []))
    
    stats_text = f"""📊 **Bot Statistics:**

👥 Users: {users_count}
👥 Groups: {groups_count}
🙏 Prayer Requests: {prayers_count}
❓ Quizzes: {quizzes_count}
📜 Verses: {len(bot_data.data.get('verses', []))}
📅 Events: {len(bot_data.data.get('events', []))}
🎂 Birthdays: {len(bot_data.data.get('birthdays', []))}
"""
    
    await update.message.reply_text(stats_text, parse_mode=ParseMode.MARKDOWN)

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /report command"""
    track_user(update)
    
    if context.args:
        report_text = ' '.join(context.args)
        username = update.effective_user.username or update.effective_user.first_name
        
        # Send to admins
        for admin_id in ADMIN_IDS:
            try:
                await context.bot.send_message(
                    chat_id=admin_id,
                    text=f"📝 **New Report from @{username}:**\n\n{report_text}",
                    parse_mode=ParseMode.MARKDOWN
                )
            except Exception as e:
                logger.error(f"Error sending report to admin: {e}")
        
        await update.message.reply_text("✅ သင့်တင်ပြချက်ကို လက်ခံပြီးပါပြီ။ ကျေးဇူးတင်ပါသည်။")
    else:
        await update.message.reply_text("📝 တင်ပြလိုသော အကြောင်းအရာကို ရေးပါ:\n\nဥပမာ: /report Bot တွင် ပြဿနာရှိနေပါသည်")

async def backup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /backup command - Admin only"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ ဤ command သည် Admin များသာ အသုံးပြုနိုင်ပါသည်။")
        return
    
    backup_file = bot_data.backup_data()
    
    if backup_file:
        with open(backup_file, 'rb') as f:
            await update.message.reply_document(
                document=f,
                caption=f"💾 Backup ပြုလုပ်ပြီးပါပြီ။\n\n📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
    else:
        await update.message.reply_text("❌ Backup ပြုလုပ်ရာတွင် အမှားအယွင်းရှိနေပါသည်။")

async def restore(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /restore command - Admin only"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ ဤ command သည် Admin များသာ အသုံးပြုနိုင်ပါသည်။")
        return
    
    await update.message.reply_text("📤 ပြန်ယူလိုသော backup file ကို upload လုပ်ပါ။")

async def handle_restore_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle restore file upload"""
    if not is_admin(update.effective_user.id):
        return
    
    if update.message.document:
        try:
            file = await context.bot.get_file(update.message.document.file_id)
            await file.download_to_drive('restore_temp.json')
            
            with open('restore_temp.json', 'r', encoding='utf-8') as f:
                restored_data = json.load(f)
                restored_data['users'] = set(restored_data.get('users', []))
                restored_data['groups'] = set(restored_data.get('groups', []))
                bot_data.data.update(restored_data)
                bot_data.save_data()
            
            os.remove('restore_temp.json')
            await update.message.reply_text("✅ Data ကို အောင်မြင်စွာ ပြန်ယူပြီးပါပြီ။")
        except Exception as e:
            logger.error(f"Error restoring data: {e}")
            await update.message.reply_text("❌ Data ပြန်ယူရာတွင် အမှားအယွင်းရှိနေပါသည်။")

async def allclear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /allclear command - Admin only"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ ဤ command သည် Admin များသာ အသုံးပြုနိုင်ပါသည်။")
        return
    
    keyboard = [
        [InlineKeyboardButton("✅ Yes, Clear All", callback_data="clear_all_yes")],
        [InlineKeyboardButton("❌ Cancel", callback_data="clear_all_no")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "⚠️ **သတိပေးချက်:**\n\nData အားလုံးကို ဖျက်ပစ်မှာ သေချာပါသလား?\n\nဤလုပ်ဆောင်ချက်ကို ပြန်ပြောင်း၍မရပါ!",
        reply_markup=reply_markup,
        parse_mode=ParseMode.MARKDOWN
    )

async def clear_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle clear all callback"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "clear_all_yes":
        bot_data.data = {
            "about": "",
            "contacts": [],
            "verses": [],
            "events": [],
            "birthdays": [],
            "prayers": [],
            "quizzes": [],
            "quiz_scores": {},
            "message_count": {},
            "quiz_trigger": 10,
            "users": set(),
            "groups": set()
        }
        bot_data.save_data()
        await query.edit_message_text("✅ Data အားလုံးကို ရှင်းလင်းပြီးပါပြီ။")
    else:
        await query.edit_message_text("❌ ပယ်ဖျက်လိုက်ပါသည်။")

async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /delete command - Admin only"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ ဤ command သည် Admin များသာ အသုံးပြုနိုင်ပါသည်။")
        return
    
    if not context.args:
        await update.message.reply_text("""❌ အသုံးပြုပုံ: /delete <type> <index>

Types: verse, quiz, event, birthday, contact, prayer

ဥပမာ: /delete verse 1""")
        return
    
    delete_type = context.args[0].lower()
    
    if len(context.args) < 2 or not context.args[1].isdigit():
        await update.message.reply_text("❌ Index နံပါတ်ကို ထည့်ပါ။")
        return
    
    index = int(context.args[1]) - 1
    
    type_map = {
        'verse': 'verses',
        'quiz': 'quizzes',
        'event': 'events',
        'birthday': 'birthdays',
        'contact': 'contacts',
        'prayer': 'prayers'
    }
    
    if delete_type not in type_map:
        await update.message.reply_text("❌ မှားယွင်းသော type။ အသုံးပြုနိုင်သော types: verse, quiz, event, birthday, contact, prayer")
        return
    
    data_key = type_map[delete_type]
    
    if 0 <= index < len(bot_data.data[data_key]):
        deleted_item = bot_data.data[data_key].pop(index)
        bot_data.save_data()
        await update.message.reply_text(f"✅ ဖျက်လိုက်ပါပြီ: {deleted_item if isinstance(deleted_item, str) else 'Item'}")
    else:
        await update.message.reply_text("❌ Index မတွေ့ရှိပါ။")

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel conversation"""
    await update.message.reply_text("❌ ပယ်ဖျက်လိုက်ပါသည်။")
    return ConversationHandler.END

def main():
    """Start the bot"""
    # သင့် Bot Token ကို ဒီမှာထည့်ပါ
    TOKEN = "8442181435:AAHigN8UCaH3hZ5_5Jkw25AnGXM7uKoxNik"
    
    application = Application.builder().token(TOKEN).build()
    
    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("edit", edit_menu))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("contact", contact))
    application.add_handler(CommandHandler("verse", verse))
    application.add_handler(CommandHandler("events", events))
    application.add_handler(CommandHandler("birthday", birthday))
    application.add_handler(CommandHandler("pray", pray))
    application.add_handler(CommandHandler("praylist", praylist))
    application.add_handler(CommandHandler("set", set_quiz_trigger))
    application.add_handler(CommandHandler("quiz", quiz))
    application.add_handler(CommandHandler("tops", tops))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("report", report))
    application.add_handler(CommandHandler("backup", backup))
    application.add_handler(CommandHandler("restore", restore))
    application.add_handler(CommandHandler("allclear", allclear))
    application.add_handler(CommandHandler("delete", delete))
    
    # Conversation handlers
    about_handler = ConversationHandler(
        entry_points=[CommandHandler("edabout", edabout)],
        states={WAITING_ABOUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_about)]},
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    
    contact_handler = ConversationHandler(
        entry_points=[CommandHandler("edcontact", edcontact)],
        states={WAITING_CONTACT: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_contact)]},
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    
    verse_handler = ConversationHandler(
        entry_points=[CommandHandler("edverse", edverse)],
        states={WAITING_VERSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_verse)]},
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    
    events_handler = ConversationHandler(
        entry_points=[CommandHandler("edevents", edevents)],
        states={WAITING_EVENTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_events)]},
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    
    birthday_handler = ConversationHandler(
        entry_points=[CommandHandler("edbirthday", edbirthday)],
        states={WAITING_BIRTHDAY: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_birthday)]},
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    
    quiz_handler = ConversationHandler(
        entry_points=[CommandHandler("edquiz", edquiz)],
        states={WAITING_QUIZ: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_quiz)]},
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    
    broadcast_handler = ConversationHandler(
        entry_points=[CommandHandler("broadcast", broadcast)],
        states={WAITING_BROADCAST: [MessageHandler((filters.TEXT | filters.PHOTO) & ~filters.COMMAND, receive_broadcast)]},
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    
    application.add_handler(about_handler)
    application.add_handler(contact_handler)
    application.add_handler(verse_handler)
    application.add_handler(events_handler)
    application.add_handler(birthday_handler)
    application.add_handler(quiz_handler)
    application.add_handler(broadcast_handler)
    
    # Callback handlers
    application.add_handler(CallbackQueryHandler(quiz_callback, pattern="^quiz_"))
    application.add_handler(CallbackQueryHandler(clear_callback, pattern="^clear_all_"))
    
    # Message tracker for quiz trigger
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, track_messages))
    
    # Document handler for restore
    application.add_handler(MessageHandler(filters.Document.ALL, handle_restore_file))
    
    # Start bot
    print("🚀 Church Community Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
