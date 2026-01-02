#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DuckHunt Challenge - Bale Bot
"""

import os
import time
import requests
import json

BOT_TOKEN = os.getenv('BALE_BOT_TOKEN', '672687492:eFf57XXkjixcslJDuAB38vAc98wZ5qxO7Uk')
GAME_URL = os.getenv('GAME_URL', 'https://duck.darmanjoo.ir')
API_URL = os.getenv('API_URL', 'http://app:3002')
BALE_API = f'https://tapi.bale.ai/bot{BOT_TOKEN}'

user_states = {}

def send_message(chat_id, text, reply_markup=None, parse_mode=None):
    """Send a message to a user"""
    url = f'{BALE_API}/sendMessage'
    data = {
        'chat_id': chat_id,
        'text': text
    }
    if reply_markup:
        data['reply_markup'] = json.dumps(reply_markup)
    if parse_mode:
        data['parse_mode'] = parse_mode

    try:
        response = requests.post(url, json=data)
        return response.json()
    except Exception as e:
        print(f'Error sending message: {e}')
        return None

def send_persistent_keyboard(chat_id):
    """Send persistent keyboard with game and leaderboard buttons"""
    keyboard = {
        'keyboard': [
            [
                {
                    'text': '🎮 شروع بازی',
                    'web_app': {'url': GAME_URL}
                },
                {'text': '🏆 جدول امتیازات'}
            ],
            [
                {'text': '📊 آمار من'}
            ]
        ],
        'resize_keyboard': True,
        'persistent': True
    }
    return keyboard

def send_contact_request(chat_id):
    """Send keyboard with contact request button"""
    keyboard = {
        'keyboard': [[
            {
                'text': '📱 ارسال شماره تماس',
                'request_contact': True
            }
        ]],
        'resize_keyboard': True,
        'one_time_keyboard': True
    }
    text = '✅ کد پرسنلی ثبت شد.\n\nحالا لطفاً شماره تماس خود را با کلیک روی دکمه زیر ارسال کنید:'
    send_message(chat_id, text, reply_markup=keyboard)

def check_user_exists(bale_user_id):
    """Check if user exists in database"""
    try:
        response = requests.get(f'{API_URL}/api/user/{bale_user_id}', timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f'Error checking user: {e}')
        return None

def register_user_in_db(bale_user_id, phone_number, first_name, last_name, employee_code):
    """Register user in database"""
    try:
        data = {
            'baleUserId': str(bale_user_id),
            'phoneNumber': phone_number,
            'firstName': first_name,
            'lastName': last_name,
            'employeeCode': employee_code
        }
        response = requests.post(f'{API_URL}/api/register', json=data, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            print(f'Registration failed: {response.text}')
            return None
    except Exception as e:
        print(f'Error registering user: {e}')
        return None

def get_user_stats(bale_user_id):
    """Get user stats"""
    try:
        stats_response = requests.get(f'{API_URL}/api/user/{bale_user_id}/stats', timeout=5)
        if stats_response.status_code == 200:
            return stats_response.json()
        return None
    except Exception as e:
        print(f'Error getting stats: {e}')
        return None

def format_phone_number(phone):
    """Format phone number to 09xxxxxxxxx format"""
    phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
    if phone.startswith('+98'):
        phone = '0' + phone[3:]
    elif phone.startswith('98'):
        phone = '0' + phone[2:]
    elif phone.startswith('0098'):
        phone = '0' + phone[4:]
    if not phone.startswith('0'):
        phone = '0' + phone
    return phone

def is_valid_phone(text):
    """Check if text looks like a phone number"""
    # Remove spaces and dashes
    cleaned = text.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
    # Check if it's mostly digits
    digits_only = ''.join(c for c in cleaned if c.isdigit() or c == '+')
    # Should be 10-14 digits (with or without country code)
    if len(digits_only) >= 10 and len(digits_only) <= 14:
        return True
    return False

def handle_typed_phone(chat_id, phone_text):
    """Handle manually typed phone number"""
    phone_number = format_phone_number(phone_text)

    user_data = user_states.get(chat_id, {})
    bale_user_id = user_data.get('user_id')
    first_name = user_data.get('first_name')
    last_name = user_data.get('last_name')
    employee_code = user_data.get('employee_code')

    if not all([bale_user_id, first_name, last_name, employee_code]):
        send_message(chat_id, '❌ خطا در ثبت اطلاعات. لطفاً دستور /start را مجدد ارسال کنید.')
        user_states.pop(chat_id, None)
        return

    result = register_user_in_db(bale_user_id, phone_number, first_name, last_name, employee_code)

    if result and result.get('success'):
        user_states[chat_id]['state'] = 'registered'

        confirmation_text = f"""✅ <b>ثبت‌نام با موفقیت انجام شد!</b>

