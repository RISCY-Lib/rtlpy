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

import os
import sys

from rtlpy.tools import cfg


def test_rtlpy_configuration_model_subcommands() -> None:
    """Test that the RTLPyConfigurationModel correctly accepts subcommands."""
    sys.path.append(os.path.dirname(__file__))

    config_model = cfg.RTLPyConfigurationModel.model_validate({
        "subcommands": [
            "tool_test_package.demo_subcommand:DummySubcommand"
        ]
    })

    from tool_test_package.demo_subcommand import DummySubcommand  # type: ignore[import]

    assert len(config_model.subcommands) == 1
    assert config_model.subcommands[0] is DummySubcommand
