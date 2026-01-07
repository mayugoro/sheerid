"""Handler Command Verifikasi"""
import asyncio
import logging
import httpx
import time
from typing import Optional

from telegram import Update
from telegram.ext import ContextTypes

from config import VERIFY_COST
from database_sqlite import Database
from one.sheerid_verifier import SheerIDVerifier as OneVerifier
from k12.sheerid_verifier import SheerIDVerifier as K12Verifier
from spotify.sheerid_verifier import SheerIDVerifier as SpotifyVerifier
from youtube.sheerid_verifier import SheerIDVerifier as YouTubeVerifier
from Boltnew.sheerid_verifier import SheerIDVerifier as BoltnewVerifier
from military.sheerid_verifier import SheerIDVerifier as MilitaryVerifier
from utils.messages import get_insufficient_balance_message, get_verify_usage_message

# Coba import concurrency control, jika gagal gunakan implementasi sederhana
try:
    from utils.concurrency import get_verification_semaphore
except ImportError:
    # Jika import gagal, buat implementasi sederhana
    def get_verification_semaphore(verification_type: str):
        return asyncio.Semaphore(3)

logger = logging.getLogger(__name__)


async def verify_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle command /verify - Gemini One Pro"""
    user_id = update.effective_user.id

    if db.is_user_blocked(user_id):
        await update.message.reply_text("Anda telah dibanned, tidak bisa menggunakan fitur ini.")
        return

    if not db.user_exists(user_id):
        await update.message.reply_text("Silakan hubungi admin untuk registrasi terlebih dahulu.")
        return

    if not context.args:
        await update.message.reply_text(
            get_verify_usage_message("/verify", "Gemini One Pro")
        )
        return

    url = context.args[0]
    user = db.get_user(user_id)
    if user["balance"] < VERIFY_COST:
        await update.message.reply_text(
            get_insufficient_balance_message(user["balance"])
        )
        return

    verification_id = OneVerifier.parse_verification_id(url)
    if not verification_id:
        await update.message.reply_text("Link SheerID tidak valid, silakan cek dan coba lagi.")
        return

    if not db.deduct_balance(user_id, VERIFY_COST):
        await update.message.reply_text("Gagal kurangi token, silakan coba lagi nanti.")
        return

    processing_msg = await update.message.reply_text(
        f"Mulai memproses Gemini One Pro verifikasi...\n"
        f"ID Verifikasi: {verification_id}\n"
        f"Telah dikurangi {VERIFY_COST} token\n\n"
        "Mohon tunggu, ini mungkin memakan waktu 1-2 menit..."
    )

    try:
        verifier = OneVerifier(verification_id)
        result = await asyncio.to_thread(verifier.verify)

        db.add_verification(
            user_id,
            "gemini_one_pro",
            url,
            "success" if result["success"] else "failed",
            str(result),
        )

        if result["success"]:
            result_msg = "✅ Verifikasi berhasil!\n\n"
            if result.get("pending"):
                result_msg += "Dokumen telah disubmit, menunggu review manual.\n"
            if result.get("redirect_url"):
                result_msg += f"Link redirect:\n{result['redirect_url']}"
            await processing_msg.edit_text(result_msg)
        else:
            db.add_balance(user_id, VERIFY_COST)
            await processing_msg.edit_text(
                f"❌ Verifikasi gagal: {result.get('message', 'Error tidak diketahui')}\n\n"
                f"Telah dikembalikan {VERIFY_COST} token"
            )
    except Exception as e:
        logger.error("Error saat proses verifikasi: %s", e)
        db.add_balance(user_id, VERIFY_COST)
        await processing_msg.edit_text(
            f"❌ Terjadi error saat proses: {str(e)}\n\n"
            f"Telah dikembalikan {VERIFY_COST} token"
        )


async def verify2_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle command /verify2 - ChatGPT Teacher K12"""
    user_id = update.effective_user.id

    if db.is_user_blocked(user_id):
        await update.message.reply_text("Anda telah diblokir, tidak dapat menggunakan fitur ini.")
        return

    if not db.user_exists(user_id):
        await update.message.reply_text("Silakan gunakan /start untuk registrasi dulu.")
        return

    if not context.args:
        await update.message.reply_text(
            get_verify_usage_message("/verify2", "ChatGPT Teacher K12")
        )
        return

    url = context.args[0]
    user = db.get_user(user_id)
    if user["balance"] < VERIFY_COST:
        await update.message.reply_text(
            get_insufficient_balance_message(user["balance"])
        )
        return

    verification_id = K12Verifier.parse_verification_id(url)
    if not verification_id:
        await update.message.reply_text("Link SheerID tidak valid, silakan cek dan coba lagi.")
        return

    if not db.deduct_balance(user_id, VERIFY_COST):
        await update.message.reply_text("Gagal kurangi token, silakan coba lagi nanti.")
        return

    processing_msg = await update.message.reply_text(
        f"Mulai memproses ChatGPT Teacher K12 verifikasi...\n"
        f"ID Verifikasi: {verification_id}\n"
        f"Telah dikurangi {VERIFY_COST} token\n\n"
        "Mohon tunggu, ini mungkin memakan waktu 1-2 menit..."
    )

    try:
        verifier = K12Verifier(verification_id)
        result = await asyncio.to_thread(verifier.verify)

        db.add_verification(
            user_id,
            "chatgpt_teacher_k12",
            url,
            "success" if result["success"] else "failed",
            str(result),
        )

        if result["success"]:
            result_msg = "✅ Verifikasi berhasil!\n\n"
            if result.get("pending"):
                result_msg += "Dokumen telah disubmit, menunggu review manual.\n"
            if result.get("redirect_url"):
                result_msg += f"Link redirect:\n{result['redirect_url']}"
            await processing_msg.edit_text(result_msg)
        else:
            db.add_balance(user_id, VERIFY_COST)
            await processing_msg.edit_text(
                f"❌ Verifikasi gagal: {result.get('message', 'Error tidak diketahui')}\n\n"
                f"Telah dikembalikan {VERIFY_COST} token"
            )
    except Exception as e:
        logger.error("Error saat proses verifikasi: %s", e)
        db.add_balance(user_id, VERIFY_COST)
        await processing_msg.edit_text(
            f"❌ Terjadi error saat proses: {str(e)}\n\n"
            f"Telah dikembalikan {VERIFY_COST} token"
        )


