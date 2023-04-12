"""Module that holds memory mapping and utilities."""
from dataclasses import dataclass

class VariableNameAlreadyUsed(Exception):
    """Raised when a variable is not found."""

@dataclass
class Variable:
    """Hold variable information."""
    name:   str
    type:   str
    index:  int

variables: list[Variable] = []
last_index = 0

def get_variable(name: str | None = None, index: int | None = None) -> Variable | None:
    """Get variable from name or index."""
    if name is not None:
        finds = [x for x in variables if x.name == name]
        if len(finds) == 1:
            return finds[0]
    if index is not None:
        finds = [x for x in variables if x.index == index]
        if len(finds) == 1:
            return finds[0]
    return None

def register_variable(name: str, type: str):
    """Register a new variable."""
    global last_index
    if get_variable(name=name) is not None:
        raise VariableNameAlreadyUsed()
    variables.append(Variable(
        name=name,
        type=type,
        index=last_index,
    ))
    last_index += 1
    return last_index - 1
