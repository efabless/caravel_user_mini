#include <firmware_apis.h>

// #include "../common/common.h"
void main(){
    // Enable managment gpio as output to use as indicator for finishing configuration  
    ManagmentGpio_outputEnable();
    ManagmentGpio_write(0);
    enableHkSpi(0); // disable housekeeping spi
    // configure all gpios as  user out then chenge gpios from 32 to 37 before loading this configurations
    GPIOs_configureAll(GPIO_MODE_USER_STD_OUT_MONITORED);
    GPIOs_configure(36, GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
    GPIOs_configure(37, GPIO_MODE_MGMT_STD_INPUT_PULLDOWN);
    GPIOs_loadConfigs(); // load the configuration 
    // enable_user_interface();
    ManagmentGpio_write(1); // configuration finished 
    User_enableIF();
    LogicAnalyzer_write(0,7);
    LogicAnalyzer_outputEnable(0,0xC0000000);
    ManagmentGpio_write(0); // configuration finished 


    LogicAnalyzer_write(0,0x80000000);
    LogicAnalyzer_outputEnable(0,0x7FFFFFFF);
    LogicAnalyzer_outputEnable(0,0xFFFFFFFF);

    return;
}