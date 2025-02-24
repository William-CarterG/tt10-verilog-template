/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_four_bit_multiplier_nasan016_npham2003 (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

    wire [3:0] m = ui_in [3:0];
    wire [3:0] q = ui_in [7:4];
    wire [12:0]temp_carry;
    wire [12:0]temp_adds;
    wire [7:0] p;
    
    assign p[0] = m[0] & q[0];

    full_adder f1((m[1] & q[0]), (m[0] & q[1]), 0, p[1], temp_carry[0]);
    full_adder f2((m[2] & q[0]), (m[1] & q[1]), temp_carry[0], temp_adds[0], temp_carry[1]);
    full_adder f3((m[3] & q[0]), (m[2] & q[1]), temp_carry[1], temp_adds[1], temp_carry[2]);
    full_adder f4(0, (m[3] & q[1]), temp_carry[2], temp_adds[2], temp_carry[3]);
    
    
    full_adder f5(temp_adds[0], (m[0] & q[2]), 0, p[2], temp_carry[4]);
    full_adder f6(temp_adds[1], (m[1] & q[2]), temp_carry[4], temp_adds[3], temp_carry[5]);
    full_adder f7(temp_adds[2], (m[2] & q[2]), temp_carry[5], temp_adds[4], temp_carry[6]);
    full_adder f8(temp_carry[3], (m[3] & q[2]), temp_carry[6], temp_adds[5], temp_carry[7]);
    
    full_adder f9(temp_adds[3], (m[0] & q[3]), 0, p[3], temp_carry[8]);
    full_adder f10(temp_adds[4], (m[1] & q[3]), temp_carry[8], p[4], temp_carry[9]);
    full_adder f11(temp_adds[5], (m[2] & q[3]), temp_carry[9], p[5], temp_carry[10]);
    full_adder f12(temp_carry[7], (m[3] & q[3]), temp_carry[10], p[6], p[7]);
    assign uo_out = p;
      assign uio_out = 0;
  assign uio_oe  = 0;

  // List all unused inputs to prevent warnings
  wire _unused = &{ena, clk, rst_n, uio_in, 1'b0};
endmodule



module full_adder (a, b, c, dout, carry);
    input a;
    input b;
    input c;
    output dout;
    output carry;

    assign dout = a ^ b ^ c;   
    assign carry = (a &b ) | (c & (a^b));
endmodule