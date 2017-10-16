import argparse as agp
import pandas as pd
import os

class tmcJsonParser:
	args = ""

	def getValuesFromJSONRows(self, data):
		string_vals = ','.join(data.values())
		return string_vals[1:]

	def __init__(self):
		json_raw_data = ""
		parsed_json = None
		self.argumentParser()
		if os.path.isfile(self.args.filepath):
			with open(self.args.filepath) as f:
				for lines in f:
					json_raw_data += lines
			parsed_json = pd.read_json(json_raw_data)
			MOUSE_DATA = []
			KEYBOARD_DATA = []
			for rows in parsed_json.rows:
				eventData = rows['doc']['eventData']
				splited_data = eventData.split(',')
				tmp_k = {}
				tmp_m = {}
				events = None
				for data in splited_data:
					event = splited_data[0]
					if(event == "NATIVE_KEY_TYPED" or event == "NATIVE_KEY_PRESSED" or event == "NATIVE_KEY_RELEASED"):
						events = 'k'
						tmp_k["modifiers"] = ""
						tmp_k["event"] = event
						if(data.find("=", 0) !=  -1):
							key_Val = data.split("=")
							tmp_k[key_Val[0]] = key_Val[1].replace("'", "")

					if (event == "NATIVE_MOUSE_MOVED" or event == "NATIVE_MOUSE_DRAGGED" or event == "NATIVE_MOUSE_CLICKED" or event=="NATIVE_MOUSE_WHEEL" or event=="NATIVE_MOUSE_RELEASED" or event=="NATIVE_MOUSE_PRESSED"):
						events = 'm'
						tmp_m["modifiers"] = ""
						tmp_m["event"] = splited_data[0]
						tmp_m["position"] = str(splited_data[1])+ ", " + str(splited_data [2])
						tmp_m["scrollAmount"] = ""
						tmp_m["scrollType"] = ""
						tmp_m["wheelRotation"] = ""
						tmp_m["wheelDirection"] = ""
						if(data.find("=", 0)!= -1):
							key_Val = data.split("=")
							tmp_m[key_Val[0]] = key_Val[1].replace("'", "")
				if events == 'k':
					tmp_k["timeStamp"] = str(rows['doc']['timeStamp']) # pussing in str as we need to join later
					tmp_k["activeWindow"] = rows['doc']['activeWindow']
				if events == 'm':
					tmp_m["timeStamp"] = str(rows['doc']['timeStamp']) # pussing in str as we need to join later
					tmp_m["activeWindow"] = rows['doc']['activeWindow']
					events = None
				if(len(tmp_k)>0):
					KEYBOARD_DATA.append(self.getValuesFromJSONRows(tmp_k))
				if(len(tmp_m)>0):
					MOUSE_DATA.append(self.getValuesFromJSONRows(tmp_m))
				tmp_k = {}
				tmp_m = {}
			file = open(self.args.destination, "w")
			for lines in KEYBOARD_DATA:
				file.write(lines+"\n")
#			for lines in MOUSE_DATA:
#				file.write(lines+"\n")
		else:
			print("Failed to Open source File.")

	def argumentParser(self):
		parser = agp.ArgumentParser()
		parser.add_argument("filepath", type=str,
		                    help="json file fetch to convert to")
		parser.add_argument("-extract", "--Csv Data Type", type=str,
		                    help="Data Type to convert to CSV (M = Mouse, K = Keystroke, A = Application Uses, ALL = Everything")
		parser.add_argument("-sep", "--Seperator", type=str,
		                    help="Location to save converted csv file")
		parser.add_argument("-dest", "--destination", type=str,
		                    help="Location to save converted csv file")
		self.args = parser.parse_args()

tjson = tmcJsonParser()