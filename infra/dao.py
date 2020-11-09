from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider


class dao_factory:
    def __init__(self, db_type="cassandra"):
        self.__db_type = db_type
        self.__session = None

    def get_session(self):
        if self.__db_type == "cassandra":
            self.__auth_provider = PlainTextAuthProvider(
                username="cassandra", password="cassandra"
            )
            self.__cluster = Cluster(
                ["0.0.0.0"], port="9042", auth_provider=self.__auth_provider
            )
            self.__session = self.__cluster.connect()
            self.create_keyspace()

        return self.__session

    def create_keyspace(self):

        query = """
				CREATE KEYSPACE IF NOT EXISTS reviews_db
				WITH REPLICATION = { 
				'class' : 'SimpleStrategy', 
				'replication_factor' : 2
				};
				"""
        self.__session.execute(query)
        self.__session.set_keyspace("reviews_db")
