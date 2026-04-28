CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    recency FLOAT NOT NULL,
    frequency FLOAT NOT NULL,
    monetary FLOAT NOT NULL,
    cluster_id INTEGER
);

CREATE TABLE IF NOT EXISTS clusters_summary (
    id INTEGER PRIMARY KEY, -- Can be -1 for noise
    avg_recency FLOAT NOT NULL,
    avg_frequency FLOAT NOT NULL,
    avg_monetary FLOAT NOT NULL,
    customer_count INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS campaign_copy (
    id SERIAL PRIMARY KEY,
    cluster_id INTEGER UNIQUE REFERENCES clusters_summary(id),
    generated_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
