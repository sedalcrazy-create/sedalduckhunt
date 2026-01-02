# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Project Overview

**DuckHunt Challenge** - A single-player shooting game for competition, integrated with Bale messenger mini-app platform.

**Target Users:** Employees of Welfare and Treatment Department
**Platform:** Bale Mini App (HTML5 + WebSocket)
**Domain:** https://duck.darmanjoo.ir

## Technology Stack

### Backend
- **Runtime:** Node.js 18+
- **Framework:** Express.js
- **Real-time:** Socket.io
- **Database:** PostgreSQL 15
- **Deployment:** Docker + Docker Compose

### Frontend
- **Game Engine:** PixiJS (WebGL)
- **Audio:** Howler.js
- **Animation:** GSAP/TweenJS
- **Integration:** Bale Mini App SDK

### Bot
- **Language:** Python 3.11
- **Framework:** python-bale-bot

## Common Commands

### Development
```bash
npm install
npm start
npm run build
```

### Docker
```bash
docker compose up -d --build
docker compose logs -f app
docker compose down
```

### Database
```bash
docker exec -it duckhunt_db psql -U duckhunt_user -d duckhunt
SELECT * FROM high_scores ORDER BY high_score DESC LIMIT 10;
```

## Architecture

### Game Flow
1. User opens mini-app from Bale
2. Check if user is registered
3. If new, show registration form
4. If registered, show game rules
5. Start game (2 minutes)
6. Save score on game end
7. Show leaderboard

### Key Files
- `app.js` - Main server
- `database/userService.js` - User/score operations
- `public/index.html` - Game UI
- `dist/duckhunt.js` - Game engine (from original DuckHunt-JS)
- `bot/bot.py` - Bale bot

### API Endpoints
- `GET /health` - Health check
- `GET /api/user/:baleUserId` - Get user
- `POST /api/register` - Register user
- `GET /api/leaderboard/top/:limit` - Top players

### Socket Events
- `join game` - Check registration
- `register user` - Register new user
- `save-score` - Save game score
- `request leaderboard` - Get top 10

## Configuration

Environment variables (`.env`):
- `PORT` - Server port (3002)
- `POSTGRES_*` - Database connection
- `GAME_DURATION` - Game time in seconds (120)
- `MAX_GAMES_PER_USER` - Game limit per user (3)
- `GAME_URL` - https://duck.darmanjoo.ir

## Deployment

Server: 37.152.174.87
Path: /opt/duckhunt

```bash
ssh root@37.152.174.87
cd /opt/duckhunt
git pull && docker compose up -d --build
```

## Code Style

- ES6 classes
- 'use strict' in Node.js files
- Semicolons required
- 4-space indentation
- RTL for Persian UI
