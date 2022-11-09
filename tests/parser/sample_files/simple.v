module simple #(
  parameter integer WIDTH = 0,
  parameter         LEN = 0
) (
  input  wire clk_in,
  input       rst_low_in,
  input       test_in,
  output reg  test_out
);

  always @(posedge clk_in) begin
    if (!rst_low_in) begin
      test_out <= '0;
    end
    else begin
      test_out <= test_in;
    end
  end

endmodule