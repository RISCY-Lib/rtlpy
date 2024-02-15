/** subblock1_reg1 - UVM register model
 * Fields:
 */
class subblock1_reg1_reg extends uvm_reg;
  `uvm_object_utils(subblock1_reg1_reg)


  // CVR Field Vals Group
  covergroup cg_vals;
    option.per_instance = 1;

  endgroup

  // Create new register
  function new (string name = "subblock1_reg1_reg");
    super.new(name, 32, build_coverage(UVM_NO_COVERAGE));
    add_coverage(build_coverage(UVM_NO_COVERAGE));

    if (has_coverage(UVM_CVR_FIELD_VALS)) begin
      cg_vals = new();
      cg_vals.set_inst_name({get_full_name(), "_cg_vals"});
    end
  endfunction

  // Build all register field objects
  virtual function void build ();

    set_coverage(UVM_NO_COVERAGE);
  endfunction


  // The register sample function
  virtual function void sample_values();
    super.sample_values();

    if (has_coverage(UVM_CVR_FIELD_VALS))
      cg_vals.sample();
  endfunction
endclass

/** subblock1_reg2 - UVM register model
 * Fields:
 */
class subblock1_reg2_reg extends uvm_reg;
  `uvm_object_utils(subblock1_reg2_reg)


  // CVR Field Vals Group
  covergroup cg_vals;
    option.per_instance = 1;

  endgroup

  // Create new register
  function new (string name = "subblock1_reg2_reg");
    super.new(name, 32, build_coverage(UVM_NO_COVERAGE));
    add_coverage(build_coverage(UVM_NO_COVERAGE));

    if (has_coverage(UVM_CVR_FIELD_VALS)) begin
      cg_vals = new();
      cg_vals.set_inst_name({get_full_name(), "_cg_vals"});
    end
  endfunction

  // Build all register field objects
  virtual function void build ();

    set_coverage(UVM_NO_COVERAGE);
  endfunction


  // The register sample function
  virtual function void sample_values();
    super.sample_values();

    if (has_coverage(UVM_CVR_FIELD_VALS))
      cg_vals.sample();
  endfunction
endclass

/** subblock1 - UVM register model
 * Registers:
 *    subblock1_reg1 - Offset: 0
 *    subblock1_reg2 - Offset: 4
 * Sub-Blocks:
 */
class subblock1_block extends uvm_reg_block;
  `uvm_object_utils(subblock1_block)

  // Registers
       subblock1_reg1_reg subblock1_reg1;
       subblock1_reg2_reg subblock1_reg2;

  // Sub-Blocks

  function new (string name = "subblock1_block");
    super.new(name, build_coverage(UVM_NO_COVERAGE));
  endfunction

  // Build all register and sub-block objects
  virtual function void build ();
    this.default_map = create_map("", 0, 4, UVM_LITTLE_ENDIAN);

    // Registers
    this.subblock1_reg1 = subblock1_reg1_reg::type_id::create({get_name(), ".subblock1_reg1"},, get_full_name());
    this.subblock1_reg1.configure(this, null, "");
    this.subblock1_reg1.build();
    this.default_map.add_reg(this.subblock1_reg1, 32'h0);

    this.subblock1_reg2 = subblock1_reg2_reg::type_id::create({get_name(), ".subblock1_reg2"},, get_full_name());
    this.subblock1_reg2.configure(this, null, "");
    this.subblock1_reg2.build();
    this.default_map.add_reg(this.subblock1_reg2, 32'h4);

    // Sub-Blocks

    lock_model();
  endfunction

  function reregister();
    this.default_map.unregister();

    // Registers
    this.default_map.add_reg(this.subblock1_reg1, 32'h0);

    this.default_map.add_reg(this.subblock1_reg2, 32'h4);

    // Sub-Blocks

  endfunction
endclass

/** subblock2_reg1 - UVM register model
 * Fields:
 */
class subblock2_reg1_reg extends uvm_reg;
  `uvm_object_utils(subblock2_reg1_reg)


  // CVR Field Vals Group
  covergroup cg_vals;
    option.per_instance = 1;

  endgroup

  // Create new register
  function new (string name = "subblock2_reg1_reg");
    super.new(name, 32, build_coverage(UVM_NO_COVERAGE));
    add_coverage(build_coverage(UVM_NO_COVERAGE));

    if (has_coverage(UVM_CVR_FIELD_VALS)) begin
      cg_vals = new();
      cg_vals.set_inst_name({get_full_name(), "_cg_vals"});
    end
  endfunction

  // Build all register field objects
  virtual function void build ();

    set_coverage(UVM_NO_COVERAGE);
  endfunction


  // The register sample function
  virtual function void sample_values();
    super.sample_values();

    if (has_coverage(UVM_CVR_FIELD_VALS))
      cg_vals.sample();
  endfunction
