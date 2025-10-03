class Field:
    def set(self, value: str): raise Exception("Cannot set to abstract Field")
    def get(self): raise Exception("Cannot get from abstract Field")

class ShortText(Field):
    def __init__(self, description: str=""):
        self.__contents = ""
        self.description = description
    def set(self, value): self.__contents = value
    def get(self): return self.__contents

class LongText(Field):
    def __init__(self, description: str=""):
        self.__contents = ""
        self.description = description
    def set(self, value): self.__contents = value
    def get(self): return self.__contents

class Options(Field):
    def __init__(self, options: list[str], description: str=""):
        self.__options = options  # leave as a list
        self.__contents = options[0]
    def set(self, value):
        if value not in self.__options: raise Exception(f"Value {value} is not one among available options: {','.join(self.__options)}")
        self.__contents = value
    def get(self): return self.__contents