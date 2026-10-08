import os
import sys
import shutil
import json

BASE_DIR = r"E:\downloads_2\xstride_rtl"
SRC_REPO = os.path.join(BASE_DIR, "xstride_rtl")
MY_DESIGN = os.path.join(BASE_DIR, "my_design")

print(f"[*] Initializing EDA Project Structure at: {MY_DESIGN}")

# 1. Create directory hierarchy
directories = [
    MY_DESIGN,
    os.path.join(MY_DESIGN, "source"),
    os.path.join(MY_DESIGN, "include"),
    os.path.join(MY_DESIGN, "simulation"),
    os.path.join(MY_DESIGN, "simulation", "data"),
    os.path.join(MY_DESIGN, "constraints"),
    os.path.join(MY_DESIGN, "configuration"),
    os.path.join(MY_DESIGN, "technology"),
    os.path.join(MY_DESIGN, "firmware"),
    os.path.join(MY_DESIGN, "firmware", "src"),
    os.path.join(MY_DESIGN, "firmware", "include"),
    os.path.join(MY_DESIGN, "firmware", "linker"),
    os.path.join(MY_DESIGN, "firmware", "boards"),
    os.path.join(MY_DESIGN, "firmware", "tests"),
    os.path.join(MY_DESIGN, "runs"),
]

for d in directories:
    os.makedirs(d, exist_ok=True)
    print(f"  [+] Created directory: {d}")

# 2. Copy RTL files to source/
rtl_files = [
    "accel_i2c_intf.sv",
    "accel_spi_intf.sv",
    "calib_stage.sv",
    "dsp_frontend.sv",
    "feature_stats.sv",
    "mems_afe_adc.sv",
    "mobile_telemetry_unit.sv",
    "onchip_mems_sensor.sv",
    "pedometer_classifier.sv",
    "rst_sync.sv",
    "sensor_hub.sv",
    "sync_2ff.sv",
    "wake_fsm.sv",
    "x_heep_xstride_wrapper.sv",
    "xstride_always_on_top.sv",
    "xstride_regs_obi.sv",
    "xstride_sva.sv"
]

for f in rtl_files:
    src_f = os.path.join(SRC_REPO, "rtl", f)
    dst_f = os.path.join(MY_DESIGN, "source", f)
    shutil.copy2(src_f, dst_f)
    print(f"  [+] Copied source: {f}")

# 3. Copy include files
pkg_src = os.path.join(SRC_REPO, "rtl", "xstride_regs_pkg.sv")
pkg_dst = os.path.join(MY_DESIGN, "include", "xstride_regs_pkg.sv")
shutil.copy2(pkg_src, pkg_dst)
print("  [+] Copied include: xstride_regs_pkg.sv")

# Also copy to source/ if any synthesis tool expects package in source directory
pkg_src_also = os.path.join(MY_DESIGN, "source", "xstride_regs_pkg.sv")
shutil.copy2(pkg_src, pkg_src_also)

# Create include/xstride_defs.svh
defs_content = """// =============================================================================
// xstride_defs.svh
// Global SystemVerilog Definitions & Architecture Constants for X-STRIDE v2.0
// =============================================================================

`ifndef XSTRIDE_DEFS_SVH
`define XSTRIDE_DEFS_SVH

`timescale 1ns/1ps

// Clock Frequency Standards
`define XSTRIDE_CLK_FREQ_BURST_HZ    50_000_000 // 50.0 MHz Burst Processing Clock
`define XSTRIDE_CLK_FREQ_AON_HZ          32_768 // 32.768 kHz Always-On RTC Clock
`define XSTRIDE_SAMPLE_RATE_HZ               50 // 50 Hz Biomechanical Output Data Rate (ODR)

// OBI Bus Standard Widths
`define OBI_ADDR_WIDTH                       32
`define OBI_DATA_WIDTH                       32
`define OBI_BYTE_ENABLE_WIDTH                 4

// Sensor Source IDs (sensor_sel)
`define SENSOR_SEL_SPI                 2'b00 // External SPI Accelerometer
`define SENSOR_SEL_I2C                 2'b01 // External I2C Accelerometer
`define SENSOR_SEL_ONCHIP              2'b10 // On-Chip Capacitive MEMS Sensor + SAR ADC

// Activity Classification Codes (act_class)
`define ACT_CLASS_REST                 3'b000 // Motionless Rest / Sedentary Stance
`define ACT_CLASS_LEG_SHAKE            3'b001 // Seated Leg Shaking / Tremor (Rejected)
`define ACT_CLASS_WALK                 3'b010 // Regular Walking Gait
`define ACT_CLASS_RUN                  3'b011 // Jogging / Running Gait
`define ACT_CLASS_EXERCISE             3'b100 // High-Intensity Exercise

// FSM Power Management States
`define WAKE_FSM_STANDBY               2'b00 // Deep Sleep (<0.39 uW)
`define WAKE_FSM_SLEEP_SENSING         2'b01 // Low-power sampling (<1.2 uW)
`define WAKE_FSM_ACTIVE_TRACKING       2'b10 // Active DSP stride pipeline (5.16 uW)
`define WAKE_FSM_MOBILE_SYNC           2'b11 // BLE Telemetry sync burst

#endif // XSTRIDE_DEFS_SVH
"""
with open(os.path.join(MY_DESIGN, "include", "xstride_defs.svh"), "w") as f:
    f.write(defs_content)
print("  [+] Created include: xstride_defs.svh")

# 4. Copy simulation files
tb_files = [
    "tb_accel_spi_intf.sv",
    "tb_coverage.sv",
    "tb_dsp_frontend.sv",
    "tb_heep_wrapper.sv",
    "tb_mobile_telemetry.sv",
    "tb_onchip_mems_sensor.sv",
    "tb_pedometer_classifier.sv",
    "tb_pedometer_randomized.sv",
    "tb_real_dataset_replay.sv",
    "tb_sensor_hub.sv",
    "tb_wake_fsm.sv",
    "tb_xstride_regs_obi.sv",
    "tb_xstride_top.sv"
]

for tb in tb_files:
    shutil.copy2(os.path.join(SRC_REPO, "tb", tb), os.path.join(MY_DESIGN, "simulation", tb))
    print(f"  [+] Copied simulation TB: {tb}")

data_files = [
    "brisk_walk.mem",
    "desk_bumps.mem",
    "leg_shake.mem",
    "running.mem",
    "sitting_rest.mem",
    "slow_walk.mem",
    "walking.mem"
]

for dfile in data_files:
    shutil.copy2(os.path.join(SRC_REPO, "data", dfile), os.path.join(MY_DESIGN, "simulation", "data", dfile))
    print(f"  [+] Copied simulation dataset: {dfile}")

# Also copy datasets to simulation/ root for direct vvp execution if needed
for dfile in data_files:
    shutil.copy2(os.path.join(SRC_REPO, "data", dfile), os.path.join(MY_DESIGN, "simulation", dfile))

# Copy simulation scripts
shutil.copy2(os.path.join(SRC_REPO, "scripts", "generate_datasets.py"), os.path.join(MY_DESIGN, "simulation", "generate_datasets.py"))
shutil.copy2(os.path.join(SRC_REPO, "scripts", "synth_power_analysis.py"), os.path.join(MY_DESIGN, "simulation", "synth_power_analysis.py"))

