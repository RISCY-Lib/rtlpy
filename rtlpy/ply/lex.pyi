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
from typing import Any, Callable

class LexToken:
  lexer: Lexer
  type: str
  value: str
  lineno: int
  lexpos: Any

class Lexer:
  lineno: int

  def input(self, s: str) -> None: ...
  def token(self) -> LexToken: ...

TokenFunc = Callable[[Any, LexToken], LexToken]

def TOKEN(r: str) -> Callable[[TokenFunc], TokenFunc]:
  def set_regex(f: TokenFunc) -> TokenFunc: ...
  return set_regex