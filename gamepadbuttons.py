from evdev import InputDevice, categorize, ecodes, KeyEvent	
gamepad = InputDevice('/dev/input/event3')
for event in gamepad.read_loop():
	keyevent=categorize(event)
	print(keyevent)
	print(keyevent.keystate)
	if event.type==ecodes.EV_KEY:
		if keyevent.keystate== KeyEvent.key_down:
			if keyevent.keycode =='BTN_B':
				print("B PRESSED")
			if keyevent.keycode =='BTN_A':
				print("A PRESSED")