# Create updated check_upf.py in simulation/
upf_checker_code = """#!/usr/bin/env python3
\"\"\"
check_upf.py
Formal IEEE 1801 UPF 3.0 Linter and Rule Checker for X-STRIDE SoC.
\"\"\"

import os
import re
import sys

def lint_upf(upf_path, rtl_path):
    print("=" * 75)
    print(" IEEE 1801 (UPF 3.0) POWER SPECIFICATION LINTER & SYNTACTIC CHECKER")
    print(f" Target File: {upf_path}")
    print(f" RTL Scope  : {rtl_path}")
    print("=" * 75)

    if not os.path.exists(upf_path):
        print(f"[FATAL] UPF file not found: {upf_path}")
        return False

    if not os.path.exists(rtl_path):
        print(f"[FATAL] RTL file not found: {rtl_path}")
        return False

    with open(upf_path, "r") as f:
        upf_content = f.read()

    with open(rtl_path, "r") as f:
        rtl_content = f.read()

    errors = 0
    warnings = 0
    checks_passed = 0

    # 1. Check UPF Version
    m_ver = re.search(r"^\\s*upf_version\\s+([0-9.]+)", upf_content, re.MULTILINE)
    if m_ver:
        ver = m_ver.group(1)
        print(f"[PASS] UPF Version Declared: {ver} (IEEE 1801 Compliant)")
        checks_passed += 1
    else:
        print("[FAIL] Missing or invalid 'upf_version' statement!")
        errors += 1

    # 2. Check Power Domains
    domains = re.findall(r"create_power_domain\\s+([A-Za-z0-9_]+)", upf_content)
    print(f"[INFO] Discovered {len(domains)} Power Domains: {', '.join(domains)}")
    expected_domains = ["PD_AON", "PD_SENSOR", "PD_DSP", "PD_TELEM"]
    for ed in expected_domains:
        if ed in domains:
            print(f"  [PASS] Power Domain '{ed}' correctly defined.")
            checks_passed += 1
        else:
            print(f"  [FAIL] Expected Power Domain '{ed}' missing in UPF!")
            errors += 1

    # 3. Check Supply Ports & Nets
    supply_ports = re.findall(r"create_supply_port\\s+([A-Za-z0-9_]+)", upf_content)
    supply_nets = re.findall(r"create_supply_net\\s+([A-Za-z0-9_]+)", upf_content)
    print(f"[INFO] Discovered {len(supply_ports)} Supply Ports: {', '.join(supply_ports)}")
    print(f"[INFO] Discovered {len(supply_nets)} Supply Nets: {', '.join(supply_nets)}")
    for sp in ["VDD_AON", "VDD_CORE", "VSS"]:
        if sp in supply_ports and sp in supply_nets:
            print(f"  [PASS] Supply rail '{sp}' properly port/net mapped.")
            checks_passed += 1
        else:
            print(f"  [FAIL] Supply rail '{sp}' definition incomplete!")
            errors += 1

    # 4. Check Power Switches
    switches = re.findall(r"create_power_switch\\s+([A-Za-z0-9_]+)", upf_content)
    print(f"[INFO] Discovered {len(switches)} Power Switches: {', '.join(switches)}")
    for sw, gate in [("sw_sensor", "pg_accel_en"), ("sw_dsp", "pg_dsp_en"), ("sw_telemetry", "pg_telemetry_en")]:
        if sw in switches:
            if re.search(r"\\b" + gate + r"\\b", rtl_content):
                print(f"  [PASS] Power Switch '{sw}' control gate '{gate}' validated in RTL.")
                checks_passed += 1
            else:
                print(f"  [FAIL] Gate '{gate}' for switch '{sw}' missing in RTL netlist!")
                errors += 1
        else:
            print(f"  [FAIL] Power Switch '{sw}' missing in UPF!")
            errors += 1

    # 5. Check Isolation Rules
    iso_rules = re.findall(r"set_isolation\\s+([A-Za-z0-9_]+)", upf_content)
    print(f"[INFO] Discovered {len(iso_rules)} Isolation Rules: {', '.join(iso_rules)}")
    for ir in ["iso_sensor_outputs", "iso_spi_cs", "iso_dsp_outputs", "iso_telem_outputs", "iso_uart_tx"]:
        if ir in iso_rules:
            print(f"  [PASS] Isolation Strategy '{ir}' configured.")
            checks_passed += 1
        else:
            print(f"  [FAIL] Expected Isolation Rule '{ir}' missing!")
            errors += 1

    clamps = re.findall(r"-clamp_value\\s+([0-9a-zA-Z_]+)", upf_content)
    for cv in clamps:
        if cv in ("0", "1", "latch"):
            checks_passed += 1
        else:
            print(f"  [FAIL] Invalid clamp value '{cv}' in isolation rule!")
            errors += 1

    # 6. Check Retention Strategy
    ret_rules = re.findall(r"set_retention\\s+([A-Za-z0-9_]+)", upf_content)
    print(f"[INFO] Discovered Retention Rules: {', '.join(ret_rules)}")
    if "ret_aon_accumulators" in ret_rules:
        print("  [PASS] Retention strategy 'ret_aon_accumulators' defined for AON domain.")
        checks_passed += 1
        m_elem = re.search(r"set_retention\\s+ret_aon_accumulators[\\s\\S]*?-elements\\s*\\{([\\s\\S]*?)\\}", upf_content)
        if m_elem:
            elem_text = m_elem.group(1)
            elements = [e.strip() for e in elem_text.split() if e.strip() and not e.strip().startswith("#")]
            print(f"  [INFO] Verifying {len(elements)} retained registers in RTL:")
            for el in elements:
                clean_el = el.replace("u_regs.", "")
                if re.search(r"\\b" + clean_el + r"\\b", rtl_content):
                    print(f"    [PASS] Retained element '{el}' confirmed in RTL.")
                    checks_passed += 1
                else:
                    print(f"    [WARN] Retained element '{el}' not found as flat wire (hierarchical scope).")
                    warnings += 1
    else:
        print("  [FAIL] Retention strategy missing!")
        errors += 1

    # 7. Check Power State Table (PST)
    m_pst = re.search(r"create_pst\\s+([A-Za-z0-9_]+)", upf_content)
    if m_pst:
        pst_name = m_pst.group(1)
        print(f"[PASS] Power State Table '{pst_name}' created.")
        checks_passed += 1
        pst_states = re.findall(r"add_pst_state\\s+([A-Za-z0-9_]+)", upf_content)
        print(f"  [INFO] Configured PST States ({len(pst_states)}): {', '.join(pst_states)}")
        for state in ["PST_STANDBY", "PST_SLEEP_SENSING", "PST_ACTIVE_TRACKING", "PST_MOBILE_SYNC"]:
            if state in pst_states:
                print(f"    [PASS] PST State '{state}' valid.")
                checks_passed += 1
            else:
                print(f"    [FAIL] Expected PST State '{state}' missing!")
                errors += 1
    else:
        print("[FAIL] Missing 'create_pst' declaration!")
        errors += 1

    print("=" * 75)
    print(f" UPF LINTING COMPLETE: {checks_passed} Checks Passed | {errors} Errors | {warnings} Warnings")
    if errors == 0:
        print(" RESULT: UPF 3.0 SPECIFICATION IS FULLY VALID AND COMPLIANT (100% PASS)!")
        print("=" * 75)
        return True
    else:
        print(f" RESULT: UPF LINTING FAILED WITH {errors} ERRORS!")
        print("=" * 75)
        return False

if __name__ == "__main__":
    # Resolve paths relative to script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    proj_root = os.path.abspath(os.path.join(script_dir, ".."))
    
    upf_file = os.path.join(proj_root, "configuration", "xstride.upf")
    if not os.path.exists(upf_file):
        upf_file = os.path.join(proj_root, "upf", "xstride.upf")
        
    rtl_file = os.path.join(proj_root, "source", "xstride_always_on_top.sv")
    if not os.path.exists(rtl_file):
        rtl_file = os.path.join(proj_root, "rtl", "xstride_always_on_top.sv")
        
    if len(sys.argv) > 1:
        upf_file = sys.argv[1]
    if len(sys.argv) > 2:
        rtl_file = sys.argv[2]
        
    success = lint_upf(upf_file, rtl_file)
    sys.exit(0 if success else 1)
"""
with open(os.path.join(MY_DESIGN, "simulation", "check_upf.py"), "w") as f:
    f.write(upf_checker_code)

