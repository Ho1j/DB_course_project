from .db_connect import DBContextManager


def execute_and_fetch(config: dict, _sql: str):
    with DBContextManager(config) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')
        else:
            cursor.execute(_sql)
            result = cursor.fetchall()
            if result:
                schema = [item[0] for item in cursor.description]  # description is a set, here are names etc
                result_dict = [dict(zip(schema, product)) for product in result]
                return result_dict
            else:
                return None

