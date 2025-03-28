from src.webservice.utils.singleton import Singleton
from src.webservice.dao.db_connection import DBConnection


class ResetDatabase(metaclass=Singleton):
    """
    Reinitialisation de la base de données
    """

    def lancer(self):
        print("Ré-initialisation de la base de données")

        init_db = open("data/init_db.sql", encoding="utf-8")
        init_db_as_string = init_db.read()

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(init_db_as_string)
        except Exception as e:
            print(e)
            raise

        print("Ré-initialisation de la base de données - Terminée")

        return True


if __name__ == "__main__":
    ResetDatabase().lancer()
