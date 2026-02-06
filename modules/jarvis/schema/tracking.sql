-- JARVIS Local Memory: Reminders & Habits Tables
-- Version: 1.0.0

-- reminders: 리마인더
CREATE TABLE IF NOT EXISTS reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    remind_at DATETIME NOT NULL,
    repeat_pattern TEXT CHECK (repeat_pattern IN ('once', 'daily', 'weekly', 'monthly', 'custom')),
    repeat_config JSON,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'triggered', 'snoozed', 'dismissed')),
    snooze_until DATETIME,
    metadata JSON,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_reminders_remind_at ON reminders(remind_at);
CREATE INDEX IF NOT EXISTS idx_reminders_status ON reminders(status);
CREATE INDEX IF NOT EXISTS idx_reminders_pending ON reminders(remind_at) WHERE status = 'pending';

-- habits: 습관 정의
CREATE TABLE IF NOT EXISTS habits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    frequency TEXT NOT NULL CHECK (frequency IN ('daily', 'weekly', 'custom')),
    frequency_config JSON,
    target_count INTEGER DEFAULT 1,
    streak_current INTEGER DEFAULT 0,
    streak_best INTEGER DEFAULT 0,
    is_active INTEGER DEFAULT 1,
    metadata JSON,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_habits_active ON habits(is_active);

-- habit_logs: 습관 실행 기록
CREATE TABLE IF NOT EXISTS habit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    habit_id INTEGER NOT NULL REFERENCES habits(id) ON DELETE CASCADE,
    logged_date DATE NOT NULL,
    count INTEGER DEFAULT 1,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(habit_id, logged_date)
);

CREATE INDEX IF NOT EXISTS idx_habit_logs_habit ON habit_logs(habit_id);
CREATE INDEX IF NOT EXISTS idx_habit_logs_date ON habit_logs(logged_date DESC);

-- Triggers
CREATE TRIGGER IF NOT EXISTS trg_reminders_updated
    AFTER UPDATE ON reminders
BEGIN
    UPDATE reminders SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS trg_habits_updated
    AFTER UPDATE ON habits
BEGIN
    UPDATE habits SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;
