import ctypes, time, threading

user32 = ctypes.windll.User32
OpenDesktop = user32.OpenDesktopA
SwitchDesktop = user32.SwitchDesktop
DESKTOP_SWITCHDESKTOP = 0x0100

hDesktop = OpenDesktop ("default", 0, False, DESKTOP_SWITCHDESKTOP)
result = SwitchDesktop (hDesktop)

print(result)

def foo():
	user32 = ctypes.windll.User32
	OpenDesktop = user32.OpenDesktopA
	SwitchDesktop = user32.SwitchDesktop
	DESKTOP_SWITCHDESKTOP = 0x0100

	hDesktop = OpenDesktop ("default", 0, False, DESKTOP_SWITCHDESKTOP)
	result = SwitchDesktop (hDesktop)

	print(str(result) + " " + time.ctime())
	#print(time.ctime())
	
	threading.Timer(1, foo).start()
	
foo()