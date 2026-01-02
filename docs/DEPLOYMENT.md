# راهنمای دیپلوی DuckHunt Challenge

## اطلاعات سرور

| آیتم | مقدار |
|------|-------|
| **IP سرور** | 37.152.174.87 |
| **یوزر** | root |
| **دامین** | duck.darmanjoo.ir |
| **پورت** | 3002 |
| **مسیر پروژه** | /opt/duckhunt |

---

## دستورات اتصال

### اتصال SSH
```bash
ssh root@37.152.174.87
```

### انتقال فایل (SCP)
```bash
# آپلود فایل
scp local_file.txt root@37.152.174.87:/opt/duckhunt/

# آپلود پوشه
scp -r public/ root@37.152.174.87:/opt/duckhunt/

# دانلود فایل
scp root@37.152.174.87:/opt/duckhunt/file.txt ./
```

---

## نصب و راه‌اندازی

### 1. کلون پروژه روی سرور
```bash
ssh root@37.152.174.87
cd /opt
git clone https://github.com/sedalcrazy-create/sedalduckhunt.git duckhunt
cd duckhunt
```

### 2. ایجاد فایل .env
```bash
cp .env.example .env
nano .env
```

محتوای .env:
```env
PORT=3002
NODE_ENV=production
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=duckhunt
POSTGRES_USER=duckhunt_user
POSTGRES_PASSWORD=DuckHunt2025!
GAME_DURATION=120
MAX_GAMES_PER_USER=3
GAME_URL=https://duck.darmanjoo.ir
```

### 3. راه‌اندازی Docker
```bash
cd /opt/duckhunt
docker compose up -d --build
```

### 4. بررسی وضعیت
```bash
docker compose ps
docker compose logs -f app
```

---

## تنظیمات Nginx

### ایجاد فایل تنظیمات
```bash
nano /etc/nginx/sites-available/duck.darmanjoo.ir
```

محتوا:
```nginx
server {
    listen 80;
    server_name duck.darmanjoo.ir;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name duck.darmanjoo.ir;

    ssl_certificate /etc/letsencrypt/live/duck.darmanjoo.ir/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/duck.darmanjoo.ir/privkey.pem;

    location / {
        proxy_pass http://localhost:3002;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_cache_bypass $http_upgrade;
    }

    location /socket.io/ {
        proxy_pass http://localhost:3002;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

### فعال‌سازی
```bash
ln -s /etc/nginx/sites-available/duck.darmanjoo.ir /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx
```

### دریافت SSL
```bash
certbot --nginx -d duck.darmanjoo.ir
```

---

## دستورات مدیریت Docker

### مشاهده وضعیت
```bash
docker compose ps
```

### مشاهده لاگ‌ها
```bash
# همه سرویس‌ها
docker compose logs -f

# فقط app
docker compose logs -f app

# فقط دیتابیس
docker compose logs -f postgres
```

### ری‌استارت
```bash
# همه سرویس‌ها
docker compose restart

# فقط app
docker compose restart app
```

### توقف
```bash
docker compose down
```

### شروع مجدد
```bash
docker compose up -d
```

### بازسازی
```bash
docker compose up -d --build
```

---

## دستورات دیتابیس

### اتصال به PostgreSQL
```bash
docker exec -it duckhunt_db psql -U duckhunt_user -d duckhunt
```

### کوئری‌های مفید
```sql
-- تعداد کاربران
SELECT COUNT(*) FROM users;

-- برترین بازیکنان
SELECT * FROM high_scores ORDER BY high_score DESC LIMIT 10;

-- تعداد بازی‌ها
SELECT COUNT(*) FROM leaderboard;

-- آمار کامل
SELECT
    u.first_name, u.last_name, u.employee_code,
    COUNT(l.id) as games,
    MAX(l.score) as best_score
FROM users u
LEFT JOIN leaderboard l ON u.id = l.user_id
GROUP BY u.id;

-- خروج
\q
```

### بکاپ دیتابیس
```bash
docker exec duckhunt_db pg_dump -U duckhunt_user duckhunt > backup_$(date +%Y%m%d).sql
```

### بازگردانی بکاپ
```bash
docker exec -i duckhunt_db psql -U duckhunt_user duckhunt < backup.sql
```

---

## Health Check

### بررسی سلامت سرویس
```bash
curl http://localhost:3002/health
```

### بررسی از خارج
```bash
curl https://duck.darmanjoo.ir/health
```

---

## عیب‌یابی

### مشکل 1: سرویس بالا نمی‌آید
```bash
docker compose logs app
docker compose down
docker compose up -d --build
```

### مشکل 2: خطای دیتابیس
```bash
docker compose logs postgres
docker compose restart postgres
```

### مشکل 3: خطای 502 Nginx
```bash
# بررسی اینکه app در حال اجراست
docker compose ps
curl http://localhost:3002/health

# ری‌استارت
docker compose restart app
systemctl reload nginx
```

### مشکل 4: SSL
```bash
certbot certificates
certbot renew
```

---

## مانیتورینگ

### مصرف منابع
```bash
docker stats
```

### فضای دیسک
```bash
df -h
```

### حافظه
```bash
free -h
```

### پردازنده
```bash
top
```

---

## به‌روزرسانی

### دریافت آخرین تغییرات
```bash
cd /opt/duckhunt
git pull origin master
docker compose up -d --build
```

### آپلود دستی فایل‌ها
```bash
# از کامپیوتر لوکال
scp -r public/ root@37.152.174.87:/opt/duckhunt/
ssh root@37.152.174.87 "cd /opt/duckhunt && docker compose up -d --build"
```

---

## پروژه‌های دیگر روی سرور

| پروژه | پورت | مسیر |
|-------|------|------|
| Snake (مار) | 3001 | /opt/yalda-snake |
| DuckHunt | 3002 | /opt/duckhunt |
| Medical Commission | - | /opt/medical-commission |
