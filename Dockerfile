# Gunakan image resmi Python 3.11
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies sistem (diperlukan Playwright)
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libwayland-client0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    build-essential gcc pkg-config libcairo2-dev libpango1.0-dev libgdk-pixbuf-2.0-dev libffi-dev python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Salin file dependencies
COPY requirements.txt .

# Install dependencies Python (tanpa cache)
RUN pip install --no-cache-dir -r requirements.txt

# Install browser Playwright
RUN playwright install chromium

# Salin file project (.dockerignore akan otomatis exclude cache)
COPY . .

# Bersihkan semua cache Python (pastikan menggunakan kode terbaru)
RUN find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
RUN find . -type f -name "*.pyc" -delete 2>/dev/null || true

# Set Python agar tidak generate bytecode (hindari masalah cache)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Konfigurasi MySQL (diteruskan melalui docker-compose.yml atau command line)
# Jangan hardcode di sini, gunakan environment variables

# Health check (periksa proses bot)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD pgrep -f "python.*bot.py" || exit 1

# Jalankan bot
CMD ["python", "-u", "bot.py"]
