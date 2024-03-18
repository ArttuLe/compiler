from dataclasses import dataclass


@dataclass
class Type:
    ...

@dataclass
class Int(Type):
    def __str__(self):
        return "Int"

@dataclass
class Bool(Type):
    def __str__(self):
        return "Bool"
    
@dataclass
class Unit(Type):
    def __str__(self):
        return "None"
    
@dataclass
class FunType(Type):
    def __init__(self, param_types, return_type):
        self.param_types = param_types
        self.return_type = return_type

    def __str__(self):
        param_types_str = ", ".join(str(param) for param in self.param_types)
        return f"({param_types_str}) -> {self.return_type}"

@dataclass
class SymTab:
    def __init__(self, parent=None):
        self.locals = {}
        # Pass the parent when going to a further scope from top-level
        self.parent = parent

    def define(self, name, value):
        self.locals[name] = value

    def lookup(self, name):
        if name in self.locals:
            return self.locals[name]
        elif self.parent:
            return self.parent.lookup(name)
        else:
            raise NameError(f"Name '{name}' not defined")