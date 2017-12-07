from sys import argv
from urllib import urlencode
from urllib2 import Request, urlopen, HTTPError, URLError
from zlib import compress

if len(argv) > 1:
	code = argv[1]
	method = argv[2]
	file_out = argv[3]
	url = "http://10.5.4.61:875/api/in_data.php"
	f = open(file_out, 'r')
	data = f.read()
	f.close()
	compress_data = compress(data)
	arrload = { 'code': code,
                'method': method,
                'data': compress_data,
				'zip' : 1 }
	send_data = urlencode(arrload)
	r = Request(url, send_data)
	
	try:
		resp = urlopen(r)
	except HTTPError as e:
		print str(e.code) + '~HTTPError~' + str(e.reason)
		raise SystemExit(96)
	except URLError as e:
		print '~URLError~' + str(e.reason)
		raise SystemExit(97)
	else:
		if resp.getcode() == 200:
			print "Sending completed"
			raise SystemExit(0)
		else:
			print str(resp.getcode()) + '~' + resp.read()
			raise SystemExit(98)
else:
	print "Wrong parametr count"
	raise SystemExit(99)
