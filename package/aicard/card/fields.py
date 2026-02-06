from datetime import datetime

class Field:
    def set(self, value: str): raise Exception("Cannot set to abstract Field")
    def get(self): raise Exception("Cannot get from abstract Field")

class ShortText(Field):
    def __init__(self, description: str=""):
        self.__contents = ""
        self.description = description
    def set(self, value):
        if isinstance(value, Field): value = value.get()
        self.__contents = value
    def get(self):
        return self.__contents
    def __bool__(self):
        return bool(self.__contents)
    def __html__(self):
        return {"value": self.__contents if self.__contents else "", "description": self.description, "type": "short text"}

class LongText(Field):
    def __init__(self, description: str="", technical_nature: bool=False):
        self.__contents = ""
        self.description = description
        self.technical_nature = technical_nature
    def set(self, value):
        if isinstance(value, Field): value = value.get()
        self.__contents = value
    def get(self):
        return self.__contents
    def __bool__(self):
        return bool(self.__contents)
    def __html__(self):
        return {"value": self.__contents if self.__contents else "", "description": self.description, "type": "long text"}

class Options(Field):
    def __init__(self, options: list[str], description: str=""):
        self.__options = options  # leave as a list
        self.__contents = None
        self.description = description
    def set(self, value):
        if isinstance(value, Field): value = value.get()
        if not value: value = None
        if value not in self.__options: value = None#raise Exception(f"Value {value} is not one among available options: {','.join(self.__options)}")
        self.__contents = value
    def options(self):
        return self.__options
    def get(self):
        return self.__contents
    def __bool__(self):
        return self.__contents != None
    def __html__(self):
        return {"value": self.__contents if self.__contents else "", "description": self.description, "type": "list:"+",".join(self.__options)}
    
class Date(Field):
    def __init__(self, description: str=""):
        self.__contents = ""
        self.description = description
        self.__format = "%Y-%m-%d"
    def set(self, value):
        if isinstance(value, Field): value = value.get()
        assert (not value) or datetime.strptime(value, self.__format), f"Date format must be {self.__format}"
        self.__contents = value
    def get(self):
        return self.__contents
    def __bool__(self):
        return bool(self.__contents)
    def __html__(self):
        return {"value": self.__contents if self.__contents else "", "description": self.description, "type": "date"}

# Ollama pattern issue: https://github.com/ollama/ollama/issues/10591
class Pattern(Field):
    def __init__(self, regex: str, description: str=""):
        self.__pattern = regex
        self.__contents = ''
        self.description = description
    def set(self, value):
        if isinstance(value, Field): value = value.get()
        self.__contents = value
    def pattern(self):
        return self.__pattern
    def get(self):
        return self.__contents
    def __bool__(self):
        return bool(self.__contents)
    def __html__(self):
        return {"value": self.__contents if self.__contents else "", "description": self.description, "type": "long text"}