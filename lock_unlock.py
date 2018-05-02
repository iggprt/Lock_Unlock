import ctypes, time, threading
import msvcrt
import sys
import stamp

user32 = ctypes.windll.User32
OpenDesktop = user32.OpenDesktopA
SwitchDesktop = user32.SwitchDesktop
DESKTOP_SWITCHDESKTOP = 0x0100

prev_state = -1
flg = 0
state = 1

# its a flag to exit all threads
def exit_flag():
	if flg: 
		return 1
	return 0
	
def log_write_cycle():
	global state
	stamp.stamp(state)
	print state
	threading.Timer(2, log_write_cycle).start()

	
def cyclic():
	global prev_state,state
	
	hDesktop = OpenDesktop ("default", 0, False, DESKTOP_SWITCHDESKTOP)
	#state = SwitchDesktop (hDesktop)	
	
	stamp.stamp(state)

	if exit_flag():
		stamp.stamp(0)
		stamp.write_report()
		sys.exit()
		
	prev_state = state
	threading.Timer(1, cyclic).start()

def looking_for_key():
	global flg, state
	while True:
		if msvcrt.kbhit():
			key = msvcrt.getch()
			if key == 'q':
				print "nuuuuu.."
				flg = 1
				sys.exit()
			if key == 'a':
				print "hm..."
			if key == 'l':
				state = 0
			if key == 'u':
				state = 1

	threading.Timer(1, looking_for_key).start()
	

def Main():
	
	stamp.write_report()
	stamp.stamp(1)	
	
	cyclic()
	looking_for_key()
	#log_write_cycle()	
	
if __name__ == "__main__":
	Main()
	