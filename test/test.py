# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_four_bit_adder(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test 4-bit adder behavior")

    # TEST 1: 2 + 1 = 3
    dut._log.info("TEST 1: 2 + 1 = 3")
    # 0001 (1) in lower 4 bits, 0010 (2) in upper 4 bits
    dut.ui_in.value = 0b00100001
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0b00000011  # Expected result: 3 (binary 00000011)

    # TEST 2: 7 + 8 = 15
    dut._log.info("TEST 2: 7 + 8 = 15")
    # 0111 (7) in lower 4 bits, 1000 (8) in upper 4 bits
    dut.ui_in.value = 0b10000111
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0b00001111  # Expected result: 15 (binary 00001111)

    # TEST 3: 15 + 15 = 30
    dut._log.info("TEST 3: 15 + 15 = 30")
    # 1111 (15) in lower 4 bits, 1111 (15) in upper 4 bits
    dut.ui_in.value = 0b11111111
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0b00011110  # Expected result: 30 (binary 00011110)

    # TEST 4: 0 + 0 = 0
    dut._log.info("TEST 4: 0 + 0 = 0")
    # 0000 (0) in lower 4 bits, 0000 (0) in upper 4 bits
    dut.ui_in.value = 0b00000000
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0b00000000  # Expected result: 0 (binary 00000000)

    # TEST 5: 10 + 5 = 15
    dut._log.info("TEST 5: 10 + 5 = 15")
    # 0101 (5) in lower 4 bits, 1010 (10) in upper 4 bits
    dut.ui_in.value = 0b10100101
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0b00001111  # Expected result: 15 (binary 00001111)

    # TEST 6: 3 + 12 = 15
    dut._log.info("TEST 6: 3 + 12 = 15")
    # 0011 (3) in lower 4 bits, 1100 (12) in upper 4 bits
    dut.ui_in.value = 0b11000011
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0b00001111  # Expected result: 15 (binary 00001111)

    # TEST 7: 8 + 8 = 16
    dut._log.info("TEST 7: 8 + 8 = 16")
    # 1000 (8) in lower 4 bits, 1000 (8) in upper 4 bits
    dut.ui_in.value = 0b10001000
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0b00010000  # Expected result: 16 (binary 00010000)

    dut._log.info("All tests passed!")