-- Enable relational integrity for every SQLite connection that uses this schema.
PRAGMA foreign_keys = ON;

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    district TEXT,
    postal_code TEXT,
    street TEXT
);

CREATE TABLE complaints (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    complaint_type TEXT,
    complaint TEXT,
    complaint_department TEXT,
    tracking_no TEXT,
    filed INTEGER NOT NULL DEFAULT 0 CHECK (filed IN (0, 1)),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX idx_complaints_user_id ON complaints(user_id);
