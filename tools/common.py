import enum


class Formattype(enum.Enum):
    """This is an indication on the format of the value. bit: 1-bit or more
    (vector) bits unsigned integer, byte: 8-bit signed integer, shortint:
    16-bit signed integer, int: 32-bit signed integer, longint: 64-bit
    signed integer, shortreal: 32-bit signed floating point number, real:
    64-bit signed floating point number, string: textual information.
    """
    BIT = 'bit'
    BYTE = 'byte'
    SHORTINT = 'shortint'
    INT = 'int'
    LONGINT = 'longint'
    SHORTREAL = 'shortreal'
    REAL = 'real'
    STRING = 'string'


class Signtype(enum.Enum):
    """This is an indication of the signedness of the value.
    """
    SIGNED = 'signed'
    UNSIGNED = 'unsigned'


class Delayvalueunittype(enum.Enum):
    """Indicates legal units for delay values.
    """
    PS = 'ps'
    NS = 'ns'
