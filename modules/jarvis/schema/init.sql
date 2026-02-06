-- JARVIS Local Memory: Full Schema Init
-- Version: 1.0.0
-- Usage: sqlite3 jarvis.db < init.sql

PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

.read core.sql
.read tasks.sql
.read tracking.sql
.read extended.sql

-- Verify tables
SELECT 'Tables created: ' || COUNT(*) FROM sqlite_master WHERE type='table';
