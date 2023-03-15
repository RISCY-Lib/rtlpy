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

from dataclasses import dataclass

from rtlpy.design import AccessType


class MissingDefinitionException (Exception):
  """The Exception raised when converting using a dictionary that is missing a required field"""
  pass


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

    return fld
