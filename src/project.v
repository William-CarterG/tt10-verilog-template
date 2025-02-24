/*
 * Copyright (c) 2024 Modified Code
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_four_bit_adder (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

    wire [3:0] a = ui_in [3:0];   // First 4-bit number
    wire [3:0] b = ui_in [7:4];   // Second 4-bit number
    wire [4:0] sum;               // 5-bit sum result
    wire [3:0] carry;             // Carry bits
    
    // First bit addition
    full_adder fa0(a[0], b[0], 1'b0, sum[0], carry[0]);
    
    // Second bit addition
    full_adder fa1(a[1], b[1], carry[0], sum[1], carry[1]);
    
    // Third bit addition
    full_adder fa2(a[2], b[2], carry[1], sum[2], carry[2]);
    
    // Fourth bit addition
    full_adder fa3(a[3], b[3], carry[2], sum[3], carry[3]);
    
    // Final carry becomes the MSB of the sum
    assign sum[4] = carry[3];
    
    // Connect sum to output
    assign uo_out = {3'b000, sum};  // First 3 bits are unused, followed by 5-bit sum
    
    // Unused outputs
    assign uio_out = 0;
    assign uio_oe = 0;

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
    assign carry = (a & b) | (c & (a ^ b));
endmodule