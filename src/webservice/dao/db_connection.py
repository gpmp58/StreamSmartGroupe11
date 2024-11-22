import os
import dotenv
import psycopg2

from psycopg2.extras import RealDictCursor


class DBConnection:
    """
    Classe de connexion à la base de données
    Elle permet de n'ouvrir qu'une seule et unique connexion
    """

    def __init__(self):
        """
                Ouverture de la connexion à la base de données PostgreSQL.
        # à verifier pour raises
                Raises:
                    psycopg2.OperationalError: Si la connexion à la base de données échoue.
        """
        dotenv.load_dotenv()

        self.__connection = psycopg2.connect(
            host=os.environ["POSTGRES_HOST"],
            port=os.environ["POSTGRES_PORT"],
            database=os.environ["POSTGRES_DATABASE"],
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
            cursor_factory=RealDictCursor,
        )

    @property
    def connection(self):
        """
        Propriété pour accéder à la connexion à la base de données.

        Returns:
            psycopg2.connection: L'objet de connexion PostgreSQL.
        """
        return self.__connection
