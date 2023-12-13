class Constants:

    @classmethod
    def list_all(cls):
        _cls = cls()
        return [
            getattr(cls, attr) for attr in dir(_cls) if not callable(getattr(_cls, attr)) and not attr.startswith("__")
        ]


class Types(Constants):
    BOOLEAN = "bool"
    INTEGER = "int"
    FLOAT = "float"
    STRING = "str"
    DATE = "date"
    DATETIME = "datetime"
    LIST = "list"
    DICTIONARY = "dict"
    NONETYPE = "NoneType"
    VARIABLE = "variable"


class Operators(Constants):
    EQUAL = "="
    DOUBLE_EQUAL = "=="
    NOT_EQUAL = "!="
    LESS_THAN = "<"
    LESS_THAN_OR_EQUAL = "<="
    GREATER_THAN = ">"
    GREATER_THAN_OR_EQUAL = ">="
    IN = "in"
    NOT_IN = "not in"
