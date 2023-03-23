##########################################################################
# Python library to help with the automatic creation of RTL              #
# Copyright (C) 2023, Benjamin Davis                                     #
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

TRAFFIC_LIGHT_FULL_DEF = {
  "name": "traffic_light",
  "address_size": 6,
  "data_size": 8,
  "endian": "little",
  "coverage": "UVM_CVR_FIELD_VALS | UVM_CVR_ADDR_MAP",
  "blocks": [
    {
      "name": "setup",
      "base_address": 0,
      "registers": [
        {
          "name": "control",
          "fields": [
            {
              "name": "mod_en",
              "size": 1,
              "lsb_pos": 0,
              "access": "RW",
              "reset": 0x0,
              "volatile": False,
              "randomizable": True,
              "reserved": False
            },
            {
              "name": "blink_yellow",
              "size": 1,
              "lsb_pos": 1,
              "access": "RW",
              "reset": 0x0,
              "volatile": False,
              "randomizable": True,
              "reserved": False
            },
            {
              "name": "blink_red",
              "size": 1,
              "lsb_pos": 2,
              "access": "RW",
              "reset": 0x0,
              "volatile": False,
              "randomizable": True,
              "reserved": False
            },
            {
              "name": "profile",
              "size": 1,
              "lsb_pos": 3,
              "access": "RW",
              "reset": 0x0,
              "volatile": False,
              "randomizable": True,
              "reserved": False
            }
          ]
        },
        {
          "name": "status",
          "fields": [
            {
              "name": "state",
              "size": 2,
              "lsb_pos": 0,
              "access": "RO",
              "reset": 0x0,
              "volatile": False,
              "randomizable": False,
              "reserved": False
            }
          ]
        },
        {
          "name": "timer",
          "dimension": 2,
          "fields": [
            {
              "name": "timer_y2r",
              "size": 3,
              "lsb_pos": 0,
              "access": "RW",
              "reset": 0x5,
              "volatile": False,
              "randomizable": True,
              "reserved": False
            },
            {
              "name": "timer_r2g",
              "size": 3,
              "lsb_pos": 0,
              "access": "RW",
              "reset": 0x7,
              "volatile": False,
              "randomizable": True,
              "reserved": False
            },
            {
              "name": "timer_g2y",
              "size": 2,
              "lsb_pos": 0,
              "access": "RW",
              "reset": 0x2,
              "volatile": False,
              "randomizable": True,
              "reserved": False
            }
          ]
        }
      ]
    }
  ]
}

TRAFFIC_LIGHT_RAL_STR = """
// Register definition for control register
class control_reg extends uvm_reg;
  `uvm_object_utils(control_reg)

  rand uvm_reg_field mod_en;
  rand uvm_reg_field blink_yellow;
  rand uvm_reg_field blink_red;
  rand uvm_reg_field profile;

  function new (string name = "control_reg");
    super.new(name, 8, build_coverage(UVM_CVR_FIELD_VALS | UVM_CVR_ADDR_MAP));
  endfunction

  virtual function void build();
    this.mod_en       = uvm_reg_field::type_id::create("mod_en",,       get_full_name());
    this.blink_yellow = uvm_reg_field::type_id::create("blink_yellow",, get_full_name());
    this.blink_red    = uvm_reg_field::type_id::create("blink_red",,    get_full_name());
    this.profile      = uvm_reg_field::type_id::create("profile",,      get_full_name());

    this.mod_en.configure       (this, 1, 0, "RW", 0, 1'h0, 1, 0, 0);
    this.blink_yellow.configure (this, 1, 1, "RW", 0, 1'h0, 1, 0, 0);
    this.blink_red.configure    (this, 1, 2, "RW", 0, 1'h0, 1, 0, 0);
    this.profile.configure      (this, 1, 3, "RW", 0, 1'h0, 1, 0, 0);
  endfunction
endclass

// Register definition for status register
class status_reg extends uvm_reg;
  `uvm_object_utils(status_reg)

  uvm_reg_field state;

  function new (string name = "status_reg");
    super.new(name, 8, build_coverage(UVM_CVR_FIELD_VALS | UVM_CVR_ADDR_MAP));
  endfunction

  virtual function void build();
    this.state = uvm_reg_field::type_id::create("state",, get_full_name());

    this.state.configure (this, 2, 0, "RO", 0, 2'h0, 0, 0, 0);
  endfunction
endclass

// Register definition for timer register
class timer_reg extends uvm_reg;
  `uvm_object_utils(timer_reg)

  rand uvm_reg_field timer_y2r;
  rand uvm_reg_field timer_r2g;
  rand uvm_reg_field timer_g2y;

  function new (string name = "timer_reg");
    super.new(name, 8, build_coverage(UVM_CVR_FIELD_VALS | UVM_CVR_ADDR_MAP));
  endfunction

  virtual function void build();
    this.timer_y2r = uvm_reg_field::type_id::create("timer_y2r",, get_full_name());
    this.timer_r2g = uvm_reg_field::type_id::create("timer_r2g",, get_full_name());
    this.timer_g2y = uvm_reg_field::type_id::create("timer_g2y",, get_full_name());

    this.timer_y2r.configure (this, 3, 0, "RW", 0, 3'h5, 1, 0, 0);
    this.timer_r2g.configure (this, 3, 3, "RW", 0, 3'h7, 1, 0, 0);
    this.timer_g2y.configure (this, 2, 6, "RW", 0, 2'h2, 1, 0, 0);
  endfunction
endclass
"""