# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer


@cocotb.test()
async def test_four_bit_adder_with_memory_comprehensive(dut):
    dut._log.info("Starting comprehensive test for 4-bit adder with memory")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset the device
    dut._log.info("Initial reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    # ----- BASIC OPERATION TESTS (MODE 0) -----
    dut._log.info("== Testing basic mode 0 operations ==")
    
    # Test case 1: Simple addition (2 + 3 = 5)
    dut._log.info("Test 1: 2 + 3 = 5 (mode 0)")
    dut.ui_in.value = 0b00110010  # b=3, a=2
    dut.uio_in.value = 0b00000000  # Mode 0
    await Timer(1, units="us")  # Small delay for simulation stability
    assert dut.uo_out.value == 0b00000101, f"Test 1 failed: Expected 5, got {dut.uo_out.value}"
    await ClockCycles(dut.clk, 1)  # Store result

    # ----- MEMORY OPERATION TESTS (MODE 1) -----
    dut._log.info("== Testing mode 1 operations (memory/accumulation) ==")
    
    # Test case 2: Add to stored result (5 + 4 = 9)
    dut._log.info("Test 2: 5 + 4 = 9 (mode 1)")
    dut.ui_in.value = 0b00000100  # a=4
    dut.uio_in.value = 0b00000001  # Mode 1
    await Timer(1, units="us")
    assert dut.uo_out.value == 0b00001001, f"Test 2 failed: Expected 9, got {dut.uo_out.value}"
    await ClockCycles(dut.clk, 1)  # Store result

    # Test case 3: Continue adding (9 + 7 = 16)
    dut._log.info("Test 3: 9 + 7 = 16 (mode 1)")
    dut.ui_in.value = 0b00000111  # a=7
    dut.uio_in.value = 0b00000001  # Mode 1
    await Timer(1, units="us")
    assert dut.uo_out.value == 0b00010000, f"Test 3 failed: Expected 16, got {dut.uo_out.value}"
    await ClockCycles(dut.clk, 1)  # Store result

    # ----- EDGE CASES -----
    dut._log.info("== Testing edge cases ==")
    
    # Reset for edge case testing
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)

    # Test case 4: Adding zero (0 + 0 = 0)
    dut._log.info("Test 4: 0 + 0 = 0 (mode 0)")
    dut.ui_in.value = 0b00000000  # b=0, a=0
    dut.uio_in.value = 0b00000000  # Mode 0
    await Timer(1, units="us")
    assert dut.uo_out.value == 0b00000000, f"Test 4 failed: Expected 0, got {dut.uo_out.value}"
    await ClockCycles(dut.clk, 1)  # Store result

    # Test case 5: Maximum input values (15 + 15 = 30)
    dut._log.info("Test 5: 15 + 15 = 30 (mode 0)")
    dut.ui_in.value = 0b11111111  # b=15, a=15
    dut.uio_in.value = 0b00000000  # Mode 0
    await Timer(1, units="us")
    assert dut.uo_out.value == 0b00011110, f"Test 5 failed: Expected 30, got {dut.uo_out.value}"
    await ClockCycles(dut.clk, 1)  # Store result

    # Test case 6: Test upper limit of 4-bit inputs (15 + 1 = 16, carry bit)
    dut._log.info("Test 6: 14 + 1 = 15 (mode 1) - Testing carry bit")
    dut.ui_in.value = 0b00000001  # a=1
    dut.uio_in.value = 0b00000001  # Mode 1 (add to stored 15)
    await Timer(1, units="us")
    assert dut.uo_out.value == 0b00001111, f"Test 6 failed: Expected 15 (with carry bit), got {dut.uo_out.value}"
    await ClockCycles(dut.clk, 1)  # Store result

    # Test case 6.1: Test upper limit of 4-bit inputs (15 + 1 = 16, carry bit)
    dut._log.info("Test 6: 15 + 1 = 16 (mode 1) - Testing carry bit")
    dut.ui_in.value = 0b00000001  # a=1
    dut.uio_in.value = 0b00000001  # Mode 1 (add to stored 15)
    await Timer(1, units="us")
    assert dut.uo_out.value == 0b00010000, f"Test 6.1 failed: Expected 16 (with carry bit), got {dut.uo_out.value}"
    await ClockCycles(dut.clk, 1)  # Store result

    # ----- OVERFLOW TESTING -----
    dut._log.info("== Testing 4-bit overflow behavior ==")
    
    # Test case 7: 4-bit overflow (add 15+15=30, then add 7 more to get 30+7=37)
    # Since 37 = 32 + 5, and we can only represent 5 bits, we should get 5 (00101)
    dut._log.info("Test 7: 16 + 15 = 31, then 31 + 7 = 38 (4-bit overflow)")
    
    # First reset to clear
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)
    
    # Add 15 + 15 = 30
    dut.ui_in.value = 0b11111111  # b=15, a=15
    dut.uio_in.value = 0b00000000  # Mode 0
    await Timer(1, units="us")
    assert dut.uo_out.value == 0b00011110, f"Test 7a failed: Expected 30, got {dut.uo_out.value}"
    await ClockCycles(dut.clk, 1)  # Store result
    
    # Now add 7 more: 14 + 7 = 21, but in 5 bits this will be 5 (00101)
    dut.ui_in.value = 0b00000111  # a=7
    dut.uio_in.value = 0b00000001  # Mode 1
    await Timer(1, units="us")
    # 37 in binary is 100101, but we only keep 5 bits so it's 00101 (5)
    assert dut.uo_out.value == 0b00010101, f"Test 7b failed: Expected 5 (overflow from 37), got {dut.uo_out.value}"
    await ClockCycles(dut.clk, 1)  # Store result

    # Test case 8: Verify stored result after overflow
    dut._log.info("Test 8: Check stored result is 4 least significant bits after overflow")
    dut.ui_in.value = 0b00000010  # a=2
    dut.uio_in.value = 0b00000001  # Mode 1
    await Timer(1, units="us")
    # Should be 0 + 2 = 2
    assert dut.uo_out.value == 0b00000111, f"Test 8 failed: Expected 2, got {dut.uo_out.value}"
    await ClockCycles(dut.clk, 1)  # Store result

    # ----- MODE SWITCHING TESTS -----
    dut._log.info("== Testing mode switching ==")
    
    # Reset again
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 2)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)
    
    # Test case 9: First store a value in mode 0
    dut._log.info("Test 9: Store 12 in mode 0")
    dut.ui_in.value = 0b10000100  # b=4, a=8
    dut.uio_in.value = 0b00000000  # Mode 0
    await Timer(1, units="us")
    assert dut.uo_out.value == 0b00001100, f"Test 9 failed: Expected 12, got {dut.uo_out.value}"
    await ClockCycles(dut.clk, 1)  # Store result

    # Test case 10: Switch to mode 1 and add a value
    dut._log.info("Test 10: Add to stored 12 in mode 1")
    dut.ui_in.value = 0b00000011  # a=3
    dut.uio_in.value = 0b00000001  # Mode 1
    await Timer(1, units="us")
    assert dut.uo_out.value == 0b00001111, f"Test 10 failed: Expected 15, got {dut.uo_out.value}"
    await ClockCycles(dut.clk, 1)  # Store result
    
    # Test case 11: Switch back to mode 0
    dut._log.info("Test 11: Switch back to mode 0")
    dut.ui_in.value = 0b00100001  # b=2, a=1
    dut.uio_in.value = 0b00000000  # Mode 0
    await Timer(1, units="us")
    assert dut.uo_out.value == 0b00000011, f"Test 11 failed: Expected 3, got {dut.uo_out.value}"
    await ClockCycles(dut.clk, 1)  # Store result
    
    # ----- RESET DURING OPERATION TEST -----
    dut._log.info("== Testing reset during operation ==")
    
    # Test case 12: Start adding
    dut._log.info("Test 12: Start accumulating")
    dut.ui_in.value = 0b10001000  # b=8, a=8
    dut.uio_in.value = 0b00000000  # Mode 0
    await Timer(1, units="us")
    assert dut.uo_out.value == 0b00010000, f"Test 12 failed: Expected 16, got {dut.uo_out.value}"
    # Start clock cycle but don't finish it
    await Timer(5, units="us")  # Half a clock cycle (clock period is 10us)
    
    # Test case 13: Reset midway
    dut._log.info("Test 13: Reset during operation")
    dut.rst_n.value = 0  # Reset
    await Timer(5, units="us")  # Complete the clock cycle
    
    # Verify reset worked
    assert dut.uio_out.value == 0b00000000, f"Test 13 failed: Expected 0 after reset, got {dut.uio_out.value}"
    
    # Release reset and verify state
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)
    dut.ui_in.value = 0b00000001  # a=1
    dut.uio_in.value = 0b00000001  # Mode 1 (should add to 0)
    await Timer(1, units="us")
    assert dut.uo_out.value == 0b00000001, f"Test 13 failed: Expected 1, got {dut.uo_out.value}"

    dut._log.info("All tests passed successfully!")