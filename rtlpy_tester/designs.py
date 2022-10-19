##########################################################################
# A general RTL Utility Library for Python                               #
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

import rtlpy.designs as designs

import unittest

import random
import string

class TestDesignHelpers (unittest.TestCase) :
  """Unit test Class for the rtlpy helper functions
  """

  def test__overlaps(self) :
    """Tests the overlaps helper function"""
    self.assertFalse(designs._overlaps((0, 2), (3, 5)), "0->2 and 3->5 do NOT overlap")
    self.assertTrue(designs._overlaps((1,2), (0,3)), "Checking internal overlap")
    self.assertTrue(designs._overlaps((0,2), (1,3)), "Checking first number overlap")
    self.assertTrue(designs._overlaps((2,4), (1,3)), "Checking last number overlap")
    self.assertTrue(designs._overlaps((0,3), (1,2)), "Checking external overlap")


  def test__str2int(self) :
    """Tests the _str2int helper function"""
    self.assertEqual(designs._str2int("0xA"), 0xA, "String '0xA' should match integer literal 0xA")
    self.assertEqual(designs._str2int("xA"), 0xA, "String 'xA' should match integer literal 0xA")
    self.assertEqual(designs._str2int("243"), 243, "String '243' should match integer literal 243")

    with self.assertRaises(TypeError, msg="rtlpy.designs._str2int should raise exception if it doesn't receive a string") :
      designs._str2int(10)