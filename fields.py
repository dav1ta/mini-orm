class Field:
    lazy = False

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def sql_type(self):
        raise NotImplementedError


class Char(Field):
    def sql_type(self):
        return "VARCHAR"


class Int(Field):
    def sql_type(self):
        return "INTEGER"


class Boolean(Field):
    def sql_type(self):
        return "BOOLEAN"


class Text(Field):
    def sql_type(self):
        return "TEXT"


class ForeignKey(Field):
    def __init__(self, related_model):
        self.related_model = related_model

    def sql_type(self):
        return "INTEGER"


class Many2one(ForeignKey):
    pass


class One2many(Field):
    lazy = True

    def __init__(self, related_model, related_field_name):
        self.related_model = related_model
        self.related_field_name = related_field_name

    def sql_type(self):
        return "INTEGER"

