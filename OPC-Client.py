from opcua import Client
from opcua import ua
import time
from time import sleep

import csv

url = "opc.tcp://192.168.0.5:4840"
client.set_user("Raspberry Pi")
client.set_passowrd("start1234")
client = Client(url)

client.connect()
print(f"Client connected to server {url}")

counter = 0

while True:

	#Take start time for performance evaluation
	time_start = time.time()

	#Check server for Start signal
	ident_available_node = client.get_node('ns=3;s="DB4_Global_Ident"."Ident_received"')
	ident_available = ident_available_node.get_value()
	print(f"[{url}]- Ident available: {ident_available}")

	#Take time for stage 1 performance
	time_stage_1 = time.time()

	#start process if start signal available
	if ident_available:

		#Change status of ES\_connected to inform S7-1500 about connection
		response_node = client.get_node('ns=3;s="DB2_OPC_UA"."ES_connected"')
		response_node.set_attribute(ua.AttributeIds.Value, ua.DataValue(True))
		print(f"[{url}]- Object ready for documentation")

		#Take time for stage 2 performance
		time_stage_2 = time.time()

		#Get Data from OPC-Server
		Data_node = client.get_node('ns=3;s="DB4_Global_Ident"."Ident"."Data"')
		Data = Data_node.get_value()
		print(f"[{url}]- Ident received: {Data}")

		#Take time for stage 3 performance
		time_stage_3 = time.time()

		#Sleep for 7 seconds => simulates documentation process
		sleep(7)

		#Sent Path of pictures to Server (Path is only simulated)
		path_node = client.get_node('ns=3;s="DB2_OPC_UA"."Directory"')
		counter = counter + 1
		directory = f"/Documents/OPC_UA/BA_{counter}"
		path_node.set_attribute(ua.AttributeIds.Value, ua.DataValue(directory))
		print(f"[{url}]- Directory set: {directory}")

		#Take time for stage 4 performance
		time_stage_4 = time.time()

		#Reset status of ES\_connected to inform about finished process
		response_node.set_attribute(ua.AttributeIds.Value, ua.DataValue(False))

		#Reset status of ident\_received to inform S7-1500 that a new ...
		#...object can be documented
		ident_available_node.set_attribute(ua.AttributeIds.Value, ua.DataValue(False))

		#Take time for stage 5 performance
		time_stage_5 = time.time()

		#Calculate performance
		#Only for test purposes
		time_after_stage_1 = round((time_stage_1 - time_start) * 1000, 3)
		time_after_stage_2 = round((time_stage_2 - time_start) * 1000, 3)
		time_after_stage_3 = round((time_stage_3 - time_start) * 1000, 3)
		time_after_stage_4 = round((time_stage_4 - time_start) * 1000, 3)
		time_total = round((time_stage_5 - time_start) * 1000, 3)

		print(f"Stage 1: {time_after_stage_1}")
		print(f"Stage 2: {time_after_stage_2}")
		print(f"Stage 3: {time_after_stage_3}")
		print(f"Stage 4: {time_after_stage_4}")
		print(f"Time complete: {time_total}")

		with open('evaluations_opc.csv', 'a', newline='') as file:
			writer = csv.writer(file)
			writer.writerow([time_after_stage_1, time_after_stage_2, time_after_stage_3, time_after_stage_4, time_total])
			file.close()

	#Check again after 2 seconds for new status
	sleep(2)