async def verify3_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle command /verify3 - Spotify Student"""
    user_id = update.effective_user.id

    if db.is_user_blocked(user_id):
        await update.message.reply_text("Anda telah diblokir, tidak dapat menggunakan fitur ini.")
        return

    if not db.user_exists(user_id):
        await update.message.reply_text("Silakan gunakan /start untuk registrasi dulu.")
        return

    if not context.args:
        await update.message.reply_text(
            get_verify_usage_message("/verify3", "Spotify Student")
        )
        return

    url = context.args[0]
    user = db.get_user(user_id)
    if user["balance"] < VERIFY_COST:
        await update.message.reply_text(
            get_insufficient_balance_message(user["balance"])
        )
        return

    # Parse verificationId
    verification_id = SpotifyVerifier.parse_verification_id(url)
    if not verification_id:
        await update.message.reply_text("Link SheerID tidak valid, silakan cek dan coba lagi.")
        return

    if not db.deduct_balance(user_id, VERIFY_COST):
        await update.message.reply_text("Gagal kurangi token, silakan coba lagi nanti.")
        return

    processing_msg = await update.message.reply_text(
        f"🎵 Mulai memproses Spotify Student verifikasi...\n"
        f"Telah dikurangi {VERIFY_COST} token\n\n"
        "📝 Sedang generate info mahasiswa...\n"
        "🎨 Sedang generate kartu mahasiswa PNG...\n"
        "📤 Sedang submit dokumen..."
    )

    # Gunakan semaphore untuk kontrol concurrent
    semaphore = get_verification_semaphore("spotify_student")

    try:
        async with semaphore:
            verifier = SpotifyVerifier(verification_id)
            result = await asyncio.to_thread(verifier.verify)

        db.add_verification(
            user_id,
            "spotify_student",
            url,
            "success" if result["success"] else "failed",
            str(result),
        )

        if result["success"]:
            result_msg = "✅ Spotify Student verifikasi berhasil!\n\n"
            if result.get("pending"):
                result_msg += "✨ Dokumen sudah disubmit, menunggu review SheerID\n"
                result_msg += "⏱️ Estimasi waktu review: beberapa menit\n\n"
            if result.get("redirect_url"):
                result_msg += f"🔗 Link redirect:\n{result['redirect_url']}"
            await processing_msg.edit_text(result_msg)
        else:
            db.add_balance(user_id, VERIFY_COST)
            await processing_msg.edit_text(
                f"❌ Verifikasi gagal: {result.get('message', 'Error tidak diketahui')}\n\n"
                f"Telah dikembalikan {VERIFY_COST} token"
            )
    except Exception as e:
        logger.error("Spotify verifikasi error: %s", e)
        db.add_balance(user_id, VERIFY_COST)
        await processing_msg.edit_text(
            f"❌ Terjadi error saat proses: {str(e)}\n\n"
            f"Telah dikembalikan {VERIFY_COST} token"
        )


async def verify4_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle command /verify4 - Bolt.new Teacher (auto dapatkan code)"""
    user_id = update.effective_user.id

    if db.is_user_blocked(user_id):
        await update.message.reply_text("Anda telah diblokir, tidak dapat menggunakan fitur ini.")
        return

    if not db.user_exists(user_id):
        await update.message.reply_text("Silakan gunakan /start untuk registrasi dulu.")
        return

    if not context.args:
        await update.message.reply_text(
            get_verify_usage_message("/verify4", "Bolt.new Teacher")
        )
        return

    url = context.args[0]
    user = db.get_user(user_id)
    if user["balance"] < VERIFY_COST:
        await update.message.reply_text(
            get_insufficient_balance_message(user["balance"])
        )
        return

    # Parse externalUserId atau verificationId
    external_user_id = BoltnewVerifier.parse_external_user_id(url)
    verification_id = BoltnewVerifier.parse_verification_id(url)

    if not external_user_id and not verification_id:
        await update.message.reply_text("Link SheerID tidak valid, silakan cek dan coba lagi.")
        return

    if not db.deduct_balance(user_id, VERIFY_COST):
        await update.message.reply_text("Gagal kurangi token, silakan coba lagi nanti.")
        return

    processing_msg = await update.message.reply_text(
        f"🚀 Mulai memproses Bolt.new Teacher verifikasi...\n"
        f"Telah dikurangi {VERIFY_COST} token\n\n"
        "📤 Sedang submit dokumen..."
    )

    # Menggunakan semaphore untuk kontrol concurrent
    semaphore = get_verification_semaphore("bolt_teacher")

    try:
        async with semaphore:
            # Step 1: Submit dokumen
            verifier = BoltnewVerifier(url, verification_id=verification_id)
            result = await asyncio.to_thread(verifier.verify)

        if not result.get("success"):
            # Submit gagal, refund
            db.add_balance(user_id, VERIFY_COST)
            await processing_msg.edit_text(
                f"❌ Submit dokumen gagal: {result.get('message', 'Error tidak diketahui')}\n\n"
                f"Telah dikembalikan {VERIFY_COST} token"
            )
            return
        
        vid = result.get("verification_id", "")
        if not vid:
            db.add_balance(user_id, VERIFY_COST)
            await processing_msg.edit_text(
                f"❌ Tidak dapat ID verifikasi\n\n"
                f"Telah dikembalikan {VERIFY_COST} token"
            )
            return
        
        # Update pesan
        await processing_msg.edit_text(
            f"✅ Dokumen sudah disubmit!\n"
            f"📋 ID Verifikasi: `{vid}`\n\n"
            f"🔍 Sedang otomatis dapatkan code verifikasi...\n"
            f"(Maksimal tunggu 20 detik)"
        )
        
        # Step 2: Otomatis dapatkan code verifikasi (maksimal 20 detik)
        code = await _auto_get_reward_code(vid, max_wait=20, interval=5)
        
        if code:
            # Berhasil dapatkan
            result_msg = (
                f"🎉 Verifikasi berhasil!\n\n"
                f"✅ Dokumen sudah disubmit\n"
                f"✅ Review sudah disetujui\n"
                f"✅ Code verifikasi sudah didapat\n\n"
                f"🎁 Code verifikasi: `{code}`\n"
            )
            if result.get("redirect_url"):
                result_msg += f"\n🔗 Link redirect:\n{result['redirect_url']}"
            
            await processing_msg.edit_text(result_msg)
            
            # Simpan record berhasil
            db.add_verification(
                user_id,
                "bolt_teacher",
                url,
                "success",
                f"Code: {code}",
                vid
            )
        else:
            # 20 detik belum dapat, user query manual nanti
            await processing_msg.edit_text(
                f"✅ Dokumen sudah disubmit berhasil!\n\n"
                f"⏳ Code verifikasi belum digenerate (mungkin butuh 1-5 menit review)\n\n"
                f"📋 ID Verifikasi: `{vid}`\n\n"
                f"💡 Silakan gunakan command berikut untuk query nanti:\n"
                f"`/getV4Code {vid}`\n\n"
                f"Catatan: Token sudah terpakai, query nanti tidak bayar lagi"
            )
            
            # Simpan record pending
            db.add_verification(
                user_id,
                "bolt_teacher",
                url,
                "pending",
                "Waiting for review",
                vid
            )
            
    except Exception as e:
        logger.error("Bolt.new proses verifikasi error: %s", e)
        db.add_balance(user_id, VERIFY_COST)
        await processing_msg.edit_text(
            f"❌ Terjadi error saat proses: {str(e)}\n\n"
            f"Telah dikembalikan {VERIFY_COST} token"
        )


