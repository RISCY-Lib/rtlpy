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

from jinja2 import Environment, PackageLoader

from rtlpy.design.memory import Register, AddressBlock


def addrblock_to_ral(ablock: AddressBlock) -> str:
  raise NotImplementedError("addrblock_to_ral not implemented")


def reg_to_ral(
      reg: Register,
      data_size: int = 32,
      coverage: str = "UVM_NO_COVERAGE"
    ) -> str:
  """Convert the provided register to a UVM Register for the RAL

  Args:
      reg (Register): The register to create the RAL for
      data_size (int, optional): The register data width. Defaults to 32.
      coverage (str, optional): The UVM built in coverage. Defaults to "UVM_NO_COVERAGE".

  Returns:
      str: The string version of the generated RAL
  """
  env = Environment(
    loader=PackageLoader("rtlpy.build", "uvm_templates"),
    lstrip_blocks=True,
    trim_blocks=True
  )

  template = env.get_template("uvm_reg.jinja")

  return template.render(reg=reg, data_size=data_size)
