from caravel_cocotb.caravel_interfaces import test_configure
from caravel_cocotb.caravel_interfaces import report_test
import cocotb 

@cocotb.test()
@report_test
async def counter_la_clk(dut):
    caravelEnv = await test_configure(dut,timeout_cycles=1346140)

    cocotb.log.info(f"[TEST] Start counter_la_clk test")  
    # wait for start of sending
    await caravelEnv.release_csb()
    selected_projeted = 0
    counter_step = selected_projeted*2+1
    cocotb.log.info(f"[TEST] seleceted project = {selected_projeted}")  
    caravelEnv.drive_gpio_in((37, 36), selected_projeted)
    await caravelEnv.wait_mgmt_gpio(1)
    await caravelEnv.release_csb()
    cocotb.log.info(f"[TEST] finish configuration") 
    cocotb.log.info(f"[TEST] project {selected_projeted} selected, counter step = {counter_step}") 
    # expect value bigger than 7 
    received_val = caravelEnv.monitor_gpio(29,0).integer 
    counter = received_val

    for i in range(5):
        if counter != caravelEnv.monitor_gpio(29,0).integer:
            cocotb.log.error(f"counter have wrong value expected = {counter} recieved = {caravelEnv.monitor_gpio(29,0).integer}")
        await wait_la_clock_cycle(caravelEnv)
        counter +=counter_step

    
async def wait_la_clock_cycle(caravelEnv): 
    # clock is synced with mgmt_gpio
    await caravelEnv.wait_mgmt_gpio(0)
    await caravelEnv.wait_mgmt_gpio(1)