/** control - UVM register model
 * Fields:
 *    mod_en - LSB: 0, Width: 1, Access: RW
 *    blink_yellow - LSB: 1, Width: 1, Access: RW
 *    blink_red - LSB: 2, Width: 1, Access: RW
 *    profile - LSB: 3, Width: 1, Access: RW
 */
class reg_control extends uvm_reg;
  `uvm_object_utils(reg_control)

       uvm_reg_field mod_en;
  rand uvm_reg_field blink_yellow;
  rand uvm_reg_field blink_red;
  rand uvm_reg_field profile;

  function new(string name = "reg_control");
    super.new(name, 32, build_coverage(UVM_NO_COVERAGE))
  endfunction

  // Build all register field objects
  virtual function void build();
    this.mod_en = uvm_reg_field::type_id::create("mod_en",, get_full_name());
    this.blink_yellow = uvm_reg_field::type_id::create("blink_yellow",, get_full_name());
    this.blink_red = uvm_reg_field::type_id::create("blink_red",, get_full_name());
    this.profile = uvm_reg_field::type_id::create("profile",, get_full_name());

    this.mod_en.configure(this, 1, 0, "RW", 0, 1'h0, 1, 0, 0);
    this.blink_yellow.configure(this, 1, 1, "RW", 0, 1'h0, 1, 1, 0);
    this.blink_red.configure(this, 1, 2, "RW", 0, 1'h0, 1, 1, 0);
    this.profile.configure(this, 1, 3, "RW", 0, 1'h0, 1, 1, 0);
  endfunction
endclass