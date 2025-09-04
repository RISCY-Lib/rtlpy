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
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import IO, ClassVar

import pydantic

__all__ = [
    "ConfigurationModel",
    "Subcommand",
]


class ConfigurationModel(pydantic.BaseModel):
    """A base class for defining configuration models in the rtlpy toolset."""


@dataclass
class Subcommand(ABC):
    """A base class for defining subcommands in the rtlpy toolset."""

    name: ClassVar[str | None] = None
    """The name of the subcommand, used in help messages.
    If none the lowercased class name will be used instead.
    """
    short_desc: ClassVar[str | None] = None
    """A short description of the subcommand, used in help messages.
    If none the class __doc__ wil be used instead.
    """
    long_desc: ClassVar[str | None] = None
    """A long description of the subcommand, used in help messages.
    If none the class __doc__ wil be used instead.
    """
    cfg_model: ClassVar[type[ConfigurationModel]] = ConfigurationModel
    """A Pydantic model for configuration options specific to this subcommand."""

    def _init_subparser(self, subgroup: argparse._SubParsersAction) -> None:
        """Initializes the subparser for this subcommand.

        Args:
            subgroup: The argument parser for the subcommand.
        """
        subparser = subgroup.add_parser(
            self.__class__.__name__.lower() if self.name is None else self.name,
            help=self.__class__.__doc__ if self.short_desc is None else self.short_desc,
            description=self.__class__.__doc__ if self.long_desc is None else self.long_desc,
        )
        subparser.set_defaults(subcommand_instance=self)

        _add_default_arguments(subparser)


    @abstractmethod
    def run(self) -> None:
        """The entry point for executing the subcommand's functionality."""


class _FromFileAction(argparse.Action):
    """An argparse action that expands arguments from a file."""

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: IO[str] | None,             # type: ignore[override]
        option_string: str | None = None,
    ) -> None:
        if values is not None:
            with values as file:
                args = file.read().split()
                print(args)
                parser.parse_args(args, namespace=namespace)


def _add_default_arguments(subparser: argparse.ArgumentParser) -> None:
    """Adds default arguments to the subparser.
    This includes the -f flag for specifying a from file and the
    --cfg flag for specifying a configuration file.

    Args:
        subparser: The argument parser for the subcommand.
    """
    subparser.add_argument(
        "-f",
        "--from-file",
        type=open,
        action=_FromFileAction,
        help="Expand the provided from file into the command line arguments.",
    )
    subparser.add_argument(
        "--cfg",
        type=str,
        help="Path to a configuration file for the subcommand.",
    )
