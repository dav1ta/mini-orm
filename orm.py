import sqlite3
from fields import Int, Field


class ConnectionPool:
    def __init__(self):
        self.conn = None

    def get_connection(self):
        if not self.conn:
            self.conn = sqlite3.connect("my_database.sqlite3")
        return self.conn

    def close_connection(self):
        if self.conn:
            self.conn.close()
            self.conn = None


connection_pool = ConnectionPool()


def execute_query(query):
    conn = connection_pool.get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


def execute_insert_query(query):
    conn = connection_pool.get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    return cursor.lastrowid


class ModelMeta(type):
    def __new__(cls, name, bases, dct):
        fields = {k: v for k, v in dct.items() if isinstance(v, Field)}
        fields['id'] = Int()
        dct["_fields"] = fields
        print(fields)
        dct["_instances"] = []
        table_name = dct.get("_name", name.lower())
        dct["_name"] = table_name.replace(".", "_")
        new_class = super().__new__(cls, name, bases, dct)
        if not name == "Model":
            new_class.create_table_if_not_exists()
        print(fields)
        return new_class


class Model(metaclass=ModelMeta):

    _classes= {}
    # id = Int()

    def __init__(self, *args, **kwargs):
        for field, value in zip(self._fields.keys(), args):
            setattr(self, field, value)

        for field, value in kwargs.items():
            setattr(self, field, value)

        self.__class__._instances.append(self)
        self._classes[self.__class__._name.lower()] = self.__class__

    def save(self):
        filtered_fields = {k: v for k, v in self._fields.items() if not v.lazy}
        field_names = ", ".join(filtered_fields.keys())
        values = ", ".join(repr(getattr(self, f)) for f in filtered_fields.keys())
        if self.id:
            query = f"UPDATE {self.__class__._name} SET {', '.join(f'{field} = {repr(getattr(self, field))}' for field in filtered_fields.keys())} WHERE id = {self.id};"
            execute_query(query)
            return self
        else:

            query = f"INSERT INTO {self.__class__._name} ({field_names}) VALUES ({values});"
            print(query)
            last_id = execute_insert_query(query)
            self.id = last_id
            return self

    @classmethod
    def create_table_if_not_exists(cls):
        id_query = "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        query = f'CREATE TABLE IF NOT EXISTS {cls._name} ({id_query +", ".join(f"{field_name} {field.sql_type()}" for field_name, field in cls._fields.items() if field_name!="id")});'
        print(query)

        rows = execute_query(query)
        print("Executing SQL:", query)
        print(rows)

    def __getattribute__(self, key):
        fields = object.__getattribute__(self, "_fields")
        if key in fields and fields[key].lazy:
            # Cache
            cache_key = f"_{key}_cache"
            if not hasattr(self, cache_key):
                related_model = fields[key].related_model
                related_field_name =fields[key].related_field_name 
                print(self._classes)
                related_model = self._classes.get(related_model.lower())
                related_instances = related_model.search(
                    [(related_field_name, "=", object.__getattribute__(self, "id"))]
                )
                setattr(self, cache_key, related_instances)
            return object.__getattribute__(self, cache_key)
        else:
            return object.__getattribute__(self, key)

    @classmethod
    def search(cls, conditions):
        condition_strs = []
        for condition in conditions:
            field, operator, value = condition
            if isinstance(value, str):
                value = f"'{value}'"
            if operator in ("=", "!=", ">", "<", ">=", "<="):
                condition_strs.append(f"{field} {operator} {value}")
            else:
                raise ValueError(f"Invalid operator: {operator}")
        print(cls._fields)
        filtered_fields = {k: v for k, v in cls._fields.items() if not v.lazy}
        query = f"SELECT {', '.join(filtered_fields.keys())} FROM {cls._name} WHERE {' AND '.join(condition_strs)};"

        print("Executing SQL:", query)

        rows = execute_query(query)
        results = []
        for row in rows:
            instance_data = {
                field: row[i] for i, field in enumerate(filtered_fields.keys())
            }
            results.append(cls(**instance_data))

        return results