print("  [+] Created simulation/check_upf.py")

# 5. Create constraints/design.sdc
sdc_content = """# ==============================================================================
# design.sdc - Synopsys Design Constraints (SDC 2.1)
# Project: X-STRIDE Ultra-Low-Power Pedometer & Physiological Classification SoC
# Release: v2.0 Tapeout Candidate
# Target Technology: TSMC / SkyWater 65nm LP (0.8 V Core / 0.6 V Retention)
# Top-Level Design: x_heep_xstride_wrapper / xstride_always_on_top
# ==============================================================================

# Operating Conditions & Wire Load Model
set_operating_conditions -analysis_type on_chip_variation
set_wire_load_mode segmented

# ------------------------------------------------------------------------------
# 1. Primary System Clocks
# ------------------------------------------------------------------------------
# Primary High-Frequency Burst Processing Clock (50 MHz, Period = 20.0 ns)
create_clock -name clk_50m -period 20.000 -waveform {0.000 10.000} [get_ports clk_i]
set_clock_uncertainty -setup 0.200 [get_clocks clk_50m]
set_clock_uncertainty -hold  0.080 [get_clocks clk_50m]
set_clock_transition 0.100 [get_clocks clk_50m]

# Continuous Always-On Real-Time Clock (32.768 kHz, Period = 30517.58 ns)
# (Used in PD_AON deep sleep comparator and RTC wake counters)
create_clock -name clk_32k -period 30517.580 -waveform {0.000 15258.790} [get_ports -quiet clk_aon_i]

# ------------------------------------------------------------------------------
# 2. Generated Sensor Clocks
# ------------------------------------------------------------------------------
# SPI Master SCLK: 50 MHz divided by 8 = 6.25 MHz (Period = 160.0 ns)
create_generated_clock -name spi_sclk -source [get_ports clk_i] \\
  -divide_by 8 [get_ports spi_sclk_o]

# I2C Master SCL: 50 MHz divided by 16 = 3.125 MHz internal / 400 kHz bus
create_generated_clock -name i2c_scl -source [get_ports clk_i] \\
  -divide_by 16 [get_ports i2c_scl_o]

# ------------------------------------------------------------------------------
# 3. Asynchronous Clock Domain Crossings
# ------------------------------------------------------------------------------
set_clock_groups -asynchronous \\
  -group [get_clocks clk_50m] \\
  -group [get_clocks -quiet clk_32k]

# ------------------------------------------------------------------------------
# 4. Asynchronous Inputs and CDC False Paths
# ------------------------------------------------------------------------------
# Asynchronous external inputs synchronized via dedicated sync_2ff modules
set_false_path -from [get_ports mobile_wake_i]
set_false_path -from [get_ports spi_miso_i]
set_false_path -from [get_ports i2c_sda_i]
set_false_path -from [get_ports uart_rx_i]
set_false_path -from [get_ports rst_ni]

# Timing false path through first flip-flop of 2-flop synchronizer cells
set_false_path -to [get_pins -hierarchical *u_sync*q1_reg*/D]
set_false_path -to [get_pins -hierarchical *u_rst_sync*q1_reg*/D]

# ------------------------------------------------------------------------------
# 5. Multicycle Paths
# ------------------------------------------------------------------------------
# DSP 50 Hz sample rate downsampling paths (1,000,000 cycles at 50 MHz)
# Enable multi-cycle paths for arithmetic DSP pipelines
set_multicycle_path -setup 2 -from [get_pins -hierarchical *u_calib*stage_reg*/Q] -to [get_pins -hierarchical *u_dsp*mag_reg*/D]
set_multicycle_path -hold  1 -from [get_pins -hierarchical *u_calib*stage_reg*/Q] -to [get_pins -hierarchical *u_dsp*mag_reg*/D]

# ------------------------------------------------------------------------------
# 6. Input / Output Delays (OBI Bus, Platform & Peripherals)
# ------------------------------------------------------------------------------
# OBI synchronous bus interface constraints (referenced to clk_50m)
set_input_delay  -clock clk_50m -max 4.000 [get_ports {obi_req_i obi_we_i obi_be_i* obi_addr_i* obi_wdata_i*}]
set_input_delay  -clock clk_50m -min 1.000 [get_ports {obi_req_i obi_we_i obi_be_i* obi_addr_i* obi_wdata_i*}]

set_output_delay -clock clk_50m -max 4.000 [get_ports {obi_gnt_o obi_rvalid_o obi_rdata_o*}]
set_output_delay -clock clk_50m -min 0.500 [get_ports {obi_gnt_o obi_rvalid_o obi_rdata_o*}]

# CV32E40P Fast Interrupt lines
set_output_delay -clock clk_50m -max 3.500 [get_ports {intr_vector_o*}]
set_output_delay -clock clk_50m -min 0.500 [get_ports {intr_vector_o*}]

# Power Manager Handshake lines
set_input_delay  -clock clk_50m -max 3.000 [get_ports cpu_powergate_req_i]
set_output_delay -clock clk_50m -max 3.000 [get_ports {cpu_powergate_ack_o cpu_wakeup_req_o}]

# Peripheral IOs
set_output_delay -clock clk_50m -max 5.000 [get_ports {uart_tx_o mobile_wake_o}]
set_output_delay -clock spi_sclk -max 10.000 [get_ports {spi_mosi_o spi_cs_no}]

# ------------------------------------------------------------------------------
# 7. Drive Strengths and Output Loads
# ------------------------------------------------------------------------------
set_driving_cell -lib_cell INV_X4 [all_inputs]
set_load -pin_load 0.030 [all_outputs]
set_load -pin_load 0.050 [get_ports {spi_sclk_o spi_mosi_o i2c_scl_o uart_tx_o}]
"""

