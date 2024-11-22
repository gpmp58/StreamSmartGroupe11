# État de session global pour l'application
session_state = {"pseudo": None, "id_utilisateur": None}


def set_session_state(**kwargs):
    """
    Met à jour les données dans le session_state global.
    Les clés et valeurs sont passées en tant que paramètres nommés.

    Exemple d'utilisation :
    set_session_state(pseudo="JohnDoe", id_utilisateur=123)
    """
    global session_state
    for key, value in kwargs.items():
        if key in session_state:
            session_state[key] = value


def get_session_state():
    """
    Récupère une copie du session_state global.
    Retourne le dictionnaire actuel de l'état de session.
    """
    return session_state.copy()


def clear_session_state():
    """
    Réinitialise le session_state global à son état initial.
    """
    global session_state
    session_state = {"pseudo": None, "id_utilisateur": None}
