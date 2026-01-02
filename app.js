'use strict';

require('dotenv').config();

const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const path = require('path');
const userService = require('./database/userService');

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
    cors: {
        origin: "*",
        methods: ["GET", "POST"]
    }
});

const PORT = process.env.PORT || 3002;
const GAME_DURATION = parseInt(process.env.GAME_DURATION) || 120;
const MAX_GAMES_PER_USER = parseInt(process.env.MAX_GAMES_PER_USER) || 3;

// Middleware
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));
app.use('/dist', express.static(path.join(__dirname, 'dist')));

// No-cache headers for game assets
app.use((req, res, next) => {
    res.set('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate');
    res.set('Pragma', 'no-cache');
    res.set('Expires', '0');
    next();
});

// Health check
app.get('/health', (req, res) => {
    res.json({ status: 'ok', game: 'duckhunt' });
});

// API Routes
app.get('/api/user/:baleUserId', async (req, res) => {
    try {
        const user = await userService.getUserByBaleId(req.params.baleUserId);
        if (user) {
            res.json(user);
        } else {
            res.status(404).json({ error: 'User not found' });
        }
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.post('/api/register', async (req, res) => {
    try {
        const { baleUserId, phoneNumber, firstName, lastName, employeeCode } = req.body;

        if (!baleUserId || !firstName || !lastName || !employeeCode) {
            return res.status(400).json({ error: 'Missing required fields' });
        }

        const user = await userService.registerUser(baleUserId, phoneNumber, firstName, lastName, employeeCode);
        res.json({ success: true, user });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.get('/api/leaderboard/top/:limit?', async (req, res) => {
    try {
        const limit = parseInt(req.params.limit) || 10;
        const leaderboard = await userService.getTopPlayers(limit);
        res.json(leaderboard);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.get('/api/user/:baleUserId/stats', async (req, res) => {
    try {
        const user = await userService.getUserByBaleId(req.params.baleUserId);
        if (!user) {
            return res.status(404).json({ error: 'User not found' });
        }
        const stats = await userService.getUserStats(user.id);
        res.json(stats);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Socket.io Events
io.on('connection', (socket) => {
    console.log('User connected:', socket.id);

    // Check if user can play
    socket.on('check-game-limit', async (data, callback) => {
        try {
            const { baleUserId } = data;
            const user = await userService.getUserByBaleId(baleUserId);

            if (!user) {
                return callback({ canPlay: false, needsRegistration: true });
            }

            const gamesPlayed = await userService.countUserGames(user.id);
            const canPlay = gamesPlayed < MAX_GAMES_PER_USER;

            callback({
                canPlay,
                gamesPlayed,
                maxGames: MAX_GAMES_PER_USER,
                user: {
                    id: user.id,
                    firstName: user.first_name,
                    lastName: user.last_name
                }
            });
        } catch (error) {
            callback({ error: error.message });
        }
    });

    // Join game
    socket.on('join game', async (data, callback) => {
        try {
            const { baleUserId } = data;
            const user = await userService.getUserByBaleId(baleUserId);

            if (!user) {
                return callback({ success: true, needsRegistration: true });
            }

            callback({
                success: true,
                user: {
                    id: user.id,
                    firstName: user.first_name,
                    lastName: user.last_name
                }
            });
        } catch (error) {
            callback({ success: false, error: error.message });
        }
    });

    // Register user
    socket.on('register user', async (data, callback) => {
        try {
            const { baleUserId, phoneNumber, firstName, lastName, employeeCode } = data;

            if (!baleUserId || !firstName || !lastName || !employeeCode) {
                return callback({ success: false, error: 'Missing required fields' });
            }

            const user = await userService.registerUser(baleUserId, phoneNumber, firstName, lastName, employeeCode);
            callback({ success: true, user });
        } catch (error) {
            callback({ success: false, error: error.message });
        }
    });

    // Save score
    socket.on('save-score', async (data, callback) => {
        try {
            const { baleUserId, score, ducksShot, accuracy, gameDuration, levelReached } = data;

            const user = await userService.getUserByBaleId(baleUserId);
            if (!user) {
                return callback({ success: false, error: 'User not found' });
            }

            // Check game limit
            const gamesPlayed = await userService.countUserGames(user.id);
            if (gamesPlayed >= MAX_GAMES_PER_USER) {
                return callback({
                    success: false,
                    error: 'Game limit reached',
                    limitReached: true
                });
            }

            const result = await userService.saveScore(
                user.id, score, ducksShot, accuracy, gameDuration, levelReached
            );

            const newGamesPlayed = gamesPlayed + 1;

            callback({
                success: true,
                gamesPlayed: newGamesPlayed,
                maxGames: MAX_GAMES_PER_USER,
                canPlayAgain: newGamesPlayed < MAX_GAMES_PER_USER
            });
        } catch (error) {
            callback({ success: false, error: error.message });
        }
    });

    // Request leaderboard
    socket.on('request leaderboard', async (callback) => {
        try {
            const leaderboard = await userService.getTopPlayers(10);
            callback({ success: true, leaderboard });
        } catch (error) {
            callback({ success: false, error: error.message });
        }
    });

    socket.on('disconnect', () => {
        console.log('User disconnected:', socket.id);
    });
});

// Start server
server.listen(PORT, () => {
    console.log(`DuckHunt Challenge server running on port ${PORT}`);
    console.log(`Game URL: https://duck.darmanjoo.ir`);
});
