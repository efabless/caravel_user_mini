from caravel_cocotb.caravel_interfaces import test_configure
from caravel_cocotb.caravel_interfaces import report_test
import cocotb 

@cocotb.test()
@report_test
async def counter_la(dut):
    caravelEnv = await test_configure(dut,timeout_cycles=1346140)

    cocotb.log.info(f"[TEST] Start counter_la test")  
    # wait for start of sending
    await caravelEnv.release_csb()
    selected_projeted = 0
    counter_step = selected_projeted*2+1
    cocotb.log.info(f"[TEST] seleceted project = {selected_projeted}")  
    caravelEnv.drive_gpio_in((37,36),selected_projeted)
    await caravelEnv.wait_mgmt_gpio(1)
    await caravelEnv.release_csb()
    cocotb.log.info("[TEST] finish configuration") 
    cocotb.log.info(f"[TEST] project {selected_projeted} selected, counter step = {counter_step}") 
    
    overwrite_val = 7 # value will be written to the counter by la 
    # expect value bigger than 7 
    received_val = caravelEnv.monitor_gpio(29,0).integer 
    counter = received_val
    if received_val <= overwrite_val :
        cocotb.log.error(f"counter started late and value captured after configuration is smaller than overwrite value: {overwrite_val} receieved: {received_val}")
    await cocotb.triggers.ClockCycles(caravelEnv.clk,1)

    while True: # wait until the value 1 start counting after the initial
        received_val = caravelEnv.monitor_gpio(29,0).integer 
        counter +=counter_step
        if received_val != counter: 
            if received_val == overwrite_val: 
                counter = received_val +counter_step
                cocotb.log.info(f"counter value has been overwritten by la to be {received_val}")
                while True: #wait until the la writing finished and the counter start running again
                    received_val = caravelEnv.monitor_gpio(29,0).integer 
                    if counter == received_val: 
                        break
                    await cocotb.triggers.ClockCycles(caravelEnv.clk,1)
                cocotb.log.info(f"counter value has been overwritten by la to be {received_val}")
                break
            else: 
                cocotb.log.error(f"counter has wrong value before overwrite happened expected: {counter} received: {received_val}")
        await cocotb.triggers.ClockCycles(caravelEnv.clk,1)

    for i in range(100):
        if counter != caravelEnv.monitor_gpio(29,0).integer:
            cocotb.log.error(f"counter have wrong value expected = {counter} recieved = {caravelEnv.monitor_gpio(29,0).integer}")
        await cocotb.triggers.ClockCycles(caravelEnv.clk,1)
        counter +=counter_step
    