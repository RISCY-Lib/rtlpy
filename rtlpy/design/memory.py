##########################################################################
# Python library to help with the automatic creation of RTL              #
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

from __future__ import annotations

from typing import Optional

import logging

import dataclasses
from dataclasses import dataclass

from rtlpy.design import AccessType

import rtlpy.utils as utils


_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())


##########################################################################
# Exception Definitions
##########################################################################
class MissingDefinitionException (Exception):
  """The Exception raised when converting using a dictionary that is missing a required field"""
  pass


##########################################################################
# Component Definitions
##########################################################################
@dataclass
class Field:
  """Class which represents a Field within a Register for a MemoryMap"""

  name: str
  """Field name"""
  size: int = 1
  """Size of the field in bits"""
  access: AccessType = AccessType.READ_ONLY
  """Access Policy of the Field"""
  reset: int = 0
  """The reset value of the field"""
  volatile: bool = False
  """Whether the value of field is volatile"""
  randomizable: bool = True
  """Whether the field can be randomized"""
  reserved: bool = False
  """Whether the field is a reserved field"""

  def valid(self) -> bool:
    """Checks the Field is validly defined

    Returns:
        bool: Returns true if the Field is valid. False otherwise
    """
    ret_val = True

    if not utils.valid_name(self.name):
      _log.error(f"Field ({self.name}) has an invalid name.")
      ret_val = False
    if self.reset.bit_length() > self.size:
      _log.error(f"Field ({self.name}) reset value ({self.reset})" +
                 f" does not fit in field (size: {self.size}).")
      ret_val = False
    if self.randomizable and self.reserved:
      _log.warning(f"Field ({self.name}) cannot be randomizable and reserved.")
      ret_val = False

    return ret_val

  @staticmethod
  def from_dict(definition: dict) -> Field:
    """Converts the dictionary definition into a Field object.
    Requires the following keys: [name]
    Accepts the optional keys: [size, lsb_pos, access, reset, volatile, randomizable]

    Args:
        definition (dict): The definition of the field in dictionary form

    Raises:
        MissingDefinitionException: Raised when a required key is missing from the definition

    Returns:
        Field: The field derived from the definition
    """
    required_keys = ['name']

    for req_key in required_keys:
      if req_key not in definition:
        _log.error(f"Missing {req_key} key from dict during Field conversion")
        raise MissingDefinitionException(f"Missing {req_key} key from dict during Field conversion")

    fld = Field(definition['name'])

    if 'size' in definition:
      fld.size = definition['size']
    if 'access' in definition:
      fld.access = AccessType.from_string(definition['access'])
    if 'reset' in definition:
      fld.reset = definition['reset']
    if 'volatile' in definition:
      fld.volatile = definition['volatile']
    if 'randomizable' in definition:
      fld.randomizable = definition['randomizable']
    if 'reserved' in definition:
      fld.reserved = definition['reserved']

    return fld


@dataclass
class Register:
  """The class which represents a Register in a MemoryMap"""

  name: str
  """The name of the register"""
  coverage: str = "UVM_NO_COVERAGE"
  """The UVM Coverage type to apply in a RAL"""
  dimension: int = 1
  """The dimension of this register (the number of times it repeats in the Map)"""
  fields: dict[int, Field] = dataclasses.field(default_factory=dict)
  """A list of the fields in the register bank"""

  def add_field(self, fld: Field, lsb_pos: Optional[int] = None) -> bool:
    """Adds the field at the given lsb position

    Args:
        fld (Field): The field to add
        lsb_pos (int, optional): The lsb_position to insert. Defaults to None.
          When None, the field is inserted at the first valid lsb position

    Returns:
        bool: True if the field was successfully inserted. False otherwise
    """
    if lsb_pos is None:
      if len(self.fields.keys()) == 0:
        self.fields[0] = fld
      else:
        last_field_lsb = max(self.fields.keys())
        lsb_pos = self.fields[last_field_lsb].size + last_field_lsb
        self.fields[lsb_pos] = fld

      return True

    # Check if the field overlaps
    for lsb, f in self.fields.items():
      if lsb_pos in range(lsb, lsb + f.size):
        return False
      if lsb_pos + fld.size - 1 in range(lsb, lsb + f.size - 1):
        return False

    self.fields[lsb_pos] = fld

    return True

  def valid(self) -> bool:
    """Checks the Register is validly defined

    Raises:
        bool: Returns true if the Field is valid. False otherwise
    """
    ret_val = True

    if not utils.valid_name(self.name):
      _log.error(f"Register ({self.name}) has an invalid name.")
      ret_val = False

    return ret_val

  @staticmethod
  def from_dict(definition: dict) -> Register:
    """Converts the dictionary definition into a Register object.
    Requires the following keys: [name]
    Accepts the optional keys: [addr, coverage, fields]

    Args:
        definition (dict): The definition of the Register in dictionary form

    Raises:
        MissingDefinitionException: Raised when a required key is missing from the definition

    Returns:
        Register: The register derived from the definition
    """
    required_keys = ['name']

    for req_key in required_keys:
      if req_key not in definition:
        err = f"Missing {req_key} key from dict during Register conversion"
        _log.error(err)
        raise MissingDefinitionException(err)

    reg = Register(definition['name'])

    if 'dimension' in definition:
      reg.dimension = definition['dimension']

    if 'coverage' in definition:
      reg.coverage = definition['coverage']

    if 'fields' in definition:
      for field in definition['fields']:
        lsb_pos = None if "lsb_pos" not in field else field['lsb_pos']

        reg.add_field(Field.from_dict(field), lsb_pos)

    reg.valid()

    return reg


@dataclass
class AddressBlock:
  """An AddressBlock in a MemoryMap which represents a collection of registers"""
  pass


@dataclass
class MemoryMap:
  """The top-level MemoryMap of a device/component"""
  pass


##########################################################################
# From Dict Methods
##########################################################################
def memory_from_dict(definition: dict) -> Field | Register | AddressBlock | MemoryMap:
  raise NotImplementedError("memory_from_dict not implemented")
