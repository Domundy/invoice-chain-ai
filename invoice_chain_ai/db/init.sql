CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    customer_prompt TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS accounts (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers (id) ON DELETE CASCADE,
    iban TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS addresses (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers (id) ON DELETE CASCADE,
    address_type TEXT,
    name TEXT,
    line1 TEXT,
    line2 TEXT,
    postal_code TEXT,
    city TEXT,
    country TEXT
);

-- Ensure column exists on pre-existing installations
ALTER TABLE customers ADD COLUMN IF NOT EXISTS customer_prompt TEXT;