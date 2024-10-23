import hashlib
import secrets


import hashlib
import secrets

def hash_mdp(password: str, sel: str = None) -> tuple:
    """
    Hachage du mot de passe avec un sel aléatoire.

    Parameters:
    ------------
    password : str
        Le mot de passe à hacher.
    sel : str, optionnel
        Le sel utilisé pour hacher le mot de passe. Si aucun sel n'est fourni,
        un nouveau sel sera généré.

    Returns:
    ---------
    tuple : (str, str)
        Retourne le hash du mot de passe et le sel utilisé pour le hachage.
    """
    if sel is None:
        # Générer un sel de 16 octets en utilisant le module secrets
        sel = secrets.token_hex(16)

    # Encoder le mot de passe et le sel en octets
    password_bytes = password.encode("utf-8")
    sel_bytes = sel.encode("utf-8")

    # Combiner le mot de passe et le sel
    combined = password_bytes + sel_bytes

    # Hacher le mot de passe avec sha256
    hash_object = hashlib.sha256(combined)
    password_hash = hash_object.hexdigest()
    
    return password_hash, sel




def verify_mdp(stored_mdp_hash: str, provided_mdp: str, sel: str) -> bool:
    """
    Vérifie si le mot de passe fourni correspond au hash stocké.

    Parameters:
    ------------
    stored_mdp_hash : str
        Le hash du mot de passe stocké.
    provided_mdp : str
        Le mot de passe fourni par l'utilisateur à vérifier.
    sel : str
        Le sel utilisé pour générer le hash du mot de passe.

    Returns:
    ---------
    bool
        True si le mot de passe est correct, sinon False.
    """
    # Hacher le mot de passe fourni avec le même sel
    provided_mdp_hash, _ = hash_mdp(provided_mdp, sel)
    
    # Comparer le hash fourni avec le hash stocké
    return provided_mdp_hash == stored_mdp_hash

