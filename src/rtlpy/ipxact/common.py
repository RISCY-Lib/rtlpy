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
"""Common elements and concepts that appear in IP-XACT.
Defined in the IEEE_1685-2022 standard under Annex C.
"""

from __future__ import annotations

from typing import Annotated, Literal, Union

from pydantic import BeforeValidator
from pydantic_xml import BaseXmlModel, attr, element, wrapped

from rtlpy import sv

NSMAP = {
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "ipxact": "http://www.accellera.org/XMLSchema/IPXACT/1685-2022",
    "schemalocation": "http://www.accellera.org/XMLSchema/IPXACT/1685-2022/index.xsd"
}


####################################################################################################
# C.1 accessHandles
####################################################################################################

class SimpleAccessHandle(BaseXmlModel, ns="ipxact", tag="accessHandle", nsmap=NSMAP):
    """The simpleAccessHandle stores a portion of a HDL path for a memory mapped object.
    Defined in the IEEE_1685-2022 standard under Section C.1.1.
    """

    viewRef: list[str] = element(ns="ipxact", nsmap=NSMAP, default_factory=list)
    """viewRef specifies the list of one or more views to which this accessHandle
    applies. If none is specified, the accessHandle is presumed to apply to all views
    """
    pathSegments: list[PathSegment] = wrapped(
        "pathSegments", ns="ipxact", nsmap=NSMAP, default_factory=list
    )
    """pathSegments is a language-independent mechanism for referencing variables in a
    view.
    """
    # TODO: Vendor Extensions


class SlicedAccessHandle(BaseXmlModel, ns="ipxact", tag="accessHandle", nsmap=NSMAP):
    """A slicedAccessHandle stores a portion of a HDL path for a memory mapped object and enables
    slicing in the HDL path. Defined in the IEEE_1685-2022 standard under Section C.1.2.
    """

    force: bool = attr("force", default=True)
    """force indicates if it is possible to directly write to this object via a back door access."""
    viewRef: list[str] = element(ns="ipxact", nsmap=NSMAP, default_factory=list)
    """viewRef specifies the list of one or more views to which this accessHandle
    applies. If none is specified, the accessHandle is presumed to apply to all views
    """
    slices: list[Slice] = wrapped(
        "slices", ns="ipxact", nsmap=NSMAP
    )
    """slices specifies a list of Slices."""
    # TODO: Vendor Extensions


class PortAccessHandle(BaseXmlModel, ns="ipxact", tag="accessHandle", nsmap=NSMAP):
    """A portAccessHandle describes how to access the associated IP-XACT object, e.g., a port in a
    view or views. Defined in the IEEE_1685-2022 standard under Section C.1.3.
    """

    force: bool = attr("force", default=True)
    """force indicates if it is possible to directly write to this object via a back door access."""
    viewRef: list[str] = element(ns="ipxact", nsmap=NSMAP, default_factory=list)
    """viewRef specifies the list of one or more views to which this accessHandle
    applies. If none is specified, the accessHandle is presumed to apply to all views
    """
    indices: list[Index] = wrapped("indices", ns="ipxact", nsmap=NSMAP, default_factory=list)
    """indicies specifies a list of Index elements."""
    slices: list[PortSlice] = wrapped(
        "slices", ns="ipxact", nsmap=NSMAP
    )
    """slices specifies a list of Slices."""
    # TODO: Vendor Extensions

class Slice(BaseXmlModel, ns="ipxact", tag="slice", nsmap=NSMAP):
    """The slices element specifies a list of slices. A slice consists of one or more pathSegments.
    If only one slice is present, the IP-XACT object is represented as one variable in the view. If
    there are multiple slices, the IP-XACT object is represented by several variables in the view.
    In this case, the calculated path for each slice is concatenated in order to define the total
    set of bits in the IP-XACT object. Concatenation is from msb to lsb.
    Defined in the IEEE_1685-2022 standard under Section C.1.4.
    """

    pathSegments: list[PathSegment] = wrapped(
        "pathSegments", ns="ipxact", nsmap=NSMAP
    )
    """pathSegments is a language-independent mechanism for referencing variables in a view."""
    range: Range = element("range", ns="ipxact", nsmap=NSMAP)
    """range corresponds to a range (bit select) into a variable in the RTL."""


class PortSlice(Slice):
    """The portSlice element specifies a slice of a port. A port slice consists of one or more
    pathSegments. Defined in the IEEE_1685-2022 standard under Section C.1.5.
    """


class PathSegment:
    pass

class Index:
    pass

####################################################################################################
# C.7 complexBaseExpression
####################################################################################################

complexTiedValueExpression = Annotated[
    Union[int, Literal['open', 'default']],
    BeforeValidator(sv.convert_to_unsigned_long_int)
]
# qualifiedExpression = Union[
#     unsignedBitExpression, unsignedBitVectorExpression, realExpression, realVectorExpression
# ]
# realExpression = Annotated[float, BeforeValidator(sv.convert_to_real)]
unsignedLongintExpression = Annotated[int, BeforeValidator(sv.convert_to_unsigned_long_int)]


####################################################################################################
# C.25 range
####################################################################################################
class Range(BaseXmlModel, ns="ipxact", tag="range", nsmap=NSMAP):
    """The range element defines the range of bits or array elements being referenced.
    Defined in the IEEE_1685-2022 standard under Section C.25.
    """

    left: unsignedLongintExpression = element("left", ns="ipxact", nsmap=NSMAP)
    """Specifies the left range for the bit slice from a parameter or port"""
    right: unsignedLongintExpression = element("right", ns="ipxact", nsmap=NSMAP)
    """Specifies the right range for the bit slice from a parameter or port"""
