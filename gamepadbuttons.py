from evdev import InputDevice, categorize, ecodes, KeyEvent	
import time
gamepad = InputDevice('/dev/input/event0')
def getInput(device,t):
        timeDone=False
        inputRecieved=False
        start=time.clock()
        while(not timeDone or not inputRecieved):
                event=gamepad.read_one()
                if event!=None:
                        if event.type!=0 and event.type!=4:
                                padin="_"
                                if (event.type==1 and event.value!=0L):
                                        if event.code==304:
                                                padin="A"
                                        elif event.code==305:
                                                padin="B"
                                        elif event.code==312:
                                                padin="SELECT"
                                        elif event.code==313:
                                                padin="START"
                                elif (event.type==3 and event.value!=127L):
                                        if event.code==1:
                                                if event.value==0L:
                                                        padin="UP"
                                                elif event.value==255L:
                                                        padin="DOWN"
                                        elif event.code==0:
                                                if event.value==0L:
                                                        padin="LEFT"
                                                if event.value==255L:
                                                        padin="RIGHT"
                                inputRecieved=True
                                return(padin)
                if t!=0:
                        if (time.clock()-start>t):
                                timeDone=True
                                return(None)
                                        
                                
                                
userin=getInput(gamepad,5)
print(userin)
if userin==None:
        print("Timed out")
