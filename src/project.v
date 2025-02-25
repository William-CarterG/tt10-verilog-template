/*
 * Copyright (c) 2024 Modified Code
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_four_bit_adder_with_memory (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

    // Input assignments - IMPORTANT: Match exact bit order from test
    wire [3:0] a = ui_in[3:0];            // First 4-bit number
    wire [3:0] b = ui_in[7:4];            // Second 4-bit number
    wire mode = uio_in[0];                // Mode select: 0 = add two inputs, 1 = add input to stored result
    
    // Internal registers
    reg [4:0] stored_result;              // 5-bit register to store previous result
    
    // Wires for the adder
    wire [4:0] sum;                       // 5-bit sum result
    wire [3:0] carry;                     // Carry bits
    wire [3:0] second_operand;            // The second operand for addition
    
    // Select second operand based on mode
    assign second_operand = mode ? stored_result[3:0] : b;
    
    // Adder implementation
    full_adder fa0(a[0], second_operand[0], 1'b0, sum[0], carry[0]);
    full_adder fa1(a[1], second_operand[1], carry[0], sum[1], carry[1]);
    full_adder fa2(a[2], second_operand[2], carry[1], sum[2], carry[2]);
    full_adder fa3(a[3], second_operand[3], carry[2], sum[3], carry[3]);
    
    // Final carry becomes the MSB of the sum
    assign sum[4] = carry[3];
    
    // CRITICAL FIX: Assign sum directly to output (combinational path)
    // This ensures the sum appears immediately without waiting for the clock
    assign uo_out = {3'b000, sum};  // First 3 bits are unused, followed by 5-bit sum
    
    // Memory logic - store the result on each clock cycle
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            stored_result <= 5'b00000;    // Reset stored result
        end else begin
            stored_result <= sum;         // Store current sum
        end
    end
    
    // Provide current stored result as feedback through uio_out
    assign uio_out = {3'b000, stored_result};
    
    // Set uio_oe to enable output on uio_out pins, but keep uio_in[0] as input
    assign uio_oe = 8'b11111110;  // All pins are outputs EXCEPT uio_in[0]
    
    // Unused wire to avoid warnings
    wire _unused = &{ena, uio_in[7:1], 1'b0};
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