# PRD - DuckHunt Challenge
## سند نیازمندی‌های محصول

---

## 1. خلاصه پروژه

| آیتم | توضیح |
|------|-------|
| **نام پروژه** | چالش شکار اردک (DuckHunt Challenge) |
| **نوع** | بازی تک‌نفره مسابقه‌ای |
| **پلتفرم** | مینی‌اپ پیام‌رسان بله |
| **مخاطب** | کارکنان اداره کل رفاه و درمان بانک ملی |
| **دامین** | https://duck.darmanjoo.ir |
| **پورت سرور** | 3002 |

---

## 2. هدف پروژه

ایجاد یک مسابقه آنلاین شکار اردک برای کارکنان با:
- ثبت‌نام با کد استخدامی
- بازی محدود (3 بار)
- زمان محدود (2 دقیقه)
- لیدربورد و رتبه‌بندی
- اعلام برندگان

---

## 3. ویژگی‌های کلیدی

### 3.1 سیستم احراز هویت
- ورود از طریق مینی‌اپ بله
- دریافت اطلاعات کاربر از Bale SDK
- ثبت‌نام با نام، نام‌خانوادگی، کد استخدامی
- ذخیره در دیتابیس PostgreSQL

### 3.2 مکانیک بازی
- بازی کلاسیک DuckHunt
- شلیک با کلیک/تاچ
- اردک‌ها با سرعت‌های مختلف
- سیستم امتیازدهی بر اساس دقت و سرعت
- مراحل (Waves) متعدد

### 3.3 قوانین مسابقه
- هر کاربر: حداکثر **3 بازی**
- مدت هر بازی: **2 دقیقه**
- امتیاز نهایی: **بهترین امتیاز** ثبت می‌شود
- رتبه‌بندی: بر اساس بالاترین امتیاز

### 3.4 سیستم امتیازدهی
| آیتم | امتیاز |
|------|--------|
| اردک قرمز | 100 امتیاز |
| اردک سیاه | 150 امتیاز |
| پاداش دقت بالا | +50 امتیاز |
| پاداش سرعت | +25 امتیاز |

### 3.5 لیدربورد
- نمایش 10 نفر برتر
- نمایش نام، کد استخدامی، امتیاز
- آپدیت Real-time
- ارسال خودکار به کانال هر 30 دقیقه

---

## 4. فنی

### 4.1 Backend
- **Runtime:** Node.js 18
- **Framework:** Express.js
- **Real-time:** Socket.io
- **Database:** PostgreSQL 15

### 4.2 Frontend
- **Engine:** PixiJS (WebGL)
- **Audio:** Howler.js
- **Animation:** GSAP/TweenJS

### 4.3 Bot
- **Language:** Python 3.11
- **Framework:** python-bale-bot

### 4.4 Deployment
- **Container:** Docker
- **Orchestration:** Docker Compose
- **Proxy:** Nginx
- **SSL:** Let's Encrypt

---

## 5. API Endpoints

| Method | Path | توضیح |
|--------|------|-------|
| GET | `/health` | Health Check |
| GET | `/api/user/:baleUserId` | بررسی کاربر |
| POST | `/api/register` | ثبت‌نام |
| GET | `/api/leaderboard/top/:limit` | لیدربورد |
| GET | `/api/user/:baleUserId/stats` | آمار کاربر |

---

## 6. Socket Events

### ورودی
| Event | Data | توضیح |
|-------|------|-------|
| `join game` | `{baleUserId}` | ورود |
| `register user` | `{...userData}` | ثبت‌نام |
| `save-score` | `{score, ducks, ...}` | ذخیره امتیاز |
| `request leaderboard` | - | درخواست رتبه‌بندی |

### خروجی
| Event | Data | توضیح |
|-------|------|-------|
| `game-limit-reached` | `{message}` | اتمام بازی‌ها |

---

## 7. دیتابیس

### جدول users
```sql
- id, bale_user_id, phone_number
- first_name, last_name, employee_code
- created_at, updated_at
```

### جدول leaderboard
```sql
- id, user_id, score
- ducks_shot, accuracy, game_duration
- level_reached, game_date
```

### ویو high_scores
```sql
- بهترین امتیاز هر کاربر
- برای نمایش لیدربورد
```

---

## 8. زمان‌بندی

| فاز | وضعیت |
|-----|--------|
| طراحی و توسعه | ⏳ |
| تست | ⏳ |
| دیپلوی | ⏳ |
| مسابقه | ⏳ |
| اعلام نتایج | ⏳ |

---

## 9. ریسک‌ها

| ریسک | راه‌حل |
|------|--------|
| بار زیاد سرور | Docker Compose + کلاستر |
| تقلب | Server-side validation |
| قطع اینترنت | ذخیره محلی + Retry |

---

## 10. معیارهای موفقیت

- حداقل 100 کاربر فعال
- میانگین 2 بازی در هر کاربر
- کمتر از 5% خطای سرور
- رضایت کاربران > 80%
