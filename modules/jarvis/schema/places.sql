-- JARVIS: 장소 추천 및 예약 관리
-- Version: 1.0.0

-- places: 즐겨찾기 장소
CREATE TABLE IF NOT EXISTS places (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL CHECK (category IN ('restaurant', 'cafe', 'attraction', 'activity', 'accommodation', 'other')),
    address TEXT,
    lat REAL,
    lng REAL,
    rating REAL CHECK (rating BETWEEN 0 AND 5),
    price_level INTEGER CHECK (price_level BETWEEN 0 AND 4),
    google_place_id TEXT UNIQUE,
    phone TEXT,
    website TEXT,
    photo_url TEXT,
    tags JSON,
    memo TEXT,
    is_bookmarked INTEGER DEFAULT 0,
    visit_count INTEGER DEFAULT 0,
    last_visited_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_places_category ON places(category);
CREATE INDEX IF NOT EXISTS idx_places_bookmarked ON places(is_bookmarked) WHERE is_bookmarked = 1;
CREATE INDEX IF NOT EXISTS idx_places_rating ON places(rating DESC);
CREATE INDEX IF NOT EXISTS idx_places_google_id ON places(google_place_id);

-- reservations: 예약 추적
CREATE TABLE IF NOT EXISTS reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    place_id INTEGER REFERENCES places(id),
    title TEXT NOT NULL,
    reserved_date DATE NOT NULL,
    reserved_time TEXT,
    party_size INTEGER DEFAULT 2,
    status TEXT DEFAULT 'confirmed' CHECK (status IN ('confirmed', 'pending', 'cancelled', 'completed')),
    booking_url TEXT,
    confirmation_code TEXT,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_reservations_date ON reservations(reserved_date);
CREATE INDEX IF NOT EXISTS idx_reservations_status ON reservations(status);

-- Triggers
CREATE TRIGGER IF NOT EXISTS trg_places_updated
    AFTER UPDATE ON places
BEGIN
    UPDATE places SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS trg_reservations_updated
    AFTER UPDATE ON reservations
BEGIN
    UPDATE reservations SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;
