####################################################################################################
# rtlpy is a open-source utility library for RTL developers                                        #
# Copyright (C) 2022, RISCY-Lib Contributors                                                       #
#                                                                                                  #
# This program is free software: you can redistribute it and/or modify                             #
# it under the terms of the GNU General Public License as published by                             #
# the Free Software Foundation, either version 3 of the License, or                                #
# (at your option) any later version.                                                              #
#                                                                                                  #
# This program is distributed in the hope that it will be useful,                                  #
# but WITHOUT ANY WARRANTY; without even the implied warranty of                                   #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                                    #
# GNU General Public License for more details.                                                     #
#                                                                                                  #
# You should have received a copy of the GNU General Public License                                #
# along with this program.  If not, see <https://www.gnu.org/licenses/>.                           #
####################################################################################################

from __future__ import annotations
from typing import NamedTuple, Literal


__all__ = [
    "__version__",
    "__author__",
    "version_info",
]


class _VersionInfo(NamedTuple):

    major: int
    minor: int
    micro: int
    releaseLevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


version_info: _VersionInfo = _VersionInfo(
    major=2,
    minor=0,
    micro=0,
    releaseLevel="beta",
    serial=1,
)

if version_info.releaseLevel == "final":
    __version__: str = f"{version_info.major}." + \
                        f"{version_info.minor}." + \
                        f"{version_info.micro}"
else:
    __version__: str = f"{version_info.major}." + \
                    f"{version_info.minor}." + \
                    f"{version_info.micro}" + \
                    f"-{version_info.releaseLevel[0]}{version_info.serial}"

__author__ = "RISCY-Lib Contributors"
__license__ = "GPL-3.0-or-later"
