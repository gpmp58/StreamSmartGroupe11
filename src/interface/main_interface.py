import streamlit as st
import interface_connexion as connexion  # Importer l'interface pour la connexion/utilisateur
import interface_film as film  # Importer l'interface pour les films

# Initialiser st.session_state si ce n'est pas déjà fait
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['user'] = None

# Interface principale avec menu de navigation déroulant dans la barre latérale
def main():
    # Créer un menu de navigation dans la barre latérale
    st.sidebar.title("Navigation")
    
    # Définir les options du menu en fonction de l'état de connexion
    if st.session_state['logged_in']:
        options = ("Accueil", "Recherche de Films")
        default_index = 1  # "Recherche de Films" sera sélectionné par défaut
    else:
        options = ("Accueil", "Se connecter", "Créer un compte")
        default_index = 0  # "Accueil" sera sélectionné par défaut
    
    # Créer le selectbox avec l'index par défaut
    option = st.sidebar.selectbox("Choisissez une page :", options, index=default_index)
    
    # Affichage des pages selon le choix fait dans le menu de navigation
    if option == "Accueil":
        # Page d'accueil générale de l'application
        st.title("Bienvenue sur notre application 🎬")
        if st.session_state['logged_in'] and st.session_state['user']:
            pseudo = st.session_state['user']['pseudo'] if isinstance(st.session_state['user'], dict) else st.session_state['user']
            st.write(f"Bonjour, {pseudo} !")
            st.markdown("""
                Vous êtes connecté. Vous pouvez :
                - Rechercher et afficher des informations sur des films.
            """)
        else:
            st.markdown("""
                Cette application vous permet de :
                - Créer un compte ou vous connecter.
                - Rechercher et afficher des informations sur des films.
                Utilisez le menu de navigation à gauche pour commencer.
            """)
    
    elif option == "Se connecter":
        connexion.page_connexion()  # Appelle la fonction `page_connexion` d'interface_connexion.py
    
    elif option == "Créer un compte":
        connexion.page_creation_compte_wrapper()  # Appelle la fonction `page_creation_compte_wrapper` d'interface_connexion.py
    
    elif option == "Recherche de Films":
        if st.session_state['logged_in']:
            film.page()  # Appelle la fonction `page` d'interface_film.py
        else:
            st.warning("Veuillez vous connecter pour accéder à cette section.")
            connexion.page_connexion()
    
    # Ajouter un bouton de déconnexion dans la barre latérale si l'utilisateur est connecté
    if st.session_state['logged_in']:
        if st.sidebar.button("Déconnexion"):
            # Réinitialiser l'état de connexion
            st.session_state['logged_in'] = False
            st.session_state['user'] = None
            
            # Réinitialiser les recherches
            st.session_state.pop('search_query', None)
            st.session_state.pop('search_results', None)
    
            st.sidebar.success("Déconnecté avec succès.")
    
            # Recharger l'application pour rediriger vers l'accueil
            st.rerun()
    
    # Optionnel : Afficher l'état de la session pour le débogage
    st.sidebar.markdown("---")
    st.sidebar.write("**État de la Session:**")
    st.sidebar.write(f"Connecté : {st.session_state['logged_in']}")
    st.sidebar.write(f"Utilisateur : {st.session_state['user']}")

if __name__ == "__main__":
    main()
