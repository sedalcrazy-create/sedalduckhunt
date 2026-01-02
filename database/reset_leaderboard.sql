-- Reset Leaderboard and Games
-- This script deletes all game records but keeps user registrations

-- Delete all game records
TRUNCATE TABLE leaderboard RESTART IDENTITY CASCADE;

-- Verify reset
SELECT 'Leaderboard reset complete!' as message;
SELECT COUNT(*) as remaining_games FROM leaderboard;
SELECT COUNT(*) as total_users FROM users;
