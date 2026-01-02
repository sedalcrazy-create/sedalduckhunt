# چالش شکار اردک - DuckHunt Challenge

بازی تک‌نفره شکار اردک برای مسابقه کارکنان اداره کل رفاه و درمان بانک ملی ایران

## لینک‌های مهم

| آیتم | لینک |
|------|------|
| **بازی** | https://duck.darmanjoo.ir |
| **سرور** | 37.152.174.87 |
| **پورت** | 3002 |

---

## قوانین مسابقه

- هر کاربر **3 بار** می‌تواند بازی کند
- مدت هر بازی: **2 دقیقه**
- فقط **بهترین امتیاز** ثبت می‌شود
- ثبت‌نام با **کد استخدامی** الزامی است

---

## امتیازدهی

| اردک | امتیاز |
|------|--------|
| اردک قرمز | 100 |
| اردک سیاه | 150 |
| پاداش دقت | +50 |
| پاداش سرعت | +25 |

---

## نحوه بازی

1. ربات بله را باز کنید
2. روی دکمه "شروع بازی" بزنید
3. اطلاعات خود را وارد کنید (نام، نام خانوادگی، کد استخدامی)
4. با کلیک یا تاچ اردک‌ها را بزنید
5. بعد از 2 دقیقه امتیاز شما ثبت می‌شود

---

## راه‌اندازی محلی

### پیش‌نیازها
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL 15

### نصب
```bash
git clone https://github.com/sedalcrazy-create/sedalduckhunt.git
cd sedalduckhunt
npm install
```

### اجرا با Docker
```bash
docker compose up -d --build
```

### اجرا بدون Docker
```bash
npm start
```

---

## ساختار پروژه

```
duckhunt/
├── app.js                 # سرور اصلی
├── database/
│   ├── db.js              # اتصال PostgreSQL
│   ├── init.sql           # ساختار دیتابیس
│   └── userService.js     # عملیات کاربر
├── public/
│   ├── index.html         # صفحه بازی
│   ├── css/style.css      # استایل
│   └── js/game.js         # لاجیک بازی
├── bot/
│   └── bot.py             # ربات بله
├── dist/
│   └── duckhunt.js        # موتور بازی
├── docs/
│   ├── PRD.md             # سند نیازمندی
│   └── DEPLOYMENT.md      # راهنمای دیپلوی
├── docker-compose.yml
├── Dockerfile
└── CLAUDE.md              # راهنمای توسعه
```

---

## مستندات

- [PRD - سند نیازمندی‌ها](docs/PRD.md)
- [DEPLOYMENT - راهنمای دیپلوی](docs/DEPLOYMENT.md)
- [CLAUDE.md - راهنمای توسعه](CLAUDE.md)

---

## تکنولوژی‌ها

- **Backend:** Node.js + Express + Socket.io
- **Database:** PostgreSQL 15
- **Frontend:** PixiJS + Howler.js + GSAP
- **Bot:** Python + python-bale-bot
- **Deploy:** Docker + Nginx + Let's Encrypt

---

## تیم توسعه

اداره کل رفاه و درمان بانک ملی ایران

---

## لایسنس

MIT License - بازی اصلی DuckHunt-JS توسط Matt Surabian
