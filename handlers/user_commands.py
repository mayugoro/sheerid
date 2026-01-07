"""Handler Command User"""
import logging
from typing import Optional

from telegram import Update
from telegram.ext import ContextTypes

from config import ADMIN_USER_ID, DEFAULT_BALANCE
from database_sqlite import Database
from utils.checks import reject_group_command
from utils.messages import (
    get_welcome_message,
    get_about_message,
    get_help_message,
)

logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle command /start - Mode whitelist, hanya admin dan user terdaftar bisa akses"""
    if await reject_group_command(update):
        return

    user = update.effective_user
    user_id = user.id
    username = user.username or ""
    full_name = user.full_name or ""

    # Jika user sudah ada
    if db.user_exists(user_id):
        # Cek apakah dibanned
        if db.is_user_blocked(user_id):
            await update.message.reply_text(
                "🚫 Anda telah dibanned, tidak bisa menggunakan bot ini.\n"
                "Jika ada pertanyaan, hubungi admin."
            )
            return
        
        await update.message.reply_text(
            f"Selamat datang kembali, {full_name}!\n"
            f"💰 Token Saat Ini: {db.get_user(user_id)['balance']:,}\n\n"
            "Kirim /help untuk melihat command yang tersedia."
        )
        return

    # User baru - hanya admin bisa auto register
    if user_id == ADMIN_USER_ID:
        if db.create_user(user_id, username, full_name, None):
            await update.message.reply_text(
                f"✅ Akun admin telah dibuat!\n"
                f"💰 Token: {DEFAULT_BALANCE:,}\n\n"
                "Gunakan /adduser untuk menambah user\n"
                "Gunakan /ban dan /unban untuk kelola permission"
            )
        return

    # Bukan admin dan belum terdaftar - tolak akses
    await update.message.reply_text(
        "⛔ Bot ini menggunakan mode whitelist.\n\n"
        "Anda perlu autorisasi admin untuk menggunakan.\n"
        f"User ID Anda: `{user_id}`\n\n"
        "Silakan kirim User ID ke admin untuk mendapat akses.",
        parse_mode="Markdown"
    )


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle command /about"""
    if await reject_group_command(update):
        return

    await update.message.reply_text(get_about_message())


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle command /help"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id
    is_admin = user_id == ADMIN_USER_ID
    await update.message.reply_text(get_help_message(is_admin))


async def balance_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle command /balance"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id

    if db.is_user_blocked(user_id):
        await update.message.reply_text("Anda telah dibanned, tidak bisa menggunakan fitur ini.")
        return

    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("Silakan hubungi admin untuk registrasi terlebih dahulu.")
        return

    await update.message.reply_text(
        f"💰 Saldo Token\n\nToken Saat Ini: {user['balance']:,}"
    )


async def checkin_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle /qd checkin command - Temporarily disabled"""
    user_id = update.effective_user.id

    # Checkin feature temporary disabled (fixing bug)
    # await update.message.reply_text(
    #     "⚠️ Fitur checkin sedang maintenance\n\n"
    #     "Karena ada bug, fitur checkin sementara ditutup, sedang diperbaiki.\n"
    #     "Diperkirakan segera pulih kembali, mohon maaf atas ketidaknyamanannya.\n\n"
    #     "💡 Anda bisa dapatkan token melalui:\n"
    #     "• Invite teman /invite (+2 token)\n"
    #     "• Pakai card key /use <key_code>"
    # )
    # return
    
    # ===== Code dibawah sudah disabled =====
    if db.is_user_blocked(user_id):
        await update.message.reply_text("⛔ Anda telah dibanned, tidak bisa menggunakan fitur ini.")
        return

    if not db.user_exists(user_id):
        await update.message.reply_text("Silakan gunakan /start untuk registrasi dulu.")
        return

    # Layer 1 check: di level command handler
    if not db.can_checkin(user_id):
        await update.message.reply_text("❌ Hari ini sudah checkin, besok lagi ya.")
        return

    # Layer 2 check: di level database (SQL atomic operation)
    if db.checkin(user_id):
        user = db.get_user(user_id)
        await update.message.reply_text(
            f"✅ Checkin berhasil!\nToken didapat: +1\nToken sekarang: {user['balance']}"
        )
    else:
        # Jika database level return False, artinya hari ini sudah checkin (double safety)
        await update.message.reply_text("❌ Hari ini sudah checkin, besok lagi ya.")


async def invite_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle /invite command"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id

    if db.is_user_blocked(user_id):
        await update.message.reply_text("⛔ Anda telah dibanned, tidak bisa menggunakan fitur ini.")
        return

    if not db.user_exists(user_id):
        await update.message.reply_text("Silakan gunakan /start untuk registrasi dulu.")
        return

    bot_username = context.bot.username
    invite_link = f"https://t.me/{bot_username}?start={user_id}"

    await update.message.reply_text(
        f"🎁 Link invite khusus Anda:\n{invite_link}\n\n"
        "Setiap berhasil invite 1 orang registrasi, Anda dapat 2 token."
    )


async def use_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle command /use - Pakai card key"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id

    if db.is_user_blocked(user_id):
        await update.message.reply_text("⛔ Anda telah dibanned, tidak bisa menggunakan fitur ini.")
        return

    if not db.user_exists(user_id):
        await update.message.reply_text("Silakan gunakan /start untuk registrasi dulu.")
        return

    if not context.args:
        await update.message.reply_text(
            "Cara penggunaan: /use <key_code>\n\nContoh: /use wandouyu"
        )
        return

    key_code = context.args[0].strip()
    result = db.use_card_key(key_code, user_id)

    if result is None:
        await update.message.reply_text("Card key tidak ada, silakan cek lagi.")
    elif result == -1:
        await update.message.reply_text("Card key ini sudah mencapai limit pemakaian.")
    elif result == -2:
        await update.message.reply_text("Card key ini sudah expire.")
    elif result == -3:
        await update.message.reply_text("Anda sudah pernah pakai card key ini.")
    else:
        user = db.get_user(user_id)
        await update.message.reply_text(
            f"Card key berhasil dipakai!\nToken didapat: {result}\nToken sekarang: {user['balance']}"
        )
