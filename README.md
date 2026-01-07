# Bot Telegram Verifikasi Otomatis SheerID

![Stars](https://img.shields.io/github/stars/PastKing/tgbot-verify?style=social)
![Forks](https://img.shields.io/github/forks/PastKing/tgbot-verify?style=social)
![Issues](https://img.shields.io/github/issues/PastKing/tgbot-verify)
![License](https://img.shields.io/github/license/PastKing/tgbot-verify)

> 🤖 Bot Telegram yang otomatis menyelesaikan verifikasi mahasiswa/guru SheerID
> 
> Berdasarkan peningkatan kode versi lama dari GGBond [@auto_sheerid_bot](https://t.me/auto_sheerid_bot)

---

## 📋 Pengantar Proyek

Ini adalah bot Telegram berbasis Python yang dapat menyelesaikan verifikasi identitas mahasiswa/guru SheerID di berbagai platform secara otomatis. Bot ini secara otomatis menghasilkan informasi identitas, membuat dokumen verifikasi, dan mengirimkannya ke platform SheerID, sehingga sangat menyederhanakan proses verifikasi.

> **⚠️ Pemberitahuan Penting**:
> 
> - Layanan seperti **Gemini One Pro**, **ChatGPT Teacher K12**, **Spotify Student**, **YouTube Premium Student** memerlukan pembaruan `programId` dan data verifikasi lainnya di file konfigurasi setiap modul sebelum digunakan. Silakan lihat bagian "Wajib Dibaca Sebelum Digunakan" di bawah untuk detailnya.
> - Proyek ini juga menyediakan dokumentasi pemikiran implementasi dan antarmuka untuk **Verifikasi Militer ChatGPT**. Untuk detail lengkap, silakan lihat [`military/README.md`](military/README.md). Pengguna dapat mengintegrasikannya sendiri berdasarkan dokumentasi.

### 🎯 Layanan Verifikasi yang Didukung

| Perintah | Layanan | Tipe | Status | Keterangan |
|------|------|------|------|------|
| `/verify` | Gemini One Pro | Verifikasi Guru | ✅ Lengkap | Diskon pendidikan Google AI Studio |
| `/verify2` | ChatGPT Teacher K12 | Verifikasi Guru | ✅ Lengkap | Diskon pendidikan OpenAI ChatGPT |
| `/verify3` | Spotify Student | Verifikasi Mahasiswa | ✅ Lengkap | Diskon langganan mahasiswa Spotify |
| `/verify4` | Bolt.new Teacher | Verifikasi Guru | ✅ Lengkap | Diskon pendidikan Bolt.new (otomatis dapat code) |
| `/verify5` | YouTube Premium Student | Verifikasi Mahasiswa | ⚠️ Setengah Jadi | Diskon mahasiswa YouTube Premium (lihat penjelasan di bawah) |

> **⚠️ Penjelasan Khusus Verifikasi YouTube**:
> 
> Fungsi verifikasi YouTube saat ini dalam status setengah jadi. Silakan baca dokumen [`youtube/HELP.MD`](youtube/HELP.MD) dengan seksama sebelum digunakan.
> 
> **Perbedaan Utama**:
> - Format link asli YouTube berbeda dengan layanan lainnya
> - Perlu ekstrak `programId` dan `verificationId` secara manual dari log jaringan browser
> - Kemudian susun secara manual ke format link SheerID standar
> 
> **Langkah Penggunaan**:
> 1. Kunjungi halaman verifikasi mahasiswa YouTube Premium
> 2. Buka developer tools browser (F12) → Tab Network (Jaringan)
> 3. Mulai proses verifikasi, cari `https://services.sheerid.com/rest/v2/verification/`
> 4. Dapatkan `programId` dari request payload, dapatkan `verificationId` dari response
> 5. Susun link secara manual: `https://services.sheerid.com/verify/{programId}/?verificationId={verificationId}`
> 6. Gunakan perintah `/verify5` untuk submit link tersebut

> **💡 Pemikiran Verifikasi Militer ChatGPT**:
> 
> Proyek ini menyediakan dokumentasi pemikiran implementasi dan antarmuka untuk verifikasi SheerID militer ChatGPT. Alur verifikasi militer berbeda dengan verifikasi mahasiswa/guru biasa. Perlu menjalankan antarmuka `collectMilitaryStatus` terlebih dahulu untuk mengatur status militer, kemudian baru submit formulir informasi pribadi. Untuk pemikiran implementasi detail dan penjelasan antarmuka, silakan lihat dokumentasi [`military/README.md`](military/README.md). Pengguna dapat mengintegrasikannya sendiri ke dalam bot berdasarkan dokumentasi tersebut.

### ✨ Fitur Inti

- 🚀 **Proses Otomatis**: Selesaikan pembuatan informasi, pembuatan dokumen, dan pengiriman verifikasi dengan satu klik
- 🎨 **Generasi Cerdas**: Otomatis menghasilkan gambar PNG kartu mahasiswa/guru
- 💰 **Sistem Poin**: Berbagai cara untuk mendapatkan poin seperti check-in, undangan, tukar kode voucher, dll
- 🔐 **Aman dan Andal**: Menggunakan database MySQL, mendukung konfigurasi environment variable
- ⚡ **Kontrol Konkurensi**: Mengelola permintaan konkuren secara cerdas, memastikan stabilitas
- 👥 **Fungsi Manajemen**: Sistem manajemen pengguna dan poin yang lengkap

---

## 🛠️ Stack Teknologi

- **Bahasa**: Python 3.11+
- **Framework Bot**: python-telegram-bot 20.0+
- **Database**: MySQL 5.7+
- **Otomasi Browser**: Playwright
- **HTTP Client**: httpx
- **Pemrosesan Gambar**: Pillow, reportlab, xhtml2pdf
- **Manajemen Environment**: python-dotenv

---

## 🚀 Mulai Cepat

### 1. Clone proyek

```bash
git clone https://github.com/PastKing/tgbot-verify.git
cd tgbot-verify
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

### 3. Konfigurasi environment variables

Salin `env.example` menjadi `.env` dan isi konfigurasi:

```env
# Konfigurasi Telegram Bot
BOT_TOKEN=your_bot_token_here
CHANNEL_USERNAME=your_channel
CHANNEL_URL=https://t.me/your_channel
ADMIN_USER_ID=your_admin_id

# Konfigurasi Database MySQL
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=tgbot_verify
```

### 4. 启动机器人

```bash
python bot.py
```

---

## 🐳 Docker 部署

### 使用 Docker Compose（推荐）

```bash
# 1. 修改 .env 文件配置
cp env.example .env
nano .env

# 2. 启动服务
docker-compose up -d

# 3. 查看日志
docker-compose logs -f
```

### 手动 Docker 部署

```bash
# 构建镜像
docker build -t tgbot-verify .

# 运行容器
docker run -d \
  --name tgbot-verify \
  --env-file .env \
  -v $(pwd)/logs:/app/logs \
  tgbot-verify
```

---

## 📖 使用说明

### 用户命令

```bash
/start              # 开始使用（注册）
/about              # 了解机器人功能
/balance            # 查看积分余额
/qd                 # 每日签到（+1积分）
/invite             # 生成邀请链接（+2积分/人）
/use <卡密>         # 使用卡密兑换积分
/verify <链接>      # Gemini One Pro 认证
/verify2 <链接>     # ChatGPT Teacher K12 认证
/verify3 <链接>     # Spotify Student 认证
/verify4 <链接>     # Bolt.new Teacher 认证
/verify5 <链接>     # YouTube Premium Student 认证
/getV4Code <id>     # 获取 Bolt.new 认证码
/help               # 查看帮助信息
```

### 管理员命令

```bash
/addbalance <用户ID> <积分>     # 增加用户积分
/block <用户ID>                 # 拉黑用户
/white <用户ID>                 # 取消拉黑
/blacklist                      # 查看黑名单
/genkey <卡密> <积分> [次数] [天数]  # 生成卡密
/listkeys                       # 查看卡密列表
/broadcast <文本>               # 群发通知
```

### 使用流程

1. **获取认证链接**
   - 访问对应服务的认证页面
   - 开始认证流程
   - 复制浏览器地址栏中的完整 URL（包含 `verificationId`）

2. **提交认证请求**
   ```
   /verify3 https://services.sheerid.com/verify/xxx/?verificationId=yyy
   ```

3. **等待处理**
   - 机器人自动生成身份信息
   - 创建学生证/教师证图片
   - 提交到 SheerID 平台

4. **获取结果**
   - 审核通常在几分钟内完成
   - 成功后会返回跳转链接

---

## 📁 项目结构

```
tgbot-verify/
├── bot.py                  # 机器人主程序
├── config.py               # 全局配置
├── database_mysql.py       # MySQL 数据库管理
├── .env                    # 环境变量配置（需自行创建）
├── env.example             # 环境变量模板
├── requirements.txt        # Python 依赖
├── Dockerfile              # Docker 镜像构建
├── docker-compose.yml      # Docker Compose 配置
├── handlers/               # 命令处理器
│   ├── user_commands.py    # 用户命令
│   ├── admin_commands.py   # 管理员命令
│   └── verify_commands.py  # 认证命令
├── one/                    # Gemini One Pro 认证模块
├── k12/                    # ChatGPT K12 认证模块
├── spotify/                # Spotify Student 认证模块
├── youtube/                # YouTube Premium 认证模块
├── Boltnew/                # Bolt.new 认证模块
├── military/               # ChatGPT 军人认证思路文档
└── utils/                  # 工具函数
    ├── messages.py         # 消息模板
    ├── concurrency.py      # 并发控制
    └── checks.py           # 权限检查
```

---

## ⚙️ 配置说明

### 环境变量

| 变量名 | 必填 | 说明 | 默认值 |
|--------|------|------|--------|
| `BOT_TOKEN` | ✅ | Telegram Bot Token | - |
| `CHANNEL_USERNAME` | ❌ | 频道用户名 | pk_oa |
| `CHANNEL_URL` | ❌ | 频道链接 | https://t.me/pk_oa |
| `ADMIN_USER_ID` | ✅ | 管理员 Telegram ID | - |
| `MYSQL_HOST` | ✅ | MySQL 主机地址 | localhost |
| `MYSQL_PORT` | ❌ | MySQL 端口 | 3306 |
| `MYSQL_USER` | ✅ | MySQL 用户名 | - |
| `MYSQL_PASSWORD` | ✅ | MySQL 密码 | - |
| `MYSQL_DATABASE` | ✅ | 数据库名称 | tgbot_verify |

### 积分配置

在 `config.py` 中可以自定义积分规则：

```python
VERIFY_COST = 1        # 验证消耗的积分
CHECKIN_REWARD = 1     # 签到奖励积分
INVITE_REWARD = 2      # 邀请奖励积分
REGISTER_REWARD = 1    # 注册奖励积分
```

---

## ⚠️ 重要说明

### 🔴 使用前必读

**在使用机器人之前，请务必检查并更新各模块的验证配置！**

由于 SheerID 平台的 `programId` 可能会定期更新，以下服务在使用前**必须**更新配置文件中的验证资料：

- `one/config.py` - **Gemini One Pro** 认证（需更新 `PROGRAM_ID`）
- `k12/config.py` - **ChatGPT Teacher K12** 认证（需更新 `PROGRAM_ID`）
- `spotify/config.py` - **Spotify Student** 认证（需更新 `PROGRAM_ID`）
- `youtube/config.py` - **YouTube Premium Student** 认证（需更新 `PROGRAM_ID`）
- `Boltnew/config.py` - Bolt.new Teacher 认证（建议检查 `PROGRAM_ID`）

**如何获取最新的 programId**：
1. 访问对应服务的认证页面
2. 打开浏览器开发者工具（F12）→ 网络（Network）标签
3. 开始认证流程
4. 查找 `https://services.sheerid.com/rest/v2/verification/` 请求
5. 从 URL 或请求载荷中提取 `programId`
6. 更新对应模块的 `config.py` 文件

> **提示**：如果认证一直失败，很可能是 `programId` 已过期，请按上述步骤更新。

---

## 🔗 相关链接

- 📺 **Telegram 频道**：https://t.me/pk_oa
- 🐛 **问题反馈**：[GitHub Issues](https://github.com/PastKing/tgbot-verify/issues)
- 📖 **部署文档**：[DEPLOY.md](DEPLOY.md)

---

## 🤝 二次开发

欢迎进行二次开发！但请遵守以下规则：

1. **保留原作者信息**
   - 在代码和文档中保留原仓库地址
   - 注明基于本项目进行的二次开发

2. **开源协议**
   - 本项目采用 MIT 开源协议
   - 二次开发的项目也必须开源

3. **商业使用**
   - 个人使用免费
   - 商业使用请自行优化并承担责任
   - 不提供任何技术支持和担保

---

## 📜 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

```
MIT License

Copyright (c) 2025 PastKing

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 🙏 致谢

- 感谢 [@auto_sheerid_bot](https://t.me/auto_sheerid_bot) GGBond 提供的旧版代码基础
- 感谢所有为本项目做出贡献的开发者
- 感谢 SheerID 平台提供的认证服务

---

## 📊 项目统计

[![Star History Chart](https://api.star-history.com/svg?repos=PastKing/tgbot-verify&type=Date)](https://star-history.com/#PastKing/tgbot-verify&Date)

---

## 📝 更新日志

### v2.0.0 (2025-01-12)

- ✨ 新增 Spotify Student 和 YouTube Premium Student 认证（YouTube 为半成品，需参考 youtube/HELP.MD 使用）
- 🚀 优化并发控制和性能
- 📝 完善文档和部署指南
- 🐛 修复已知 BUG

### v1.0.0

- 🎉 初始版本发布
- ✅ 支持 Gemini、ChatGPT、Bolt.new 认证

---

<p align="center">
  <strong>⭐ 如果这个项目对你有帮助，请给个 Star 支持一下！</strong>
</p>

<p align="center">
  Made with ❤️ by <a href="https://github.com/PastKing">PastKing</a>
</p>
