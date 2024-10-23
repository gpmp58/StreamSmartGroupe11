import streamlit as st
from src.webservice.services.service_utilisateur import UtilisateurService
from src.webservice.dao.utilisateur_dao import UtilisateurDAO  # Importer le DAO réel pour interagir avec la base de données

# Interface principale avec Streamlit pour la gestion des utilisateurs
def page_accueil():
    st.title("Accueil - Connexion et Création de Compte Utilisateur")

    # Sélectionner l'action souhaitée : Se connecter ou Créer un compte
    action = st.radio("Choisissez une action :", ("Se connecter", "Créer un compte"))

    # Initialisation du DAO et du Service Utilisateur
    utilisateur_dao = UtilisateurDAO()  # Utilisation d'une instance réelle de DAO
    utilisateur_service = UtilisateurService(utilisateur=utilisateur_dao)

    if action == "Créer un compte":
        st.header("Création de Compte Utilisateur")

        # Champs d'entrée pour l'utilisateur
        nom = st.text_input("Nom")
        prenom = st.text_input("Prénom")
        pseudo = st.text_input("Pseudo")
        adresse_mail = st.text_input("Adresse Mail")
        mdp = st.text_input("Mot de Passe", type="password")
        langue = st.selectbox("Langue", ["français", "anglais", "espagnol"])

        # Lorsque l'utilisateur clique sur "Créer un compte"
        if st.button("Créer un compte"):
            if not (nom and prenom and pseudo and adresse_mail and mdp):
                st.error("Veuillez remplir tous les champs obligatoires.")
            else:
                # Appeler la méthode du service pour créer un compte
                resultat = utilisateur_service.creer_compte(
                    nom=nom,
                    prenom=prenom,
                    pseudo=pseudo,
                    adresse_mail=adresse_mail,
                    mdp=mdp,
                    langue=langue,
                )

                # Vérifier le résultat
                if isinstance(resultat, dict) and "error" in resultat:
                    st.error(f"Erreur : {resultat.get('error')}")
                else:
                    st.success(f"Compte créé avec succès pour {resultat.pseudo}.")

    elif action == "Se connecter":
        st.header("Connexion Utilisateur")

        # Champs de connexion
        pseudo = st.text_input("Pseudo")
        mdp = st.text_input("Mot de Passe", type="password")

        if st.button("Se connecter"):
            if not (pseudo and mdp):
                st.error("Veuillez entrer votre pseudo et mot de passe.")
            else:
                try:
                    # Tenter de se connecter avec les informations fournies
                    message = utilisateur_service.se_connecter(pseudo=pseudo, mdp=mdp)
                    st.success(message)
                except ValueError as e:
                    st.error(str(e))

if __name__ == "__main__":
    page_accueil()
