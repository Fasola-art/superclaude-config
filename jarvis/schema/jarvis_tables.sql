-- JARVIS 모듈별 PostgreSQL 테이블 스키마
-- Version: 1.0.0
-- Database: claude_mcp

-- ============================================
-- Learning System Tables
-- ============================================

CREATE TABLE IF NOT EXISTS learning_patterns (
    id SERIAL PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    input_text TEXT NOT NULL,
    output_action VARCHAR(100) NOT NULL,
    context JSONB DEFAULT '{}',
    confidence DECIMAL(3,2) DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS learning_feedback (
    id SERIAL PRIMARY KEY,
    pattern_id INTEGER REFERENCES learning_patterns(id),
    positive BOOLEAN NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_learning_patterns_category ON learning_patterns(category);
CREATE INDEX idx_learning_patterns_created ON learning_patterns(created_at);

-- ============================================
-- Habit Tracking Tables
-- ============================================

CREATE TABLE IF NOT EXISTS habits (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    frequency VARCHAR(20) DEFAULT 'daily',
    target_days INTEGER[],
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS habit_completions (
    id SERIAL PRIMARY KEY,
    habit_id INTEGER REFERENCES habits(id),
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT
);

CREATE INDEX idx_habits_active ON habits(active);
CREATE INDEX idx_habit_completions_date ON habit_completions(completed_at);

-- ============================================
-- Client & Work Tracking Tables
-- ============================================

CREATE TABLE IF NOT EXISTS clients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    project VARCHAR(200),
    hourly_rate DECIMAL(10,2) DEFAULT 0,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS work_logs (
    id SERIAL PRIMARY KEY,
    client_id INTEGER REFERENCES clients(id),
    hours DECIMAL(4,2) NOT NULL,
    description TEXT,
    hourly_rate DECIMAL(10,2),
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_clients_active ON clients(active);
CREATE INDEX idx_work_logs_client ON work_logs(client_id);
CREATE INDEX idx_work_logs_date ON work_logs(logged_at);

-- ============================================
-- Session & Memory Tables
-- ============================================

CREATE TABLE IF NOT EXISTS work_sessions (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(100) UNIQUE NOT NULL,
    project_path TEXT,
    files_edited JSONB DEFAULT '[]',
    tools_used JSONB DEFAULT '[]',
    summary TEXT,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP
);

CREATE TABLE IF NOT EXISTS context_entries (
    id SERIAL PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sessions_time ON work_sessions(start_time);
CREATE INDEX idx_context_category ON context_entries(category);

-- ============================================
-- Log Aggregation Tables (I-03)
-- ============================================

CREATE TABLE IF NOT EXISTS system_logs (
    id SERIAL PRIMARY KEY,
    level VARCHAR(10) NOT NULL,
    source VARCHAR(100) NOT NULL,
    message TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS error_logs (
    id SERIAL PRIMARY KEY,
    error_type VARCHAR(100) NOT NULL,
    message TEXT NOT NULL,
    stack_trace TEXT,
    context JSONB DEFAULT '{}',
    resolved BOOLEAN DEFAULT false,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_logs_level ON system_logs(level);
CREATE INDEX idx_logs_source ON system_logs(source);
CREATE INDEX idx_logs_time ON system_logs(timestamp);
CREATE INDEX idx_errors_type ON error_logs(error_type);
CREATE INDEX idx_errors_resolved ON error_logs(resolved);
