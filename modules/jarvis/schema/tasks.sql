-- JARVIS Local Memory: Tasks & GitHub Tables
-- Version: 1.0.0

-- tasks: 작업 목록 및 상태
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER REFERENCES projects(id) ON DELETE SET NULL,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'todo' CHECK (status IN ('todo', 'in_progress', 'blocked', 'done', 'cancelled')),
    priority INTEGER DEFAULT 5 CHECK (priority BETWEEN 1 AND 10),
    due_date DATETIME,
    tags JSON,
    metadata JSON,
    parent_task_id INTEGER REFERENCES tasks(id) ON DELETE CASCADE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME
);

CREATE INDEX IF NOT EXISTS idx_tasks_project ON tasks(project_id);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority DESC);
CREATE INDEX IF NOT EXISTS idx_tasks_due ON tasks(due_date) WHERE due_date IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_tasks_parent ON tasks(parent_task_id) WHERE parent_task_id IS NOT NULL;

-- github_events: GitHub 이슈/PR 캐시
CREATE TABLE IF NOT EXISTS github_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    event_type TEXT NOT NULL CHECK (event_type IN ('issue', 'pr', 'commit', 'release', 'review')),
    github_id INTEGER NOT NULL,
    number INTEGER,
    title TEXT NOT NULL,
    state TEXT,
    author TEXT,
    url TEXT,
    body TEXT,
    labels JSON,
    metadata JSON,
    github_created_at DATETIME,
    github_updated_at DATETIME,
    cached_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(project_id, event_type, github_id)
);

CREATE INDEX IF NOT EXISTS idx_github_project ON github_events(project_id);
CREATE INDEX IF NOT EXISTS idx_github_type ON github_events(event_type);
CREATE INDEX IF NOT EXISTS idx_github_state ON github_events(state);
CREATE INDEX IF NOT EXISTS idx_github_cached ON github_events(cached_at);

-- Triggers
CREATE TRIGGER IF NOT EXISTS trg_tasks_updated
    AFTER UPDATE ON tasks
BEGIN
    UPDATE tasks SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS trg_tasks_completed
    AFTER UPDATE OF status ON tasks
    WHEN NEW.status = 'done' AND OLD.status != 'done'
BEGIN
    UPDATE tasks SET completed_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;
