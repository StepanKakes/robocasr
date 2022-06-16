let right = false
let left = false
let L_sensor = DigitalPin.P15
let R_sensor = DigitalPin.P13
let F_sensor = DigitalPin.P8
let prevodovka = 0
// 0 - manual, 1 - automat
let sonarr = 0
let pojistka = false
// pojistka pro zatáčení
let speed = 1.0
bluetooth.startUartService()
pins.setPull(F_sensor, PinPullMode.PullNone)
pins.setPull(R_sensor, PinPullMode.PullNone)
pins.setPull(L_sensor, PinPullMode.PullNone)
// bluetooth.start_accelerometer_service()
// bluetooth.start_button_service()
// bluetooth.start_io_pin_service()
// bluetooth.start_led_service()
// bluetooth.start_temperature_service()
// bluetooth.start_magnetometer_service()
function motor_run(left: number, right: number, speed: number = 1) {
    PCAmotor.MotorRun(PCAmotor.Motors.M2, left * speed)
    PCAmotor.MotorRun(PCAmotor.Motors.M4, right * speed)
}

function objetí() {
    motor_run(120, -255)
    basic.pause(200)
    motor_run(120, 255)
    basic.pause(700)
    motor_run(-80, 180)
    basic.pause(350)
    motor_run(120, 255)
    basic.pause(800)
    motor_run(-80, 180)
    basic.pause(300)
    motor_run(120, 255)
}

bluetooth.onBluetoothConnected(function on_bluetooth_connected() {
    basic.showIcon(IconNames.Happy)
})
bluetooth.onBluetoothDisconnected(function on_bluetooth_disconnected() {
    basic.showIcon(IconNames.Sad)
})
control.inBackground(function onIn_background() {
    input.onButtonPressed(Button.A, function on_button_pressed_a() {
        
        if (prevodovka == 0) {
            prevodovka = 1
            basic.clearScreen()
            whaleysans.showNumber(prevodovka)
        } else {
            prevodovka = 0
            motor_run(0, 0)
            basic.clearScreen()
            whaleysans.showNumber(prevodovka)
        }
        
    })
})
control.onEvent(EventBusSource.MES_DPAD_CONTROLLER_ID, EventBusValue.MICROBIT_EVT_ANY, function on_mes_dpad_controller_id_microbit_evt() {
    
    // prepinani prevodovky
    if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_1_DOWN) {
        if (prevodovka == 0) {
            prevodovka = 1
        } else {
            prevodovka = 0
            motor_run(0, 0)
        }
        
        whaleysans.showNumber(prevodovka)
    }
    
    // zapinani/vypinani sonaru
    if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_2_DOWN) {
        if (sonarr == 0) {
            sonarr = 1
        } else {
            sonarr = 0
        }
        
    }
    
    // manualni rizeni
    if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_3_DOWN) {
        speed -= 0.05
        basic.showNumber(speed)
    } else if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_4_DOWN) {
        speed += 0.05
        basic.showNumber(speed)
    }
    
    if (prevodovka == 0) {
        if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_A_DOWN) {
            motor_run(120, 255, speed)
            pojistka = true
        } else if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_A_UP) {
            pojistka = false
            motor_run(0, 0)
        }
        
        if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_B_DOWN) {
            motor_run(-120, -255, speed)
            pojistka = true
        } else if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_B_UP) {
            motor_run(0, 0)
            pojistka = false
        }
        
        if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_C_DOWN) {
            motor_run(-120, 255, speed)
        }
        
        if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_D_DOWN) {
            motor_run(120, -255, speed)
        } else if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_D_UP && pojistka == false) {
            motor_run(0, 0)
        } else if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_C_UP && pojistka == false) {
            motor_run(0, 0)
        } else if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_D_UP && pojistka == true) {
            motor_run(120, 255, speed)
        } else if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_C_UP && pojistka == true) {
            motor_run(85, 255, speed)
        }
        
        if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_D_DOWN && pojistka == true) {
            motor_run(120, 125, speed)
        } else if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_C_DOWN && pojistka == true) {
            motor_run(115, 255, speed)
        }
        
    } else if (prevodovka == 1) {
        //  autonomní ovládání
        // if control.event_value() == EventBusValue.MES_DPAD_BUTTON_A_DOWN:
        //     pojistka = True
        // elif control.event_value() == EventBusValue.MES_DPAD_BUTTON_A_UP:
        //     pojistka = False
        // if control.event_value() == EventBusValue.MES_DPAD_BUTTON_B_DOWN:
        //     pojistka = True
        // elif control.event_value() == EventBusValue.MES_DPAD_BUTTON_B_UP:
        //    pojistka = False
        if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_C_DOWN) {
            left = true
        }
        
        if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_D_DOWN) {
            right = true
        } else if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_D_UP) {
            right = false
        } else if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_C_UP) {
            left = false
        }
        
    }
    
})
// autonomni rizeni
forever(function ovladani_forev() {
    
    if (prevodovka == 1) {
        if (sonarr == 1) {
            if (sonar.ping(DigitalPin.P2, DigitalPin.P1, PingUnit.Centimeters) <= 13) {
                sonarr = 0
                objetí()
            }
            
        } else if (pins.digitalReadPin(F_sensor) == 0 && pins.digitalReadPin(R_sensor) == 0 && pins.digitalReadPin(L_sensor) == 0) {
            // elif pins.digital_read_pin(F_sensor) == 1 and pins.digital_read_pin(L_sensor) == 1:
            //     both_time=control.millis()
            //     if left==True:
            //         PCAmotor.motor_run(PCAmotor.Motors.M2, -120)
            //         PCAmotor.motor_run(PCAmotor.Motors.M4, 120)
            //     elif right==True:
            //         PCAmotor.motor_run(PCAmotor.Motors.M2, 120)
            //         PCAmotor.motor_run(PCAmotor.Motors.M4, -120)
            //     #else:
            console.log(control.millis())
            if (left == true) {
                motor_run(-130, 100)
                basic.pause(150)
                motor_run(100, 120)
                basic.pause(150)
            } else if (right == true) {
                motor_run(80, -150)
                basic.pause(150)
                motor_run(100, 120)
                basic.pause(150)
            } else {
                motor_run(100, 120, speed)
                basic.pause(150)
            }
            
        } else if (pins.digitalReadPin(R_sensor) == 0) {
            motor_run(100, -80, speed)
        } else if (pins.digitalReadPin(L_sensor) == 0) {
            motor_run(-80, 120, speed)
        } else if (pins.digitalReadPin(F_sensor) == 0) {
            motor_run(100, 120, speed)
        }
        
    }
    
})
