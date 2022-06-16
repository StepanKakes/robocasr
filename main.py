right = False
left = False
L_sensor = DigitalPin.P15
R_sensor = DigitalPin.P13
F_sensor = DigitalPin.P8
prevodovka = 0 #0 - manual, 1 - automat
sonarr = 0
pojistka = False #pojistka pro zatáčení
speed=1.0

bluetooth.start_uart_service()
pins.set_pull(F_sensor, PinPullMode.PULL_NONE)
pins.set_pull(R_sensor, PinPullMode.PULL_NONE)
pins.set_pull(L_sensor, PinPullMode.PULL_NONE)
#bluetooth.start_accelerometer_service()
#bluetooth.start_button_service()
#bluetooth.start_io_pin_service()
#bluetooth.start_led_service()
#bluetooth.start_temperature_service()
#bluetooth.start_magnetometer_service()

def motor_run(left, right, speed=1):
    PCAmotor.motor_run(PCAmotor.Motors.M2,left*speed)
    PCAmotor.motor_run(PCAmotor.Motors.M4,right*speed)

def objetí():
    motor_run(120,-255)
    basic.pause(200)
    motor_run(120,255)
    basic.pause(700)
    motor_run(-80,180)
    basic.pause(350)
    motor_run(120,255)
    basic.pause(800)
    motor_run(-80,180)
    basic.pause(300)
    motor_run(120,255)



def on_bluetooth_connected():
    basic.show_icon(IconNames.HAPPY)
bluetooth.on_bluetooth_connected(on_bluetooth_connected)

def on_bluetooth_disconnected():
    basic.show_icon(IconNames.SAD)
bluetooth.on_bluetooth_disconnected(on_bluetooth_disconnected)

def onIn_background():
    def on_button_pressed_a():
        global prevodovka
        if prevodovka == 0:
            prevodovka = 1
            basic.clear_screen()
            whaleysans.show_number(prevodovka)
        else:
            prevodovka = 0
            motor_run(0, 0)
            basic.clear_screen()
            whaleysans.show_number(prevodovka)
    input.on_button_pressed(Button.A, on_button_pressed_a)
control.in_background(onIn_background)


def on_mes_dpad_controller_id_microbit_evt():
    global prevodovka, pojistka, left, right, speed, sonarr
    #prepinani prevodovky
    if control.event_value() == EventBusValue.MES_DPAD_BUTTON_1_DOWN:
        if prevodovka == 0:
            prevodovka = 1
            
        else:
            prevodovka = 0
            motor_run(0, 0)
        whaleysans.show_number(prevodovka)
    #zapinani/vypinani sonaru
    if control.event_value() == EventBusValue.MES_DPAD_BUTTON_2_DOWN:
        if sonarr == 0:
            sonarr = 1
        else:
            sonarr = 0
    #manualni rizeni
    if control.event_value() == EventBusValue.MES_DPAD_BUTTON_3_DOWN:
        speed -= 0.05
        basic.show_number(speed)
    elif control.event_value() == EventBusValue.MES_DPAD_BUTTON_4_DOWN:
        speed += 0.05
        basic.show_number(speed)

    if prevodovka == 0:
        if control.event_value() == EventBusValue.MES_DPAD_BUTTON_A_DOWN:
            motor_run(120, 255, speed)
            pojistka = True
        
        elif control.event_value() == EventBusValue.MES_DPAD_BUTTON_A_UP:
            pojistka = False
            motor_run(0, 0)
        if control.event_value() == EventBusValue.MES_DPAD_BUTTON_B_DOWN:
            motor_run(-120,-255, speed)
            pojistka = True
        elif control.event_value() == EventBusValue.MES_DPAD_BUTTON_B_UP:
            motor_run(0, 0)
            pojistka = False
        if control.event_value() == EventBusValue.MES_DPAD_BUTTON_C_DOWN:
            motor_run(-120, 255, speed)
        if control.event_value() == EventBusValue.MES_DPAD_BUTTON_D_DOWN:
            motor_run(120, -255, speed)
        elif control.event_value() == EventBusValue.MES_DPAD_BUTTON_D_UP and pojistka == False:
            motor_run(0, 0)
        elif control.event_value() == EventBusValue.MES_DPAD_BUTTON_C_UP and pojistka == False:
            motor_run(0, 0)
        elif control.event_value() == EventBusValue.MES_DPAD_BUTTON_D_UP and pojistka == True:
            motor_run(120, 255, speed)
        elif control.event_value() == EventBusValue.MES_DPAD_BUTTON_C_UP and pojistka == True:
            motor_run(85, 255, speed)
        if control.event_value() == EventBusValue.MES_DPAD_BUTTON_D_DOWN and pojistka == True:
            motor_run(120, 125, speed)
        elif control.event_value() == EventBusValue.MES_DPAD_BUTTON_C_DOWN and pojistka == True:
            motor_run(115, 255, speed)
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
    global prevodovka, left, right, speed, sonarr
    
    if prevodovka == 1:
        if sonarr == 1:
            if sonar.ping(DigitalPin.P2, DigitalPin.P1, PingUnit.CENTIMETERS)<= 13:
                sonarr=0
                objetí()
       
        #elif pins.digital_read_pin(F_sensor) == 1 and pins.digital_read_pin(L_sensor) == 1:
        #    both_time=control.millis()
        #    if left==True:
        #        PCAmotor.motor_run(PCAmotor.Motors.M2, -120)
        #        PCAmotor.motor_run(PCAmotor.Motors.M4, 120)
        #    elif right==True:
        #        PCAmotor.motor_run(PCAmotor.Motors.M2, 120)
        #        PCAmotor.motor_run(PCAmotor.Motors.M4, -120)
        #    #else:
        
        
        elif pins.digital_read_pin(F_sensor) == 0 and pins.digital_read_pin(R_sensor) == 0 and pins.digital_read_pin(L_sensor) == 0:
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
                motor_run(100,120, speed)
                basic.pause(150)
        elif pins.digital_read_pin(R_sensor) == 0:
            motor_run(100,-80, speed)
        elif pins.digital_read_pin(L_sensor) == 0:
             motor_run(-80,120, speed)
        elif pins.digital_read_pin(F_sensor) == 0:
           motor_run(100,120, speed)
forever(ovladani_forev) 

    
    