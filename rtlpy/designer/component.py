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

from attr import validators
import attr

import rtlpy.utils as utils
import rtlpy.designer.memory as memory
import rtlpy.designer.types as types


@attr.s
class Port:
  name: str = attr.ib(validator=utils.name_validator)
  """The name of the Component"""

  direction: types.PortDirection = attr.ib(validator=validators.instance_of(types.PortDirection))
  """The direction of the port"""

  width: int = attr.ib(validator=validators.instance_of(int), default=1)
  """The width of the port in bits"""

  signal_type: types.SignalType = attr.ib(validator=validators.instance_of(types.SignalType),
                                          default=types.SignalType.WIRE)
  """The type signal used by the port"""


@attr.s
class Parameter:
  name: str = attr.ib(validator=utils.name_validator)
  """The name of the Component"""

  param_type: types.ParamType = attr.ib(default=None)
  """The type of the parameter"""

  default: str = attr.ib(default=None)
  """The default value of the parameter"""


@attr.s
class DesignNode:
  # TODO
  pass


@attr.s
class Design:
  # TODO
  pass


@attr.s
class Component:
  """Class to represent an RTL component
  """

  name: str = attr.ib(validator=utils.name_validator)
  """The name of the Component"""

  version: str = attr.ib(validator=validators.instance_of(str), default="")
  """The component version"""

  vendor: str = attr.ib(validator=validators.instance_of(str), default="")
  """The component vendor"""

  library: str = attr.ib(validator=validators.instance_of(str), default="")
  """The component library"""

  description: str = attr.ib(validator=validators.instance_of(str), default="")
  """Text description of the component"""

  memory_map: memory.MemoryMap = attr.ib(init=False)
  """The memory map of the component"""

  ports: list[Port] = attr.ib(factory=list, init=False)
  """List of ports for the component"""

  parameters: list[Parameter] = attr.ib(factory=list, init=False)
  """List of parameters for the component"""

  design: Design = attr.ib(init=False)
  """The underlying design of the component"""

  @staticmethod
  def from_dict(cdict: dict) -> Component:
    raise NotImplementedError("Component.from_dict not implemented")
