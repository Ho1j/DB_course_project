from pymysql import connect
from pymysql.err import OperationalError

class DBContextManager:
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
            print(f"Database connection error: {err.args}")
            return None
        except Exception as err:
            print(f"Unexpected error: {err}")
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type:
                print(f"Exception type: {exc_type}")
                print(f"Exception value: {exc_val}")
                print(f"Traceback: {exc_tb}")
                if self.conn:
                    self.conn.rollback()
            else:
                if self.conn:
                    self.conn.commit()
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
        return exc_type is None
