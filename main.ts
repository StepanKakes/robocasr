let speed_factor = 80
let right = false
let left = false
let prevodovka = 0
// 0 - manual, 1 - automat
let pojistka = false
// pojistka pro zatáčení
let speed = 120
let counter = 0
let P15_time = 0
let P8_time = 0
let both_time = 0
bluetooth.startUartService()
pins.setPull(DigitalPin.P8, PinPullMode.PullNone)
pins.setPull(DigitalPin.P13, PinPullMode.PullNone)
pins.setPull(DigitalPin.P15, PinPullMode.PullNone)
bluetooth.startAccelerometerService()
bluetooth.startButtonService()
bluetooth.startIOPinService()
bluetooth.startLEDService()
bluetooth.startTemperatureService()
bluetooth.startMagnetometerService()
function motor_run(left: number = 0, right: number = 0) {
    PCAmotor.MotorRun(PCAmotor.Motors.M2, left)
    PCAmotor.MotorRun(PCAmotor.Motors.M4, right)
}

bluetooth.onBluetoothConnected(function on_bluetooth_connected() {
    basic.showIcon(IconNames.Happy)
})
bluetooth.onBluetoothDisconnected(function on_bluetooth_disconnected() {
    basic.showIcon(IconNames.Sad)
})
input.onButtonPressed(Button.A, function on_button_pressed_a() {
    
    if (prevodovka == 0) {
        prevodovka = 1
    } else {
        prevodovka = 0
    }
    
    basic.showIcon(IconNames.Heart)
})
// def on_forever():
// print(control.event_value())
// basic.forever(on_forever)
control.onEvent(EventBusSource.MES_DPAD_CONTROLLER_ID, EventBusValue.MICROBIT_EVT_ANY, function on_mes_dpad_controller_id_microbit_evt() {
    
    console.log(speed_factor)
    // prepinani prevodovky
    if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_1_DOWN) {
        if (prevodovka == 0) {
            prevodovka = 1
        } else {
            prevodovka = 0
            motor_run(0, 0)
        }
        
        console.log(prevodovka)
    }
    
    // manualni rizeni
    if (prevodovka == 0) {
        if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_A_DOWN) {
            motor_run(120, 255)
            pojistka = true
        } else if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_A_UP) {
            pojistka = false
            motor_run(0, 0)
        }
        
        if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_B_DOWN) {
            motor_run(-120, -255)
            pojistka = true
        } else if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_B_UP) {
            motor_run(0, 0)
            pojistka = false
        }
        
        if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_C_DOWN) {
            motor_run(-120, 255)
        }
        
        if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_D_DOWN) {
            motor_run(120, -255)
        } else if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_D_UP && pojistka == false) {
            motor_run(0, 0)
        } else if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_C_UP && pojistka == false) {
            motor_run(0, 0)
        } else if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_D_UP && pojistka == true) {
            motor_run(120, 255)
        } else if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_C_UP && pojistka == true) {
            motor_run(120, 255)
        }
        
        if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_D_DOWN && pojistka == true) {
            motor_run(120, 125)
        } else if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_C_DOWN && pojistka == true) {
            motor_run(115, 255)
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
        if (sonar.ping(DigitalPin.P0, DigitalPin.P1, PingUnit.Centimeters) <= 15) {
            motor_run(120, -255)
            basic.pause(200)
            motor_run(120, 255)
            basic.pause(1000)
            motor_run(-100, 200)
            basic.pause(250)
            motor_run(120, 255)
            basic.pause(1300)
            motor_run(-100, 200)
            basic.pause(250)
            motor_run(140, 255)
            basic.pause(500)
            motor_run(120, -255)
            basic.pause(200)
        }
        
        // elif pins.digital_read_pin(DigitalPin.P8) == 1 and pins.digital_read_pin(DigitalPin.P15) == 1:
        //     both_time=control.millis()
        //     if left==True:
        //         PCAmotor.motor_run(PCAmotor.Motors.M2, -120)
        //         PCAmotor.motor_run(PCAmotor.Motors.M4, 120)
        //     elif right==True:
        //         PCAmotor.motor_run(PCAmotor.Motors.M2, 120)
        //         PCAmotor.motor_run(PCAmotor.Motors.M4, -120)
        //     #else:
        if (pins.digitalReadPin(DigitalPin.P8) == 0 && pins.digitalReadPin(DigitalPin.P13) == 0 && pins.digitalReadPin(DigitalPin.P15) == 0) {
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
                motor_run(100, 120)
                basic.pause(150)
            }
            
        } else if (pins.digitalReadPin(DigitalPin.P13) == 0) {
            P8_time = control.millis()
            // print(control.millis())
            motor_run(100, -80)
        } else if (pins.digitalReadPin(DigitalPin.P15) == 0) {
            motor_run(-80, 120)
        } else if (pins.digitalReadPin(DigitalPin.P8) == 0) {
            motor_run(100, 120)
        }
        
    }
    
})
