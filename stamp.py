import time, ctypes
import csv
import threading
import random

def stamp( state ,time_):
	with open("wl.log","a") as log_file:
		f_writer = csv.writer(log_file, delimiter = ',')
		#f_writer.writerow([str(state), str(int(time.time()))])
		f_writer.writerow([str(state), time_])
		print ([str(state), str(int(time.time()))])

def write_raport():
	rap_file = open("raport.csv","a")
	fw = csv.writer(rap_file, delimiter = ',')

	log_file = open("wl.log", "r")
	fr = list(csv.reader(log_file))

	prev_state = fr[0][0]
	last_stamp = fr[0][1]

	index = 0
	for row in fr:
		index +=1
		if row[0] != prev_state:
			fw.writerow([str(index), prev_state, time.ctime(int(last_stamp)), 
				time.ctime(int(row[1])), str(int(row[1]) - int(last_stamp))])
			last_stamp = row[1]
			prev_state = row[0]
	rap_file.close()
	log_file.close()

prev_rand = 1
def debug_wirte_log():
	global prev_rand
	time_ = int(time.time())

	for _ in range(500):
		rand = random.random()
		if prev_rand == 1:
			rand += 0.45
		else:
			rand -=0.45

		if (rand > 0.5):
			stamp(1,time_)
			time_ +=3
			prev_rand = 1
		else:
			stamp(0, time_)
			time_ += 1
			prev_rand = 0

start = time.time()

#debug_wirte_log()
write_raport()

print (time.time()-start)