📋 اطلاعات ثبت شده:
• نام: {first_name} {last_name}
• شماره پرسنلی: {employee_code}
• شماره تماس: {phone_number}

🦆 حالا می‌توانید بازی کنید! 🎮

از منوی زیر می‌توانید استفاده کنید:"""

        keyboard = send_persistent_keyboard(chat_id)
        send_message(chat_id, confirmation_text, reply_markup=keyboard, parse_mode='HTML')
    else:
        send_message(chat_id, '❌ خطا در ثبت‌نام. لطفاً دوباره تلاش کنید.\n\nدستور /start را ارسال کنید.')
        user_states.pop(chat_id, None)

def show_leaderboard(chat_id):
    """Display leaderboard"""
    try:
        response = requests.get(f'{API_URL}/api/leaderboard/top/10', timeout=5)
        if response.status_code == 200:
            leaderboard = response.json()

            message = "🏆 <b>۱۰ بازیکن برتر شکار اردک</b>\n\n"

            for i, player in enumerate(leaderboard[:10], 1):
                medal = '🥇' if i == 1 else '🥈' if i == 2 else '🥉' if i == 3 else f'{i}.'
                name = f"{player.get('first_name', '')} {player.get('last_name', '')}"
                score = player.get('high_score', 0)
                ducks = player.get('max_ducks', 0)
                message += f"{medal} {name}: {score} امتیاز ({ducks} اردک)\n"

            message += "\n🦆 شادابی و سلامت در سایه رفاه 🦆"
            send_message(chat_id, message, parse_mode='HTML')
        else:
            send_message(chat_id, '❌ خطا در دریافت جدول امتیازات.')
    except Exception as e:
        print(f'Error showing leaderboard: {e}')
        send_message(chat_id, '❌ خطا در دریافت جدول امتیازات.')

def show_user_stats(chat_id, bale_user_id):
    """Display user statistics"""
    stats = get_user_stats(bale_user_id)

    if stats:
        name = f"{stats.get('first_name', '')} {stats.get('last_name', '')}"
        games_played = stats.get('games_played', 0)
        games_remaining = max(0, 3 - games_played)

        message = f"""📊 <b>آمار {name}</b>

🏅 رتبه شما: {stats.get('rank', 'نامشخص')}
⭐ بالاترین امتیاز: {stats.get('high_score', 0)}
🦆 بیشترین اردک: {stats.get('max_ducks', 0)}
📈 بالاترین مرحله: {stats.get('max_level', 0)}
🎮 تعداد بازی: {games_played} از 3"""

        if games_remaining > 0:
            message += f"\n\n📍 شما هنوز {games_remaining} بازی دارید!"
        else:
            message += "\n\n⚠️ شما تمام بازی‌های خود را انجام داده‌اید."

        message += "\n\n🦆 شادابی و سلامت در سایه رفاه 🦆"
        send_message(chat_id, message, parse_mode='HTML')
    else:
        send_message(chat_id, '❌ خطا در دریافت آمار. لطفاً دوباره تلاش کنید.')

def handle_start(chat_id, user):
    """Handle /start command"""
    bale_user_id = user.get('id')
    first_name = user.get('first_name', 'کاربر')

    existing_user = check_user_exists(bale_user_id)

    if existing_user:
        stats = get_user_stats(bale_user_id)

        if stats:
            welcome_text = f"""خوش آمدید {stats.get('first_name', first_name)} 👋

