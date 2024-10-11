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
-- plateforme
--------------------------------------------------------------

DROP TABLE IF EXISTS projet11.plateforme CASCADE;

CREATE TABLE projet11.plateforme (
    id_plateforme INT PRIMARY KEY NOT NULL,
    nom_plateforme text NOT NULL
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
-- abonnement
--------------------------------------------------------------

DROP TABLE IF EXISTS projet11.abonnement CASCADE;

CREATE TABLE projet11.abonnement (
    id_abonnement INT UNIQUE PRIMARY KEY NOT NULL,
    id_plateforme INT REFERENCES projet11.plateforme(id_plateforme),
    prix INT NOT NULL, 
    pub boolean NOT NULL
);

