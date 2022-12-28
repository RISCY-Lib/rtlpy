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
"""This module contains a SystemVerilog builder class
"""

from __future__ import annotations

from rtlpy.builder.generic import GenericBuilder
import rtlpy.designer as designer
from typing import List


class SystemVerilogBuilder(GenericBuilder):
  """Class to build SystemVerilog files
  """

  def line_comment(self, comment: str) -> None:
    """Create a line comment in the SystemVerilog file

    Args:
        comment (str): The comment line to add to the SystemVerilog file
    """
    self.write_line(f"// {comment}")

  def block_comment(self, comment_lines: List[str]) -> None:
    """Creates a block comment in the SystemVerilog file

    Args:
        comment_lines (List[str]): The list of strings to use for the block comment
    """
    self.write_line("/*")
    for line in comment_lines:
      self.write_line(f" * {line}")
    self.write_line(" */")

  def module_definition(self, module: designer.Component) -> None:
    module_line = f"module {module.name}"
    if (len(module.parameters) > 0):
      module_line += " #("
    else:
      module_line += " ("
    self.write_line(module_line)
    self.tab_in()

    if len(module.parameters) > 0:
      params = []
      for p in module.parameters:
        params.append(self.parameter_definition(p))
      self.write_aligned_lines(params)
      self.tab_out()
      self.write_line(") (")

    for port in module.ports:
      self.write_line(self.port_definition(port))

  def parameter_definition(self, param: designer.Parameter) -> list[str]:
    ret_val: list[str] = [] * 4
    ret_val[0] = "parameter "
    ret_val[1] = "" if param.param_type is None else f"{param.param_type} "
    ret_val[2] = f"{param.name} "
    ret_val[3] = "" if param.default is None else f"= {param.default}"

    return ret_val

  def port_definition(self, port: designer.Port) -> str:
    ret_str = f"{port.direction} {port.signal_type}"
    if port.width > 1:
      ret_str += f"[{port.width - 1}:0] "
    ret_str += f"{port.name}"

    return ret_str

  def end_module(self) -> None:
    pass

  def register(self, reg: designer.Register) -> None:
    pass
