CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    rut VARCHAR(20),
    nombre VARCHAR(100),
    email VARCHAR(100),
    sexo VARCHAR(10),
    edad INTEGER,
    estado_civil VARCHAR(50),
    tiene_hijos BOOLEAN,
    profesion VARCHAR(100),
    ingreso_mensual_clp FLOAT,
    segmento VARCHAR(50),
    es_cliente BOOLEAN,
    antiguedad_cuenta_meses FLOAT,
    conocimiento_inversiones VARCHAR(50),
    acepta_comunicaciones BOOLEAN,
    oferta_credito_clp FLOAT,
    tasa_credito_pct FLOAT,
    oferta_tc_limite_clp FLOAT,
    cluster_id INTEGER
);

CREATE TABLE IF NOT EXISTS clusters_summary (
    id INTEGER PRIMARY KEY, -- Can be -1 for noise
    customer_count INTEGER NOT NULL,
    centroid_features JSONB
);

CREATE TABLE IF NOT EXISTS campaign_copy (
    id SERIAL PRIMARY KEY,
    cluster_id INTEGER UNIQUE REFERENCES clusters_summary(id),
    generated_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
