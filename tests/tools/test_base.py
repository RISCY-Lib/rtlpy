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

import argparse
import pathlib

from rtlpy.tools import base


def test_from_file_action(tmp_path: pathlib.Path) -> None:
    """Test the FromFileAction correctly expands arguments from a file."""
    args_file = tmp_path / "args.txt"
    args_file.write_text("--option1 value1\n--option2 value2\n")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--option1",
        type=str,
    )
    parser.add_argument(
        "--option2",
        type=str,
    )
    parser.add_argument(
        "-f",
        "--from-file",
        type=argparse.FileType('r'),
        action=base._FromFileAction,
        help="Expand the provided from file into the command line arguments.",
    )

    parsed_args = parser.parse_args(["-f", str(args_file)])

    assert parsed_args.option1 == "value1"
    assert parsed_args.option2 == "value2"
