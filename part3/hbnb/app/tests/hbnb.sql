-- ============================
-- HBnB: TESTS du schéma complet
-- ============================

-- Nettoyage préalable
DROP TABLE IF EXISTS place_amenity;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS places;
DROP TABLE IF EXISTS amenities;
DROP TABLE IF EXISTS users;

-- 1. Création du schéma (copié/ajusté du script précédent)
CREATE TABLE users (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE amenities (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE places (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    owner_id CHAR(36) NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE reviews (
    id CHAR(36) PRIMARY KEY,
    text TEXT NOT NULL,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    user_id CHAR(36) NOT NULL,
    place_id CHAR(36) NOT NULL,
    CONSTRAINT one_review_per_user_place UNIQUE (user_id, place_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE
);

CREATE TABLE place_amenity (
    place_id CHAR(36) NOT NULL,
    amenity_id CHAR(36) NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
    FOREIGN KEY (amenity_id) REFERENCES amenities(id) ON DELETE CASCADE
);

-- 2. Données initiales (admin + 3 amenities)
INSERT INTO users (id, first_name, last_name, email, password, is_admin) VALUES
('36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'Admin', 'HBnB', 'admin@hbnb.io',
'$argon2id$v=19$m=65536,t=3,p=4$ylUtdC2wJ7BluyfA1SgRgQ$ql1KWi6nsgAbTlpvqG7OQZHSCN+Zk4f8Hf0+RWQWv/w', -- hash pour "admin1234"
TRUE);

INSERT INTO amenities (id, name) VALUES
('e0e3b7f2-2d8e-4c72-b2ba-0a76e9f7a012', 'WiFi'),
('6369e1e2-253d-4195-9e5c-cae2b871a800', 'Swimming Pool'),
('a7b57d82-f6ad-4958-914a-4c4bfa633f7b', 'Air Conditioning');

-- 3. Insertion d’un user lambda pour tests
INSERT INTO users (id, first_name, last_name, email, password, is_admin) VALUES
('c8ed624a-3b2a-4717-8e71-0be8a6dabe12', 'Jean', 'Client', 'jean.client@hbnb.io', 'fakehash', FALSE);

-- 4. CRUD sur Place
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id) VALUES
('b8c58c4e-82c7-433e-afe6-2e9bcaa30613', 'Maison du bonheur', 'Grande maison', 120.00, 48.85, 2.35, 'c8ed624a-3b2a-4717-8e71-0be8a6dabe12');

SELECT * FROM places; -- lecture

UPDATE places SET price=130.00 WHERE id='b8c58c4e-82c7-433e-afe6-2e9bcaa30613';

DELETE FROM places WHERE id='b8c58c4e-82c7-433e-afe6-2e9bcaa30613';

-- 5. CRUD sur Review
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id) VALUES
('9b3a7f74-3ad2-4ad4-80e4-df7aebb00b4e', 'Cabane dans les arbres', 'Vue forêt', 80.00, 43.61, 1.44, 'c8ed624a-3b2a-4717-8e71-0be8a6dabe12');

INSERT INTO reviews (id, text, rating, user_id, place_id) VALUES
('99ec34d6-60f1-4bfa-b259-b4f0a632ae19', 'Super séjour', 5, 'c8ed624a-3b2a-4717-8e71-0be8a6dabe12', '9b3a7f74-3ad2-4ad4-80e4-df7aebb00b4e');

SELECT * FROM reviews;

UPDATE reviews SET rating=4 WHERE id='99ec34d6-60f1-4bfa-b259-b4f0a632ae19';

DELETE FROM reviews WHERE id='99ec34d6-60f1-4bfa-b259-b4f0a632ae19';

-- 6. CRUD sur Amenity
SELECT * FROM amenities;

UPDATE amenities SET name='Wifi Premium' WHERE id='e0e3b7f2-2d8e-4c72-b2ba-0a76e9f7a012';

DELETE FROM amenities WHERE id='a7b57d82-f6ad-4958-914a-4c4bfa633f7b';

-- 7. CRUD sur place_amenity
INSERT INTO place_amenity (place_id, amenity_id) VALUES
('9b3a7f74-3ad2-4ad4-80e4-df7aebb00b4e', 'e0e3b7f2-2d8e-4c72-b2ba-0a76e9f7a012');

SELECT * FROM place_amenity;

DELETE FROM place_amenity WHERE place_id='9b3a7f74-3ad2-4ad4-80e4-df7aebb00b4e' AND amenity_id='e0e3b7f2-2d8e-4c72-b2ba-0a76e9f7a012';

-- 8. Lecture finale (état des tables)
SELECT * FROM users;
SELECT * FROM amenities;
SELECT * FROM places;
SELECT * FROM reviews;
SELECT * FROM place_amenity;
