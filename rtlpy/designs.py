##########################################################################
# A module in the library to hold all of the classes necessary for design#
#   creation and some functions to manipulate them                       #
# Copyright (C) 2022, Benjamin Davis                                     #
#                                                                        #
# This program is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# This program is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <https://www.gnu.org/licenses/>. #
##########################################################################

from abc import ABC
from enum import Enum
from typing import Tuple, Union

##########################################################################
# Helper functions
##########################################################################
def _str2int(val:str) -> int:
  if (not isinstance(val, str)) :
    raise TypeError("Function _str2int takes one argument that must be type: str")
  
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

##########################################################################
# Base Classes
##########################################################################
class _named_design (ABC) :

  def __init__(self, name:str) :
    self.name = name

  @property
  def name(self) -> str :
    """The name of the design element
    """
    return self._name

  @name.setter
  def name(self, val: str) -> None :
    if (not isinstance(val, str)) :
      raise TypeError(f"{type(self)}.name must be str")
    else :
      self._name = val

class _wide_design (ABC) :
  def __init__(self, width:int) :
    self.width = width

  @property
  def width(self) -> int :
    """The width of the design element
    """
    return self._width
  
  @width.setter
  def width(self, val: int) -> None :
    if (not isinstance(val, int)) :
      raise TypeError(f"{type(self)}.width must be int")
    else :
      self._width = val

##########################################################################
# Memory Classes
##########################################################################

class Field (_named_design, _wide_design):
  def __init__(self, name:str, access:AccessType, lsb_pos:int, width:int=1, volatile:bool=False, reset:Union[int, str]=0) :
    self.name = name
    self.access = access
    self.lsb_pos = lsb_pos
    self.width = width
    self.volatile = volatile
    self.reset = reset

  @property
  def access(self) -> AccessType :
    """The access of the design element
    """
    return self._access

  @access.setter
  def access(self, val: AccessType) -> None :
    if (not isinstance(val, AccessType)) :
      raise TypeError(f"{type(self)}.access must be AccessType")
    else :
      self._access = val

  @property
  def lsb_pos(self) -> int :
    """The lsb_pos of the design element
    """
    return self._lsb_pos

  @lsb_pos.setter
  def lsb_pos(self, val: int) -> None :
    if (not isinstance(val, int)) :
      raise TypeError(f"{type(self)}.lsb_pos must be int")
    else :
      self._lsb_pos = val

  def msb_pos(self) -> int :
    """The position of the field MSB

    Returns:
        int: The MSB offset (zero indexed)
    """
    return self.lsb_pos + self.width - 1

  @property
  def volatile(self) -> bool :
    """The volatile of the design element
    """
    return self._volatile

  @volatile.setter
  def volatile(self, val: bool) -> None :
    if (not isinstance(val, bool)) :
      raise TypeError(f"{type(self)}.volatile must be bool")
    else :
      self._volatile = val

  @property
  def reset(self) -> Union[int, str] :
    """The reset of the design element
    """
    return self._reset

  @reset.setter
  def reset(self, val: Union[int, str]) -> None :
    if (val is None) :
      self._reset = 0
    elif (isinstance(val, str)) :
      self._reset = _str2int(val)
    elif (not isinstance(val, int)) :
      raise TypeError(f"{type(self)}.reset must be int")
    else :
      self._reset = val


class Register (_named_design):
  def __init__(self, name:str, offset: Union[int, str]) :
    self.name   = name
    self.offset = offset
    self.flds   = []

  @property
  def offset(self) -> Union[int, str] :
    """The offset of the design element
    """
    return self._offset
  
  @offset.setter
  def offset(self, val: Union[int, str]) -> None :
    if (val is None) :
      self._offset = 0
    elif (isinstance(val, str)) :
      self._offset = _str2int(val)
    elif (not isinstance(val, int)) :
      raise TypeError(f"{type(self)}.offset must be Union[int, str]")
    else :
      self._offset = val

  def msb_pos(self) -> int :
    """The position of the MSB of a field in the register

    Returns:
        int: The position of the register MSB (zero indexed)
    """
    reg_msb = 0

    for f in self.flds :
      if (f.msb_pos() > reg_msb) :
        reg_msb = f.msb_pos()

    return reg_msb

  def has_writable_fields(self) -> bool :
    """Determines if the register has writable fields

    Returns:
        bool: True if the register has writable fields, false otherwise
    """
    for f in self.flds :
      if f.access in [AccessType.READ_WRITE, AccessType.WRITE_CLEARS, AccessType.WRITE_ONE_CLEARS, AccessType.WRITE_ZERO_CLEARS, AccessType.WRITE_READ_CLEARS] :
        return True
    return False

  def get_flds(self) -> list[Field] :
    """Returns a list of the fields in the register

    Returns:
        list[Field]: The fields in the register
    """
    return self.flds

  def add_fld(self, fld:Field) -> None :
    """Adds the given field to the register

    Args:
        fld (Field): The field to add to the register

    Raises:
        ValueError: Raised when the field overlaps with or shares a name with an existing field
    """
    fld_msb = fld.msb_pos()
    fld_lsb = fld.lsb_pos

    for f in self.flds :
      if (_overlaps((fld_lsb, fld_msb), (f.lsb_pos, f.msb_pos()))):
        raise ValueError(f"Can't add field named {fld.name} to register named {self.name}. Overlaps with existing field (named {f.name}).")
      if (fld.name == f.name) :
        raise ValueError(f"Cant add field named {fld.name} to register named {self.name}. A field of that name already exists.")

    self.flds.append(fld)

  def append_fld(self, fld:Field) -> int :
    """Appends a field to the register

    Args:
        fld (Field): The field to append

    Returns:
        int: The lsb_pos of the added field
    """

    fld.lsb_pos = self.msb_pos() + 1
    self.flds.append(fld)

    return fld.lsb_pos

class AddressBlock (_named_design) :
  def __init__(self, name:str) :
    raise NotImplementedError("AddressBlock class Not Implemented")


class MemoryMap :
  def __init__(self) :
    raise NotImplementedError("MemoryMap class Not Implemented")

##########################################################################
# Design Classes
##########################################################################
class Parameter :
  def __init__(self) :
    raise NotImplementedError("Parameter class Not Implemented")


class Port :
  def __init__(self) :
    raise NotImplementedError("Port class Not Implemented")


class Module :
  def __init__(self) :
    raise NotImplementedError("Module class Not Implemented")