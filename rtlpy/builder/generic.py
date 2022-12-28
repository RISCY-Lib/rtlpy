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

from __future__ import annotations

from abc import ABC, abstractmethod

import rtlpy.designer as designer


# TODO: Add header capabilities

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

  def write_lines(self, lines: list[str]) -> None:
    for line in lines:
      self.write_line(line)

  def write_aligned_lines(self, lines: list[list[str]]) -> None:
    # Check all lines are the same length
    num_cols = len(lines[0])
    max_len = [0] * num_cols
    for line in lines:
      if len(line) != num_cols:
        raise ValueError(f"Different length lines passed to {type(self)} ({num_cols}" +
                         f" != {len(line)})")

      for idx, col in enumerate(line):
        max_len[idx] = max(len(col), max_len[idx])

    for line in lines:
      print_str = ""
      for idx, col in enumerate(line):
        print_str += f"{col: >{max_len[idx]}}"
      self.write_line(print_str)

  @abstractmethod
  def line_comment(self, comment: str) -> None:
    pass

  @abstractmethod
  def block_comment(self, comment_lines: list[str]) -> None:
    pass

  def module(self, module: designer.Component) -> None:
    self.module_definition(module)
    self.end_module()

  @abstractmethod
  def module_definition(self, module: designer.Component) -> None:
    """Creates the module definition from the component

    Args:
        module (designer.Component): The component to create the module definition from
    """
    pass

  @abstractmethod
  def end_module(self) -> None:
    pass

  @abstractmethod
  def register(self, reg: designer.Register) -> None:
    pass

  @abstractmethod
  def field(self, fld: designer.Field) -> None:
    pass
