"""
Telegram Bot Integration for Karyakarta Field Reporting
========================================================
- Works in a Telegram GROUP (not individual chats)
- 300 karyakartas can send reports from their phones
- Reports are stored in SQLite and shown on dashboard
- Bot commands:
    /report <booth_no> <message> - Submit a field report
    /status - Check booth completion status
    /help - Show help

Setup Instructions:
1. Open Telegram and search for @BotFather
2. Send /newbot and follow instructions to create a bot
3. Copy the bot token
4. Create a Telegram Group and add the bot to it
5. Make the bot a group admin
6. Get the group chat_id (send a message in group, then check
   https://api.telegram.org/bot<TOKEN>/getUpdates)
7. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID below or in config
"""

import os
import sys
import json
import sqlite3
import time
import threading
import requests
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "voters.db"
CONFIG_PATH = BASE_DIR / "telegram_config.json"

# ============================================================
# Configuration
# ============================================================

def load_config():
    """Load Telegram bot configuration."""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    return {
        'bot_token': '',
        'chat_id': '',
        'enabled': False,
    }


def save_config(config):
    """Save Telegram bot configuration."""
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)


# ============================================================
# Database
# ============================================================

def init_reports_db():
    """Create reports table if not exists."""
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        telegram_user_id INTEGER,
        telegram_username TEXT,
        telegram_name TEXT,
        booth_area TEXT,
        booth_no INTEGER,
        message TEXT,
        report_type TEXT DEFAULT 'general'
    )''')
    c.execute('''CREATE INDEX IF NOT EXISTS idx_reports_booth
                 ON reports(booth_area, booth_no)''')
    c.execute('''CREATE INDEX IF NOT EXISTS idx_reports_time
                 ON reports(timestamp DESC)''')
    conn.commit()
    conn.close()


def save_report(user_id, username, name, booth_area, booth_no, message, report_type='general'):
    """Save a field report to database."""
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    c.execute('''INSERT INTO reports
        (timestamp, telegram_user_id, telegram_username, telegram_name,
         booth_area, booth_no, message, report_type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        datetime.now().isoformat(),
        user_id, username, name,
        booth_area, booth_no, message, report_type
    ))
    conn.commit()
    conn.close()


def get_recent_reports(limit=50):
    """Get recent reports for dashboard."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    rows = conn.execute('''
        SELECT * FROM reports ORDER BY timestamp DESC LIMIT ?
    ''', (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_reports_by_booth(area=None, booth_no=None):
    """Get reports filtered by booth."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    if area and booth_no:
        rows = conn.execute('''
            SELECT * FROM reports WHERE booth_area=? AND booth_no=?
            ORDER BY timestamp DESC
        ''', (area, booth_no)).fetchall()
    else:
        rows = conn.execute('SELECT * FROM reports ORDER BY timestamp DESC').fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ============================================================
# Telegram Bot Polling
# ============================================================

class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{token}"
        self.last_update_id = 0
        self.running = False

    def send_message(self, chat_id, text, parse_mode='HTML'):
        """Send a message to a chat."""
        try:
            resp = requests.post(f"{self.base_url}/sendMessage", json={
                'chat_id': chat_id,
                'text': text,
                'parse_mode': parse_mode,
            }, timeout=10)
            return resp.json()
        except Exception as e:
            print(f"Telegram send error: {e}")
            return None

    def get_updates(self, timeout=30):
        """Long-poll for new messages."""
        try:
            resp = requests.get(f"{self.base_url}/getUpdates", params={
                'offset': self.last_update_id + 1,
                'timeout': timeout,
            }, timeout=timeout + 5)
            data = resp.json()
            if data.get('ok'):
                return data.get('result', [])
        except Exception as e:
            print(f"Telegram poll error: {e}")
        return []

    def process_message(self, message):
        """Process an incoming message."""
        chat_id = message['chat']['id']
        user = message.get('from', {})
        user_id = user.get('id', 0)
        username = user.get('username', '')
        name = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
        text = message.get('text', '').strip()

        if not text:
            return

        # /help command
        if text.startswith('/help') or text.startswith('/start'):
            help_text = (
                "🗳️ <b>રણોલી જિલ્લા પંચાયત - કાર્યકર્તા રિપોર્ટિંગ</b>\n\n"
                "Commands:\n"
                "📝 <code>/report [booth_no] [message]</code>\n"
                "   Report from field. Example:\n"
                "   <code>/report 5 વોટર્સ કોન્ટેક્ટ થયા 50</code>\n\n"
                "📊 <code>/status</code> - Booth status\n"
                "❓ <code>/help</code> - Show this help\n\n"
                "You can also just send a message and it will be logged."
            )
            self.send_message(chat_id, help_text)
            return

        # /report command
        if text.startswith('/report'):
            parts = text.split(maxsplit=2)
            if len(parts) >= 3:
                try:
                    booth_no = int(parts[1])
                    report_msg = parts[2]

                    # Determine area from booth number (1-10 = various areas)
                    # For now, store without area - can be refined
                    save_report(user_id, username, name, '', booth_no, report_msg)

                    reply = f"✅ Report saved!\n📍 Booth {booth_no}\n📝 {report_msg}\n👤 {name}"
                    self.send_message(chat_id, reply)
                except ValueError:
                    self.send_message(chat_id, "❌ Invalid booth number. Use: /report [booth_no] [message]")
            elif len(parts) == 2:
                self.send_message(chat_id, "❌ Please add a message. Use: /report [booth_no] [message]")
            else:
                self.send_message(chat_id, "❌ Usage: /report [booth_no] [message]")
            return

        # /status command
        if text.startswith('/status'):
            conn = sqlite3.connect(str(DB_PATH))
            reports = conn.execute('''
                SELECT booth_no, COUNT(*) as count, MAX(timestamp) as last
                FROM reports GROUP BY booth_no ORDER BY booth_no
            ''').fetchall()
            conn.close()

            if reports:
                status = "📊 <b>Booth Report Status</b>\n\n"
                for r in reports:
                    status += f"Booth {r[0]}: {r[1]} reports (last: {r[2][:16]})\n"
            else:
                status = "📊 No reports yet. Use /report to submit."
            self.send_message(chat_id, status)
            return

        # Any other message - log as general report
        save_report(user_id, username, name, '', 0, text, 'chat')

    def start_polling(self):
        """Start polling for messages in a background thread."""
        self.running = True
        init_reports_db()

        def poll_loop():
            print(f"Telegram bot polling started...")
            while self.running:
                try:
                    updates = self.get_updates()
                    for update in updates:
                        self.last_update_id = update['update_id']
                        if 'message' in update:
                            self.process_message(update['message'])
                except Exception as e:
                    print(f"Telegram error: {e}")
                    time.sleep(5)

        thread = threading.Thread(target=poll_loop, daemon=True)
        thread.start()
        return thread

    def stop(self):
        """Stop polling."""
        self.running = False


