"""File Konfigurasi Global"""
import os
from dotenv import load_dotenv

# Load file .env
load_dotenv()

# Konfigurasi Telegram Bot
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# Konfigurasi Admin
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", "123456789"))

# Konfigurasi Token
DEFAULT_BALANCE = 1000000000  # Default 1 milyar token (unlimited)
VERIFY_COST = 1  # Token yang dikonsumsi per verifikasi

# Mode Whitelist - Default hanya izinkan user terdaftar
WHITELIST_MODE = True

# Link bantuan
HELP_NOTION_URL = "https://rhetorical-era-3f3.notion.site/dd78531dbac745af9bbac156b51da9cc"
