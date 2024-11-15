import streamlit as st

# Configuration de la page principale
st.set_page_config(page_title="Application Multi-Page", layout="wide")

# Initialisation de l'état de session si nécessaire
if 'pseudo' not in st.session_state:
    st.session_state['pseudo'] = None


# Fonction utilitaire pour afficher la barre latérale
def afficher_etat_connexion():
    with st.sidebar:
        if st.session_state['pseudo']:
            st.write(f"**Utilisateur :** {st.session_state['pseudo']}")
            st.write("**État : Connecté**")
        else:
            st.write("**Utilisateur :** Non connecté")
            st.write("**État : Déconnecté")

# Appel de la fonction pour afficher la barre latérale
afficher_etat_connexion()

st.title("Bienvenue dans l'Application Multi-Page")
st.write("Sélectionnez une option ci-dessous pour naviguer vers la page correspondante.")

st.markdown("---")  # Ligne de séparation

# Affichage si l'utilisateur n'est pas connecté
if not st.session_state['pseudo']:
    st.write("Vous n'êtes pas connecté.")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Connexion"):
            st.switch_page("pages/interface_connexion.py")

    with col2:
        if st.button("Création de Compte"):
            st.switch_page("pages/interface_creation_compte.py")
