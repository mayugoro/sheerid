"""Utility Pemeriksaan Permission dan Validasi"""
import logging
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


def is_group_chat(update: Update) -> bool:
    """Cek apakah chat adalah grup"""
    chat = update.effective_chat
    return chat and chat.type in ("group", "supergroup")


async def reject_group_command(update: Update) -> bool:
    """Pembatasan grup: hanya izinkan command tertentu"""
    if is_group_chat(update):
        await update.message.reply_text("Grup hanya support /verify /verify2 /verify3 /verify4 /verify5, silakan chat private untuk command lain.")
        return True
    return False


def check_user_registered(user_id: int, db) -> bool:
    """Cek apakah user terdaftar di database"""
    return db.user_exists(user_id)


def check_user_authorized(user_id: int, db) -> tuple[bool, str]:
    """
    Cek apakah user diizinkan menggunakan bot
    Returns: (is_authorized, error_message)
    """
    # Cek apakah user terdaftar
    if not db.user_exists(user_id):
        return False, "❌ Anda belum terdaftar. Hubungi admin untuk mendapat akses."
    
    # Cek apakah user dibanned
    if db.is_user_blocked(user_id):
        return False, "🚫 Anda telah dibanned. Hubungi admin jika ada pertanyaan."
    
    return True, ""


async def require_authorization(update: Update, db) -> bool:
    """
    Middleware untuk cek authorization user
    Returns: True jika user authorized, False jika tidak (dan sudah kirim pesan error)
    """
    user_id = update.effective_user.id
    is_authorized, error_msg = check_user_authorized(user_id, db)
    
    if not is_authorized:
        await update.message.reply_text(error_msg)
        return False
    
    return True