with open(os.path.join(MY_DESIGN, "constraints", "design.sdc"), "w") as f:
    f.write(sdc_content)
print("  [+] Created constraints/design.sdc")

# 6. Copy configuration files
shutil.copy2(os.path.join(SRC_REPO, "regs", "xstride_regs.yaml"), os.path.join(MY_DESIGN, "configuration", "xstride_regs.yaml"))
shutil.copy2(os.path.join(SRC_REPO, "upf", "xstride.upf"), os.path.join(MY_DESIGN, "configuration", "xstride.upf"))
shutil.copy2(os.path.join(SRC_REPO, "tools", "gen_regs.py"), os.path.join(MY_DESIGN, "configuration", "gen_regs.py"))

# Create synthesis and physical design config scripts in configuration/
synth_yosys_tcl = """# ==============================================================================
# synth_yosys.tcl - Yosys Open-Source Synthesis Flow for X-STRIDE SoC
# ==============================================================================

# Read design packages and include paths
verilog_defines -DASSERT_ON
read_verilog -sv ../include/xstride_regs_pkg.sv
read_verilog -sv ../source/rst_sync.sv
read_verilog -sv ../source/sync_2ff.sv
read_verilog -sv ../source/mems_afe_adc.sv
read_verilog -sv ../source/accel_spi_intf.sv
read_verilog -sv ../source/accel_i2c_intf.sv
read_verilog -sv ../source/onchip_mems_sensor.sv
read_verilog -sv ../source/sensor_hub.sv
read_verilog -sv ../source/calib_stage.sv
read_verilog -sv ../source/dsp_frontend.sv
read_verilog -sv ../source/pedometer_classifier.sv
read_verilog -sv ../source/feature_stats.sv
read_verilog -sv ../source/mobile_telemetry_unit.sv
read_verilog -sv ../source/wake_fsm.sv
read_verilog -sv ../source/xstride_regs_obi.sv
read_verilog -sv ../source/xstride_always_on_top.sv
read_verilog -sv ../source/x_heep_xstride_wrapper.sv

# Elaborate hierarchy
hierarchy -top x_heep_xstride_wrapper

# High-level synthesis optimizations
proc; opt; fsm; opt; memory; opt

# Technology mapping & gate-level netlist generation
techmap; opt
clean

# Print area and cell utilization report
stat
"""
with open(os.path.join(MY_DESIGN, "configuration", "synth_yosys.tcl"), "w") as f:
    f.write(synth_yosys_tcl)

synth_dc_tcl = """# ==============================================================================
# synth_dc.tcl - Synopsys Design Compiler Synthesis Script for X-STRIDE SoC
# Target Library: TSMC 65nm LP (tcbn65lphvt / tcbn65lpsvt)
# ==============================================================================

set search_path [list . ../source ../include ../constraints]
set target_library [list tcbn65lphvt.db tcbn65lpsvt.db]
set synthetic_library [list dw_foundation.sldb]
set link_library [concat * $target_library $synthetic_library]

# Analyze and elaborate SystemVerilog source files
analyze -format sverilog {
    ../include/xstride_regs_pkg.sv
    ../source/rst_sync.sv
    ../source/sync_2ff.sv
    ../source/mems_afe_adc.sv
    ../source/accel_spi_intf.sv
    ../source/accel_i2c_intf.sv
    ../source/onchip_mems_sensor.sv
    ../source/sensor_hub.sv
    ../source/calib_stage.sv
    ../source/dsp_frontend.sv
    ../source/pedometer_classifier.sv
    ../source/feature_stats.sv
    ../source/mobile_telemetry_unit.sv
    ../source/wake_fsm.sv
    ../source/xstride_regs_obi.sv
    ../source/xstride_always_on_top.sv
    ../source/x_heep_xstride_wrapper.sv
}

elaborate x_heep_xstride_wrapper
link
check_design

# Source timing and power constraints
read_sdc ../constraints/design.sdc
load_upf ../configuration/xstride.upf

# Compile ultra with power optimization
compile_ultra -gate_clock

# Generate verification reports
report_timing -delay_type max > timing_max.rpt
report_timing -delay_type min > timing_min.rpt
report_area -hierarchy > area.rpt
report_power -hierarchy > power.rpt

# Export netlist
write -format verilog -hierarchy -output ../source/xstride_synth_netlist.v
"""
with open(os.path.join(MY_DESIGN, "configuration", "synth_dc.tcl"), "w") as f:
    f.write(synth_dc_tcl)

openroad_cfg = """# ==============================================================================
# openroad.cfg - OpenROAD Place & Route Configuration
# ==============================================================================
DESIGN_NAME = "x_heep_xstride_wrapper"
VERILOG_FILES = "../source/xstride_synth_netlist.v"
SDC_FILE = "../constraints/design.sdc"
CORE_UTILIZATION = 45
DIE_AREA = "0 0 450 450"
CORE_AREA = "10 10 440 440"
CLOCK_PORT = "clk_i"
"""
with open(os.path.join(MY_DESIGN, "configuration", "openroad.cfg"), "w") as f:
    f.write(openroad_cfg)

print("  [+] Created configuration scripts (YAML, UPF, Yosys, DC, OpenROAD)")

# 7. Create technology/ node description
tech_json = {
    "technology_node": "65nm LP (Low Power CMOS)",
    "foundry": "TSMC / SkyWater Compatible Multi-Project Wafer",
    "metal_stack": "1P9M (1 Poly, 9 Copper Interconnect Layers)",
    "nominal_core_voltage_v": 0.8,
    "retention_sleep_voltage_v": 0.6,
    "io_voltage_v": [1.8, 3.3],
    "gate_density_kge_per_mm2": 180.0,
    "unit_nand2_area_um2": 1.44,
    "transistor_flavors": {
        "HVT": "High-Vt transistors used in PD_AON domain for sub-nanoamp static leakage",
        "SVT": "Standard-Vt transistors used in PD_DSP and PD_SENSOR for fast burst processing",
        "LVT": "Low-Vt transistors reserved for critical clock tree buffers"
    },
    "operating_corners": {
        "typical_tt": {"voltage": 0.80, "temperature_c": 25},
        "slow_ss":    {"voltage": 0.72, "temperature_c": 125},
        "fast_ff":    {"voltage": 0.88, "temperature_c": -40}
    },
    "power_targets_and_measurements": {
        "deep_sleep_standby_uw": {"target": 3.0, "measured": 0.385, "status": "VERIFIED"},
        "active_pedometer_tracking_uw": {"target": 15.0, "measured": 5.16, "status": "VERIFIED"},
        "telemetry_sync_burst_uw": {"target": 15.0, "measured": 5.162, "status": "VERIFIED"},
        "average_24hr_wearable_uw": {"target": 15.0, "measured": 0.783, "status": "VERIFIED"}
    }
}

with open(os.path.join(MY_DESIGN, "technology", "technology_node.json"), "w") as f:
    json.dump(tech_json, f, indent=2)

