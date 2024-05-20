
int selected_project(){
    // wait until one project selected 
    // while (true)
    //     if (get_gpio_h() != 0)
    //         break;
    int high_gpios = get_gpio_h();
    switch (high_gpios){
        case 0x1:
            write_user_double_word(0x0,0x3FFFF);
            return 0;
        case 0x2:
            write_user_double_word(0x1,0x3FFFF);
            return 1;
        case 0x4:
            write_user_double_word(0x2,0x3FFFF);
            return 2;
        case 0x8:
            write_user_double_word(0x3,0x3FFFF);
            return 3;
        case 0x10:
            write_user_double_word(0x4,0x3FFFF);
            return 4;
        case 0x20:
            write_user_double_word(0x5,0x3FFFF);
            return 5;
        default:
            return 0;
    }
}