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

import pytest

from rtlpy.ipxact import component


@pytest.fixture
def example_component_2014() -> str:
    with open("tests/ipxact/src_files/example_component_2014.xml") as f:
        return f.read()


@pytest.fixture
def simplest_bus_interface() -> str:
    return """<ipxact:busInterface xmlns:ipxact="http://www.accellera.org/XMLSchema/IPXACT/2.0">
    <ipxact:name>MirroredMaster</ipxact:name>
    <ipxact:displayName>Mirrored Master Interface</ipxact:displayName>
    <ipxact:description>A mirrored master interface for the component</ipxact:description>
    <ipxact:busType vendor="accellera.org" library="Sample" name="SampleBusDefinition" version="1.0"/>
    <ipxact:mirroredMaster/>
</ipxact:busInterface>"""


# def test_busInterface_nameGroup_group(simplest_bus_interface: str) -> None:
#     bus_if = component.BusInterface.from_xml(simplest_bus_interface)

#     assert bus_if.name == "MirroredMaster"
#     assert bus_if.display_name == "Mirrored Master Interface"
#     assert bus_if.description == "A mirrored master interface for the component"


# def test_busInterface_isPresent_default(simplest_bus_interface: str) -> None:
#     bus_if = component.BusInterface.from_xml(simplest_bus_interface)

#     assert bus_if.is_present is True


# def test_busInterface_busType(simplest_bus_interface: str) -> None:
#     bus_if = component.BusInterface.from_xml(simplest_bus_interface)

#     assert bus_if.bus_type.vendor == "accellera.org"
#     assert bus_if.bus_type.library == "Sample"
#     assert bus_if.bus_type.name == "SampleBusDefinition"
#     assert bus_if.bus_type.version == "1.0"


# def test_component_versionedIdentifier_group(example_component_2014: str):
#     comp = component.Component.from_xml(example_component_2014)

#     assert comp.vendor == "accellera.org"
#     assert comp.library == "Sample"
#     assert comp.name == "SampleComponent"
#     assert comp.version == "1.0"


# def test_component_busInterfaces(example_component_2014: str):
#     comp = component.Component.from_xml(example_component_2014)

#     assert len(comp.bus_interfaces) == 7
#     assert comp.bus_interfaces[0].name == "Slave"
#     assert comp.bus_interfaces[1].name == "Master"

