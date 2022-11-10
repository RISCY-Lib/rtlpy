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
"""Module to test the rtlpy.designs module
"""

import pytest

from rtlpy.parser.systemverilog import SystemVerilogLexer


@pytest.mark.parametrize("val,expected", [
  ("|",   ["OR_OPERATOR"]),
  ("^&^", ["XOR_OPERATOR", "AND_OPERATOR", "XOR_OPERATOR"]),
  ("<<",  ["LSHIFT_OPERATOR"]),
  ("**",  ["POWER_OPERATOR"])
])
def test_SimpleOperatorLexing(val, expected):
  lexer = SystemVerilogLexer()
  lexer.build()
  lexer.load_from_string(val)

  tokens = 0
  for idx, tok in enumerate(lexer):
    assert tok.type == expected[idx]
    tokens += 1

  assert tokens == len(expected)


@pytest.mark.parametrize("val,expected", [
  ("3'h0A",   ["UNSIGNED_HEXADECIMAL_LITERAL"]),
  ('"always"', ["STRING_LITERAL"]),
  ('3.4e-10', ['REAL_LITERAL']),
  ('314', ['UNSIGNED_DECIMAL_LITERAL'])
])
def test_LiteralLexing(val, expected):
  lexer = SystemVerilogLexer()
  lexer.build()
  lexer.load_from_string(val)

  tokens = 0
  for idx, tok in enumerate(lexer):
    assert tok.type == expected[idx]
    tokens += 1

  assert tokens == len(expected)


@pytest.mark.parametrize("val,expected", [
  ("@",   ["AT"]),
  (".;", ["DOT", "SEMICOLON"]),
  ("+:", ["PLUSCOLON"])
])
def test_SimpleControlLexing(val, expected):
  lexer = SystemVerilogLexer()
  lexer.build()
  lexer.load_from_string(val)

  tokens = 0
  for idx, tok in enumerate(lexer):
    assert tok.type == expected[idx]
    tokens += 1

  assert tokens == len(expected)


@pytest.mark.parametrize("val,expected", [
  ("test_name",  ["ID"]),
  ("always and", ["ALWAYS", "AND"]),
  ("_test_reg0", ["ID"]),
  ("trireg",     ["TRIREG"]),
  ("always_ff",  ["ALWAYS_FF"]),
  ("logic",      ["LOGIC"])
])
def test_SimpleIDLexing(val, expected):
  lexer = SystemVerilogLexer()
  lexer.build()
  lexer.load_from_string(val)

  tokens = 0
  for idx, tok in enumerate(lexer):
    assert tok.type == expected[idx]
    tokens += 1

  assert tokens == len(expected)


def test_SimpleAST():
  # f = open("tests/parser/sample_files/simple.v", "r")
  pass
