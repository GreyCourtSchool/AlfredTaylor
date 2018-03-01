from evdev import InputDevice, categorize, ecodes
gamepad = InputDevice('/dev/input/event0')
num=0
#EVENT TYPES FROM MY STUPID RESEARCH
#0 is empty movement
#4 is empty button press
#3 is D Pad input
#1 is Button presses
#BUTTONS CODES
#1 Y-axis
#0 X-axis
#304
#305
#312
#313
#VALUE CODES
#0L UP,LEFT,BUTTON RELEASED
#1L BUTTON PRESSED
#127L AXIS NEUTRAL
#255L DOWN RIGHT

for event in gamepad.read_loop():
        if event.type!=0 and event.type!=4:
                print(event.code,event.type,event.value)
                if event.type==3:
                        if event.code==1:
                                if event.value==0L:
                                        print("UP")
                                elif event.value==255L:
                                        print("DOWN")
                                elif event.value==127L:
                                        print("Y-RELEASE")
                        elif event.code==0:
                                if event.value==0L:
                                        print("LEFT")
                                elif event.value==255L:
                                        print("RIGHT")
                                elif event.value==127L:
                                        print("X-RELEASE")
                if event.type==1:
                        if event.code==304:
                                if event.value==1L:
                                        print("A PRESSED")
                                elif event.value==0L:
                                        print("A RELEASED")
                        elif event.code==305:
                                if event.value==1L:
                                        print("B PRESSED")
                                if event.value==0L:
                                        print("B RELEASED")
                        elif event.code==312:
                                if event.value==1L:
                                        print("SELECT PRESSED")
                                elif event.value==0L:
                                        print("SELECT RELEASED")
                        elif event.code==313:
                                if event.value==1L:
                                        print("START PRESSED")
                                elif event.value==0L:
                                        print("START RELEASED")
                                
                                        
                
