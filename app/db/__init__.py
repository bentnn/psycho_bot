class DBConfs:
    engine = None
    db_session = None
    db_connection = None

    def set_engine(self, engine):
        self.engine = engine

    def set_session(self, new_session):
        self.db_session = new_session

    def set_connection(self, conn):
        self.db_connection = conn



db_confs = DBConfs()
