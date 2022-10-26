from __future__ import annotations
from typing import Any, Iterator, Union, Tuple
from attrs import define, field, validators
from enum import Enum

##########################################################################
# Helper functions
##########################################################################
def _val2int(val:Union[str, int]) -> int:
  if (isinstance(val, int)) :
    return val

  if (not isinstance(val, str)) :
    raise TypeError("Function _val2int takes one argument that must be type: str or int")
  
  if (val.startswith("0x")) :
    return int(val, base=16)
  elif (val.startswith("x")) :
    return int("0"+val, base=16)
  else :
    return int(val)

def _overlaps(range1:Tuple[int, int], range2:Tuple[int, int]) -> bool :
  """Determines if the two ranges overlap

  Args:
      range1 (Tuple[int, int]): The first range
      range2 (Tuple[int, int]): The second range

  Returns:
      bool: True if the ranges overlap, otherwise false
  """
  if (range1[0] < range2[0] and range1[1] > range2[0]) : # Overlaps low point of range
    return True
  if (range1[0] < range2[1] and range1[1] > range2[1]) : # Overlaps high point of range
    return True
  if (range1[0] > range2[0] and range1[1] < range2[1]) : # Inside case
    return True

  return False

##########################################################################
# ENUMS
##########################################################################
class AccessType (Enum) :
  READ_ONLY         = "RO"
  READ_WRITE        = "RW"
  READ_CLEARS       = "RC"
  WRITE_READ_CLEARS = "WRC"
  WRITE_CLEARS      = "WC"
  WRITE_ONE_CLEARS  = "W1C"
  WRITE_ZERO_CLEARS = "W0C"

def _conv2access(val:Union[str, AccessType]) -> AccessType :
  if (isinstance(val, AccessType)) : return val
  if (isinstance(val, str)) : return AccessType[val.upper()]
  raise ValueError("Function _conv2access takes a single argument of type str or AccessType")

##########################################################################
# Memory Classes
##########################################################################

@define
class Field :
  """Class to represent a field of a Register
  """
  name    : str        = field(validator=validators.instance_of(str))
  access  : AccessType = field(validator=validators.instance_of(AccessType), converter=_conv2access)
  lsb_pos : int        = field(validator=validators.instance_of(int))
  width   : int        = field(validator=validators.instance_of(int), default=1)
  volatile: bool       = field(validator=validators.instance_of(bool), default=False)
  reset   : int        = field(validator=validators.instance_of((int, str)), default=0, converter=_val2int)

  def get_msb_pos(self) -> int : 
    """
    Returns:
        int: The position of the msb (zero indexed) 
    """
    return self.lsb_pos + self.width - 1

  def overlaps(self, fld:Field) -> bool :
    return _overlaps((self.lsb_pos, self.get_msb_pos()), (fld.lsb_pos, fld.get_msb_pos()))


@define
class Register :
  """Class to represent a Register from a register bank
  """
  name: str = field(validator=validators.instance_of(str))
  offset: int = field(validator=validators.instance_of(int))
  _flds: list[Field] = field(init=False, factory=list)
  
  def add(self, fld:Field) -> None :
    """Adds a field to the register at the provided fields specified lsb_pos

    Args:
        fld (Field): The field to add to the register

    Raises:
        ValueError: If the field's size overlaps an existing field
        ValueError: If the field shares a name with an existing field
    """
    new_idx = None
    for idx, val in enumerate(self._flds) :
      if fld.overlaps(val) :
        raise ValueError(f"Can't add field named {fld.name} to register named {self.name}. Overlaps with existing field (named {val.name}).")
      if fld.name == self.name :
        raise ValueError(f"Cant add field named {fld.name} to register named {self.name}. A field of that name already exists.")

      if (val.get_msb_pos() > fld.lsb_pos) :
        new_idx = idx + 1

    self._flds.insert(new_idx, fld)

  def append(self, fld:Field) -> int :
    """Adds a field to the end of the existing register

    Args:
        fld (Field): The field to add to the end of the register

    Raises:
        ValueError: If the field shares a name with an existing field

    Returns:
        int: The new lsb_pos of the field
    """
    if sum([(1 if fld.name == f.name else 0) for f in self._flds]) > 0 :
      raise ValueError(f"Cant add field named {fld.name} to register named {self.name}. A field of that name already exists.")

    if (len(self._flds) == 0) :
      fld.lsb_pos = 0
    else :
      fld.lsb_pos = self._flds[-1].get_msb_pos() + 1
    self._flds.append(fld)
    return fld.lsb_pos

  def get(self, i:int) -> Field :
    return self._flds[i]

  def size(self) -> int :
    """The size of the register in bits

    Returns:
        int: The size of the register
    """
    if (len(self._flds) == 0) : return 0
    return self._flds[-1].get_msb_pos()

  def __len__(self) -> int :
    return len(self._flds)

  def __iter__(self) -> Iterator[Field] :
    return self._flds.__iter__()


@define
class AddressBlock :
  """Class to represent an address block from a memory map
  """
  name: str = field(validator=validators.instance_of(str))


@define
class MemoryMap :
  """Class to represent an RTL memory map
  """
  name: str = field(validator=validators.instance_of(str))


##########################################################################
# Design Classes
##########################################################################

@define
class Port :
  """Class to represent the port in an RTL Module
  """
  name: str = field(validator=validators.instance_of(str))


@define
class Parameter :
  """Class to represent a parameter in an RTL Module
  """
  name: str = field(validator=validators.instance_of(str))


@define
class Module :
  """Class to represent the top-level definition of an RTL module
  """
  name: str = field(validator=validators.instance_of(str))