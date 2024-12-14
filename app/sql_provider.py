import os
from string import Template


class SQL_Provider:
    def __init__(self, sql_path: str):
        self._scripts = {}
        for file in os.listdir(sql_path):
            full_file = f'{sql_path}/{file}'
            if not full_file.endswith('.sql'):
                continue
            template = Template(open(full_file, "r").read())
            self._scripts[file] = template
        pass

    def get_sql(self, template_name: str, **params)->str:
        return self._scripts[template_name].substitute(**params)