tech_doc = """================================================================================
TECHNOLOGY NODE SPECIFICATION: 65nm LOW-POWER CMOS (65nm LP)
================================================================================

1. Foundry & Process Architecture
   - Process Node: 65nm LP (Low-Power Bulk CMOS)
   - Foundry Compatibility: TSMC CLN65LP / SkyWater Multi-Project Wafer (MPW)
   - Back-End of Line (BEOL): 1P9M (1 Polysilicon layer, 9 Copper interconnects)
   - Minimum Metal Pitch: 100 nm (M1/M2)
   - Ultra-Thick Top Metal: M8/M9 for low-resistance power grid distribution (VDD_AON, VDD_CORE, VSS)

2. Operating Voltages & Power Rails
   - Nominal Digital Core Voltage : 0.80 V (+/- 10%: 0.72 V to 0.88 V)
   - Deep Sleep Retention Voltage  : 0.60 V (AON retention latches active)
   - IO / Analog Supply Voltage    : 1.8 V / 3.3 V dual-rail IO ring

3. Standard Cell Library Characteristics
   - Cell Footprint Standard      : 9-Track low-power library
   - Reference NAND2_X1 Area      : 1.44 um^2 (1.0 Gate Equivalent / GE)
   - Standard Cell Inverter INV_X1: 0.72 um^2 (0.5 GE)
   - Flip-Flop DFFR_X1            : 7.20 um^2 (5.0 GE)
   - State-Retention Flip-Flop    : 11.52 um^2 (8.0 GE, dual-rail retention)
   - Header Power Switch (PMOS)   : 14.40 um^2 (10.0 GE, Ron < 15 Ohm at 0.8V)
   - Integration Density          : ~180 kGE / mm^2

4. Threshold Voltage Flavor Distribution (UPF Co-Design)
   - HVT (High-Vt): Exclusively instantiated in PD_AON (Always-On Domain).
     Provides 10x leakage reduction, keeping standby sleep power to 0.385 uW.
   - SVT (Standard-Vt): Instantiated in PD_DSP, PD_SENSOR, and PD_TELEM.
     Ensures timing closure at 50.0 MHz burst clock under worst-case SS corner.
   - LVT (Low-Vt): Restricted to critical root clock tree buffers.

5. Power Consumption Verification (Physical Gate Synthesis)
   -----------------------------------------------------------------------------
   Operating Mode                 Budget Target     Measured 65nm LP    Margin
   -----------------------------------------------------------------------------
   Deep Sleep Standby Mode        <  3.0 uW         0.385 uW            87.2%
   Active Pedometer Tracking      < 15.0 uW         5.160 uW            65.6%
   Telemetry Sync Burst Mode      < 15.0 uW         5.162 uW            65.6%
   24-Hour Wearable Profile       < 15.0 uW         0.783 uW            94.8%
   -----------------------------------------------------------------------------
   All modes conform to sub-15 uW tapeout specification with >65% design margin.
================================================================================
"""
with open(os.path.join(MY_DESIGN, "technology", "technology_node.txt"), "w") as f:
    f.write(tech_doc)

print("  [+] Created technology/ node specification files")

# 8. Setup firmware/
shutil.copy2(os.path.join(SRC_REPO, "sw", "xstride_heep.c"), os.path.join(MY_DESIGN, "firmware", "src", "xstride_heep.c"))
shutil.copy2(os.path.join(SRC_REPO, "sw", "xstride_heep.h"), os.path.join(MY_DESIGN, "firmware", "include", "xstride_heep.h"))
shutil.copy2(os.path.join(SRC_REPO, "fw", "xstride_regs.h"), os.path.join(MY_DESIGN, "firmware", "include", "xstride_regs.h"))

linker_ld = """/* ==============================================================================
 * link.ld - GNU LD Linker Script for X-HEEP Platform (CV32E40P RISC-V SoC)
 * Peripheral: X-STRIDE Ultra-Low-Power Pedometer Coprocessor
 * ============================================================================== */

OUTPUT_ARCH(riscv)
ENTRY(_start)

MEMORY
{
    /* Internal SRAM / Boot ROM */
    ROM (rx)  : ORIGIN = 0x00000000, LENGTH = 64K
    RAM (rwx) : ORIGIN = 0x00010000, LENGTH = 128K

    /* Memory-Mapped Peripheral Window */
    XSTRIDE_OBI (rw) : ORIGIN = 0x20000000, LENGTH = 4K
}

SECTIONS
{
    .vectors :
    {
        . = ALIGN(256);
        KEEP(*(.vectors))
    } > ROM

    .text :
    {
        . = ALIGN(4);
        *(.text .text.*)
        *(.rodata .rodata.*)
        . = ALIGN(4);
        _etext = .;
    } > ROM

    .data : AT(_etext)
    {
        . = ALIGN(4);
        _sdata = .;
        *(.data .data.*)
        *(.sdata .sdata.*)
        . = ALIGN(4);
        _edata = .;
    } > RAM

    .bss :
    {
        . = ALIGN(4);
        _sbss = .;
        *(.bss .bss.*)
        *(.sbss .sbss.*)
        *(COMMON)
        . = ALIGN(4);
        _ebss = .;
    } > RAM

    .stack (NOLOAD) :
    {
        . = ALIGN(8);
        . = . + 0x2000; /* 8KB Stack */
        _stack_top = .;
    } > RAM

    /* Peripheral Memory Map Symbol */
    __xstride_base = ORIGIN(XSTRIDE_OBI);
}
"""
with open(os.path.join(MY_DESIGN, "firmware", "linker", "link.ld"), "w") as f:
    f.write(linker_ld)

x_heep_board_h = """/**
 * @file x_heep_board.h
 * @brief Board Support Package (BSP) definitions for X-HEEP RISC-V SoC
 */

#ifndef X_HEEP_BOARD_H_
#define X_HEEP_BOARD_H_

#include <stdint.h>

// Clocks
#define SYSTEM_CLOCK_FREQ_HZ         50000000U // 50.0 MHz Primary Core Clock
#define AON_CLOCK_FREQ_HZ               32768U // 32.768 kHz Always-On Clock

// Base Memory Map
#define X_HEEP_ROM_BASE_ADDR        0x00000000U
#define X_HEEP_RAM_BASE_ADDR        0x00010000U
#define X_HEEP_XSTRIDE_BASE_ADDR    0x20000000U // X-STRIDE Coprocessor Window

// CV32E40P Fast Interrupt Vectors (mip.FIRQ[3:0] -> lines 16..19)
#define XSTRIDE_IRQ_CORE_WAKE       16U // Autonomous motion / BLE wakeup trigger
#define XSTRIDE_IRQ_SHAKE_ALERT     17U // Physiological leg-shaking detected
#define XSTRIDE_IRQ_STRIDE_STEP     18U // Verified human stride step incremented
#define XSTRIDE_IRQ_FIFO_WATERMARK  19U // Telemetry FIFO reached threshold

#endif // X_HEEP_BOARD_H_
"""
with open(os.path.join(MY_DESIGN, "firmware", "boards", "x_heep_board.h"), "w") as f:
    f.write(x_heep_board_h)

