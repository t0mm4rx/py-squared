"""Pysquared module."""
from dataclasses import dataclass
from .tokenization import Token, TokenTypes

@dataclass(kw_only=True)
class PrimitiveType:
    """Primitive type."""
    type_c_name:    str
    type_size:      int

PRIMITIVE_TYPES: dict[str, str] = {
    "byte": PrimitiveType(type_c_name="unsigned char", type_size=1),
    "int": PrimitiveType(type_c_name="int", type_size=4),
    "int16": PrimitiveType(type_c_name="int", type_size=4),
    "int32": PrimitiveType(type_c_name="long int", type_size=8),
}
