import sys, requests, json
from os.path import isfile

LINK_LABEL = 'link'
ERROR_LABEL = 'error'
URL = 'https://api.anonfiles.com/upload'

if (len(sys.argv) < 2):
	print('please specify a file to upload')
else:
	filename = sys.argv[1]
	if (isfile(filename)):
		r = requests.post(URL, files={'file': open(filename, 'rb')})
		response = json.loads(r.text)
		output = f"{LINK_LABEL}: {response['data']['file']['url']['short']}" if response['status'] else f"{ERROR_LABEL}: {response['error']['message']}"
		print(output)
	else:
		print(f'{filename} doesn\'t exist')
