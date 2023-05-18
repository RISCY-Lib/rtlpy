##########################################################################
# rtlpy is a open-source utility library for RTL developers              #
# Copyright (C) 2022, RISC-Lib Contributors                                     #
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

VERSION = {"major": 0, "minor": 0, "patch": 0, "status": "alpha"}
"""Version Dictionary (keys: major, minor, patch, status)"""

if (VERSION['status'] != ''):
  __version__ = f"{VERSION['major']}.{VERSION['minor']}.{VERSION['patch']}-{VERSION['status']}"
else:
  __version__ = f"{VERSION['major']}.{VERSION['minor']}.{VERSION['patch']}"
