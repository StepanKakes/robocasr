speed_factor = 80
right = False
left = False
prevodovka = 0 #0 - manual, 1 - automat
pojistka = False #pojistka pro zatáčení
speed=100
counter=0
P15_time=0
P8_time=0
both_time=0
bluetooth.start_uart_service()
pins.set_pull(DigitalPin.P8, PinPullMode.PULL_NONE)
pins.set_pull(DigitalPin.P15, PinPullMode.PULL_NONE)
bluetooth.start_accelerometer_service()
bluetooth.start_button_service()
bluetooth.start_io_pin_service()
bluetooth.start_led_service()
bluetooth.start_temperature_service()
bluetooth.start_magnetometer_service()

def motor_run(left = 0, right = 0, speed_factor = 80):
    PCAmotor.motor_run(PCAmotor.Motors.M1, Math.map(Math.constrain(left * (speed_factor / 100), -100, 100), -100, 100, -150, 150))
    PCAmotor.motor_run(PCAmotor.Motors.M4, Math.map(Math.constrain(right * (speed_factor / 100), -100, 100), -100, 100, -255, 255))

def on_bluetooth_connected():
    basic.show_icon(IconNames.HAPPY)
bluetooth.on_bluetooth_connected(on_bluetooth_connected)

def on_bluetooth_disconnected():
    basic.show_icon(IconNames.SAD)
bluetooth.on_bluetooth_disconnected(on_bluetooth_disconnected)

def on_button_pressed_a():
    global prevodovka
    if prevodovka == 0:
        prevodovka = 1
    else:
        prevodovka = 0
    basic.show_icon(IconNames.HEART)
input.on_button_pressed(Button.A, on_button_pressed_a)

#def on_forever():
    
    #print(control.event_value())
#basic.forever(on_forever)

def on_mes_dpad_controller_id_microbit_evt():
    global prevodovka, speed_factor,pojistka
    print(speed_factor)
    #prepinani prevodovky
    if control.event_value() == EventBusValue.MES_DPAD_BUTTON_1_DOWN:
        if prevodovka == 0:
            prevodovka = 1
            
        else:
            prevodovka = 0
            motor_run(0, 0)
        print(prevodovka)
    if control.event_value() == EventBusValue.MES_DPAD_BUTTON_3_DOWN:
        speed_factor-=10
    #manualni rizeni
    if prevodovka == 0:
        if control.event_value() == EventBusValue.MES_DPAD_BUTTON_A_DOWN:
            motor_run(100, 100,speed_factor)
            pojistka = True
        
        elif control.event_value() == EventBusValue.MES_DPAD_BUTTON_A_UP:
            pojistka = False
            motor_run(0, 0)
        if control.event_value() == EventBusValue.MES_DPAD_BUTTON_B_DOWN:
            motor_run(-100,-100,speed_factor)
            pojistka = True
        elif control.event_value() == EventBusValue.MES_DPAD_BUTTON_B_UP:
            motor_run(0, 0)
            pojistka = False
        if control.event_value() == EventBusValue.MES_DPAD_BUTTON_C_DOWN:
            motor_run(-100, 100)
        if control.event_value() == EventBusValue.MES_DPAD_BUTTON_D_DOWN:
            motor_run(100, -100)
        elif control.event_value() == EventBusValue.MES_DPAD_BUTTON_D_UP and pojistka == False:
            motor_run(0, 0)
        elif control.event_value() == EventBusValue.MES_DPAD_BUTTON_C_UP and pojistka == False:
            motor_run(0, 0)
        elif control.event_value() == EventBusValue.MES_DPAD_BUTTON_D_UP and pojistka == True:
            motor_run(100, 100)
        elif control.event_value() == EventBusValue.MES_DPAD_BUTTON_C_UP and pojistka == True:
            motor_run(100, 100)
        if control.event_value() == EventBusValue.MES_DPAD_BUTTON_D_DOWN and pojistka == True:
            motor_run(100, 50)
        elif control.event_value() == EventBusValue.MES_DPAD_BUTTON_C_DOWN and pojistka == True:
            motor_run(50, 100)
control.on_event(EventBusSource.MES_DPAD_CONTROLLER_ID,EventBusValue.MICROBIT_EVT_ANY,on_mes_dpad_controller_id_microbit_evt)

#autonomni rizeni
def ovladani_forev():
    global prevodovka, left, right, counter, both_time,P15_time,P8_time
    if prevodovka == 1:
        
        if pins.digital_read_pin(DigitalPin.P8) == 0 and pins.digital_read_pin(DigitalPin.P15) == 0:
            PCAmotor.motor_run(PCAmotor.Motors.M1, 100)
            PCAmotor.motor_run(PCAmotor.Motors.M4, 100)
        elif pins.digital_read_pin(DigitalPin.P8) == 1 and pins.digital_read_pin(DigitalPin.P15) == 1:
            both_time=control.millis()
        #    if left==True:
        #        PCAmotor.motor_run(PCAmotor.Motors.M1, -100)
        #        PCAmotor.motor_run(PCAmotor.Motors.M4, 100)
        #    elif right==True:
        #        PCAmotor.motor_run(PCAmotor.Motors.M1, 100)
        #        PCAmotor.motor_run(PCAmotor.Motors.M4, -100)
        #    #else:
        #    #if control.millis()-P8_time<=550 or control.millis()-P15_time<=550:
        #    #    counter+=1
        #    #else:
        #    #    counter=0
        #    #if counter==2:
        #    #    counter=0
        #    #PCAmotor.motor_run(PCAmotor.Motors.M1, 70)
        #    #PCAmotor.motor_run(PCAmotor.Motors.M4, 70)
        elif pins.digital_read_pin(DigitalPin.P8) == 1:
            right = True
            if left == True:
                left = False
            #print(control.millis())
#
            if control.millis()-P15_time<=550 or control.millis()-both_time<=550:
                counter+=1
            else:
                counter=0
            if counter==2:
                print(counter)
                counter=0
                PCAmotor.motor_run(PCAmotor.Motors.M1, 100)
                PCAmotor.motor_run(PCAmotor.Motors.M4, 100)
            else :
                P8_time=control.millis()
                PCAmotor.motor_run(PCAmotor.Motors.M1, 100)
                PCAmotor.motor_run(PCAmotor.Motors.M4, -120)
        elif pins.digital_read_pin(DigitalPin.P15) == 1:
            #left = True
            #if right == True:
            #    right = False
            if control.millis()-P8_time<=550 or control.millis()-both_time<=550:
                counter+=1
            else:
                counter=0
            if counter==2:
                print(counter)
                counter=0
                PCAmotor.motor_run(PCAmotor.Motors.M1, 100)
                PCAmotor.motor_run(PCAmotor.Motors.M4, 100)
            else :
                P15_time=control.millis()
                PCAmotor.motor_run(PCAmotor.Motors.M1, -100)
                PCAmotor.motor_run(PCAmotor.Motors.M4, 100)
forever(ovladani_forev)

    
    