endclass

/** subblock2_reg2 - UVM register model
 * Fields:
 */
class subblock2_reg2_reg extends uvm_reg;
  `uvm_object_utils(subblock2_reg2_reg)


  // CVR Field Vals Group
  covergroup cg_vals;
    option.per_instance = 1;

  endgroup

  // Create new register
  function new (string name = "subblock2_reg2_reg");
    super.new(name, 32, build_coverage(UVM_NO_COVERAGE));
    add_coverage(build_coverage(UVM_NO_COVERAGE));

    if (has_coverage(UVM_CVR_FIELD_VALS)) begin
      cg_vals = new();
      cg_vals.set_inst_name({get_full_name(), "_cg_vals"});
    end
  endfunction

  // Build all register field objects
  virtual function void build ();

    set_coverage(UVM_NO_COVERAGE);
  endfunction


  // The register sample function
  virtual function void sample_values();
    super.sample_values();

    if (has_coverage(UVM_CVR_FIELD_VALS))
      cg_vals.sample();
  endfunction
endclass

/** subblock2 - UVM register model
 * Registers:
 *    subblock2_reg1 - Offset: 0
 *    subblock2_reg2 - Offset: 4
 * Sub-Blocks:
 */
class subblock2_block extends uvm_reg_block;
  `uvm_object_utils(subblock2_block)

  // Registers
       subblock2_reg1_reg subblock2_reg1;
       subblock2_reg2_reg subblock2_reg2;

  // Sub-Blocks

  function new (string name = "subblock2_block");
    super.new(name, build_coverage(UVM_NO_COVERAGE));
  endfunction

  // Build all register and sub-block objects
  virtual function void build ();
    this.default_map = create_map("", 0, 4, UVM_LITTLE_ENDIAN);

    // Registers
    this.subblock2_reg1 = subblock2_reg1_reg::type_id::create({get_name(), ".subblock2_reg1"},, get_full_name());
    this.subblock2_reg1.configure(this, null, "");
    this.subblock2_reg1.build();
    this.default_map.add_reg(this.subblock2_reg1, 32'h0);

    this.subblock2_reg2 = subblock2_reg2_reg::type_id::create({get_name(), ".subblock2_reg2"},, get_full_name());
    this.subblock2_reg2.configure(this, null, "");
    this.subblock2_reg2.build();
    this.default_map.add_reg(this.subblock2_reg2, 32'h4);

    // Sub-Blocks

    lock_model();
  endfunction

  function reregister();
    this.default_map.unregister();

    // Registers
    this.default_map.add_reg(this.subblock2_reg1, 32'h0);

    this.default_map.add_reg(this.subblock2_reg2, 32'h4);

    // Sub-Blocks

  endfunction
endclass

/** page_reg - UVM register model
 * Fields:
 *    page - LSB: 0, Width: 4, Access: RW
 */
class page_reg_reg extends uvm_reg;
  `uvm_object_utils(page_reg_reg)

  rand uvm_reg_field page;

  // CVR Field Vals Group
  covergroup cg_vals;
    option.per_instance = 1;

    page: coverpoint page.value {
      bins vals[] = {[0:15]};
    }
  endgroup

  // Create new register
  function new (string name = "page_reg_reg");
    super.new(name, 32, build_coverage(UVM_NO_COVERAGE));
    add_coverage(build_coverage(UVM_NO_COVERAGE));

    if (has_coverage(UVM_CVR_FIELD_VALS)) begin
      cg_vals = new();
      cg_vals.set_inst_name({get_full_name(), "_cg_vals"});
    end
  endfunction

  // Build all register field objects
  virtual function void build ();
    this.page = uvm_reg_field::type_id::create("page",, get_full_name());

    this.page.configure(this, 4, 0, "RW", 0, 4'h0, 1, 1, 0);
    set_coverage(UVM_NO_COVERAGE);
  endfunction


  // The register sample function
  virtual function void sample_values();
    super.sample_values();

    if (has_coverage(UVM_CVR_FIELD_VALS))
      cg_vals.sample();
  endfunction
endclass

/** test_paged_block - UVM register model
 * Registers:
 * Sub-Blocks:
 *    subblock1 - Offset: 0
 *    subblock2[4] - Offset: 16
 */
class test_paged_block_block extends uvm_reg_block;
  `uvm_object_utils(test_paged_block_block)

  // Maps
       uvm_reg_map subblock1_map;
       uvm_reg_map subblock2_map[4];


  // Registers
  rand page_reg_reg page_reg;


  // Sub-Blocks
       subblock1_block subblock1;
       subblock2_block subblock2[4];

  // Constructor
  function new (string name = "test_paged_block_block");
    super.new(name, build_coverage(UVM_NO_COVERAGE));
  endfunction

  virtual function void _add_registers(uvm_reg_map map);
    // Page Register
    map.add_reg(this.page_reg, 32'h100);

    // Registers
  endfunction

  // Build all register and sub-block objects
  virtual function void build ();
    this.default_map = create_map("", 0, 4, UVM_LITTLE_ENDIAN);

    // Page Register
    this.page_reg = page_reg_reg::type_id::create("page_reg",, get_full_name());
    this.page_reg.configure(this, null, "");
    this.page_reg.build();

    // Registers

    // Sub-Blocks
    this.subblock1 = subblock1_block::type_id::create("subblock1",, get_full_name());
    this.subblock1.configure(this);
    this.subblock1.build();
    this.subblock1_map = create_map("subblock1_map", 0, 4, UVM_LITTLE_ENDIAN);
    this._add_registers(subblock1_map);
    this.subblock1_map.add_submap(this.subblock1.default_map, 0);

    this.subblock2[0] = subblock2_block::type_id::create("subblock2[0]",, get_full_name());
    this.subblock2[0].configure(this);
    this.subblock2[0].build();
    this.subblock2_map[0] = create_map("subblock2_map[0]", 0, 4, UVM_LITTLE_ENDIAN);
    this._add_registers(subblock2_map[0]);
    this.subblock2_map[0].add_submap(this.subblock2[0].default_map, 0);

    this.subblock2[1] = subblock2_block::type_id::create("subblock2[1]",, get_full_name());
    this.subblock2[1].configure(this);
    this.subblock2[1].build();
    this.subblock2_map[1] = create_map("subblock2_map[1]", 0, 4, UVM_LITTLE_ENDIAN);
    this._add_registers(subblock2_map[1]);
    this.subblock2_map[1].add_submap(this.subblock2[1].default_map, 0);

    this.subblock2[2] = subblock2_block::type_id::create("subblock2[2]",, get_full_name());
    this.subblock2[2].configure(this);
    this.subblock2[2].build();
    this.subblock2_map[2] = create_map("subblock2_map[2]", 0, 4, UVM_LITTLE_ENDIAN);
    this._add_registers(subblock2_map[2]);
    this.subblock2_map[2].add_submap(this.subblock2[2].default_map, 0);

    this.subblock2[3] = subblock2_block::type_id::create("subblock2[3]",, get_full_name());
    this.subblock2[3].configure(this);
    this.subblock2[3].build();
    this.subblock2_map[3] = create_map("subblock2_map[3]", 0, 4, UVM_LITTLE_ENDIAN);
    this._add_registers(subblock2_map[3]);
    this.subblock2_map[3].add_submap(this.subblock2[3].default_map, 0);


    // Add default Sub-Block
    this.default_map = this.subblock1_map;
    lock_model();
  endfunction

  function set_map_sequencer(uvm_sequencer_base sqr, uvm_reg_adapter adapter = null);
    this.subblock1_map.set_sequencer(sqr, adapter);
    this.subblock2_map[0].set_sequencer(sqr, adapter);
    this.subblock2_map[1].set_sequencer(sqr, adapter);
    this.subblock2_map[2].set_sequencer(sqr, adapter);
    this.subblock2_map[3].set_sequencer(sqr, adapter);

    this.default_map.set_sequencer(sqr, adapter);

  endfunction

  function set_map_auto_predict(bit on = 1);
    this.subblock1_map.set_auto_predict(.on(on));
    this.subblock2_map[0].set_auto_predict(.on(on));
    this.subblock2_map[1].set_auto_predict(.on(on));
    this.subblock2_map[2].set_auto_predict(.on(on));
    this.subblock2_map[3].set_auto_predict(.on(on));

    this.default_map.set_auto_predict(.on(on));

  endfunction

  function set_map_check_on_read(bit on = 1);
    this.subblock1_map.set_check_on_read(.on(on));
    this.subblock2_map[0].set_check_on_read(.on(on));
    this.subblock2_map[1].set_check_on_read(.on(on));
    this.subblock2_map[2].set_check_on_read(.on(on));
    this.subblock2_map[3].set_check_on_read(.on(on));

    this.default_map.set_check_on_read(.on(on));

  endfunction

  task page_subblock1();
    uvm_status_e status;
    uvm_reg_predictor#(uvm_sequence_item) pred;

    unlock_model();

    this.default_map = this.subblock1_map;

    if (!uvm_config_db #(uvm_reg_predictor#(uvm_sequence_item))::get(null, "", "ral_pred", pred) )
      `uvm_fatal("CONFIG_LOAD", $sformatf("Cannot get() configuration %s from uvm_config_db. Have you set() it?", "ral_pred") )

    pred.map = this.default_map;

    lock_model();
    if (!is_locked()) begin
      `uvm_warning("RAL", "Reg Model Not Locked!")
    end

    this.page_reg.write(status, 0);
  endtask

  task page_subblock2(int idx, uvm_sequence_base parent = null);
    uvm_status_e status;
    uvm_reg_predictor#(uvm_sequence_item) pred;

    unlock_model();

    this.default_map = this.subblock2_map[idx];

    if (!uvm_config_db #(uvm_reg_predictor#(uvm_sequence_item))::get(null, "", "ral_pred", pred) )
      `uvm_fatal("CONFIG_LOAD", $sformatf("Cannot get() configuration %s from uvm_config_db. Have you set() it?", "ral_pred") )

    pred.map = this.default_map;

    lock_model();
    if (!is_locked()) begin
      `uvm_warning("RAL", "Reg Model Not Locked!")
    end

    this.page_reg.write(status, 16 + idx);
  endtask


  task page(ref uvm_reg_block blk);
    if (blk == this.subblock1) page_subblock1();
    else if (blk == this.subblock2[0]) page_subblock2(0);
    else if (blk == this.subblock2[1]) page_subblock2(1);
    else if (blk == this.subblock2[2]) page_subblock2(2);
    else if (blk == this.subblock2[3]) page_subblock2(3);
    else `uvm_error("RAL", $sformatf("Unknown block %s", blk.get_full_name()))
  endtask
endclass