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
-- Abonnements (pour stocker les informations des abonnements)
--------------------------------------------------------------

DROP TABLE IF EXISTS projet11.abonnement_details CASCADE;

CREATE TABLE projet11.abonnement_details (
    id_abonnement INT PRIMARY KEY NOT NULL,
    type_abonnement TEXT NOT NULL,
    qualite_video TEXT NOT NULL, -- 4K ou HD
    prix_mensuel DECIMAL(5, 2) NOT NULL, 
    pub BOOLEAN NOT NULL,
    id_plateforme INT REFERENCES projet11.plateforme_abonnement(id_plateforme)
);

-- Insertion des abonnements
INSERT INTO projet11.abonnement_infos (id_abonnement, type_abonnement, qualite_video, prix_mensuel, pub, id_plateforme)
VALUES 
(1, 'Avec pub', '4K', 6.99, TRUE, 1),
(2, 'Sans pub', '4K', 8.98, FALSE, 2),
(3, '-24 ans', '4K', 3.49, FALSE, 3),
(4, 'Standard', '4K', 9.99, FALSE, 4),
(5, 'Standard', '4K', 19.99, FALSE, 5),
(6, 'Pass Coupes d’Europe', '4K', 29.99, FALSE, 6),
(7, 'Ciné Séries', '4K', 29.99, FALSE, 7),
(8, 'Friends & Family', '4K', 64.99, FALSE, 8),
(9, 'Sport', '4K', 29.99, FALSE, 9),
(10, 'Super Sports', 'HD', 19.99, FALSE, 10),
(11, 'Unlimited', 'HD', 39.99, FALSE, 11),
(12, 'Premium', '4K', 11.99, FALSE, 12),
(13, 'Standard', 'HD', 8.99, FALSE, 13),
(14, 'Avec pub', 'HD', 5.99, TRUE, 14),
(15, 'Standard', 'HD', 6.99, FALSE, 15),
(16, 'Avec tickets', 'HD', 11.99, FALSE, 16),
(17, 'Standard avec pub', 'HD', 5.99, TRUE, 17),
(18, 'Standard', 'HD', 13.49, FALSE, 18),
(19, 'Premium', '4K', 19.99, FALSE, 19),
(20, 'Basique avec pub', 'HD', 5.99, TRUE, 20),
(21, 'Standard', '4K', 9.99, FALSE, 21),
(22, 'Premium', '4K', 13.99, FALSE, 22),
(23, 'Extended', 'HD', 10.99, FALSE, 23),
(24, 'Extra', 'HD', 6.99, FALSE, 24),
(25, 'Premium', '4K', 10.99, FALSE, 25),
(26, 'Standard', 'HD', 7.99, FALSE, 26);

