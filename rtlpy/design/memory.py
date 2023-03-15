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

import dataclasses
from dataclasses import dataclass

from rtlpy.design import AccessType

import rtlpy.utils as utils


##########################################################################
# Exception Definitions
##########################################################################
class MissingDefinitionException (Exception):
  """The Exception raised when converting using a dictionary that is missing a required field"""
  pass


class InvalidMemoryComponent (Exception):
  """Exception which is use to communicate issues in the definition of a memory component"""
  def __init__(self, message: str, errors: list[str]):
    super().__init__(message)

    self.errors = errors


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
  lsb_pos: int = 0
  """Position of the LSB in register"""
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

  def validate(self) -> None:
    """Checks the Field is validly defined

    Raises:
        InvalidMemoryComponent: Raised if there are issues with the field definition
    """
    errors = []

    if not utils.valid_name(self.name):
      errors.append("Invalid field name")
    if self.reset.bit_length() > self.size:
      errors.append("Reset value does not fit in field")
    if self.randomizable and self.reserved:
      errors.append("Field cannot be randomizable and reserved")

    if len(errors) > 0:
      raise InvalidMemoryComponent(f"Field {self.name} is not correctly defined", errors)

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
        raise MissingDefinitionException(f"Missing {req_key} key from dict during Field conversion")

    fld = Field(definition['name'])

    if 'size' in definition:
      fld.size = definition['size']
    if 'lsb_pos' in definition:
      fld.lsb_pos = definition['lsb_pos']
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

    # Check the generated field is valid
    fld.validate()

    return fld


@dataclass
class Register:
  """The class which represents a Register in a MemoryMap"""

  name: str
  """The name of the register"""
  addr: int = 0
  """The address of the register in the MemoryMap"""
  coverage: str = "UVM_NO_COVERAGE"
  """The UVM Coverage type to apply in a RAL"""
  fields: list[Field] = dataclasses.field(default_factory=list)
  """A list of the fields in the register bank"""

  def validate(self) -> None:
    """Checks the Register is validly defined

    Raises:
        InvalidMemoryComponent: Raised if there are issues with the register definition
    """
    errors = []

    if not utils.valid_name(self.name):
      errors.append("Invalid register name")

    if len(errors) > 0:
      raise InvalidMemoryComponent(f"Field {self.name} is not correctly defined", errors)

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
        raise MissingDefinitionException(f"Missing {req_key} key from dict during Field conversion")

    reg = Register(definition['name'])

    if 'addr' in definition:
      reg.addr = definition['addr']
    if 'coverage' in definition:
      reg.coverage = definition['coverage']

    if 'fields' in definition:
      for field in definition['fields']:
        reg.fields.append(Field.from_dict(field))

    reg.validate()

    return reg
