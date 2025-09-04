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

import importlib
import re
from typing import Annotated, Any

import pydantic

__all__ = [
    "RTLPyConfigurationModel",
    "ConfigurationModel",
]

def _class_before_validator(value: Any) -> type:
    """A Pydantic validator that ensures the value is an instance of the specified class type.
    """
    if not isinstance(value, str):
        raise ValueError(f"Expected a string for class path, got {type(value).__name__}")

    if (match := re.match(r"^([\w\.\:]+):(\w+)$", str(value))) is None:
        raise ValueError(f"Could not resolve class from path: {value}")

    try:
        module = importlib.import_module(match.group(1))
    except ModuleNotFoundError as e:
        raise ValueError(f"Could not import module from path: {match.group(1)}") from e

    try:
        cls = getattr(module, match.group(2))
    except AttributeError as e:
        raise ValueError(
            f"Could not find class '{match.group(2)}' in module '{match.group(1)}'"
        ) from e

    if not isinstance(cls, type):
        raise ValueError(
            f"Resolved object '{match.group(2)}' in module '{match.group(1)}' is not a class"
        )

    return cls


SubcommandType = Annotated[type, pydantic.BeforeValidator(_class_before_validator)]


class RTLPyConfigurationModel(pydantic.BaseModel):
    """Class which contains common configuration options for all rtlpy tools.
    """

    subcommands: list[SubcommandType] = pydantic.Field(default_factory=list)
    """List of additional subcommands that are available for the rtlpy toolset.
    Should be provided to the configuration model in the format 'some.module.path:ClassName'.
    This allows for dynamic loading of subcommands from different modules and packages.
    """


class ConfigurationModel(pydantic.BaseModel):
    """A base class for defining configuration models in the rtlpy toolset."""

    general: RTLPyConfigurationModel
    """The general configuration options for the rtlpy toolset."""