async def _auto_get_reward_code(
    verification_id: str,
    max_wait: int = 20,
    interval: int = 5
) -> Optional[str]:
    """Otomatis dapatkan code verifikasi (polling ringan, tidak ganggu concurrent)
    
    Args:
        verification_id: ID Verifikasi
        max_wait: Waktu tunggu maksimal (detik)
        interval: Interval polling (detik)
        
    Returns:
        str: Code verifikasi, jika gagal return None
    """
    import time
    start_time = time.time()
    attempts = 0
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        while True:
            elapsed = int(time.time() - start_time)
            attempts += 1
            
            # Cek apakah timeout
            if elapsed >= max_wait:
                logger.info(f"Otomatis dapatkan code timeout({elapsed} detik), biarkan user query manual")
                return None
            
            try:
                # Query status verifikasi
                response = await client.get(
                    f"https://my.sheerid.com/rest/v2/verification/{verification_id}"
                )
                
                if response.status_code == 200:
                    data = response.json()
                    current_step = data.get("currentStep")
                    
                    if current_step == "success":
                        # Dapatkan code verifikasi
                        code = data.get("rewardCode") or data.get("rewardData", {}).get("rewardCode")
                        if code:
                            logger.info(f"✅ Otomatis dapatkan code berhasil: {code} (waktu {elapsed} detik)")
                            return code
                    elif current_step == "error":
                        # Review gagal
                        logger.warning(f"Review gagal: {data.get('errorIds', [])}")
                        return None
                    # else: pending, terus tunggu
                
                # Tunggu polling berikutnya
                await asyncio.sleep(interval)
                
            except Exception as e:
                logger.warning(f"Query code verifikasi error: {e}")
                await asyncio.sleep(interval)
    
    return None


