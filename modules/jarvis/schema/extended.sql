-- JARVIS Local Memory: Extended Tables
-- Version: 1.0.0

-- calendar_events: 일정 관리
CREATE TABLE IF NOT EXISTS calendar_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    start_time DATETIME NOT NULL,
    end_time DATETIME,
    location TEXT,
    attendees JSON,
    metadata JSON,
    reminder_minutes INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_calendar_start ON calendar_events(start_time);
CREATE INDEX IF NOT EXISTS idx_calendar_end ON calendar_events(end_time);

-- context_history: 대화 컨텍스트 히스토리
CREATE TABLE IF NOT EXISTS context_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    context_type TEXT NOT NULL CHECK (context_type IN ('conversation', 'task', 'query', 'command')),
    data TEXT NOT NULL,
    metadata JSON,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_context_type ON context_history(context_type);
CREATE INDEX IF NOT EXISTS idx_context_timestamp ON context_history(timestamp DESC);

-- Triggers
CREATE TRIGGER IF NOT EXISTS trg_calendar_updated
    AFTER UPDATE ON calendar_events
BEGIN
    UPDATE calendar_events SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;
