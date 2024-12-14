from pymysql import connect
from pymysql.err import OperationalError


class DB_Context_Manager:
    def __init__(self, config: dict):
        self.config = config
        self.conn = None
        self.cursor = None

    def __enter__(self):
        try:
            self.conn = connect(**self.config)
            self.cursor = self.conn.cursor()
            return self.cursor
        except OperationalError as err:
            print(err.args)
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(exc_type)
            print(exc_val)
            print(exc_tb)
        if self.conn and self.cursor:
            if exc_type:
                self.conn.rollback()
            else:
                self.conn.commit()
            self.conn.close()
            self.cursor.close()
        return True

