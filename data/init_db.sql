DROP SCHEMA IF EXISTS projet11 CASCADE ;
CREATE SCHEMA projet11;

--------------------------------------------------------------
-- Utilisateur
--------------------------------------------------------------

DROP TABLE IF EXISTS projet11.utilisateur CASCADE ;
CREATE TABLE projet11.utilisateur (
    id_utilisateur text UNIQUE PRIMARY KEY NOT NULL
    pseudo text NOT NULL,
    nom text NOT NULL,
    prenom text NOT NULL,
    mdp text NOT NULL,
    adresse_mail text NOT NULL
);


--------------------------------------------------------------
-- watchlist
--------------------------------------------------------------

DROP TABLE IF EXISTS projet11.watchlist;

CREATE TABLE projet11.watchlist (
    id_watchlist INT PRIMARY KEY NOT NULL,
    nom_watchlist text NOT NULL,
    id_utilisateur text REFERENCES projet11.utilisateur(id_utilisateur)
);


--------------------------------------------------------------
-- film
--------------------------------------------------------------

DROP TABLE IF EXISTS projet11.film CASCADE;

CREATE TABLE projet11.film (
    id_film INT UNIQUE PRIMARY KEY NOT NULL,
    nom_film text NOT NULL
);


--------------------------------------------------------------
-- film_watchlist
--------------------------------------------------------------

DROP TABLE IF EXISTS projet11.film_watchlist CASCADE;

CREATE TABLE projet11.film_watchlist (
    id_watchlist INT REFERENCES projet11.watchlist(id_watchlist),
    id_film INT REFERENCES projet11.film(id_film),
    PRIMARY KEY (id_watchlist, id_film)
);


--------------------------------------------------------------
-- plateformes
--------------------------------------------------------------

DROP TABLE IF EXISTS projet11.plateforme_abonnement CASCADE;

CREATE TABLE projet11.plateforme_abonnement (
    id_plateforme INT PRIMARY KEY NOT NULL,
    nom_plateforme TEXT NOT NULL
);



--------------------------------------------------------------
-- film_plateforme
--------------------------------------------------------------

DROP TABLE IF EXISTS projet11.film_plateforme CASCADE;

CREATE TABLE projet11.film_plateforme (
    id_plateforme INT REFERENCES projet11.plateforme(id_plateforme),
    id_film INT REFERENCES projet11.film(id_film),
    PRIMARY KEY (id_plateforme, id_film)
);


--------------------------------------------------------------
-- Abonnement (id_abonnement, nom de l'abonnement, nom de la plateforme, qualité, prix, pub)
--------------------------------------------------------------

DROP TABLE IF EXISTS projet11.abonnement CASCADE;

CREATE TABLE projet11.abonnement (
    id_abonnement INT PRIMARY KEY NOT NULL,
    nom_abonnement TEXT NOT NULL, -- Le type d'abonnement (ex: 'Avec pub', 'Sans pub')
    nom_plateforme TEXT NOT NULL, -- Le nom de la plateforme (ex: 'Amazon')
    qualite TEXT NOT NULL, -- Cette colonne stockera la qualité vidéo (ex: HD, 4K)
    prix DECIMAL(5, 2) NOT NULL, -- Le prix mensuel de l'abonnement
    pub BOOLEAN NOT NULL -- Indique si l'abonnement contient de la publicité (TRUE/FALSE)
);

-- Insertion des abonnements dans la table "abonnement"
INSERT INTO projet11.abonnement (id_abonnement, nom_abonnement, nom_plateforme, qualite, prix, pub)
VALUES 
(1, 'Avec pub', 'Amazon', '4K', 6.99, TRUE),
(2, 'Sans pub', 'Amazon', '4K', 8.98, FALSE),
(3, '-24 ans', 'Amazon', '4K', 3.49, FALSE),
(4, 'Standard', 'Apple TV+', '4K', 9.99, FALSE),
(5, 'Standard', 'Canal+', '4K', 19.99, FALSE),
(6, 'Pass Coupes d’Europe', 'Canal+', '4K', 29.99, FALSE),
(7, 'Ciné Séries', 'Canal+', '4K', 29.99, FALSE),
(8, 'Friends & Family', 'Canal+', '4K', 64.99, FALSE),
(9, 'Sport', 'Canal+', '4K', 29.99, FALSE),
(10, 'Super Sports', 'DAZN', 'HD', 19.99, FALSE),
(11, 'Unlimited', 'DAZN', 'HD', 39.99, FALSE),
(12, 'Premium', 'Disney+', '4K', 11.99, FALSE),
(13, 'Standard', 'Disney+', 'HD', 8.99, FALSE),
(14, 'Avec pub', 'Disney+', 'HD', 5.99, TRUE),
(15, 'Standard', 'Filmo', 'HD', 6.99, FALSE),
(16, 'Avec tickets', 'Filmo', 'HD', 11.99, FALSE),
(17, 'Standard avec pub', 'Netflix', 'HD', 5.99, TRUE),
(18, 'Standard', 'Netflix', 'HD', 13.49, FALSE),
(19, 'Premium', 'Netflix', '4K', 19.99, FALSE),
(20, 'Basique avec pub', 'Max', 'HD', 5.99, TRUE),
(21, 'Standard', 'Max', '4K', 9.99, FALSE),
(22, 'Premium', 'Max', '4K', 13.99, FALSE),
(23, 'Extended', 'Molotov', 'HD', 10.99, FALSE),
(24, 'Extra', 'Molotov', 'HD', 6.99, FALSE),
(25, 'Premium', 'Paramount+', '4K', 10.99, FALSE),
(26, 'Standard', 'Paramount+', 'HD', 7.99, FALSE);
