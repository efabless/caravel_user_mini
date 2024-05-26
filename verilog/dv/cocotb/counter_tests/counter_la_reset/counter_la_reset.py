from caravel_cocotb.caravel_interfaces import test_configure
from caravel_cocotb.caravel_interfaces import report_test
import cocotb 

@cocotb.test()
@report_test
async def counter_la_reset(dut):
    caravelEnv = await test_configure(dut,timeout_cycles=1346140)
    await get_reset_val(caravelEnv)
    cocotb.log.info(f"[TEST] Start counter_la_clk test")  
    # wait for start of sending
    await caravelEnv.release_csb()
    selected_projeted = 0
    counter_step = selected_projeted*2+1
    cocotb.log.info(f"[TEST] seleceted project = {selected_projeted}")  
    caravelEnv.drive_gpio_in((37, 36), selected_projeted)
    await caravelEnv.wait_mgmt_gpio(1)
    cocotb.log.info(f"[TEST] finish configuration") 
    cocotb.log.info(f"[TEST] project {selected_projeted} selected, counter step = {counter_step}") 
    
    overwrite_val = 7 
    await caravelEnv.wait_mgmt_gpio(0) # wait until writing 7 through
    # expect value bigger than 7 
    received_val = int ((caravelEnv.monitor_gpio(29,0).binstr ),2) 
    counter = received_val
    if received_val < overwrite_val :
        cocotb.log.error(f"counter started late and value captured after configuration is smaller than overwrite value: {overwrite_val} receieved: {received_val}")
    await cocotb.triggers.ClockCycles(caravelEnv.clk,1)

    while True: # wait until reset asserted
        if await get_reset_val(caravelEnv) == 1: 
            cocotb.log.info(f"[TEST] Reset asserted by la")  
            break
    while True: # wait until reset deasserted
        if await get_reset_val(caravelEnv) == 0: 
            cocotb.log.info(f"[TEST] Reset deasserted by la")  
            break
    counter =0

    for i in range(100):
        if counter != int ((caravelEnv.monitor_gpio(29,0).binstr ),2) :
            cocotb.log.error(f"counter have wrong value expected = {counter} recieved = {int ((caravelEnv.monitor_gpio(29,0).binstr ),2) }")
        await cocotb.triggers.ClockCycles(caravelEnv.clk,1)
        counter +=counter_step
    
async def get_reset_val(caravelEnv): 
    """ get the counter reset value"""
    await cocotb.triggers.ClockCycles(caravelEnv.clk,1)
    cocotb.log.debug(dir(caravelEnv.user_hdl))
    # cocotb.log.info(caravelEnv.user_hdl._sub_handles)
    # cocotb.log.info(caravelEnv.user_hdl.user_project)
    # cocotb.log.info(dir(caravelEnv.user_hdl._sub_handles))
    # all project shares the same value
    try:
        return int(caravelEnv.user_hdl.la_data_in.value.binstr[-32],2)
    except ValueError:
        return "x"
    return int(caravelEnv.user_hdl.la_data_in.value.binstr[31],2)
# 00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000
