import csv
import datetime
import pprint as prettyPrint

#Groups the data per 1 minute interval.
def getHourMinutes(timestamp):
	dateTime = datetime.datetime.fromtimestamp(timestamp).isoformat().split("T")
	hrmin = dateTime[1].split(":")
	return [hrmin[0], hrmin[1]]

def csv_reader(file):
	users = {}
	with open(file, 'rU') as mycsv:
		reader = csv.reader(x.replace('\0', '') for x in mycsv)
		begin = True
		for row in reader:
			if begin == False:
				tmp_data = ""
				tmp_key  = ""
				if(row[0] == "NATIVE_KEY_TYPED" or row[0] == "NATIVE_KEY_PRESSED" or row[0] == "NATIVE_KEY_RELEASED"):
					hr_min = "_".join(getHourMinutes(int(row[10])))
				else:
					hr_min = "_".join(getHourMinutes(int(row[8])))
				if not row[0] in users:
					users[row[0]] ={}
				if not hr_min in users[row[0]]:
					users[row[0]][hr_min] = []
				users[row[0]][hr_min].append(row)
				#users[row[0]][hr_min].append(row)
			else:
				pass
			begin = False
		prettyPrint.pprint(users)
csv_reader("data.csv")