async def verify5_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle command /verify5 - YouTube Student Premium"""
    user_id = update.effective_user.id

    if db.is_user_blocked(user_id):
        await update.message.reply_text("⛔ Anda telah dibanned, tidak bisa menggunakan fitur ini.")
        return

    if not db.user_exists(user_id):
        await update.message.reply_text("Silakan gunakan /start untuk registrasi dulu.")
        return

    if not context.args:
        await update.message.reply_text(
            get_verify_usage_message("/verify5", "YouTube Student Premium")
        )
        return

    url = context.args[0]
    user = db.get_user(user_id)
    if user["balance"] < VERIFY_COST:
        await update.message.reply_text(
            get_insufficient_balance_message(user["balance"])
        )
        return

    # Parse verificationId
    verification_id = YouTubeVerifier.parse_verification_id(url)
    if not verification_id:
        await update.message.reply_text("Link SheerID tidak valid, silakan cek dan coba lagi.")
        return

    if not db.deduct_balance(user_id, VERIFY_COST):
        await update.message.reply_text("Gagal kurangi token, silakan coba lagi nanti.")
        return

    processing_msg = await update.message.reply_text(
        f"📺 Mulai memproses YouTube Student Premium verifikasi...\n"
        f"Telah dikurangi {VERIFY_COST} token\n\n"
        "📝 Sedang generate info siswa...\n"
        "🎨 Sedang generate kartu siswa PNG...\n"
        "📤 Sedang submit dokumen..."
    )

    # Gunakan semaphore untuk kontrol concurrent
    semaphore = get_verification_semaphore("youtube_student")

    try:
        async with semaphore:
            verifier = YouTubeVerifier(verification_id)
            result = await asyncio.to_thread(verifier.verify)

        db.add_verification(
            user_id,
            "youtube_student",
            url,
            "success" if result["success"] else "failed",
            str(result),
        )

        if result["success"]:
            result_msg = "✅ YouTube Student Premium verifikasi berhasil!\n\n"
            if result.get("pending"):
                result_msg += "✨ Dokumen sudah disubmit, menunggu review SheerID\n"
                result_msg += "⏱️ Estimasi waktu review: beberapa menit\n\n"
            if result.get("redirect_url"):
                result_msg += f"🔗 Link redirect:\n{result['redirect_url']}"
            await processing_msg.edit_text(result_msg)
        else:
            db.add_balance(user_id, VERIFY_COST)
            await processing_msg.edit_text(
                f"❌ Verifikasi gagal: {result.get('message', 'Error tidak diketahui')}\n\n"
                f"Telah dikembalikan {VERIFY_COST} token"
            )
    except Exception as e:
        logger.error("YouTube proses verifikasi error: %s", e)
        db.add_balance(user_id, VERIFY_COST)
        await processing_msg.edit_text(
            f"❌ Terjadi error saat proses: {str(e)}\n\n"
            f"Telah dikembalikan {VERIFY_COST} token"
        )


async def getV4Code_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle command /getV4Code - Dapatkan code verifikasi Bolt.new Teacher"""
    user_id = update.effective_user.id

    if db.is_user_blocked(user_id):
        await update.message.reply_text("⛔ Anda telah dibanned, tidak bisa menggunakan fitur ini.")
        return

    if not db.user_exists(user_id):
        await update.message.reply_text("Silakan gunakan /start untuk registrasi dulu.")
        return

    # Cek apakah verification_id diberikan
    if not context.args:
        await update.message.reply_text(
            "Cara penggunaan: /getV4Code <verification_id>\n\n"
            "Contoh: /getV4Code 6929436b50d7dc18638890d0\n\n"
            "verification_id akan diberikan setelah pakai command /verify4."
        )
        return

    verification_id = context.args[0].strip()

    processing_msg = await update.message.reply_text(
        "🔍 Sedang query code verifikasi, mohon tunggu..."
    )

    try:
        # Query SheerID API untuk dapatkan code verifikasi
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"https://my.sheerid.com/rest/v2/verification/{verification_id}"
            )

            if response.status_code != 200:
                await processing_msg.edit_text(
                    f"❌ Query gagal, status code: {response.status_code}\n\n"
                    "Silakan coba lagi nanti atau hubungi admin."
                )
                return

            data = response.json()
            current_step = data.get("currentStep")
            reward_code = data.get("rewardCode") or data.get("rewardData", {}).get("rewardCode")
            redirect_url = data.get("redirectUrl")

            if current_step == "success" and reward_code:
                result_msg = "✅ Verifikasi berhasil!\n\n"
                result_msg += f"🎉 Code verifikasi: `{reward_code}`\n\n"
                if redirect_url:
                    result_msg += f"Link redirect:\n{redirect_url}"
                await processing_msg.edit_text(result_msg)
            elif current_step == "pending":
                await processing_msg.edit_text(
                    "⏳ Verifikasi masih dalam review, silakan coba lagi nanti.\n\n"
                    "Biasanya butuh 1-5 menit, mohon sabar menunggu."
                )
            elif current_step == "error":
                error_ids = data.get("errorIds", [])
                await processing_msg.edit_text(
                    f"❌ Verifikasi gagal\n\n"
                    f"Info error: {', '.join(error_ids) if error_ids else 'Error tidak diketahui'}"
                )
            else:
                await processing_msg.edit_text(
                    f"⚠️ Status saat ini: {current_step}\n\n"
                    "Code verifikasi belum digenerate, silakan coba lagi nanti."
                )

    except Exception as e:
        logger.error("Dapatkan code verifikasi Bolt.new gagal: %s", e)
        await processing_msg.edit_text(
            f"❌ Terjadi error saat query: {str(e)}\n\n"
            "Silakan coba lagi nanti atau hubungi admin."
        )


