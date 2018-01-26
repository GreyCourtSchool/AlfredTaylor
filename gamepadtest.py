from evdev import InputDevice, categorize, ecodes
gamepad = InputDevice('/dev/input/event3')
num=0
for event in gamepad.read_loop():
	if event.type==ecodes.EV_KEY:
		print(categorize(event))
	else:
		print('Not a button')
	num+=1
	print(num)
