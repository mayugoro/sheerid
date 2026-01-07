"""Program Utama Telegram Bot"""
import logging
from functools import partial

from telegram.ext import Application, CommandHandler

from config import BOT_TOKEN
from database_sqlite import Database
from handlers.user_commands import (
    start_command,
    about_command,
    help_command,
    balance_command,
)
from handlers.verify_commands import (
    verify_command,
    verify2_command,
    verify3_command,
    verify4_command,
    getV4Code_command,
)
from handlers.admin_commands import (
    adduser_command,
    addbalance_command,
    ban_command,
    unban_command,
    block_command,
    white_command,
    blacklist_command,
    broadcast_command,
)

# Konfigurasi logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def error_handler(update: object, context) -> None:
    """Handler error global"""
    logger.exception("Error saat memproses update: %s", context.error, exc_info=context.error)


def main():
    """Fungsi utama"""
    # Inisialisasi database
    db = Database()

    # Buat aplikasi - aktifkan concurrent processing
    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .concurrent_updates(True)  # 🔥 Penting: aktifkan concurrent processing
        .build()
    )

    # Register user commands (menggunakan partial untuk passing db parameter)
    application.add_handler(CommandHandler("start", partial(start_command, db=db)))
    application.add_handler(CommandHandler("about", partial(about_command, db=db)))
    application.add_handler(CommandHandler("help", partial(help_command, db=db)))
    application.add_handler(CommandHandler("balance", partial(balance_command, db=db)))

    # Register verification commands
    application.add_handler(CommandHandler("verify", partial(verify_command, db=db)))
    application.add_handler(CommandHandler("verify2", partial(verify2_command, db=db)))
    application.add_handler(CommandHandler("verify3", partial(verify3_command, db=db)))
    application.add_handler(CommandHandler("verify4", partial(verify4_command, db=db)))
    application.add_handler(CommandHandler("getV4Code", partial(getV4Code_command, db=db)))

    # Register admin commands
    application.add_handler(CommandHandler("adduser", partial(adduser_command, db=db)))
    application.add_handler(CommandHandler("addbalance", partial(addbalance_command, db=db)))
    application.add_handler(CommandHandler("ban", partial(ban_command, db=db)))
    application.add_handler(CommandHandler("unban", partial(unban_command, db=db)))
    application.add_handler(CommandHandler("block", partial(block_command, db=db)))  # Alias
    application.add_handler(CommandHandler("white", partial(white_command, db=db)))  # Alias
    application.add_handler(CommandHandler("blacklist", partial(blacklist_command, db=db)))
    application.add_handler(CommandHandler("broadcast", partial(broadcast_command, db=db)))

    # Register error handler
    application.add_error_handler(error_handler)

    logger.info("Bot sedang startup...")
    application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
