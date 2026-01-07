"""Handler Command Admin"""
import asyncio
import logging
from datetime import datetime

from telegram import Update
from telegram.ext import ContextTypes

from config import ADMIN_USER_ID, DEFAULT_BALANCE
from database_sqlite import Database
from utils.checks import reject_group_command

logger = logging.getLogger(__name__)


async def adduser_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle command /adduser - Admin menambah user baru"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id

    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("Anda tidak punya izin untuk menggunakan command ini.")
        return

    if not context.args or len(context.args) < 1:
        await update.message.reply_text(
            "Cara penggunaan: /adduser <User ID> [Username] [Nama Lengkap]\n\n"
            "Contoh: /adduser 123456789\n"
            "Contoh: /adduser 123456789 username \"Full Name\""
        )
        return

    try:
        target_user_id = int(context.args[0])
        username = context.args[1] if len(context.args) > 1 else ""
        full_name = " ".join(context.args[2:]) if len(context.args) > 2 else f"User_{target_user_id}"

        if db.user_exists(target_user_id):
            await update.message.reply_text(f"⚠️ User {target_user_id} sudah ada.")
            return

        if db.create_user(target_user_id, username, full_name, None):
            await update.message.reply_text(
                f"✅ Berhasil menambah user!\n"
                f"User ID: {target_user_id}\n"
                f"Username: {username or 'Tidak diset'}\n"
                f"Nama Lengkap: {full_name}\n"
                f"💰 Token Awal: {DEFAULT_BALANCE:,}"
            )
        else:
            await update.message.reply_text("Gagal menambah user, silakan coba lagi nanti.")
    except ValueError:
        await update.message.reply_text("Format parameter salah, User ID harus angka.")


async def addbalance_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle command /addbalance - Admin menambah token"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id

    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("Anda tidak punya izin untuk menggunakan command ini.")
        return

    if not context.args or len(context.args) < 2:
        await update.message.reply_text(
            "Cara penggunaan: /addbalance <User ID> <jumlah>\n\nContoh: /addbalance 123456789 10"
        )
        return

    try:
        target_user_id = int(context.args[0])
        amount = int(context.args[1])

        if not db.user_exists(target_user_id):
            await update.message.reply_text("User tidak ada.")
            return

        if db.add_balance(target_user_id, amount):
            user = db.get_user(target_user_id)
            await update.message.reply_text(
                f"✅ Berhasil menambah {amount:,} token untuk user {target_user_id}.\n"
                f"Token saat ini: {user['balance']:,}"
            )
        else:
            await update.message.reply_text("Operasi gagal, silakan coba lagi nanti.")
    except ValueError:
        await update.message.reply_text("Format parameter salah, silakan input angka yang valid.")


async def ban_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle command /ban - Admin ban user"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id

    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("Anda tidak punya izin untuk menggunakan command ini.")
        return

    if not context.args:
        await update.message.reply_text(
            "Cara penggunaan: /ban <User ID>\n\nContoh: /ban 123456789"
        )
        return

    try:
        target_user_id = int(context.args[0])

        if not db.user_exists(target_user_id):
            await update.message.reply_text("User tidak ada.")
            return

        if db.block_user(target_user_id):
            await update.message.reply_text(f"🚫 User {target_user_id} telah dibanned.")
        else:
            await update.message.reply_text("Operasi gagal, silakan coba lagi nanti.")
    except ValueError:
        await update.message.reply_text("Format parameter salah, silakan input User ID yang valid.")


async def block_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Alias for ban_command"""
    await ban_command(update, context, db)


async def unban_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle command /unban - Admin unban user"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id

    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("Anda tidak punya izin untuk menggunakan command ini.")
        return

    if not context.args:
        await update.message.reply_text(
            "Cara penggunaan: /unban <User ID>\n\nContoh: /unban 123456789"
        )
        return

    try:
        target_user_id = int(context.args[0])

        if not db.user_exists(target_user_id):
            await update.message.reply_text("User tidak ada.")
            return

        if db.unblock_user(target_user_id):
            await update.message.reply_text(f"✅ User {target_user_id} telah di-unban.")
        else:
            await update.message.reply_text("Operasi gagal, silakan coba lagi nanti.")
    except ValueError:
        await update.message.reply_text("Format parameter salah, silakan input User ID yang valid.")


async def white_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Alias for unban_command"""
    await unban_command(update, context, db)


async def blacklist_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle command /blacklist - Lihat blacklist"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id

    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("Anda tidak punya izin untuk menggunakan command ini.")
        return

    blacklist = db.get_blacklist()

    if not blacklist:
        await update.message.reply_text("Blacklist kosong.")
        return

    msg = "📋 Daftar Blacklist:\n\n"
    for user in blacklist:
        msg += f"User ID: {user['user_id']}\n"
        msg += f"Username: @{user['username']}\n"
        msg += f"Nama: {user['full_name']}\n"
        msg += "---\n"

    await update.message.reply_text(msg)


