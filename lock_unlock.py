import ctypes, time, threading, math

user32 = ctypes.windll.User32
OpenDesktop = user32.OpenDesktopA
SwitchDesktop = user32.SwitchDesktop
DESKTOP_SWITCHDESKTOP = 0x0100

due_time = time.time()+ 31500
prev_state = -1
lock = 0
unlock = 0



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
	global lock, unlock, work_today, break_today
	
	time_left = due_time - time.time()
	
	hDesktop = OpenDesktop ("default", 0, False, DESKTOP_SWITCHDESKTOP)
	state = SwitchDesktop (hDesktop)	

	
	#detect change of state
	if prev_state !=  state:
		file = open("log.txt", "a+")
		if state == 1:
			unlock = time.time()
			work_today += unlock - lock
			file.write("\nunlocked: " + time.ctime() + " " + time_str(unlock - lock) + " work, Total today:" + time_str(work_today)) 
		else:
			lock = time.time()
			break_today += lock - unlock
			file.write("\nlocked:   " + time.ctime() + " " + time_str(lock - unlock) + " brak, Total today:" + time_str(work_today))  
		file.close()
		

	if(int(time.time())%5 == 0):
		#print str(time.time()) + "\b\b\b\b\b\b\b\b", end="", flush=True		
		print("hello", end="")
		print("hello") 

	
	prev_state = state
	threading.Timer(1, cyclic).start()

if __name__ == "__main__":
	print time_str(due_time)
	lock = time.time()
	unlock = time.time()
	work_today = 0
	break_today = 0
	cyclic()