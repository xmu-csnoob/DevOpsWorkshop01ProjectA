import cv2
import socket
import numpy as np
import pickle
import struct

# Replace this with your host IP address
host = '0.0.0.0'
port = 12345

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)

conn,addr=s.accept()
print("Connected to client ...")

try:
	name = str('image')+'.jpg'
	data = b""
	payload_size = struct.calcsize(">L")
	print("payload_size: {}".format(payload_size))
	while len(data) < payload_size:
		print("Recv: {}".format(len(data)))
		data += conn.recv(4096)
	print("Done Recv: {}".format(len(data)))
	packed_msg_size = data[:payload_size]
	data = data[payload_size:]
	msg_size = struct.unpack(">L", packed_msg_size)[0]
	print("msg_size: {}".format(msg_size))
	while len(data) < msg_size:
		data += conn.recv(4096)
	frame_data = data[:msg_size]
	data = data[msg_size:]

	frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
	frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
	cv2.imwrite(name,frame)
	cv2.waitKey(1)
	
finally:
	conn.close()
	s.close()
	

