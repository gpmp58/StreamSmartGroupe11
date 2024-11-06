import streamlit as st
import interface_connexion as connexion  # Importez l'interface pour la connexion/utilisateur
import interface_film as film  # Importez l'interface pour les films


# Interface principale avec menu de navigation déroulant dans la barre latérale
def main():
    # Créer un menu de navigation dans la barre latérale
    st.sidebar.title("Navigation")
    option = st.sidebar.selectbox("Choisissez une page :", ("Accueil", "Se connecter", "Recherche de Films"))

    # Affichage des pages selon le choix fait dans le menu de navigation
    if option == "Accueil":
        # Page d'accueil générale de l'application
        st.title("Bienvenue sur notre application 🎬")
        st.markdown("""
            Cette application vous permet de :
            - Créer un compte ou vous connecter.
            - Rechercher et afficher des informations sur des films.
            Utilisez le menu de navigation à gauche pour commencer.
        """)
    
    elif option == "Se connecter":
        connexion.page()  # Appelle la fonction `page()` d'interface_connexion.py
    
    elif option == "Recherche de Films":
        film.page()  # Appelle la fonction `page()` d'interface_film.py

if __name__ == "__main__":
    main()

