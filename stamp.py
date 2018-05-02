import time, ctypes
import csv
import os
import lock_unlock

def stamp( state ):
	with open("wl.log","a") as log_file:
		f_writer = csv.writer(log_file, delimiter = ',')
		f_writer.writerow([str(state), str(int(time.time()))])
		print lock_unlock.state

def write_report():

	rap_file = open("raport.csv","ab")
	fw = csv.writer(rap_file, delimiter = ',')

	try:
		log_file = open("wl.log", "r")
		fr = list(csv.reader(log_file))
	except IOError:
		return 0

	prev_state = fr[0][0]
	last_stamp = int(fr[0][1])
	
	for row in fr:
		if row[0] != prev_state:
			w_row = []
			
			#time stamp	
			w_row.append(str(row[1]))
			
			#date
			date = time.strftime("%m/%d/%Y", time.gmtime(int(row[1])))
			w_row.append(date)
			
			#state
			w_row.append(prev_state)
			
			#start time
			w_row.append(time.strftime("%H:%M:%S", time.gmtime(last_stamp)))
			
			#end time
			w_row.append(time.strftime("%H:%M:%S", time.gmtime(int(row[1]))))
			
			#interval 
			session_len = int(row[1]) - last_stamp
			w_row.append(time.strftime("%H:%M:%S", time.gmtime(session_len)))
			
			print w_row
			
			if session_len <= 8*3600:
				fw.writerow(w_row)
			else:
				fw.writerow([])
			last_stamp = int(row[1])
			prev_state = row[0]
	rap_file.close()
	log_file.close()
	
	os.remove("wl.log")
	
	return 0

def start_stamp():
	log_file = open("wl.log", "r")
	fr = csv.reader(log_file)
	start = next(fr)[0]
	log_file.close()	
	return start
	
def Main():
	write_report()
	
if __name__ == "__main__":
	Main()
	