##########################################################################
# Python library to help with the automatic creation of RTL              #
# Copyright (C) 2022, RISCY-Lib Contributors                                    #
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

from rtlpy.design.memory import Register
import rtlpy.uvm as ral

reg_def = {
  "name": "control",
  "fields": [
    {
      "name": "mod_en",
      "size": 1,
      "lsb_pos": 0,
      "access": "RW",
      "reset": 0x0,
      "volatile": False,
      "randomizable": False,
      "reserved": False
    },
    {
      "name": "blink_yellow",
      "size": 1,
      "lsb_pos": 1,
      "access": "RW",
      "reset": 0x0,
      "volatile": False,
      "randomizable": True,
      "reserved": False
    },
    {
      "name": "blink_red",
      "size": 1,
      "lsb_pos": 2,
      "access": "RW",
      "reset": 0x0,
      "volatile": False,
      "randomizable": True,
      "reserved": False
    },
    {
      "name": "profile",
      "size": 1,
      "lsb_pos": 3,
      "access": "RW",
      "reset": 0x0,
      "volatile": False,
      "randomizable": True,
      "reserved": False
    }
  ]
}

reg = Register.from_dict(reg_def)

with open("control_reg.sv", "w") as fout:
    fout.write(ral.reg_to_ral(reg))