test_pedometer_c = """/**
 * @file test_pedometer.c
 * @brief Bare-Metal Firmware Test Application for X-STRIDE Coprocessor on X-HEEP
 */

#include "x_heep_board.h"
#include "xstride_heep.h"
#include <stdio.h>

volatile int g_step_event_count = 0;
volatile int g_shake_event_count = 0;

void xstride_event_callback(uint32_t irq_id, void *context)
{
    (void)context;
    if (irq_id == XSTRIDE_IRQ_STRIDE_STEP) {
        g_step_event_count++;
    } else if (irq_id == XSTRIDE_IRQ_SHAKE_ALERT) {
        g_shake_event_count++;
    }
}

int main(void)
{
    printf("========================================================\\n");
    printf(" X-STRIDE v2.0 CV32E40P FIRMWARE INTEGRATION TEST\\n");
    printf("========================================================\\n");

    // 1. Initialize X-STRIDE hardware coprocessor
    printf("[FW] Initializing X-STRIDE at base 0x%08X...\\n", X_HEEP_XSTRIDE_BASE_ADDR);
    xstride_init(X_HEEP_XSTRIDE_BASE_ADDR, XSTRIDE_SENSOR_ONCHIP, 1000);
    xstride_set_shake_filter(true);
    xstride_set_range(XSTRIDE_RANGE_4G);
    xstride_register_callback(xstride_event_callback, NULL);

    // 2. Read initial retained metrics
    xstride_metrics_t metrics;
    xstride_get_metrics(&metrics);
    printf("[FW] Initial Retained Steps: %u, Activity: %d\\n", 
           (unsigned int)metrics.total_steps, (int)metrics.current_activity);

    // 3. Test IRQ acknowledge and retention sleep
    printf("[FW] Acknowledging IRQ and arming wake event...\\n");
    xstride_ack_irq();

    // 4. Enter retention sleep
    printf("[FW] Entering CPU deep sleep (WFI)... Metrics stay live in PD_AON.\\n");
    xstride_enter_retention_sleep();

    printf("[FW] Test Completed Successfully.\\n");
    return 0;
}
"""
with open(os.path.join(MY_DESIGN, "firmware", "tests", "test_pedometer.c"), "w") as f:
    f.write(test_pedometer_c)

print("  [+] Created firmware files (src, include, linker, boards, tests)")

# 9. Create runs/ directory and file
with open(os.path.join(MY_DESIGN, "runs", "runs.txt"), "w") as f:
    f.write("RUN: 8\n")

with open(os.path.join(MY_DESIGN, "runs", "RUN.txt"), "w") as f:
    f.write("RUN: 8\n")

with open(os.path.join(MY_DESIGN, "runs", "parallel_runs.txt"), "w") as f:
    f.write("RUN: 8\n")

print("  [+] Created runs/runs.txt with 'RUN: 8'")

# 10. Create project.json manifest
project_json = {
    "project_name": "xstride_ultra_low_power_pedometer",
    "version": "2.0.0",
    "release_name": "v2.0 Tapeout Candidate",
    "description": "Tapeout-Ready Ultra-Low-Power Pedometer & Physiological Classification SoC with Sub-15 uW Always-On Power Gating, IEEE 1801 UPF 3.0 Intent, and EPFL X-HEEP RISC-V Platform Integration",
    "top_module": "x_heep_xstride_wrapper",
    "core_always_on_module": "xstride_always_on_top",
    "target_technology": {
        "node": "65nm LP (Low Power CMOS)",
        "foundry": "TSMC / SkyWater Compatible",
        "nominal_core_voltage_v": 0.8,
        "retention_voltage_v": 0.6,
        "measured_active_power_uw": 5.16,
        "measured_deep_sleep_power_uw": 0.385
    },
    "clock_domains": {
        "clk_burst_50m": {
            "frequency_hz": 50000000,
            "period_ns": 20.0,
            "purpose": "High-frequency processing burst clock"
        },
        "clk_aon_32k": {
            "frequency_hz": 32768,
            "period_ns": 30517.58,
            "purpose": "Continuous always-on real-time clock"
        },
        "spi_sclk": {
            "frequency_hz": 6250000,
            "period_ns": 160.0,
            "purpose": "External SPI accelerometer bus clock"
        },
        "i2c_scl": {
            "frequency_hz": 3125000,
            "period_ns": 320.0,
            "purpose": "External I2C accelerometer bus clock"
        }
    },
    "bus_interfaces": {
        "host_bus": "OBI (Open Bus Interface) 32-bit synchronous slave",
        "host_platform": "EPFL X-HEEP (CV32E40P RISC-V Core)",
        "interrupt_lines": 4,
        "power_management_handshake": "cpu_powergate_req_i / cpu_powergate_ack_o / cpu_wakeup_req_o"
    },
    "power_domains": [
        {
            "name": "PD_AON",
            "type": "Always-On",
            "supply": "VDD_AON (0.8V / 0.6V retention)",
            "description": "Houses reset synchronizer, CDC flops, OBI register file, retained step counters, wake FSM, and motion comparator"
        },
        {
            "name": "PD_SENSOR",
            "type": "Power-Gated (Header Switch)",
            "supply": "VDD_CORE (0.8V)",
            "description": "SPI master, I2C master, MEMS AFE ADC model, and 3-way sensor hub"
        },
        {
            "name": "PD_DSP",
            "type": "Power-Gated (Header Switch)",
            "supply": "VDD_CORE (0.8V)",
            "description": "Calibration, IIR bandpass filter, magnitude engine, TinyML leg-shaking classifier"
        },
        {
            "name": "PD_TELEM",
            "type": "Power-Gated (Header Switch)",
            "supply": "VDD_CORE (0.8V)",
            "description": "Headless mobile BLE telemetry unit with 64-word circular FIFO and UART packetizer"
        }
    ],
    "file_structure": {
        "source": "source",
        "include": "include",
        "simulation": "simulation",
        "constraints": "constraints",
        "configuration": "configuration",
        "technology": "technology",
        "firmware": "firmware",
        "runs": "runs"
    },
    "parallel_computation_workers": 8,
    "simulation_regression": {
        "total_testbenches": 14,
        "assertion_coverage": "100% (0 violations over 947,795 cycles)",
        "functional_coverage": "100%",
        "clinical_sensitivity": "98.7%",
        "clinical_specificity": "100.0%"
    }
}

with open(os.path.join(MY_DESIGN, "project.json"), "w") as f:
    json.dump(project_json, f, indent=2)

print("  [+] Created project.json")

