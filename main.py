speed_factor = 80
right = False
left = False
prevodovka = 0 #0 - manual, 1 - automat
pojistka = False #pojistka pro zatáčení
speed=120
counter=0
P15_time=0
P8_time=0
both_time=0

bluetooth.start_uart_service()
pins.set_pull(DigitalPin.P8, PinPullMode.PULL_NONE)
pins.set_pull(DigitalPin.P13, PinPullMode.PULL_NONE)
pins.set_pull(DigitalPin.P15, PinPullMode.PULL_NONE)
bluetooth.start_accelerometer_service()
bluetooth.start_button_service()
bluetooth.start_io_pin_service()
bluetooth.start_led_service()
bluetooth.start_temperature_service()
bluetooth.start_magnetometer_service()

def motor_run(left = 0, right = 0):
    PCAmotor.motor_run(PCAmotor.Motors.M2,left)
    PCAmotor.motor_run(PCAmotor.Motors.M4,right)

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
    global prevodovka, pojistka, left, right
    print(speed_factor)
    #prepinani prevodovky
    if control.event_value() == EventBusValue.MES_DPAD_BUTTON_1_DOWN:
        if prevodovka == 0:
            prevodovka = 1
            
        else:
            prevodovka = 0
            motor_run(0, 0)
        print(prevodovka)
    #manualni rizeni
    if prevodovka == 0:
        if control.event_value() == EventBusValue.MES_DPAD_BUTTON_A_DOWN:
            motor_run(120, 255)
            pojistka = True
        
        elif control.event_value() == EventBusValue.MES_DPAD_BUTTON_A_UP:
            pojistka = False
            motor_run(0, 0)
        if control.event_value() == EventBusValue.MES_DPAD_BUTTON_B_DOWN:
            motor_run(-120,-255)
            pojistka = True
        elif control.event_value() == EventBusValue.MES_DPAD_BUTTON_B_UP:
            motor_run(0, 0)
            pojistka = False
        if control.event_value() == EventBusValue.MES_DPAD_BUTTON_C_DOWN:
            motor_run(-120, 255)
        if control.event_value() == EventBusValue.MES_DPAD_BUTTON_D_DOWN:
            motor_run(120, -255)
        elif control.event_value() == EventBusValue.MES_DPAD_BUTTON_D_UP and pojistka == False:
            motor_run(0, 0)
        elif control.event_value() == EventBusValue.MES_DPAD_BUTTON_C_UP and pojistka == False:
            motor_run(0, 0)
        elif control.event_value() == EventBusValue.MES_DPAD_BUTTON_D_UP and pojistka == True:
            motor_run(120, 255)
        elif control.event_value() == EventBusValue.MES_DPAD_BUTTON_C_UP and pojistka == True:
            motor_run(120, 255)
        if control.event_value() == EventBusValue.MES_DPAD_BUTTON_D_DOWN and pojistka == True:
            motor_run(120, 125)
        elif control.event_value() == EventBusValue.MES_DPAD_BUTTON_C_DOWN and pojistka == True:
            motor_run(115, 255)
    # autonomní ovládání
    elif prevodovka == 1: 
        #if control.event_value() == EventBusValue.MES_DPAD_BUTTON_A_DOWN:
        #    pojistka = True
        #elif control.event_value() == EventBusValue.MES_DPAD_BUTTON_A_UP:
        #    pojistka = False
        #if control.event_value() == EventBusValue.MES_DPAD_BUTTON_B_DOWN:
        #    pojistka = True
        #elif control.event_value() == EventBusValue.MES_DPAD_BUTTON_B_UP:
        #   pojistka = False
        if control.event_value() == EventBusValue.MES_DPAD_BUTTON_C_DOWN:
            left=True
        if control.event_value() == EventBusValue.MES_DPAD_BUTTON_D_DOWN:
            right=True
        elif control.event_value() == EventBusValue.MES_DPAD_BUTTON_D_UP:
            right=False
        elif control.event_value() == EventBusValue.MES_DPAD_BUTTON_C_UP:
            left=False
control.on_event(EventBusSource.MES_DPAD_CONTROLLER_ID,EventBusValue.MICROBIT_EVT_ANY,on_mes_dpad_controller_id_microbit_evt)

#autonomni rizeni
def ovladani_forev():
    global prevodovka, left, right, counter, both_time,P15_time,P8_time
    
    if prevodovka == 1:
        if sonar.ping(DigitalPin.P0, DigitalPin.P1, PingUnit.CENTIMETERS)<= 15:
            motor_run(120,-255)
            basic.pause(200)
            motor_run(120,255)
            basic.pause(1000)
            motor_run(-100,200)
            basic.pause(250)
            motor_run(120,255)
            basic.pause(1300)
            motor_run(-100,200)
            basic.pause(250)
            motor_run(140,255)
            basic.pause(500)
            motor_run(120,-255)
            basic.pause(200)
       
        #elif pins.digital_read_pin(DigitalPin.P8) == 1 and pins.digital_read_pin(DigitalPin.P15) == 1:
        #    both_time=control.millis()
        #    if left==True:
        #        PCAmotor.motor_run(PCAmotor.Motors.M2, -120)
        #        PCAmotor.motor_run(PCAmotor.Motors.M4, 120)
        #    elif right==True:
        #        PCAmotor.motor_run(PCAmotor.Motors.M2, 120)
        #        PCAmotor.motor_run(PCAmotor.Motors.M4, -120)
        #    #else:
        
        
        if pins.digital_read_pin(DigitalPin.P8) == 0 and pins.digital_read_pin(DigitalPin.P13) == 0 and pins.digital_read_pin(DigitalPin.P15) == 0:
            print(control.millis())
            if left==True:
                motor_run(-130,100)
                basic.pause(150)
                motor_run(100,120)
                basic.pause(150)
            elif right==True:
                motor_run(80,-150)
                basic.pause(150)
                motor_run(100,120)
                basic.pause(150)
            else:
                motor_run(100,120)
                basic.pause(150)
        elif pins.digital_read_pin(DigitalPin.P13) == 0:
            P8_time=control.millis()
            #print(control.millis())
            motor_run(100,-80)
        elif pins.digital_read_pin(DigitalPin.P15) == 0:
             motor_run(-80,120)
        elif pins.digital_read_pin(DigitalPin.P8) == 0:
           motor_run(100,120)
forever(ovladani_forev) 

    
    