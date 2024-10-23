DROP SCHEMA IF EXISTS projet11 CASCADE;
CREATE SCHEMA projet11;

--------------------------------------------------------------
-- Utilisateur
--------------------------------------------------------------

DROP TABLE IF EXISTS projet11.utilisateur CASCADE;
CREATE TABLE projet11.utilisateur (
    id_utilisateur SERIAL UNIQUE PRIMARY KEY NOT NULL,
    pseudo TEXT NOT NULL,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    mdp TEXT NOT NULL,
    adresse_mail TEXT NOT NULL
);

--------------------------------------------------------------
-- Watchlist
--------------------------------------------------------------

DROP TABLE IF EXISTS projet11.watchlist CASCADE;

CREATE TABLE projet11.watchlist (
    id_watchlist SERIAL PRIMARY KEY NOT NULL, -- Utilisation de SERIAL pour autoincrémentation
    nom_watchlist TEXT NOT NULL,
    id_utilisateur TEXT REFERENCES projet11.utilisateur(id_utilisateur)
);

--------------------------------------------------------------
-- Film
--------------------------------------------------------------

DROP TABLE IF EXISTS projet11.film CASCADE;

CREATE TABLE projet11.film (
    id_film SERIAL PRIMARY KEY NOT NULL, -- Utilisation de SERIAL pour autoincrémentation
    nom_film TEXT NOT NULL
);

--------------------------------------------------------------
-- film_watchlist
--------------------------------------------------------------

DROP TABLE IF EXISTS projet11.film_watchlist CASCADE;

CREATE TABLE projet11.film_watchlist (
    id_watchlist INT REFERENCES projet11.watchlist(id_watchlist) ON DELETE CASCADE,
    id_film INT REFERENCES projet11.film(id_film) ON DELETE CASCADE,
    PRIMARY KEY (id_watchlist, id_film)
);

--------------------------------------------------------------
-- Plateforme d'abonnement
--------------------------------------------------------------

DROP TABLE IF EXISTS projet11.plateforme_abonnement CASCADE;

CREATE TABLE projet11.plateforme_abonnement (
    id_plateforme SERIAL PRIMARY KEY NOT NULL, -- Utilisation de SERIAL pour autoincrémentation
    nom_plateforme TEXT NOT NULL
);

--------------------------------------------------------------
-- film_plateforme
--------------------------------------------------------------

DROP TABLE IF EXISTS projet11.film_plateforme CASCADE;

CREATE TABLE projet11.film_plateforme (
    id_plateforme INT REFERENCES projet11.plateforme_abonnement(id_plateforme) ON DELETE CASCADE,
    id_film INT REFERENCES projet11.film(id_film) ON DELETE CASCADE,
    PRIMARY KEY (id_plateforme, id_film)
);

--------------------------------------------------------------
-- Abonnement
--------------------------------------------------------------

DROP TABLE IF EXISTS projet11.abonnement CASCADE;

CREATE TABLE projet11.abonnement (
    id_abonnement SERIAL PRIMARY KEY NOT NULL, -- Utilisation de SERIAL pour autoincrémentation
    nom_abonnement TEXT NOT NULL, -- Le type d'abonnement (ex: 'Avec pub', 'Sans pub')
    nom_plateforme TEXT NOT NULL, -- Le nom de la plateforme (ex: 'Amazon')
    qualite TEXT NOT NULL, -- Cette colonne stockera la qualité vidéo (ex: HD, 4K)
    prix DECIMAL(5, 2) NOT NULL, -- Le prix mensuel de l'abonnement
    pub BOOLEAN NOT NULL -- Indique si l'abonnement contient de la publicité (TRUE/FALSE)
);

-- Insertion des abonnements dans la table "abonnement"
INSERT INTO projet11.abonnement (nom_abonnement, nom_plateforme, qualite, prix, pub)
VALUES
('Avec pub', 'Amazon', '4K', 6.99, TRUE),
('Sans pub', 'Amazon', '4K', 8.98, FALSE),
('-24 ans', 'Amazon', '4K', 3.49, FALSE),
('Standard', 'Apple TV+', '4K', 9.99, FALSE),
('Standard', 'Canal+', '4K', 19.99, FALSE),
('Pass Coupes d’Europe', 'Canal+', '4K', 29.99, FALSE),
('Ciné Séries', 'Canal+', '4K', 29.99, FALSE),
('Friends & Family', 'Canal+', '4K', 64.99, FALSE),
('Sport', 'Canal+', '4K', 29.99, FALSE),
('Super Sports', 'DAZN', 'HD', 19.99, FALSE),
('Unlimited', 'DAZN', 'HD', 39.99, FALSE),
('Premium', 'Disney+', '4K', 11.99, FALSE),
('Standard', 'Disney+', 'HD', 8.99, FALSE),
('Avec pub', 'Disney+', 'HD', 5.99, TRUE),
('Standard', 'Filmo', 'HD', 6.99, FALSE),
('Avec tickets', 'Filmo', 'HD', 11.99, FALSE),
('Standard avec pub', 'Netflix', 'HD', 5.99, TRUE),
('Standard', 'Netflix', 'HD', 13.49, FALSE),
('Premium', 'Netflix', '4K', 19.99, FALSE),
('Basique avec pub', 'Max', 'HD', 5.99, TRUE),
('Standard', 'Max', '4K', 9.99, FALSE),
('Premium', 'Max', '4K', 13.99, FALSE),
('Extended', 'Molotov', 'HD', 10.99, FALSE),
('Extra', 'Molotov', 'HD', 6.99, FALSE),
('Premium', 'Paramount+', '4K', 10.99, FALSE),
('Standard', 'Paramount+', 'HD', 7.99, FALSE);

