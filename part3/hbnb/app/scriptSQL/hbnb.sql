-- =======================
-- HBnB: Création du schéma
-- =======================

-- Table : users
CREATE TABLE IF NOT EXISTS users (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Table : amenities
CREATE TABLE IF NOT EXISTS amenities (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Table : places
CREATE TABLE IF NOT EXISTS places (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    owner_id CHAR(36) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Table : reviews
CREATE TABLE IF NOT EXISTS reviews (
    id CHAR(36) PRIMARY KEY,
    text TEXT NOT NULL,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    user_id CHAR(36) NOT NULL,
    place_id CHAR(36) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT one_review_per_user_place UNIQUE (user_id, place_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE
);

-- Table de jointure : place_amenity
CREATE TABLE IF NOT EXISTS place_amenity (
    place_id CHAR(36) NOT NULL,
    amenity_id CHAR(36) NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
    FOREIGN KEY (amenity_id) REFERENCES amenities(id) ON DELETE CASCADE
);

-- ===============================
-- Données initiales
-- ===============================

-- ADMIN (Argon2 hash)
INSERT OR IGNORE INTO users (id, first_name, last_name, email, password, is_admin) VALUES
('36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'Admin', 'HBnB', 'admin@hbnb.io',
'$argon2id$v=19$m=65536,t=3,p=4$ylUtdC2wJ7BluyfA1SgRgQ$ql1KWi6nsgAbTlpvqG7OQZHSCN+Zk4f8Hf0+RWQWv/w', TRUE);

-- 3 amenities de base (UUID v4)
INSERT OR IGNORE INTO amenities (id, name) VALUES
('e0e3b7f2-2d8e-4c72-b2ba-0a76e9f7a012', 'WiFi'),
('6369e1e2-253d-4195-9e5c-cae2b871a800', 'Swimming Pool'),
('a7b57d82-f6ad-4958-914a-4c4bfa633f7b', 'Air Conditioning');

-- ===============================
-- TESTS CRUD
-- ===============================

-- 1. Créer un user test
INSERT INTO users (id, first_name, last_name, email, password) VALUES
('bf3d793d-2a19-4af1-b276-d9e7e40058c7', 'Jean', 'Test', 'jean@test.fr', 'test1234');

-- 2. Créer un place
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id) VALUES
('74b2c84d-f0c1-4e53-81d5-c6c845faacb1', 'Petit Loft', 'Charmant loft à Dijon', 95.50, 47.3167, 5.0167, 'bf3d793d-2a19-4af1-b276-d9e7e40058c7');

-- 3. Lier un amenity à un lieu
INSERT INTO place_amenity (place_id, amenity_id) VALUES
('74b2c84d-f0c1-4e53-81d5-c6c845faacb1', 'e0e3b7f2-2d8e-4c72-b2ba-0a76e9f7a012');

-- 4. Laisser un avis
INSERT INTO reviews (id, text, rating, user_id, place_id) VALUES
('5e9a8f24-bfc6-46c6-bf9f-2b9a340d396a', 'Génial, très propre', 5, 'bf3d793d-2a19-4af1-b276-d9e7e40058c7', '74b2c84d-f0c1-4e53-81d5-c6c845faacb1');

-- 5. SELECT : tout voir
SELECT * FROM users;
SELECT * FROM amenities;
SELECT * FROM places;
SELECT * FROM place_amenity;
SELECT * FROM reviews;

-- 6. UPDATE : changer le nom d’un amenity
UPDATE amenities SET name = 'WIFI ULTRA' WHERE name = 'WiFi';

-- 7. DELETE : supprimer une review (test FK)
DELETE FROM reviews WHERE id = '5e9a8f24-bfc6-46c6-bf9f-2b9a340d396a';

-- ===============================
-- Fin du script
-- ===============================