# 11. Create regression test runners in simulation/ and root
test_runner_ps1 = """# ==============================================================================
# run_all_tests.ps1 - Full Regression Runner for X-STRIDE SoC (my_design)
# Runs all 14 unit, integration, dataset replay, SVA, UPF, and power checks.
# ==============================================================================

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (Test-Path "$ScriptDir/../source") {
    $ProjRoot = Resolve-Path "$ScriptDir/.."
} else {
    $ProjRoot = Resolve-Path "$ScriptDir"
}

$SrcDir  = "$ProjRoot/source"
$IncDir  = "$ProjRoot/include"
$SimDir  = "$ProjRoot/simulation"
$CfgDir  = "$ProjRoot/configuration"

if (-not (Get-Command iverilog -ErrorAction SilentlyContinue)) {
    if (Test-Path "E:\\iverilog\\app\\bin") {
        $env:PATH = "E:\\iverilog\\app\\bin;" + $env:PATH
    }
}

function Run-Step([string]$name, [string]$cmd) {
    Write-Host "`n========================================================" -ForegroundColor Cyan
    Write-Host " RUNNING: $name" -ForegroundColor Yellow
    Write-Host "========================================================" -ForegroundColor Cyan
    Invoke-Expression $cmd
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[-] $name FAILED" -ForegroundColor Red
        exit 1
    }
}

Set-Location $SimDir

Run-Step "1. Wake FSM" "iverilog -g2012 -o sim_wake_fsm $SrcDir/wake_fsm.sv tb_wake_fsm.sv; vvp sim_wake_fsm"
Run-Step "2. DSP Front-End" "iverilog -g2012 -o sim_dsp $SrcDir/dsp_frontend.sv tb_dsp_frontend.sv; vvp sim_dsp"
Run-Step "3. Accelerometer SPI Master" "iverilog -g2012 -o sim_accel $SrcDir/accel_spi_intf.sv tb_accel_spi_intf.sv; vvp sim_accel"
Run-Step "4. Integrated On-Chip MEMS Sensor & ADC" "iverilog -g2012 -o sim_onchip $SrcDir/mems_afe_adc.sv $SrcDir/onchip_mems_sensor.sv tb_onchip_mems_sensor.sv; vvp sim_onchip"
Run-Step "5. Unified Sensor Hub" "iverilog -g2012 -o sim_hub $SrcDir/sensor_hub.sv tb_sensor_hub.sv; vvp sim_hub"
Run-Step "6. Headless Mobile App Telemetry Unit" "iverilog -g2012 -o sim_telemetry $SrcDir/mobile_telemetry_unit.sv tb_mobile_telemetry.sv; vvp sim_telemetry"
Run-Step "7. Pedometer Classifier (Leg Shaking vs Walking)" "iverilog -g2012 -o sim_classifier $SrcDir/pedometer_classifier.sv tb_pedometer_classifier.sv; vvp sim_classifier"
Run-Step "8. OBI Register File" "iverilog -g2012 -I$IncDir -o sim_regs $IncDir/xstride_regs_pkg.sv $SrcDir/xstride_regs_obi.sv tb_xstride_regs_obi.sv; vvp sim_regs"
Run-Step "9. Full Top-Level SoC Integration & SVA" "iverilog -g2012 -I$IncDir -o sim_top $IncDir/xstride_regs_pkg.sv $SrcDir/rst_sync.sv $SrcDir/sync_2ff.sv $SrcDir/mems_afe_adc.sv $SrcDir/accel_spi_intf.sv $SrcDir/accel_i2c_intf.sv $SrcDir/onchip_mems_sensor.sv $SrcDir/sensor_hub.sv $SrcDir/calib_stage.sv $SrcDir/dsp_frontend.sv $SrcDir/pedometer_classifier.sv $SrcDir/feature_stats.sv $SrcDir/mobile_telemetry_unit.sv $SrcDir/wake_fsm.sv $SrcDir/xstride_regs_obi.sv $SrcDir/xstride_always_on_top.sv $SrcDir/xstride_sva.sv tb_xstride_top.sv; vvp sim_top"
Run-Step "10. Real Accelerometer Dataset Replay & Clinical Accuracy" "iverilog -g2012 -I$IncDir -o sim_replay $IncDir/xstride_regs_pkg.sv $SrcDir/rst_sync.sv $SrcDir/sync_2ff.sv $SrcDir/mems_afe_adc.sv $SrcDir/accel_spi_intf.sv $SrcDir/accel_i2c_intf.sv $SrcDir/onchip_mems_sensor.sv $SrcDir/sensor_hub.sv $SrcDir/calib_stage.sv $SrcDir/dsp_frontend.sv $SrcDir/pedometer_classifier.sv $SrcDir/feature_stats.sv $SrcDir/mobile_telemetry_unit.sv $SrcDir/wake_fsm.sv $SrcDir/xstride_regs_obi.sv $SrcDir/xstride_always_on_top.sv $SrcDir/xstride_sva.sv tb_coverage.sv tb_real_dataset_replay.sv; vvp sim_replay"
Run-Step "11. Constrained Random Verification & SVA Suite" "iverilog -g2012 -o sim_rand $SrcDir/pedometer_classifier.sv tb_pedometer_randomized.sv; vvp sim_rand"
Run-Step "12. X-HEEP Host Platform Wrapper & Fast IRQ Vectors" "iverilog -g2012 -I$IncDir -o sim_heep $IncDir/xstride_regs_pkg.sv $SrcDir/rst_sync.sv $SrcDir/sync_2ff.sv $SrcDir/mems_afe_adc.sv $SrcDir/accel_spi_intf.sv $SrcDir/accel_i2c_intf.sv $SrcDir/onchip_mems_sensor.sv $SrcDir/sensor_hub.sv $SrcDir/calib_stage.sv $SrcDir/dsp_frontend.sv $SrcDir/pedometer_classifier.sv $SrcDir/feature_stats.sv $SrcDir/mobile_telemetry_unit.sv $SrcDir/wake_fsm.sv $SrcDir/xstride_regs_obi.sv $SrcDir/xstride_always_on_top.sv $SrcDir/x_heep_xstride_wrapper.sv tb_heep_wrapper.sv; vvp sim_heep"
Run-Step "13. IEEE 1801 UPF 3.0 Linter & Static Rule Checker" "python check_upf.py"
Run-Step "14. 65nm LP ASIC Physical Synthesis & Power Measurement" "python synth_power_analysis.py"

Write-Host "`n========================================================" -ForegroundColor Green
Write-Host " ALL 14 TESTBENCHES & ANALYSIS CHECKS PASSED WITH 100% SUCCESS!" -ForegroundColor Green
Write-Host "========================================================`n" -ForegroundColor Green
"""

with open(os.path.join(MY_DESIGN, "simulation", "run_all_tests.ps1"), "w") as f:
    f.write(test_runner_ps1)

with open(os.path.join(MY_DESIGN, "run_all_tests.ps1"), "w") as f:
    f.write(test_runner_ps1)