async def genkey_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle command /genkey - Admin generate card key"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id

    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("Anda tidak punya izin untuk menggunakan command ini.")
        return

    if not context.args or len(context.args) < 2:
        await update.message.reply_text(
            "Cara penggunaan: /genkey <key_code> <token> [jumlah_pakai] [expire_hari]\n\n"
            "Contoh:\n"
            "/genkey wandouyu 20 - Generate card key 20 token (pakai 1x, tidak expire)\n"
            "/genkey vip100 50 10 - Generate card key 50 token (pakai 10x, tidak expire)\n"
            "/genkey temp 30 1 7 - Generate card key 30 token (pakai 1x, expire 7 hari)"
        )
        return

    try:
        key_code = context.args[0].strip()
        balance = int(context.args[1])
        max_uses = int(context.args[2]) if len(context.args) > 2 else 1
        expire_days = int(context.args[3]) if len(context.args) > 3 else None

        if balance <= 0:
            await update.message.reply_text("Jumlah token harus lebih dari 0.")
            return

        if max_uses <= 0:
            await update.message.reply_text("Jumlah pakai harus lebih dari 0.")
            return

        if db.create_card_key(key_code, balance, user_id, max_uses, expire_days):
            msg = (
                "✅ Card key berhasil digenerate!\n\n"
                f"Key code: {key_code}\n"
                f"Token: {balance}\n"
                f"Jumlah pakai: {max_uses}x\n"
            )
            if expire_days:
                msg += f"Expire: {expire_days} hari\n"
            else:
                msg += "Expire: Permanent\n"
            msg += f"\nCara pakai user: /use {key_code}"
            await update.message.reply_text(msg)
        else:
            await update.message.reply_text("Card key sudah ada atau gagal generate, silakan ganti nama key.")
    except ValueError:
        await update.message.reply_text("Format parameter salah, silakan input angka yang valid.")


async def listkeys_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle command /listkeys - Admin lihat daftar card key"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id

    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("Anda tidak punya izin untuk menggunakan command ini.")
        return

    keys = db.get_all_card_keys()

    if not keys:
        await update.message.reply_text("Belum ada card key.")
        return

    msg = "📋 Daftar Card Key:\n\n"
    for key in keys[:20]:  # Hanya tampilkan 20 pertama
        msg += f"Key code: {key['key_code']}\n"
        msg += f"Token: {key['balance']}\n"
        msg += f"Jumlah pakai: {key['current_uses']}/{key['max_uses']}\n"

        if key["expire_at"]:
            expire_time = datetime.fromisoformat(key["expire_at"])
            if datetime.now() > expire_time:
                msg += "Status: Sudah expire\n"
            else:
                days_left = (expire_time - datetime.now()).days
                msg += f"Status: Valid (sisa {days_left} hari)\n"
        else:
            msg += "Status: Permanent\n"

        msg += "---\n"

    if len(keys) > 20:
        msg += f"\n(Hanya tampilkan 20 pertama, total {len(keys)} keys)"

    await update.message.reply_text(msg)


async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle command /broadcast - Admin broadcast notifikasi"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id
    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("Anda tidak punya izin untuk menggunakan command ini.")
        return

    text = " ".join(context.args).strip() if context.args else ""
    if not text and update.message.reply_to_message:
        text = update.message.reply_to_message.text or ""

    if not text:
        await update.message.reply_text("Cara penggunaan: /broadcast <teks>, atau reply message lalu kirim /broadcast")
        return

    user_ids = db.get_all_user_ids()
    success, failed = 0, 0

    status_msg = await update.message.reply_text(f"📢 Mulai broadcast, total {len(user_ids)} user...")

    for uid in user_ids:
        try:
            await context.bot.send_message(chat_id=uid, text=text)
            success += 1
            await asyncio.sleep(0.05)  # Rate limit sedikit untuk hindari limit
        except Exception as e:
            logger.warning("Broadcast ke %s gagal: %s", uid, e)
            failed += 1

    await status_msg.edit_text(f"✅ Broadcast selesai!\nBerhasil: {success}\nGagal: {failed}")


async def userlist_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle command /userlist - Admin lihat semua user"""
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id

    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("Anda tidak punya izin untuk menggunakan command ini.")
        return

    users = db.get_all_users()
    
    if not users:
        await update.message.reply_text("Tidak ada user yang terdaftar.")
        return

    # Buat file txt
    txt_content = "Daftar User Bot Verifikasi SheerID\n"
    txt_content += "=" * 80 + "\n"
    txt_content += f"Total User: {len(users)}\n"
    txt_content += f"Dibuat pada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    txt_content += "=" * 80 + "\n\n"
    txt_content += f"{'ID':<15} | {'Username':<20} | {'Tanggal Bergabung':<20} | {'Status':<10}\n"
    txt_content += "-" * 80 + "\n"

    for user in users:
        user_id_str = str(user['user_id'])
        username = f"@{user['username']}" if user['username'] else "No Username"
        created_at = user['created_at'][:10] if user['created_at'] else "Unknown"
        
        # Status: ✅ jika tidak blocked, ❌ jika blocked
        status = "❌ Blocked" if user['is_blocked'] == 1 else "✅ Allowed"
        
        txt_content += f"{user_id_str:<15} | {username:<20} | {created_at:<20} | {status:<10}\n"

    # Simpan ke file temporary
    file_path = "userlist.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(txt_content)

    # Kirim file ke admin
    with open(file_path, "rb") as f:
        await update.message.reply_document(
            document=f,
            filename=f"userlist_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            caption=f"📊 Daftar {len(users)} user"
        )

    # Hapus file temporary
    import os
    os.remove(file_path)
