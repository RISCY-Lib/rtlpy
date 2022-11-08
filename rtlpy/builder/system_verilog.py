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

from rtlpy.builder.generic import GenericBuilder
import rtlpy.designer as designer


class SystemVerilogBuilder(GenericBuilder):
  """Class to build SystemVerilog files
  """

  def line_comment(self, comment: str) -> None:
    """Create a line comment in the SystemVerilog file

    Args:
        comment (str): The comment line to add to the SystemVerilog file
    """
    self.write_line(f"// {comment}")

  def block_comment(self, comment_lines: list[str]) -> None:
    """Creates a block comment in the SystemVerilog file

    Args:
        comment_lines (list[str]): The list of strings to use for the block comment
    """
    self.write_line("/*")
    for line in comment_lines:
      self.write_line(f" * {line}")
    self.write_line(" */")

  def module(self, module: designer.Component) -> None:
    pass

  def register(self, reg: designer.Register) -> None:
    pass

  def field(self, fld: designer.Field) -> None:
    pass
