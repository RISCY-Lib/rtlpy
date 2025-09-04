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

# ruff: noqa

# from __future__ import annotations

# from pydantic_xml import BaseXmlModel, element, wrapped

# from rtlpy.ipxact.common import NSMAP, ConfigurableLibraryRefType, _NameGroup, _VersionedIdentifier


# class Component(_VersionedIdentifier, tag="component", ns="ipxact", nsmap=NSMAP):
#     """An IP-XACT Component. Defined in the IEEE_1685-2014 Section 6.1.

#     An IP-XACT component is used to describe the meta-data associated with any IP that can be
#     instantiated in a design. Examples include IP such as cores (e.g., processors, co-processors,
#     DSPs), peripherals (e.g., memories, DMA controllers, timers, UART), buses (e.g., simple buses,
#     multi-layer buses, cross bars, network on chip), or any other IP block that can be instantiated
#     in a design. An IP-XACT component can be of two kinds: static or configurable. A DE cannot
#     change a static component. A configurable (or parameterized) component has configurable elements
#     (such as parameters) that can be configured by the DE, and these elements may also configure the
#     RTL or TLM model.
#     """

#     bus_interfaces: list[BusInterface] = wrapped(
#         "busInterfaces", ns="ipxact", nsmap=NSMAP,
#         default_factory=list
#     )
#     """A list of bus interfaces associated with this component"""


# class BusInterface(_NameGroup, tag="busInterface", ns="ipxact", nsmap=NSMAP):
#     """An IP-XACT BusInterface. Defined in the IEEE_1685-2014 Section 6.5.

#     Bus interfaces enable individual ports that appear on the component to be grouped together into
#     a meaningful, known protocol. When the protocol is known, a lot of additional information can be
#     written down about the characteristics of that interface.
#     """

#     is_present: bool = element(
#         tag="isPresent", ns="ipxact", nsmap=NSMAP, default=True
#     )
#     """Defines whether the bus interface is present in the component."""
#     bus_type: ConfigurableLibraryRefType = element(
#         tag="busType", ns="ipxact", nsmap=NSMAP
#     )
#     """Specifies the bus definition that this bus interface is referenced."""
#     interface_mode: MasterInterfaceMode | SlaveInterfaceMode = element(
#         tag="interfaceMode", ns="ipxact", nsmap=NSMAP
#     )


# class AddressSpaceRef(BaseXmlModel):
#     pass


# class MasterInterfaceMode(BaseXmlModel):
#     """An IP-XACT MasterInterfaceMode. Defined in the IEEE_1685-2014 Section 6.5.3.
#     """

#     address_space_ref: AddressSpaceRef | None = element(
#         tag="addressSpaceRef", ns="ipxact", nsmap=NSMAP, default=None
#     )
#     """References a name of an address space defined in the containing description."""


# class SlaveInterfaceMode(BaseXmlModel):
#     """An IP-XACT MasterInterfaceMode. Defined in the IEEE_1685-2014 Section 6.5.3.
#     """

#     address_space_ref: AddressSpaceRef | None = element(
#         tag="addressSpaceRef", ns="ipxact", nsmap=NSMAP, default=None
#     )
#     """References a name of an address space defined in the containing description."""
