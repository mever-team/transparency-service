from datetime import datetime
import re

class Field:
    def set(self, value: str): raise Exception("Cannot set to abstract Field")
    def get(self): raise Exception("Cannot get from abstract Field")

def _clean_html(text: str):
    return re.sub(r"<[^>]+>", "", text) if text else ""

class ShortText(Field):
    def __init__(self, description: str="", technical_nature: bool=False, is_simple: bool=False, is_refinable: bool=False):
        self.__contents = ""
        self.description = description
        self.technical_nature = technical_nature
        self.is_simple = is_simple
        self.is_refinable = is_refinable
    def set(self, value):
        if isinstance(value, Field): value = value.get()
        self.__contents = _clean_html(value)
    def get(self):
        return _clean_html(self.__contents)
    def __bool__(self):
        return bool(self.__contents)
    def __html__(self):
        return {"value": _clean_html(self.__contents) if self.__contents else "", "description": self.description, "type": "short text"}

class LongText(Field):
    def __init__(self, description: str="", technical_nature: bool=False, is_simple: bool=False, is_refinable: bool=False):
        self.__contents = ""
        self.description = description
        self.technical_nature = technical_nature
        self.is_simple = is_simple
        self.is_refinable = is_refinable
    def set(self, value):
        if isinstance(value, Field): value = value.get()
        self.__contents = _clean_html(value)
    def get(self):
        return _clean_html(self.__contents)
    def __bool__(self):
        return bool(self.__contents)
    def __html__(self):
        return {"value": _clean_html(self.__contents) if self.__contents else "", "description": self.description, "type": "long text"}

class Options(Field):
    def __init__(self, options: list[str], description: str="", is_simple: bool=False):
        self.__options = options  # leave as a list
        self.__contents = ""
        self.description = description
        self.is_simple = is_simple
        self.is_refinable = False
    def set(self, value):
        if isinstance(value, Field): value = value.get()
        self.__contents = _clean_html(value)
    def options(self):
        return self.__options
    def get(self):
        return _clean_html(self.__contents)
    def __bool__(self):
        return bool(self.__contents)
    def __html__(self):
        return {"value": _clean_html(self.__contents) if self.__contents else "", "description": self.description, "type": "list:"+",".join(self.__options)}
    
class Date(Field):
    def __init__(self, description: str="", is_simple: bool=False):
        self.__contents = ""
        self.description = description
        self.__format = "%Y-%m-%d"
        self.is_simple = is_simple
        self.is_refinable = False
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
        return {"value": self.__contents if self.__contents else "", "description": self.description, "type": "date"}

# Ollama pattern issue: https://github.com/ollama/ollama/issues/10591
class Pattern(Field):
    def __init__(self, regex: str, description: str="", is_simple: bool=False):
        self.__pattern = regex
        self.__contents = ''
        self.description = description
        self.is_simple = is_simple
        self.is_refinable = False
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