"""Template Pesan"""
from config import VERIFY_COST, HELP_NOTION_URL


def get_welcome_message(full_name: str, invited_by: bool = False) -> str:
    """Mendapatkan pesan selamat datang"""
    msg = (
        f"🎉 Selamat datang, {full_name}!\n"
        "Bot ini dapat melakukan verifikasi SheerID secara otomatis.\n"
    )
    msg += (
        "\nPanduan Cepat:\n"
        "/about - Tentang fungsi bot\n"
        "/balance - Cek saldo token\n"
        "/help - Lihat daftar command lengkap\n"
    )
    return msg


def get_about_message() -> str:
    """Mendapatkan pesan tentang bot"""
    return (
        "🤖 Bot Verifikasi Otomatis SheerID\n"
        "\n"
        "PastKing (Developer utama)\n"
        "@Mayugoro (merubah susunan sistem ke sqlite3 dan sistem inti lainnya)\n"
        "\n"
        "Fitur:\n"
        "- Otomatis menyelesaikan verifikasi pelajar/guru SheerID\n"
        "- Mendukung verifikasi Gemini One Pro, ChatGPT Teacher K12, Spotify Student, YouTube Student, Bolt.new Teacher\n"
        "\n"
        "Cara Penggunaan:\n"
        "1. Mulai verifikasi di website dan copy link verifikasi lengkap\n"
        "2. Kirim /verify, /verify2, /verify3, /verify4 atau /verify5 dengan link tersebut\n"
        "3. Tunggu proses dan lihat hasilnya\n"
        "4. Untuk Bolt.new, kode verifikasi otomatis didapatkan. Jika perlu query manual gunakan /getV4Code <verification_id>\n"
        "\n"
        "Untuk command lengkap kirim /help"
    )


def get_help_message(is_admin: bool = False) -> str:
    """Mendapatkan pesan bantuan"""
    msg = (
        "📖 Bot Verifikasi Otomatis SheerID - Bantuan\n"
        "\n"
        "Command User:\n"
        "/start - Mulai menggunakan (registrasi)\n"
        "/about - Tentang fungsi bot\n"
        "/balance - Cek saldo token\n"
        f"/verify <link> - Verifikasi Gemini One Pro (-{VERIFY_COST} token)\n"
        f"/verify2 <link> - Verifikasi ChatGPT Teacher K12 (-{VERIFY_COST} token)\n"
        f"/verify3 <link> - Verifikasi Spotify Student (-{VERIFY_COST} token)\n"
        f"/verify4 <link> - Verifikasi Bolt.new Teacher (-{VERIFY_COST} token)\n"
        f"/verify5 <link> - Verifikasi YouTube Student Premium (-{VERIFY_COST} token)\n"
        "/getV4Code <verification_id> - Dapatkan kode verifikasi Bolt.new\n"
        "/help - Lihat info bantuan ini\n"
        f"Jika verifikasi gagal lihat: {HELP_NOTION_URL}\n"
    )

    if is_admin:
        msg += (
            "\nCommand Admin:\n"
            "/adduser <User ID> [username] [nama] - Tambah user baru\n"
            "/addbalance <User ID> <jumlah> - Tambah token user\n"
            "/ban <User ID> - Ban user\n"
            "/unban <User ID> - Unban user\n"
            "/blacklist - Lihat daftar blacklist\n"
            "/broadcast <teks> - Broadcast pesan ke semua user\n"
        )

    return msg


def get_insufficient_balance_message(current_balance: int) -> str:
    """Mendapatkan pesan token tidak cukup"""
    return (
        f"Token tidak cukup! Perlu {VERIFY_COST} token, saat ini {current_balance:,} token.\n\n"
        "Hubungi admin untuk mendapat lebih banyak token."
    )


def get_verify_usage_message(command: str, service_name: str) -> str:
    """Mendapatkan panduan penggunaan command verifikasi"""
    return (
        f"Cara penggunaan: {command} <Link SheerID>\n\n"
        "Contoh:\n"
        f"{command} https://services.sheerid.com/verify/xxx/?verificationId=xxx\n\n"
        "Cara mendapat link verifikasi:\n"
        f"1. Kunjungi halaman verifikasi {service_name}\n"
        "2. Mulai proses verifikasi\n"
        "3. Copy URL lengkap dari address bar browser\n"
        f"4. Submit menggunakan command {command}"
    )
