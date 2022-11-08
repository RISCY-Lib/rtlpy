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
"""This module contains a generic builder class
"""

from abc import ABC, abstractmethod
from typing import List

import rtlpy.designer as designer


class GenericBuilder (ABC):
  def __init__(self, name: str, tab_size: int, filename: str):
    if (not isinstance(name, str)):
      raise TypeError("GenericBuilder name member is string")
    if (not isinstance(tab_size, int)):
      raise TypeError("GenericBuilder tab_size member is integer")
    self.name = name
    self.tab_size = tab_size
    self._tabs = 0
    self.file = open(filename, "w")

  def tab_in(self):
    self._tabs += 1

  def tab_out(self):
    self._tabs -= 1

  def tab(self) -> str:
    return self.tab_size * self._tabs * " "

  def close(self) -> None:
    self.file.close()

  def write_line(self, line: str) -> None:
    self.file.write(f"{self.tab()}{line}\n")

  @abstractmethod
  def line_comment(self, comment: str) -> None:
    pass

  @abstractmethod
  def block_comment(self, comment_lines: List[str]) -> None:
    pass

  @abstractmethod
  def module(self, module: designer.Component) -> None:
    pass

  @abstractmethod
  def register(self, reg: designer.Register) -> None:
    pass

  @abstractmethod
  def field(self, fld: designer.Field) -> None:
    pass