# ============================================================
# Flask routes for dashboard integration
# ============================================================

def register_telegram_routes(app):
    """Register Telegram-related API routes with the Flask app."""
    from flask import request, jsonify

    @app.route('/api/reports')
    def api_reports():
        """Get recent field reports."""
        limit = int(request.args.get('limit', 50))
        reports = get_recent_reports(limit)
        return jsonify(reports)

    @app.route('/api/reports/booth/<int:booth_no>')
    def api_reports_booth(booth_no):
        """Get reports for a specific booth."""
        reports = get_reports_by_booth(booth_no=booth_no)
        return jsonify(reports)

    @app.route('/api/telegram/config', methods=['GET'])
    def api_telegram_config_get():
        """Get current Telegram config (without token)."""
        config = load_config()
        return jsonify({
            'enabled': config.get('enabled', False),
            'has_token': bool(config.get('bot_token')),
            'chat_id': config.get('chat_id', ''),
        })

    @app.route('/api/telegram/config', methods=['POST'])
    def api_telegram_config_set():
        """Update Telegram config."""
        data = request.json
        config = load_config()
        if 'bot_token' in data:
            config['bot_token'] = data['bot_token']
        if 'chat_id' in data:
            config['chat_id'] = data['chat_id']
        if 'enabled' in data:
            config['enabled'] = data['enabled']
        save_config(config)
        return jsonify({'status': 'ok'})

    @app.route('/api/telegram/test', methods=['POST'])
    def api_telegram_test():
        """Test Telegram bot connection."""
        config = load_config()
        if not config.get('bot_token'):
            return jsonify({'error': 'No bot token configured'}), 400

        bot = TelegramBot(config['bot_token'])
        try:
            resp = requests.get(f"{bot.base_url}/getMe", timeout=10)
            data = resp.json()
            if data.get('ok'):
                bot_info = data['result']
                return jsonify({
                    'status': 'connected',
                    'bot_name': bot_info.get('first_name'),
                    'bot_username': bot_info.get('username'),
                })
            else:
                return jsonify({'error': data.get('description', 'Unknown error')}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500


# Global bot instance
_bot_instance = None

def start_telegram_bot():
    """Start the Telegram bot if configured."""
    global _bot_instance
    config = load_config()
    if config.get('enabled') and config.get('bot_token'):
        init_reports_db()
        _bot_instance = TelegramBot(config['bot_token'])
        _bot_instance.start_polling()
        print(f"Telegram bot started!")
        return True
    return False


def stop_telegram_bot():
    """Stop the Telegram bot."""
    global _bot_instance
    if _bot_instance:
        _bot_instance.stop()
        _bot_instance = None


if __name__ == '__main__':
    # Test mode - run bot directly
    config = load_config()
    if not config.get('bot_token'):
        print("No bot token configured. Please set token in telegram_config.json")
        print("Or run: python telegram_bot.py <YOUR_BOT_TOKEN>")
        if len(sys.argv) > 1:
            config['bot_token'] = sys.argv[1]
            config['enabled'] = True
            save_config(config)
            print(f"Token saved!")

    if config.get('bot_token'):
        init_reports_db()
        bot = TelegramBot(config['bot_token'])
        print(f"Starting bot polling... Press Ctrl+C to stop.")
        bot.running = True
        try:
            while True:
                updates = bot.get_updates()
                for update in updates:
                    bot.last_update_id = update['update_id']
                    if 'message' in update:
                        bot.process_message(update['message'])
        except KeyboardInterrupt:
            print("\nBot stopped.")
