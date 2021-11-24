import sys, requests, json
from os.path import isfile
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from tqdm import tqdm
from termcolor import colored

PROGRESSBAR_LABEL = 'uploading'
LINK_LABEL = 'link'
ERROR_LABEL = 'error'
URL = 'https://api.anonfiles.com/upload'


def monitor_callback(monitor, tqdm_handler):
	tqdm_handler.total = monitor.len
	tqdm_handler.update(monitor.bytes_read - tqdm_handler.n)


def get_fields(filename):
	return {'file': (filename, open(filename, 'rb'), 'application/octet-stream')}


if (len(sys.argv) < 2):
	print(colored('please specify a file to upload', 'yellow'))
else:
	filename = sys.argv[1]
	if (isfile(filename)):
		fields = get_fields(filename)
		encoder = MultipartEncoder(fields)
		tqdm_handler = tqdm(desc=PROGRESSBAR_LABEL, total=encoder.len, disable=not PROGRESSBAR_LABEL, dynamic_ncols=True, unit='B', unit_scale=True, unit_divisor=1024)
		multipart_monitor = MultipartEncoderMonitor.from_fields(fields, callback=lambda monitor: monitor_callback(monitor, tqdm_handler))
		headers = {'Content-Type': multipart_monitor.content_type}

		r = requests.post(URL, data=multipart_monitor, headers=headers)
		tqdm_handler.close()

		response = json.loads(r.text)
		output = f"{LINK_LABEL}: {colored(response['data']['file']['url']['short'], 'green', attrs=['bold'])}" if response['status'] else colored(f"{ERROR_LABEL}: {response['error']['message']}", 'red', attrs=['bold'])
		print(output)
	else:
		print(colored(f'{filename} doesn\'t exist', 'yellow'))