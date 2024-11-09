import streamlit as st
import interface_connexion as connexion  # Importer l'interface pour la connexion/utilisateur
import interface_film as film  # Importer l'interface pour les films

# Configuration globale de la page


# Initialiser `st.session_state` pour suivre l'état de connexion et la page actuelle
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = "Accueil"  # Page par défaut
if 'user' not in st.session_state:
    st.session_state['user'] = None

# Fonction de la page d'accueil
def page_accueil():
    st.title("Bienvenue sur notre application 🎬")
    if st.session_state['logged_in']:
        st.write(f"Bonjour, {st.session_state.get('user', 'utilisateur')} !")
        st.markdown("Vous êtes connecté. Utilisez le menu pour accéder aux fonctionnalités.")
    else:
        st.markdown("""
            Cette application vous permet de :
            - Créer un compte ou vous connecter.
            - Rechercher et afficher des informations sur des films.
            Utilisez le menu de navigation pour commencer.
        """)

# Fonction pour se connecter
def page_connexion():
    connexion.page_connexion()  # Affiche la page de connexion

# Fonction pour créer un compte
def page_creation_compte():
    connexion.page_creation_compte_wrapper()  # Affiche la page de création de compte

# Fonction pour afficher la recherche de films
def page_recherche_film():
    film.page()  # Affiche la page de recherche de films depuis `interface_film`

# Gestion de la navigation en fonction de l'état de connexion
if st.session_state['logged_in']:
    # Pages disponibles après connexion
    navigation_options = ["Recherche de Films", "Déconnexion"]
else:
    # Pages disponibles pour les non-connectés
    navigation_options = ["Accueil", "Se connecter", "Créer un compte"]

# Menu de navigation dans la barre latérale
st.session_state['current_page'] = st.sidebar.selectbox("Navigation", navigation_options)

# Navigation vers la page sélectionnée
if st.session_state['current_page'] == "Accueil":
    page_accueil()
elif st.session_state['current_page'] == "Se connecter":
    page_connexion()
elif st.session_state['current_page'] == "Créer un compte":
    page_creation_compte()
elif st.session_state['current_page'] == "Recherche de Films":
    page_recherche_film()
elif st.session_state['current_page'] == "Déconnexion":
    # Gestion de la déconnexion
    st.session_state['logged_in'] = False
    st.session_state['user'] = None
    st.session_state['current_page'] = "Accueil"
    st.experimental_rerun()  # Recharge l'application pour revenir à la page d'accueil

# Afficher l'état de la session pour le débogage
st.sidebar.markdown("---")
st.sidebar.write("**État de la Session :**")
st.sidebar.write(f"Connecté : {st.session_state['logged_in']}")
st.sidebar.write(f"Utilisateur : {st.session_state.get('user', 'Aucun')}")
st.sidebar.write(f"Page actuelle : {st.session_state['current_page']}")
