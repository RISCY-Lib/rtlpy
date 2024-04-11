##########################################################################
# Python library to help with the automatic creation of RTL              #
# Copyright (C) 2024, RISCY-Lib Contributors                             #
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

import logging

from dataclasses import dataclass
import dataclasses
from abc import ABC, abstractmethod


from rtlpy.memory.registers import Register, Field
from rtlpy._version_cfg import _dc_kwargs
import rtlpy.utils as utils

##########################################################################
# Logging
##########################################################################
_log = logging.getLogger(__name__)
_log.addHandler(logging.NullHandler())


##########################################################################
# Class Definitions
##########################################################################
@dataclass(**_dc_kwargs)
class RemapState:

  name: str = ""
  """The name of the remap state"""
  conditions: list[RemapCondition] = dataclasses.field(default_factory=list)
  """The conditions which enable the remap state"""

  def validate(self, recurse: bool = True) -> bool:
    """Validate the re-map state. Errors and warnings are logged.

    Args:
        recurse (bool, optional): Whether to only validate this element
          or recursively validate all children. Defaults to True.

    Returns:
        bool: True if valid, False otherwise
    """
    ret_val = True

    class_name = type(self).__name__

    if not utils.valid_name(self.name):
      _log.error(f"Invalid {class_name} Name {self.name}")
      ret_val = False

    if recurse:
      for condition in self.conditions:
        if not condition.validate():
          ret_val = False

    return ret_val


class RemapCondition(ABC):
  def __new__(cls, *args, **kwargs):
    if cls is RemapCondition:
      raise TypeError("RemapCondition cannot be instantiated directly, only children")
    return super().__new__(cls, *args, **kwargs)

  @abstractmethod
  def validate(self, recurse: bool = True) -> bool:
    """Validate the re-map condition. Errors and warnings are logged.

    Args:
        recurse (bool, optional): Whether to only validate this element
          or recursively validate all children. Defaults to True.

    Returns:
        bool: True if valid, False otherwise
    """
    pass


@dataclass(**_dc_kwargs)
class AlwaysTrueRemapCondition(RemapCondition):
  def validate(self, recurse: bool = True) -> bool:
    return True


@dataclass(**_dc_kwargs)
class RegisterValueRemapCondition(RemapCondition):
  register: Register | Field | None = None
  """The register to use for the remap state"""
  value: int = 0
  """The value of the register which enables the remap state"""

  def validate(self, recurse: bool = True) -> bool:
    ret_val = True

    if self.register is None:
      _log.error("Invalid Register Value Remap Condition (None)")
      ret_val = False

    return ret_val


@dataclass(**_dc_kwargs)
class PortValueRemapCondition(RemapCondition):
  port: None = None
  """The port to use for the remap state"""
  value: int = 0
  """The value of the port which enables the remap state"""

  def validate(self, recurse: bool = True) -> bool:
    raise NotImplementedError("PortValueRemapCondition is not yet implemented")
