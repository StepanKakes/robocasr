let speed_factor = 80
let right = false
let left = false
let prevodovka = 0
// 0 - manual, 1 - automat
let pojistka = false
// pojistka pro zatáčení
let speed = 100
bluetooth.startUartService()
pins.setPull(DigitalPin.P8, PinPullMode.PullNone)
pins.setPull(DigitalPin.P15, PinPullMode.PullNone)
bluetooth.startAccelerometerService()
bluetooth.startButtonService()
bluetooth.startIOPinService()
bluetooth.startLEDService()
bluetooth.startTemperatureService()
bluetooth.startMagnetometerService()
function motor_run(left: number = 0, right: number = 0, speed_factor: number = 80) {
    PCAmotor.MotorRun(PCAmotor.Motors.M1, Math.map(Math.constrain(left * (speed_factor / 100), -100, 100), -100, 100, -150, 150))
    PCAmotor.MotorRun(PCAmotor.Motors.M4, Math.map(Math.constrain(right * (speed_factor / 100), -100, 100), -100, 100, -255, 255))
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
forever(function ovladani_forev() {
    
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
        
        if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_3_DOWN) {
            speed_factor -= 10
        }
        
        // manualni rizeni
        if (prevodovka == 0) {
            if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_A_DOWN) {
                motor_run(100, 100, speed_factor)
                pojistka = true
            } else if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_A_UP) {
                pojistka = false
                motor_run(0, 0)
            }
            
            if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_B_DOWN) {
                motor_run(-100, -100, speed_factor)
                pojistka = true
            } else if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_B_UP) {
                motor_run(0, 0)
                pojistka = false
            }
            
            if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_C_DOWN) {
                motor_run(-100, 100)
            }
            
            if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_D_DOWN) {
                motor_run(100, -100)
            } else if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_D_UP && pojistka == false) {
                motor_run(0, 0)
            } else if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_C_UP && pojistka == false) {
                motor_run(0, 0)
            } else if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_D_UP && pojistka == true) {
                motor_run(100, 100)
            } else if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_C_UP && pojistka == true) {
                motor_run(100, 100)
            }
            
            if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_D_DOWN && pojistka == true) {
                motor_run(100, 50)
            } else if (control.eventValue() == EventBusValue.MES_DPAD_BUTTON_C_DOWN && pojistka == true) {
                motor_run(50, 100)
            }
            
        }
        
    })
    // autonomni rizeni
    if (prevodovka == 1) {
        if (pins.digitalReadPin(DigitalPin.P8) == 0 && pins.digitalReadPin(DigitalPin.P15) == 0) {
            PCAmotor.MotorRun(PCAmotor.Motors.M1, 80)
            PCAmotor.MotorRun(PCAmotor.Motors.M4, 100)
        } else if (pins.digitalReadPin(DigitalPin.P8) == 1 && pins.digitalReadPin(DigitalPin.P15) == 1) {
            // if left==True:
            //     PCAmotor.motor_run(PCAmotor.Motors.M1, -80)
            //     PCAmotor.motor_run(PCAmotor.Motors.M4, 80)
            // elif right==True:
            //     PCAmotor.motor_run(PCAmotor.Motors.M1, 80)
            //     PCAmotor.motor_run(PCAmotor.Motors.M4, -80)
            // else:
            PCAmotor.MotorRun(PCAmotor.Motors.M1, 80)
            PCAmotor.MotorRun(PCAmotor.Motors.M4, 100)
        } else if (pins.digitalReadPin(DigitalPin.P8) == 1) {
            right = true
            if (left == true) {
                left = false
            }
            
            PCAmotor.MotorRun(PCAmotor.Motors.M1, 60)
            PCAmotor.MotorRun(PCAmotor.Motors.M4, -60)
        } else if (pins.digitalReadPin(DigitalPin.P15) == 1) {
            left = true
            if (right == true) {
                right = false
            }
            
            PCAmotor.MotorRun(PCAmotor.Motors.M1, -60)
            PCAmotor.MotorRun(PCAmotor.Motors.M4, 60)
        }
        
    }
    
})
