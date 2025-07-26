####################################################################################################
# rtlpy is a open-source utility library for RTL developers                                        #
# Copyright (C) 2025, RISCY-Lib Contributors                                                       #
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
from typing import Union

import pyslang


def print_pyslang_tree(tree: pyslang.SyntaxTree) -> None:
    def printer(node: Union[pyslang.Token, pyslang.SyntaxNode]):
        print("Type:", type(node))
        print("Node:", node.kind)
        print("Properties:", [attr for attr in dir(node) if not attr.startswith("_")])
        print("Same line:", getattr(node, "isOnSameLine", None))
        print()

    tree.root.visit(
        printer
    )


def begin_linting(tree: pyslang.SyntaxTree) -> list[pyslang.SourceLocation]:
    """Lint the provided code for begin-end syntax issues."""
    print_pyslang_tree(tree)

    issues = []

    def begin_linting_match(node: Union[pyslang.Token, pyslang.SyntaxNode]) -> None:
        match node:
            case pyslang.Token(
                alloc=_,
                kind=pyslang.TokenKind.BeginKeyword,
                trivia=_,
                rawText=_,
                location=_,
            ):
                issues.append(node.location)

    tree.root.visit(begin_linting_match)

    return issues

def end_linting(code: str) -> None:
    raise NotImplementedError("End linting is not yet implemented.")