🦆 به چالش شکار اردک خوش آمدید!

📊 رکورد شما: {stats.get('high_score', 0)} امتیاز
🏅 رتبه: {stats.get('rank', 'نامشخص')}

از منوی زیر می‌توانید بازی کنید:"""
        else:
            welcome_text = f"خوش آمدید {first_name} 👋\n\n🦆 از منوی زیر بازی کنید:"

        keyboard = send_persistent_keyboard(chat_id)
        send_message(chat_id, welcome_text, reply_markup=keyboard, parse_mode='HTML')
        user_states[chat_id] = {'state': 'registered', 'user_id': bale_user_id}
    else:
        welcome_text = f"""سلام {first_name} عزیز! 👋

🦆 به <b>چالش شکار اردک</b> خوش آمدید!

🎯 اداره کل رفاه و درمان

برای شروع، لطفاً <b>نام</b> خود را ارسال کنید:"""

        send_message(chat_id, welcome_text, parse_mode='HTML')
        user_states[chat_id] = {
            'state': 'waiting_first_name',
            'user_id': bale_user_id
        }

def handle_first_name(chat_id, first_name):
    """Handle first name input"""
    if not first_name or len(first_name) < 2:
        send_message(chat_id, '❌ نام نامعتبر است. لطفاً نام معتبر وارد کنید:')
        return

    user_states[chat_id]['first_name'] = first_name
    user_states[chat_id]['state'] = 'waiting_last_name'
    send_message(chat_id, '✅ نام ثبت شد.\n\nحالا لطفاً <b>نام خانوادگی</b> خود را ارسال کنید:', parse_mode='HTML')

def handle_last_name(chat_id, last_name):
    """Handle last name input"""
    if not last_name or len(last_name) < 2:
        send_message(chat_id, '❌ نام خانوادگی نامعتبر است. لطفاً نام خانوادگی معتبر وارد کنید:')
        return

    user_states[chat_id]['last_name'] = last_name
    user_states[chat_id]['state'] = 'waiting_employee_code'
    send_message(chat_id, '✅ نام خانوادگی ثبت شد.\n\nحالا لطفاً <b>شماره پرسنلی</b> خود را ارسال کنید:', parse_mode='HTML')

def handle_employee_code(chat_id, employee_code):
    """Handle employee code input"""
    if not employee_code or len(employee_code) < 3:
        send_message(chat_id, '❌ شماره پرسنلی نامعتبر است. لطفاً دوباره وارد کنید:')
        return

    user_states[chat_id]['employee_code'] = employee_code
    user_states[chat_id]['state'] = 'waiting_contact'
    send_contact_request(chat_id)

def handle_contact(chat_id, contact):
    """Handle contact (phone number) received"""
    phone_number = contact.get('phone_number')

    if not phone_number:
        send_message(chat_id, '❌ شماره تماس دریافت نشد. لطفاً دوباره تلاش کنید.')
        send_contact_request(chat_id)
        return

    phone_number = format_phone_number(phone_number)

    user_data = user_states.get(chat_id, {})
    bale_user_id = user_data.get('user_id')
    first_name = user_data.get('first_name')
    last_name = user_data.get('last_name')
    employee_code = user_data.get('employee_code')

    if not all([bale_user_id, first_name, last_name, employee_code]):
        send_message(chat_id, '❌ خطا در ثبت اطلاعات. لطفاً دستور /start را مجدد ارسال کنید.')
        user_states.pop(chat_id, None)
        return

    result = register_user_in_db(bale_user_id, phone_number, first_name, last_name, employee_code)

    if result and result.get('success'):
        user_states[chat_id]['state'] = 'registered'

        confirmation_text = f"""✅ <b>ثبت‌نام با موفقیت انجام شد!</b>

