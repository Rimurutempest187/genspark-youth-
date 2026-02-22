"""
Church Community Bot - Quick Setup Script
Created by: PINLON-YOUTH

This script helps you set up the bot quickly.
"""

import os
import sys

def setup_bot():
    print("=" * 50)
    print("Church Community Bot Setup")
    print("Created by: PINLON-YOUTH")
    print("=" * 50)
    print()
    
    # Check if .env exists
    if not os.path.exists('.env'):
        print("⚠️  .env file not found!")
        print()
        
        # Get bot token
        bot_token = input("Enter your Bot Token (from @BotFather): ").strip()
        if not bot_token:
            print("❌ Bot token is required!")
            sys.exit(1)
        
        # Get admin IDs
        admin_ids = input("Enter Admin User IDs (comma-separated): ").strip()
        if not admin_ids:
            print("❌ At least one admin ID is required!")
            sys.exit(1)
        
        # Create .env file
        with open('.env', 'w') as f:
            f.write(f"BOT_TOKEN={bot_token}\n")
            f.write(f"ADMIN_IDS={admin_ids}\n")
        
        print()
        print("✅ .env file created successfully!")
        print()
    else:
        print("✅ .env file already exists")
        print()
    
    # Check if bot_data.json exists
    if not os.path.exists('bot_data.json'):
        print("📝 Creating initial data file...")
        import json
        initial_data = {
            "about": "",
            "contacts": [],
            "verses": [
                "တရားတော်သည် ငါ့ခြေ၌ မီးခွက်ဖြစ်၍ ငါ့လမ်း၌ အလင်းဖြစ်၏။ - ဆာလံ ၁၁၉:၁၀၅",
                "သင်တို့သည် ငါ့ကိုခေါ်၍ ဆုတောင်းသောအခါ ငါနားထောင်မည်။ - ယေရမိ ၂၉:၁၂",
                "ငါသည် လမ်းခရီးစဉ်လျှောက်ရာတွင် သင်၏စကားကို ငါ့နှလုံးသွင်း၍ သိုထားပါပြီ။ - ဆာလံ ၁၁၉:၁၁"
            ],
            "events": [],
            "birthdays": [],
            "prayers": [],
            "quizzes": [
                {
                    "question": "လောကကို ဖန်ဆင်းခဲ့သူမှာ မည်သူနည်း?",
                    "choices": {
                        "A": "မောရှေ",
                        "B": "ယေရှု",
                        "C": "ဘုရားသခင်",
                        "D": "အာဗြဟံ"
                    },
                    "answer": "C"
                },
                {
                    "question": "ကယ်တင်ရှင်မည်သူနည်း?",
                    "choices": {
                        "A": "ယောန",
                        "B": "ဒါဝိဒ်",
                        "C": "ယေရှုခရစ်တော်",
                        "D": "ပေတရု"
                    },
                    "answer": "C"
                }
            ],
            "quiz_scores": {},
            "message_count": {},
            "quiz_threshold": 10,
            "users": [],
            "groups": []
        }
        
        with open('bot_data.json', 'w', encoding='utf-8') as f:
            json.dump(initial_data, f, ensure_ascii=False, indent=2)
        
        print("✅ Initial data file created with sample content")
        print()
    
    print("=" * 50)
    print("✅ Setup complete!")
    print()
    print("To start the bot, run:")
    print("  python bot.py")
    print()
    print("Or use the start script:")
    print("  Linux/Mac: ./start.sh")
    print("  Windows:   start.bat")
    print()
    print("=" * 50)

if __name__ == '__main__':
    try:
        setup_bot()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        sys.exit(1)
