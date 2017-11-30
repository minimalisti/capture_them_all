import argparse as agp
import pandas as pd
import os

#Example usage python TMC-json-csv.py -filepath db.json -extract 'K' -sep ';' -dest ./data.csv
class tmcJsonParser:
	args = ""

	def getValuesFromJSONRows(self, data):
		string_vals = ','.join(data.values())
		return string_vals

	def __init__(self):
		json_raw_data = ""
		parsed_json = None
		self.argumentParser()
		if os.path.isfile(self.args.filepath):
			print("Reading Json File...")
			with open(self.args.filepath) as f:
				for lines in f:
					json_raw_data += lines
			parsed_json = pd.read_json(json_raw_data)
			MOUSE_DATA = []
			KEYBOARD_DATA = []
			for rows in parsed_json.rows:
				eventData = rows['doc']['eventData']
				userId = rows['doc']['userID']
				splited_data = eventData.split(',')
				if(splited_data[0] == "NATIVE_KEY_TYPED" or splited_data[0] == "NATIVE_KEY_PRESSED" or splited_data[0] == "NATIVE_KEY_RELEASED"):
					eventData = eventData.replace("'\r'","'\\r'")
					eventData = eventData.replace("\"", '\\"')
					splited_data = eventData.split(',')
				tmp_k = {'userId':userId, 'event':'', 'keyCode':'', 'keyText':'', 'keyChar':'','modifiers':'', 'keyLocation':'', 'rawCode':'', 'timeStamp':'','activeWindow':''}
				tmp_m = {'userId':userId,'event':'', 'position':'', 'button':'','modifiers':'', 'clickCount':'', 'scrollType':'','scrollAmount':'', 'wheelRotation':'', 'wheelDirection':''}
				events = None
				for data in splited_data:
					event = splited_data[0]
					if(event == "NATIVE_KEY_TYPED" or event == "NATIVE_KEY_PRESSED" or event == "NATIVE_KEY_RELEASED"):
						events = 'k'
						tmp_k["event"] = splited_data[0]
						if(data.find("=", 0) !=  -1):
							key_Val = data.split("=")
							tmp_k[key_Val[0]] = key_Val[1].replace("'", "")
					else:
					#if (event == "NATIVE_MOUSE_MOVED" or event == "NATIVE_MOUSE_DRAGGED" or event == "NATIVE_MOUSE_CLICKED" or event=="NATIVE_MOUSE_WHEEL" or event=="NATIVE_MOUSE_RELEASED" or event=="NATIVE_MOUSE_PRESSED"):
						events = 'm'
						tmp_m["event"] = splited_data[0]
						tmp_m["position"] = str(splited_data[1])+ "/ " + str(splited_data [2])
						if(data.find("=", 0)!= -1):
							key_Val = data.split("=")
							tmp_m[key_Val[0]] = key_Val[1].replace("'", "")		
				if events == 'k':
					tmp_k["timeStamp"] = str(rows['doc']['timeStamp']) # pussing in str as we need to join later
					tmp_k["activeWindow"] = rows['doc']['activeWindow']
				if events == 'm':
					tmp_m["timeStamp"] = str(rows['doc']['timeStamp']) # pussing in str as we need to join later
					tmp_m["activeWindow"] = rows['doc']['activeWindow']
				if events == 'k':
					KEYBOARD_DATA.append(self.getValuesFromJSONRows(tmp_k))
				if events == 'm':
					MOUSE_DATA.append(self.getValuesFromJSONRows(tmp_m))
				tmp_k = {}
				tmp_m = {}
				events = ''
			print("Finished Read Operation..")
			print("Writing Data to - "+self.args.destination+"...")
			if self.args.CsvDataType == "A" or self.args.CsvDataType == "K":
				KEYBOARD_DATA = ["UserId, Event,Key Code, Key Text, key Character,Modifiers, Key Location,Raw Code, Time Stamp,Active Window"] + KEYBOARD_DATA
			if self.args.CsvDataType == "A" or self.args.CsvDataType == "M":
				MOUSE_DATA = ["UserId, Event, Screen Location, Button, Modifiers, Click Count, Scroll Type, Scroll Amount, Wheel Rotation, Wheel Direction, Time Stamp, Active Window"] + MOUSE_DATA
			file = open(self.args.destination, "w")
			if self.args.CsvDataType == "A" or self.args.CsvDataType == "K":
				for lines in KEYBOARD_DATA:
					file.write(lines+"\n")
			if self.args.CsvDataType == "A" or self.args.CsvDataType == "M":
				for lines in MOUSE_DATA:
					file.write(lines+"\n")
			print("Finished writing data to "+self.args.destination+".")
		else:
			print("Failed to Open source File.")

	def argumentParser(self):
		parser = agp.ArgumentParser()
		parser.add_argument("-filepath", type=str,
		                    help="json file fetch to convert to")
		parser.add_argument("-extract", "--CsvDataType", type=str,
		                    help="Data Type to convert to CSV (M = Mouse, K = Keystroke, A = Application Uses, ALL = Everything")
		parser.add_argument("-sep", "--Seperator", type=str,
		                    help="Location to save converted csv file")
		parser.add_argument("-dest", "--destination", type=str,
		                    help="Location to save converted csv file")
		self.args = parser.parse_args()

tjson = tmcJsonParser()