📋 اطلاعات ثبت شده:
• نام: {first_name} {last_name}
• شماره پرسنلی: {employee_code}
• شماره تماس: {phone_number}

🦆 حالا می‌توانید بازی کنید! 🎮

از منوی زیر می‌توانید استفاده کنید:"""

        keyboard = send_persistent_keyboard(chat_id)
        send_message(chat_id, confirmation_text, reply_markup=keyboard, parse_mode='HTML')
    else:
        send_message(chat_id, '❌ خطا در ثبت‌نام. لطفاً دوباره تلاش کنید.\n\nدستور /start را ارسال کنید.')
        user_states.pop(chat_id, None)

def handle_message(message):
    """Handle incoming messages"""
    chat_id = message['chat']['id']
    user = message.get('from', {})
    text = message.get('text', '').strip()
    contact = message.get('contact')

    print(f'Message from {chat_id}: {text if text else "contact"}')

    if text and text.startswith('/start'):
        handle_start(chat_id, user)
        return

    if contact:
        handle_contact(chat_id, contact)
        return

    bale_user_id = user.get('id')

    if text == '📊 آمار من':
        if bale_user_id:
            existing_user = check_user_exists(bale_user_id)
            if existing_user:
                show_user_stats(chat_id, bale_user_id)
            else:
                send_message(chat_id, 'شما هنوز ثبت‌نام نکرده‌اید. لطفاً دستور /start را ارسال کنید.')
        else:
            send_message(chat_id, 'لطفاً ابتدا دستور /start را ارسال کنید.')
        return

    if text == '🏆 جدول امتیازات':
        show_leaderboard(chat_id)
        return

    user_state = user_states.get(chat_id, {})
    current_state = user_state.get('state')

    if current_state == 'waiting_first_name':
        handle_first_name(chat_id, text)
    elif current_state == 'waiting_last_name':
        handle_last_name(chat_id, text)
    elif current_state == 'waiting_employee_code':
        handle_employee_code(chat_id, text)
    elif current_state == 'waiting_contact':
        # Check if user typed a phone number
        if text and is_valid_phone(text):
            handle_typed_phone(chat_id, text)
        else:
            send_message(chat_id, 'لطفاً شماره تماس خود را وارد کنید یا از دکمه زیر استفاده کنید.')
            send_contact_request(chat_id)
    elif current_state == 'registered':
        send_message(chat_id, 'از دکمه‌های زیر استفاده کنید:\n\n🎮 شروع بازی\n📊 آمار من\n🏆 جدول امتیازات')
    else:
        send_message(chat_id, 'لطفاً دستور /start را ارسال کنید تا شروع کنیم.')

def get_updates(offset=None):
    """Get updates from Bale"""
    url = f'{BALE_API}/getUpdates'
    params = {'timeout': 30}
    if offset:
        params['offset'] = offset

    try:
        response = requests.get(url, params=params, timeout=35)
        return response.json()
    except Exception as e:
        print(f'Error getting updates: {e}')
        return None

def main():
    """Main bot loop"""
    print('DuckHunt Bot starting...')
    print(f'Game URL: {GAME_URL}')
    print(f'API URL: {API_URL}')
    print(f'Bale API: {BALE_API}')
    print('Bot running. Press Ctrl+C to stop.')

    offset = None

    while True:
        try:
            updates = get_updates(offset)

            if not updates or not updates.get('ok'):
                time.sleep(1)
                continue

            for update in updates.get('result', []):
                offset = update['update_id'] + 1

                if 'message' in update:
                    handle_message(update['message'])

        except KeyboardInterrupt:
            print('\nBot stopped.')
            break
        except Exception as e:
            print(f'Error in main loop: {e}')
            time.sleep(5)

if __name__ == '__main__':
    main()
