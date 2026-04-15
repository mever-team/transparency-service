from datetime import datetime

class Field:
    def set(self, value: str): raise Exception("Cannot set to abstract Field")
    def get(self): raise Exception("Cannot get from abstract Field")

class ShortText(Field):
    def __init__(self, description: str="", technical_nature: bool=False, in_summary: bool=False):
        self.__contents = ""
        self.description = description
        self.technical_nature = technical_nature
        self.in_summary = in_summary
    def set(self, value):
        if isinstance(value, Field): value = value.get()
        self.__contents = value
    def get(self):
        return self.__contents
    def __bool__(self):
        return bool(self.__contents)
    def __html__(self):
        return {"value": self.__contents if self.__contents else "", "description": self.description, "type": "short text", "in_summary": self.in_summary}

class LongText(Field):
    def __init__(self, description: str="", technical_nature: bool=False, in_summary: bool=False):
        self.__contents = ""
        self.description = description
        self.technical_nature = technical_nature
        self.in_summary = in_summary
    def set(self, value):
        if isinstance(value, Field): value = value.get()
        self.__contents = value
    def get(self):
        return self.__contents
    def __bool__(self):
        return bool(self.__contents)
    def __html__(self):
        return {"value": self.__contents if self.__contents else "", "description": self.description, "type": "long text", "in_summary": self.in_summary}

class Options(Field):
    def __init__(self, options: list[str], description: str="", in_summary: bool=False):
        self.__options = options  # leave as a list
        self.__contents = None
        self.description = description
        self.in_summary = in_summary
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
        return {"value": self.__contents if self.__contents else "", "description": self.description, "type": "list:"+",".join(self.__options), "in_summary": self.in_summary}
    
class Date(Field):
    def __init__(self, description: str="", in_summary: bool=False):
        self.__contents = ""
        self.description = description
        self.__format = "%Y-%m-%d"
        self.in_summary = in_summary
    def set(self, value):
        if isinstance(value, Field): value = value.get()
        try:
            datetime.strptime(value, self.__format)
            self.__contents = value
        except:
            return
    def get(self):
        return self.__contents
    def __bool__(self):
        return bool(self.__contents)
    def __html__(self):
        return {"value": self.__contents if self.__contents else "", "description": self.description, "type": "date", "in_summary": self.in_summary}

# Ollama pattern issue: https://github.com/ollama/ollama/issues/10591
class Pattern(Field):
    def __init__(self, regex: str, description: str="", in_summary: bool=False):
        self.__pattern = regex
        self.__contents = ''
        self.description = description
        self.in_summary = in_summary
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
        return {"value": self.__contents if self.__contents else "", "description": self.description, "type": "long text", "in_summary": self.in_summary}