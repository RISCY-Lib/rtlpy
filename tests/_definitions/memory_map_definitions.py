##########################################################################
# Python library to help with the automatic creation of RTL              #
# Copyright (C) 2023, RISCY-Lib Contributors                                    #
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
  "addr_size": 6,
  "data_size": 8,
  "endian": "little",
  "coverage": "UVM_CVR_FIELD_VALS | UVM_CVR_ADDR_MAP",
  "sub_blocks": [
    {
      "name": "setup",
      "base_address": 16,
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
              "access": "RW",
              "reset": 0x7,
              "volatile": False,
              "randomizable": True,
              "reserved": False
            },
            {
              "name": "timer_g2y",
              "size": 2,
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
  ],
  "page_reg": {
    "name": "page_reg",
    "offset": 0x3F,
    "fields": [
      {
        "name": "page",
        "size": 8,
        "lsb_pos": 0,
        "access": "RW",
        "reset": 0x0
      }
    ]
  }
}

TRAFFIC_LIGHT_RAL_STR = """/** control - UVM register model
 * Fields:
 *    mod_en - LSB: 0, Width: 1, Access: RW
 *    blink_yellow - LSB: 1, Width: 1, Access: RW
 *    blink_red - LSB: 2, Width: 1, Access: RW
 *    profile - LSB: 3, Width: 1, Access: RW
 */
class control_reg extends uvm_reg;
  `uvm_object_utils(control_reg)

  rand uvm_reg_field mod_en;
  rand uvm_reg_field blink_yellow;
  rand uvm_reg_field blink_red;
  rand uvm_reg_field profile;

  // CVR Field Vals Group
  covergroup cg_vals;
    option.per_instance = 1;

    mod_en: coverpoint mod_en.value {
      bins vals[] = {[0:1]};
    }
    blink_yellow: coverpoint blink_yellow.value {
      bins vals[] = {[0:1]};
    }
    blink_red: coverpoint blink_red.value {
      bins vals[] = {[0:1]};
    }
    profile: coverpoint profile.value {
      bins vals[] = {[0:1]};
    }
  endgroup

  // Create new register
  function new (string name = "control_reg");
    super.new(name, 8, build_coverage(UVM_CVR_FIELD_VALS | UVM_CVR_ADDR_MAP));
    add_coverage(build_coverage(UVM_CVR_FIELD_VALS | UVM_CVR_ADDR_MAP));

    if (has_coverage(UVM_CVR_FIELD_VALS)) begin
      cg_vals = new();
      cg_vals.set_inst_name({get_full_name(), "_cg_vals"});
    end
  endfunction

  // Build all register field objects
  virtual function void build ();
    this.mod_en = uvm_reg_field::type_id::create("mod_en",, get_full_name());
    this.blink_yellow = uvm_reg_field::type_id::create("blink_yellow",, get_full_name());
    this.blink_red = uvm_reg_field::type_id::create("blink_red",, get_full_name());
    this.profile = uvm_reg_field::type_id::create("profile",, get_full_name());

    this.mod_en.configure(this, 1, 0, "RW", 0, 1'h0, 1, 1, 0);
    this.blink_yellow.configure(this, 1, 1, "RW", 0, 1'h0, 1, 1, 0);
    this.blink_red.configure(this, 1, 2, "RW", 0, 1'h0, 1, 1, 0);
    this.profile.configure(this, 1, 3, "RW", 0, 1'h0, 1, 1, 0);
    set_coverage(UVM_CVR_FIELD_VALS | UVM_CVR_ADDR_MAP);
  endfunction


  // The register sample function
  virtual function void sample_values();
    super.sample_values();

    if (has_coverage(UVM_CVR_FIELD_VALS))
      cg_vals.sample();
  endfunction
endclass

/** status - UVM register model
 * Fields:
 *    state - LSB: 0, Width: 2, Access: RO
 */
class status_reg extends uvm_reg;
  `uvm_object_utils(status_reg)

       uvm_reg_field state;

  // CVR Field Vals Group
  covergroup cg_vals;
    option.per_instance = 1;

    state: coverpoint state.value {
      bins vals[] = {[0:3]};
    }
  endgroup

  // Create new register
  function new (string name = "status_reg");
    super.new(name, 8, build_coverage(UVM_CVR_FIELD_VALS | UVM_CVR_ADDR_MAP));
    add_coverage(build_coverage(UVM_CVR_FIELD_VALS | UVM_CVR_ADDR_MAP));

    if (has_coverage(UVM_CVR_FIELD_VALS)) begin
      cg_vals = new();
      cg_vals.set_inst_name({get_full_name(), "_cg_vals"});
    end
  endfunction

  // Build all register field objects
  virtual function void build ();
    this.state = uvm_reg_field::type_id::create("state",, get_full_name());

    this.state.configure(this, 2, 0, "RO", 0, 2'h0, 1, 0, 0);
    set_coverage(UVM_CVR_FIELD_VALS | UVM_CVR_ADDR_MAP);
  endfunction


  // The register sample function
  virtual function void sample_values();
    super.sample_values();

    if (has_coverage(UVM_CVR_FIELD_VALS))
      cg_vals.sample();
  endfunction
endclass

/** timer - UVM register model
 * Fields:
 *    timer_y2r - LSB: 0, Width: 3, Access: RW
 *    timer_r2g - LSB: 3, Width: 3, Access: RW
 *    timer_g2y - LSB: 6, Width: 2, Access: RW
 */
class timer_reg extends uvm_reg;
  `uvm_object_utils(timer_reg)

  rand uvm_reg_field timer_y2r;
  rand uvm_reg_field timer_r2g;
  rand uvm_reg_field timer_g2y;

  // CVR Field Vals Group
  covergroup cg_vals;
    option.per_instance = 1;

    timer_y2r: coverpoint timer_y2r.value {
      bins vals[] = {[0:7]};
    }
    timer_r2g: coverpoint timer_r2g.value {
      bins vals[] = {[0:7]};
    }
    timer_g2y: coverpoint timer_g2y.value {
      bins vals[] = {[0:3]};
    }
  endgroup

  // Create new register
  function new (string name = "timer_reg");
    super.new(name, 8, build_coverage(UVM_CVR_FIELD_VALS | UVM_CVR_ADDR_MAP));
    add_coverage(build_coverage(UVM_CVR_FIELD_VALS | UVM_CVR_ADDR_MAP));

    if (has_coverage(UVM_CVR_FIELD_VALS)) begin
      cg_vals = new();
      cg_vals.set_inst_name({get_full_name(), "_cg_vals"});
    end
  endfunction

  // Build all register field objects
  virtual function void build ();
    this.timer_y2r = uvm_reg_field::type_id::create("timer_y2r",, get_full_name());
    this.timer_r2g = uvm_reg_field::type_id::create("timer_r2g",, get_full_name());
    this.timer_g2y = uvm_reg_field::type_id::create("timer_g2y",, get_full_name());

    this.timer_y2r.configure(this, 3, 0, "RW", 0, 3'h5, 1, 1, 0);
    this.timer_r2g.configure(this, 3, 3, "RW", 0, 3'h7, 1, 1, 0);
    this.timer_g2y.configure(this, 2, 6, "RW", 0, 2'h2, 1, 1, 0);
    set_coverage(UVM_CVR_FIELD_VALS | UVM_CVR_ADDR_MAP);
  endfunction


  // The register sample function
  virtual function void sample_values();
    super.sample_values();

    if (has_coverage(UVM_CVR_FIELD_VALS))
      cg_vals.sample();
  endfunction
endclass

/** setup - UVM register model
 * Registers:
 *    control - Offset: 0
 *    status - Offset: 1
 *    timer[2] - Offset: 2
 * Sub-Blocks:
 */
class setup_block extends uvm_reg_block;
  `uvm_object_utils(setup_block)

  // Registers
  rand control_reg control;
       status_reg status;
  rand timer_reg timer[2];

  // Sub-Blocks

  function new (string name = "setup_block");
    super.new(name, build_coverage(UVM_CVR_FIELD_VALS | UVM_CVR_ADDR_MAP));
  endfunction

  // Build all register and sub-block objects
  virtual function void build ();
    this.default_map = create_map("", 16, 1, UVM_LITTLE_ENDIAN);

    // Registers
    this.control = control_reg::type_id::create({get_name(), ".control"},, get_full_name());
    this.control.configure(this, null, "");
    this.control.build();
    this.default_map.add_reg(this.control, 6'h0);

    this.status = status_reg::type_id::create({get_name(), ".status"},, get_full_name());
    this.status.configure(this, null, "");
    this.status.build();
    this.default_map.add_reg(this.status, 6'h1);

    this.timer[0] = timer_reg::type_id::create({get_name(), ".timer[0]"},, get_full_name());
    this.timer[0].configure(this, null, "");
    this.timer[0].build();
    this.default_map.add_reg(this.timer[0], 6'h2);

    this.timer[1] = timer_reg::type_id::create({get_name(), ".timer[1]"},, get_full_name());
    this.timer[1].configure(this, null, "");
    this.timer[1].build();
    this.default_map.add_reg(this.timer[1], 6'h3);

    // Sub-Blocks

    lock_model();
  endfunction

  function reregister();
    this.default_map.unregister();

    // Registers
    this.default_map.add_reg(this.control, 6'h0);

    this.default_map.add_reg(this.status, 6'h1);

    this.default_map.add_reg(this.timer[0], 6'h2);

    this.default_map.add_reg(this.timer[1], 6'h3);

    // Sub-Blocks

  endfunction
endclass

/** traffic_light - UVM register model
 * Registers:
 * Sub-Blocks:
 *    setup - Offset: 16
 */
class traffic_light_block extends uvm_reg_block;
  `uvm_object_utils(traffic_light_block)

  // Registers

  // Sub-Blocks
  rand setup_block setup;

  function new (string name = "traffic_light_block");
    super.new(name, build_coverage(UVM_CVR_FIELD_VALS | UVM_CVR_ADDR_MAP));
  endfunction

  // Build all register and sub-block objects
  virtual function void build ();
    this.default_map = create_map("", 0, 1, UVM_LITTLE_ENDIAN);

    // Registers
    // Sub-Blocks
    this.setup = setup_block::type_id::create("setup",, get_full_name());
    this.setup.configure(this);
    this.setup.build();
    this.default_map.add_submap(this.setup.default_map, 6'h10);

    lock_model();
  endfunction

  function reregister();
    this.default_map.unregister();

    // Registers
    // Sub-Blocks
    this.default_map.add_submap(this.setup.default_map, 6'h10);

  endfunction
endclass"""
