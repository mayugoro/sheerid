# Bot Otomatis Verifikasi SheerID - Panduan Deploy

Dokumen ini menjelaskan secara detail cara deploy bot Telegram verifikasi otomatis SheerID.

---

## 📋 Daftar Isi

1. [Persyaratan Lingkungan](#persyaratan-lingkungan)
2. [Deploy Cepat](#deploy-cepat)
3. [Deploy Docker](#deploy-docker)
4. [Deploy Manual](#deploy-manual)
5. [Penjelasan Konfigurasi](#penjelasan-konfigurasi)
6. [Masalah Umum](#masalah-umum)
7. [Pemeliharaan dan Update](#pemeliharaan-dan-update)

---

## 🔧 Persyaratan Lingkungan

### Konfigurasi Minimum

- **Sistem Operasi**: Linux (Ubuntu 20.04+ direkomendasikan) / Windows 10+ / macOS 10.15+
- **Python**: 3.11 atau lebih tinggi
- **MySQL**: 5.7 atau lebih tinggi
- **Memori**: 512MB RAM (direkomendasikan 1GB+)
- **Ruang Disk**: 2GB+
- **Jaringan**: Koneksi internet stabil

### Konfigurasi yang Direkomendasikan

- **Sistem Operasi**: Ubuntu 22.04 LTS
- **Python**: 3.11
- **MySQL**: 8.0
- **Memori**: 2GB+ RAM
- **Ruang Disk**: 5GB+
- **Jaringan**: Bandwidth 10Mbps+

---

## 🚀 Deploy Cepat

### Menggunakan Docker Compose (Paling Mudah)

```bash
# 1. Clone repository
git clone https://github.com/PastKing/tgbot-verify.git
cd tgbot-verify

# 2. Konfigurasi environment variables
cp env.example .env
nano .env  # Isi konfigurasi Anda

# 3. Jalankan service
docker-compose up -d

# 4. Lihat log
docker-compose logs -f

# 5. Hentikan service
docker-compose down
```

Selesai! Bot seharusnya sudah berjalan.

---

## 🐳 Deploy Docker

### Metode 1: Menggunakan Docker Compose (Direkomendasikan)

#### 1. Siapkan file konfigurasi

Buat file `.env`:

```env
# Konfigurasi Telegram Bot
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
CHANNEL_USERNAME=pk_oa
CHANNEL_URL=https://t.me/pk_oa
ADMIN_USER_ID=123456789

# Konfigurasi Database MySQL
MYSQL_HOST=your_mysql_host
MYSQL_PORT=3306
MYSQL_USER=tgbot_user
MYSQL_PASSWORD=your_secure_password
MYSQL_DATABASE=tgbot_verify
```

#### 2. Jalankan service

```bash
docker-compose up -d
```

#### 3. Lihat status

```bash
# Lihat status container
docker-compose ps

# Lihat log real-time
docker-compose logs -f

# Lihat 50 baris log terakhir
docker-compose logs --tail=50
```

#### 4. Restart service

```bash
# Restart semua service
docker-compose restart

# Restart service tunggal
docker-compose restart tgbot
```

#### 5. Update kode

```bash
# Pull kode terbaru
git pull

# Rebuild dan jalankan
docker-compose up -d --build
```

### Metode 2: Deploy Docker Manual

```bash
# 1. Build image
docker build -t tgbot-verify:latest .

# 2. Jalankan container
docker run -d \
  --name tgbot-verify \
  --restart unless-stopped \
  --env-file .env \
  -v $(pwd)/logs:/app/logs \
  tgbot-verify:latest

# 3. Lihat log
docker logs -f tgbot-verify

# 4. Hentikan container
docker stop tgbot-verify

# 5. Hapus container
docker rm tgbot-verify
```

---

## 🔨 Deploy Manual

### Linux / macOS

#### 1. Install dependencies

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y python3.11 python3.11-pip python3.11-venv mysql-server

# macOS (menggunakan Homebrew)
brew install python@3.11 mysql
```

#### 2. Buat virtual environment

```bash
python3.11 -m venv venv
source venv/bin/activate  # Linux/macOS
```

#### 3. Install package Python

```bash
pip install --upgrade pip
pip install -r requirements.txt
playwright install chromium
```

#### 4. Konfigurasi database

```bash
# Login MySQL
mysql -u root -p

# Buat database dan user
CREATE DATABASE tgbot_verify CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'tgbot_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON tgbot_verify.* TO 'tgbot_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

#### 5. Konfigurasi environment variables

```bash
cp env.example .env
nano .env  # Edit konfigurasi
```

#### 6. Jalankan bot

```bash
# Jalankan di foreground (testing)
python bot.py

# Jalankan di background (menggunakan nohup)
nohup python bot.py > bot.log 2>&1 &

# Jalankan di background (menggunakan screen)
screen -S tgbot
python bot.py
# Ctrl+A+D keluar dari screen
# screen -r tgbot untuk koneksi ulang
```

### Windows

#### 1. Install dependencies

- Download dan install [Python 3.11+](https://www.python.org/downloads/)
- Download dan install [MySQL](https://dev.mysql.com/downloads/installer/)

#### 2. Buat virtual environment

```cmd
python -m venv venv
venv\Scripts\activate
```

#### 3. Install package Python

```cmd
pip install --upgrade pip
pip install -r requirements.txt
playwright install chromium
```

#### 4. Konfigurasi database

Gunakan MySQL Workbench atau command line untuk membuat database.

#### 5. Konfigurasi environment variables

Salin `env.example` menjadi `.env` dan edit.

#### 6. Jalankan bot

```cmd
python bot.py
```

---

## ⚙️ Penjelasan Konfigurasi

### Detail Environment Variables

#### Konfigurasi Telegram

```env
# Bot Token (wajib)
# Dapatkan dari @BotFather
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz

# Username channel (opsional)
# Tidak perlu simbol @
CHANNEL_USERNAME=pk_oa

# Link channel (opsional)
CHANNEL_URL=https://t.me/pk_oa

# ID Telegram admin (wajib)
# Bisa didapat melalui @userinfobot
ADMIN_USER_ID=123456789
```

#### Konfigurasi MySQL

```env
# Host database (wajib)
MYSQL_HOST=localhost         # Deploy lokal
# MYSQL_HOST=192.168.1.100  # Database remote
# MYSQL_HOST=mysql          # Docker Compose

# Port database (opsional, default 3306)
MYSQL_PORT=3306

# Username database (wajib)
MYSQL_USER=tgbot_user

# Password database (wajib)
MYSQL_PASSWORD=your_secure_password

# Nama database (wajib)
MYSQL_DATABASE=tgbot_verify
```

### Konfigurasi Sistem Poin

Ubah di `config.py`:

```python
# Konfigurasi poin
VERIFY_COST = 1        # Poin yang digunakan untuk verifikasi
CHECKIN_REWARD = 1     # Reward poin check-in
INVITE_REWARD = 2      # Reward poin undangan
REGISTER_REWARD = 1    # Reward poin registrasi
```

### Kontrol Konkurensi

Sesuaikan di `utils/concurrency.py`:

```python
# Hitung otomatis berdasarkan resource sistem
_base_concurrency = _calculate_max_concurrency()

# Limit konkurensi untuk setiap tipe verifikasi
_verification_semaphores = {
    "gemini_one_pro": Semaphore(_base_concurrency // 5),
    "chatgpt_teacher_k12": Semaphore(_base_concurrency // 5),
    "spotify_student": Semaphore(_base_concurrency // 5),
    "youtube_student": Semaphore(_base_concurrency // 5),
    "bolt_teacher": Semaphore(_base_concurrency // 5),
}
```

---

## 🔍 Masalah Umum

### 1. Bot Token tidak valid

**Masalah**: `telegram.error.InvalidToken: The token was rejected by the server.`

**Solusi**:
- Periksa apakah `BOT_TOKEN` di file `.env` benar
- Pastikan tidak ada spasi atau tanda kutip ekstra
- Dapatkan Token baru dari @BotFather

### 2. Koneksi database gagal

**Masalah**: `pymysql.err.OperationalError: (2003, "Can't connect to MySQL server")`

**Solusi**:
- Periksa apakah service MySQL berjalan: `systemctl status mysql`
- Periksa apakah konfigurasi database benar
- Periksa pengaturan firewall
- Konfirmasi permission user database

### 3. Instalasi browser Playwright gagal

**Masalah**: `playwright._impl._api_types.Error: Executable doesn't exist`

**Solusi**:
```bash
playwright install chromium
# Atau install semua dependencies
playwright install-deps chromium
```

### 4. Port sudah digunakan

**Masalah**: Docker container tidak bisa start, konflik port

**Solusi**:
```bash
# Lihat penggunaan port
netstat -tlnp | grep :3306
# Ubah port mapping di docker-compose.yml
```

### 5. Memori tidak cukup

**Masalah**: Server crash karena memori tidak cukup

**Solusi**:
- Tambah memori server
- Kurangi jumlah konkurensi
- Aktifkan swap space:
```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### 6. File log terlalu besar

**Masalah**: File log menghabiskan banyak ruang disk

**Solusi**:
- Docker otomatis membatasi ukuran log (lihat `docker-compose.yml`)
- Bersihkan manual: `truncate -s 0 logs/*.log`
- Atur log rotation

---

## 🔄 Pemeliharaan dan Update

### Lihat log

```bash
# Docker Compose
docker-compose logs -f --tail=100

# Deploy manual
tail -f bot.log
tail -f logs/bot.log
```

### Backup database

```bash
# Backup lengkap
mysqldump -u tgbot_user -p tgbot_verify > backup_$(date +%Y%m%d).sql

# Backup data saja
mysqldump -u tgbot_user -p --no-create-info tgbot_verify > data_backup.sql

# Restore backup
mysql -u tgbot_user -p tgbot_verify < backup.sql
```

### Update kode

```bash
# Pull kode terbaru
git pull origin main

# Deploy Docker
docker-compose down
docker-compose up -d --build

# Deploy manual
source venv/bin/activate
pip install -r requirements.txt
python bot.py
```

### Monitor status running

#### Menggunakan systemd (Direkomendasikan untuk Linux)

Buat file service `/etc/systemd/system/tgbot-verify.service`:

```ini
[Unit]
Description=SheerID Telegram Verification Bot
After=network.target mysql.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/path/to/tgbot-verify
ExecStart=/path/to/tgbot-verify/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Jalankan service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable tgbot-verify
sudo systemctl start tgbot-verify
sudo systemctl status tgbot-verify
```

#### Menggunakan supervisor

Install supervisor:

```bash
sudo apt install supervisor
```

Buat file konfigurasi `/etc/supervisor/conf.d/tgbot-verify.conf`:

```ini
[program:tgbot-verify]
directory=/path/to/tgbot-verify
command=/path/to/tgbot-verify/venv/bin/python bot.py
autostart=true
autorestart=true
stderr_logfile=/var/log/tgbot-verify.err.log
stdout_logfile=/var/log/tgbot-verify.out.log
user=ubuntu
```

Jalankan:

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start tgbot-verify
```

---

## 🔒 Rekomendasi Keamanan

1. **Gunakan password kuat**
   - Rotasi Bot Token secara berkala
   - Password database minimal 16 karakter
   - Jangan gunakan password default

2. **Batasi akses database**
   ```sql
   # Hanya izinkan koneksi lokal
   CREATE USER 'tgbot_user'@'localhost' IDENTIFIED BY 'password';
   
   # Izinkan IP spesifik
   CREATE USER 'tgbot_user'@'192.168.1.100' IDENTIFIED BY 'password';
   ```

3. **Konfigurasi firewall**
   ```bash
   # Buka hanya port yang diperlukan
   sudo ufw allow 22/tcp      # SSH
   sudo ufw enable
   ```

4. **Update berkala**
   ```bash
   sudo apt update && sudo apt upgrade
   pip install --upgrade -r requirements.txt
   ```

5. **Strategi backup**
   - Backup database otomatis setiap hari
   - Simpan minimal 7 hari backup
   - Test proses restore secara berkala

---

## 📞 Dukungan Teknis

- 📺 Channel Telegram: https://t.me/pk_oa
- 🐛 Laporan masalah: [GitHub Issues](https://github.com/PastKing/tgbot-verify/issues)

---

<p align="center">
  <strong>Semoga deploy berjalan lancar!</strong>
</p>