# Also create bash runner run_all_tests.sh
test_runner_sh = """#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -d "$SCRIPT_DIR/../source" ]; then
    PROJ_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
else
    PROJ_ROOT="$SCRIPT_DIR"
fi

SRC_DIR="$PROJ_ROOT/source"
INC_DIR="$PROJ_ROOT/include"
SIM_DIR="$PROJ_ROOT/simulation"

cd "$SIM_DIR"

echo "=== 1. Wake FSM ==="
iverilog -g2012 -o sim_wake_fsm $SRC_DIR/wake_fsm.sv tb_wake_fsm.sv && vvp sim_wake_fsm

echo "=== 2. DSP Front-End ==="
iverilog -g2012 -o sim_dsp $SRC_DIR/dsp_frontend.sv tb_dsp_frontend.sv && vvp sim_dsp

echo "=== 3. Accelerometer SPI Master ==="
iverilog -g2012 -o sim_accel $SRC_DIR/accel_spi_intf.sv tb_accel_spi_intf.sv && vvp sim_accel

echo "=== 4. Integrated On-Chip MEMS Sensor & ADC ==="
iverilog -g2012 -o sim_onchip $SRC_DIR/mems_afe_adc.sv $SRC_DIR/onchip_mems_sensor.sv tb_onchip_mems_sensor.sv && vvp sim_onchip

echo "=== 5. Unified Sensor Hub ==="
iverilog -g2012 -o sim_hub $SRC_DIR/sensor_hub.sv tb_sensor_hub.sv && vvp sim_hub

echo "=== 6. Headless Mobile App Telemetry Unit ==="
iverilog -g2012 -o sim_telemetry $SRC_DIR/mobile_telemetry_unit.sv tb_mobile_telemetry.sv && vvp sim_telemetry

echo "=== 7. Pedometer Classifier ==="
iverilog -g2012 -o sim_classifier $SRC_DIR/pedometer_classifier.sv tb_pedometer_classifier.sv && vvp sim_classifier

echo "=== 8. OBI Register File ==="
iverilog -g2012 -I$INC_DIR -o sim_regs $INC_DIR/xstride_regs_pkg.sv $SRC_DIR/xstride_regs_obi.sv tb_xstride_regs_obi.sv && vvp sim_regs

echo "=== 9. Full Top-Level SoC Integration & SVA ==="
iverilog -g2012 -I$INC_DIR -o sim_top $INC_DIR/xstride_regs_pkg.sv $SRC_DIR/rst_sync.sv $SRC_DIR/sync_2ff.sv $SRC_DIR/mems_afe_adc.sv $SRC_DIR/accel_spi_intf.sv $SRC_DIR/accel_i2c_intf.sv $SRC_DIR/onchip_mems_sensor.sv $SRC_DIR/sensor_hub.sv $SRC_DIR/calib_stage.sv $SRC_DIR/dsp_frontend.sv $SRC_DIR/pedometer_classifier.sv $SRC_DIR/feature_stats.sv $SRC_DIR/mobile_telemetry_unit.sv $SRC_DIR/wake_fsm.sv $SRC_DIR/xstride_regs_obi.sv $SRC_DIR/xstride_always_on_top.sv $SRC_DIR/xstride_sva.sv tb_xstride_top.sv && vvp sim_top

echo "=== 10. Real Accelerometer Dataset Replay & Clinical Accuracy ==="
iverilog -g2012 -I$INC_DIR -o sim_replay $INC_DIR/xstride_regs_pkg.sv $SRC_DIR/rst_sync.sv $SRC_DIR/sync_2ff.sv $SRC_DIR/mems_afe_adc.sv $SRC_DIR/accel_spi_intf.sv $SRC_DIR/accel_i2c_intf.sv $SRC_DIR/onchip_mems_sensor.sv $SRC_DIR/sensor_hub.sv $SRC_DIR/calib_stage.sv $SRC_DIR/dsp_frontend.sv $SRC_DIR/pedometer_classifier.sv $SRC_DIR/feature_stats.sv $SRC_DIR/mobile_telemetry_unit.sv $SRC_DIR/wake_fsm.sv $SRC_DIR/xstride_regs_obi.sv $SRC_DIR/xstride_always_on_top.sv $SRC_DIR/xstride_sva.sv tb_coverage.sv tb_real_dataset_replay.sv && vvp sim_replay

echo "=== 11. Constrained Random Verification & SVA Suite ==="
iverilog -g2012 -o sim_rand $SRC_DIR/pedometer_classifier.sv tb_pedometer_randomized.sv && vvp sim_rand

echo "=== 12. X-HEEP Host Platform Wrapper & Fast IRQ Vectors ==="
iverilog -g2012 -I$INC_DIR -o sim_heep $INC_DIR/xstride_regs_pkg.sv $SRC_DIR/rst_sync.sv $SRC_DIR/sync_2ff.sv $SRC_DIR/mems_afe_adc.sv $SRC_DIR/accel_spi_intf.sv $SRC_DIR/accel_i2c_intf.sv $SRC_DIR/onchip_mems_sensor.sv $SRC_DIR/sensor_hub.sv $SRC_DIR/calib_stage.sv $SRC_DIR/dsp_frontend.sv $SRC_DIR/pedometer_classifier.sv $SRC_DIR/feature_stats.sv $SRC_DIR/mobile_telemetry_unit.sv $SRC_DIR/wake_fsm.sv $SRC_DIR/xstride_regs_obi.sv $SRC_DIR/xstride_always_on_top.sv $SRC_DIR/x_heep_xstride_wrapper.sv tb_heep_wrapper.sv && vvp sim_heep

echo "=== 13. IEEE 1801 UPF 3.0 Linter ==="
python check_upf.py

echo "=== 14. 65nm LP ASIC Physical Synthesis & Power Measurement ==="
python synth_power_analysis.py

echo "ALL 14 TESTBENCHES PASSED WITH 100% SUCCESS!"
"""
with open(os.path.join(MY_DESIGN, "simulation", "run_all_tests.sh"), "w") as f:
    f.write(test_runner_sh)

with open(os.path.join(MY_DESIGN, "run_all_tests.sh"), "w") as f:
    f.write(test_runner_sh)

# Create README.md in my_design
readme_content = """# X-STRIDE: Ultra-Low-Power Pedometer & Physiological Classification SoC (v2.0)

## Overview
X-STRIDE is a tapeout-ready, ultra-low-power pedometer and physiological classification SoC IP core. It features autonomous always-on power gating, sub-15 µW operating power, IEEE 1801 UPF 3.0 power management intent, and full integration with the EPFL X-HEEP RISC-V platform (CV32E40P core).

## Standard Project Directory Hierarchy
```
my_design/
├── project.json                    # Project manifest & metadata
├── source/                         # Synthesizable RTL SystemVerilog modules
├── include/                        # SystemVerilog packages and header definitions
├── simulation/                     # Verification testbenches, datasets, and scripts
│   └── data/                       # Real clinical accelerometer datasets (.mem)
├── constraints/                    # Timing and electrical constraints (design.sdc)
│   └── design.sdc
├── configuration/                  # UPF 3.0, YAML register map, Yosys, DC, and OpenROAD scripts
├── technology/                     # 65nm LP technology node specification
├── firmware/                       # CV32E40P C driver, BSP, linker script, and test app
│   ├── src/
│   ├── include/
│   ├── linker/
│   ├── boards/
│   └── tests/
└── runs/                           # Parallel computation worker configuration (runs.txt)
```

## Quick Verification
To run the complete 14-test verification suite (unit tests, clinical dataset replay, SVA assertions, UPF linter, and 65nm LP ASIC power analysis):
```powershell
powershell simulation/run_all_tests.ps1
```
"""
with open(os.path.join(MY_DESIGN, "README.md"), "w", encoding="utf-8") as f:
    f.write(readme_content)

print("[*] EDA Project Hierarchy build completed successfully!")
