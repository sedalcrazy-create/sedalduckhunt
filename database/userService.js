'use strict';

const pool = require('./db');

const userService = {
    // Register new user
    async registerUser(baleUserId, phoneNumber, firstName, lastName, employeeCode) {
        try {
            const result = await pool.query(
                `INSERT INTO users (bale_user_id, phone_number, first_name, last_name, employee_code)
                 VALUES ($1, $2, $3, $4, $5)
                 ON CONFLICT (bale_user_id) DO UPDATE SET
                    first_name = EXCLUDED.first_name,
                    last_name = EXCLUDED.last_name,
                    updated_at = CURRENT_TIMESTAMP
                 RETURNING *`,
                [baleUserId, phoneNumber, firstName, lastName, employeeCode]
            );
            return result.rows[0];
        } catch (error) {
            console.error('Error registering user:', error);
            throw error;
        }
    },

    // Get user by Bale ID
    async getUserByBaleId(baleUserId) {
        try {
            const result = await pool.query(
                'SELECT * FROM users WHERE bale_user_id = $1',
                [baleUserId]
            );
            return result.rows[0] || null;
        } catch (error) {
            console.error('Error getting user:', error);
            throw error;
        }
    },

    // Update user names
    async updateUserNames(userId, firstName, lastName) {
        try {
            const result = await pool.query(
                `UPDATE users SET first_name = $1, last_name = $2, updated_at = CURRENT_TIMESTAMP
                 WHERE id = $3 RETURNING *`,
                [firstName, lastName, userId]
            );
            return result.rows[0];
        } catch (error) {
            console.error('Error updating user:', error);
            throw error;
        }
    },

    // Save game score
    async saveScore(userId, score, ducksShot, accuracy, gameDuration, levelReached) {
        try {
            const result = await pool.query(
                `INSERT INTO leaderboard (user_id, score, ducks_shot, accuracy, game_duration, level_reached)
                 VALUES ($1, $2, $3, $4, $5, $6)
                 RETURNING *`,
                [userId, score, ducksShot, accuracy, gameDuration, levelReached]
            );
            return result.rows[0];
        } catch (error) {
            console.error('Error saving score:', error);
            throw error;
        }
    },

    // Get top players
    async getTopPlayers(limit = 10) {
        try {
            const result = await pool.query(
                `SELECT * FROM high_scores LIMIT $1`,
                [limit]
            );
            return result.rows;
        } catch (error) {
            console.error('Error getting top players:', error);
            throw error;
        }
    },

    // Get user rank
    async getUserRank(userId) {
        try {
            const result = await pool.query(
                `SELECT COUNT(*) + 1 as rank FROM high_scores
                 WHERE high_score > (SELECT COALESCE(MAX(score), 0) FROM leaderboard WHERE user_id = $1)`,
                [userId]
            );
            return parseInt(result.rows[0].rank);
        } catch (error) {
            console.error('Error getting user rank:', error);
            throw error;
        }
    },

    // Get user stats
    async getUserStats(userId) {
        try {
            const result = await pool.query(
                `SELECT
                    u.first_name, u.last_name, u.employee_code,
                    COALESCE(MAX(l.score), 0) as high_score,
                    COALESCE(MAX(l.ducks_shot), 0) as max_ducks,
                    COALESCE(MAX(l.level_reached), 0) as max_level,
                    COUNT(l.id) as games_played
                 FROM users u
                 LEFT JOIN leaderboard l ON u.id = l.user_id
                 WHERE u.id = $1
                 GROUP BY u.id`,
                [userId]
            );
            const stats = result.rows[0];
            if (stats) {
                stats.rank = await this.getUserRank(userId);
            }
            return stats;
        } catch (error) {
            console.error('Error getting user stats:', error);
            throw error;
        }
    },

    // Count games played by user
    async countUserGames(userId) {
        try {
            const result = await pool.query(
                'SELECT COUNT(*) as count FROM leaderboard WHERE user_id = $1',
                [userId]
            );
            return parseInt(result.rows[0].count);
        } catch (error) {
            console.error('Error counting games:', error);
            throw error;
        }
    }
};

module.exports = userService;
