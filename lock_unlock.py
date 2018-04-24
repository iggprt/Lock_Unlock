import ctypes, time, threading
import msvcrt
import sys

user32 = ctypes.windll.User32
OpenDesktop = user32.OpenDesktopA
SwitchDesktop = user32.SwitchDesktop
DESKTOP_SWITCHDESKTOP = 0x0100

start_time = 0
due_time = 0
prev_state = -1
lock = 0
unlock = 0
flg = 0
time_left = 0
worked = 0
breaked = 0
last_lock = 0
last_unlock = 0
state = 1
lock = threading.Lock()

#its a function to write in this file
def print_in_file(msg):
	file = open("work.log","a+")
	file.write(msg)
	file.close()

# its a flag to exit all threads
def exit_flag():
	if flg: 
		return 1
	return 0

# display the time nicely
def	time_str(a):
	hours = int(a/3600)
	msg = str(hours)
	msg += ':'
	minutes = int((a-hours*3600)/60)
	msg += str(int((a-hours*3600)/60))
	secs = int(a-(hours*3600) - minutes*60)
	msg+= ":"+str(secs)
	return msg

def cyclic():

	global prev_state
	global time_left, last_lock, last_unlock
	global worked, breaked
	global state
	
	time_left = due_time - worked - start_time
	
	hDesktop = OpenDesktop ("default", 0, False, DESKTOP_SWITCHDESKTOP)
	#state = SwitchDesktop (hDesktop)	
	
	#detect change of state
	if prev_state !=  state:
		if state == 1:
			if last_lock != 0:
				breaked += time.time() - last_lock		
			last_unlock = time.time()
			print "unlocked: " + time_str(breaked) + " " + time.ctime()
		else:
			print "locked:   " + time_str(worked)  + " " + time.ctime()
			worked += time.time() - last_unlock
			last_lock = time.time()
			print_in_file( "\nwork sesion started at: " + time.ctime(last_unlock) + " and endded at: " + time.ctime(last_lock) + " been working: " + time_str(time.time() - last_unlock))

	if exit_flag():
		worked += time.time() - last_unlock
		last_lock = time.time()
		
		msg = "\nwork sesion started at: " + time.ctime(last_unlock) + " and endded at: " + time.ctime(last_lock) + " been working: " + time_str(time.time() - last_unlock)
		msg += "\nday endded at: " + time.ctime()
		msg += "\nworked this day: " + time_str(worked)
		msg += "\nbreaked this day: " + time_str(breaked)
		
		print_in_file(msg)
		sys.exit()
		
	prev_state = state
	threading.Timer(1, cyclic).start()

def looking_for_key():
	global flg
	global due_time, last_lock, last_unlock, breaked, worked, state, start_time
	while True:
		if msvcrt.kbhit():
			key = msvcrt.getch()
			if key == 'q':
				print "nuuuuu.."
				flg = 1
				sys.exit()
			if key == 'a':
				print "\n" + time.ctime(time.time() + (due_time - start_time - (time.time()-last_unlock) - worked) + 2700)
				print time_str(due_time - start_time - (time.time()-last_unlock) - worked) + " l"
				print time_str(time.time()-last_unlock + worked) + " w"
				print time_str(breaked) + " b"
			if key == 'l':
				state = 0
			if key == 'u':
				state = 1

	threading.Timer(1, looking_for_key).start()
	
def Main():
	global start_time, due_time, last_unlock
	print("press: a for info or q to quit")
	print_in_file("\n\nDay started at: " + time.ctime())
	start_time = time.time()
	due_time = start_time + 31500;
	last_unlock = time.time()
	
	cyclic()
	looking_for_key()
	
if __name__ == "__main__":
	Main()
	