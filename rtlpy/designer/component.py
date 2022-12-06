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
from attr import define, field, validators

import rtlpy.utils as utils
import rtlpy.designer.memory as memory


class Port:
  # TODO: Add type
  # TODO: Add direction
  name: str = field(validator=utils.name_validator)
  """The name of the Component"""

  width: int = field(validator=validators.instance_of(int), default=1)
  """The width of the port in bits"""


class Parameter:
  # TODO: Add type
  # TODO: Add default
  name: str = field(validator=utils.name_validator)
  """The name of the Component"""


class DesignNode:
  # TODO
  pass


class Design:
  # TODO
  pass


@define
class Component:
  """Class to represent an RTL component
  """

  name: str = field(validator=utils.name_validator)
  """The name of the Component"""

  version: str = field(validator=validators.instance_of(str), default="")
  """The component version"""

  vendor: str = field(validator=validators.instance_of(str), default="")
  """The component vendor"""

  library: str = field(validator=validators.instance_of(str), default="")
  """The component library"""

  description: str = field(validator=validators.instance_of(str), default="")
  """Text description of the component"""

  memory_map: memory.MemoryMap = field(init=False)
  """The memory map of the component"""

  ports: list[Port] = field(factory=list, init=False)
  """List of ports for the component"""

  parameters: list[Parameter] = field(factory=list, init=False)
  """List of parameters for the component"""

  design: Design = field(init=False)

  @staticmethod
  def from_dict(cdict: dict) -> Component:
    raise NotImplementedError("Component.from_dict not implemented")