async def verify5_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    """Handle command /verify5 - ChatGPT Military Veteran"""
    user_id = update.effective_user.id

    if db.is_user_blocked(user_id):
        await update.message.reply_text("Anda telah diblokir, tidak dapat menggunakan fitur ini.")
        return

    if not db.user_exists(user_id):
        await update.message.reply_text("Silakan gunakan /start untuk registrasi dulu.")
        return

    if not context.args or len(context.args) < 2:
        await update.message.reply_text(
            "Cara penggunaan: /verify5 <link> <email>\n\n"
            "Contoh:\n"
            "/verify5 https://services.sheerid.com/verify/...?verificationId=xxx user@gmail.com\n\n"
            "⚠️ Gunakan email Anda sendiri karena SheerID akan mengirim link verifikasi ke email tersebut.\n"
            "Setelah bot submit data, cek email dan klik link verifikasi dari SheerID."
        )
        return

    url = context.args[0]
    email = context.args[1]
    
    user = db.get_user(user_id)
    if user["balance"] < VERIFY_COST:
        await update.message.reply_text(
            get_insufficient_balance_message(user["balance"])
        )
        return

    verification_id = MilitaryVerifier.parse_verification_id(url)
    if not verification_id:
        await update.message.reply_text("Link SheerID tidak valid, silakan cek dan coba lagi.")
        return

    if not db.deduct_balance(user_id, VERIFY_COST):
        await update.message.reply_text("Gagal kurangi token, silakan coba lagi nanti.")
        return

    processing_msg = await update.message.reply_text(
        f"🎖️ Mulai memproses ChatGPT Military verifikasi...\n"
        f"ID Verifikasi: {verification_id}\n"
        f"Email: {email}\n"
        f"Telah dikurangi {VERIFY_COST} token\n\n"
        "Mohon tunggu, ini mungkin memakan waktu 1-2 menit..."
    )

    try:
        verifier = MilitaryVerifier(verification_id)
        result = await asyncio.to_thread(verifier.verify, email=email)

        db.add_verification(
            user_id,
            "chatgpt_military",
            url,
            "success" if result["success"] else "failed",
            str(result),
        )

        if result["success"]:
            result_msg = "✅ Verifikasi military berhasil!\n\n"
            if result.get("pending"):
                result_msg += f"📧 Silakan cek email: {email}\n"
                result_msg += "Klik link verifikasi dari SheerID untuk menyelesaikan verifikasi.\n\n"
                result_msg += result.get("message", "")
            if result.get("redirect_url"):
                result_msg += f"\n\nLink redirect:\n{result['redirect_url']}"
            await processing_msg.edit_text(result_msg)
        else:
            db.add_balance(user_id, VERIFY_COST)
            await processing_msg.edit_text(
                f"❌ Verifikasi gagal: {result.get('message', 'Error tidak diketahui')}\n\n"
                f"Telah dikembalikan {VERIFY_COST} token"
            )
    except Exception as e:
        logger.error("Error saat proses verifikasi military: %s", e)
        db.add_balance(user_id, VERIFY_COST)
        await processing_msg.edit_text(
            f"❌ Terjadi error saat proses: {str(e)}\n\n"
            f"Telah dikembalikan {VERIFY_COST} token"
        )
