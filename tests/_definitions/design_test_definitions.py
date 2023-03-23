##########################################################################
# Python library to help with the automatic creation of RTL              #
# Copyright (C) 2023, Benjamin Davis                                     #
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

MINIMUM_FIELD_DEFINITION = {
  "name": "test_name"
}

FULL_FIELD_DEFINITION = {
  "name": "abacadabra",
  "size": 4,
  "lsb_pos": 1,
  "access": "WC",
  "volatile": True,
  "reset": 10,
  "randomizable": False,
}

RESERVED_FIELD_DEFINITION = {
  "name": "part_id",
  "size": 8,
  "lsb_pos": 0,
  "access": "RO",
  "reset": 0xFA,
  "randomizable": False,
  "reserved": True
}

MINIMUM_REGISTER_DEFINITION = {
  "name": "test_reg"
}

FULL_REGISTER_DEFINITION = {
  "name": "full_reg",
  "coverage": "UVM_FULL_COVERAGE",
  "addr": 0x10,
  "fields": [
    MINIMUM_FIELD_DEFINITION,
    FULL_FIELD_DEFINITION
  ]
}
