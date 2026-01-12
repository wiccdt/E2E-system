CREATE TABLE IF NOT EXISTS taxi_rides (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    from_address VARCHAR(255) NOT NULL,
    to_address VARCHAR(255) NOT NULL,
    distance_km DECIMAL(5,2) CHECK (distance_km BETWEEN 1 AND 50),
    price DECIMAL(10,2) CHECK (price BETWEEN 100 AND 3000),
    rating DECIMAL(3,1) CHECK (rating BETWEEN 1.0 AND 5.0),
    vehicle_type VARCHAR(20) CHECK (vehicle_type IN ('economy', 'comfort', 'business')),
    duration_min INTEGER CHECK (duration_min BETWEEN 5 AND 120),
    payment_method VARCHAR(10) CHECK (payment_method IN ('cash', 'card')),
    created_at TIMESTAMP DEFAULT NOW()
);