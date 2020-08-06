from phue import Bridge
import os
from dotenv import load_dotenv
import requests
load_dotenv()

HUE_IP = os.environ.get('HUE_IP')
IP_URL = os.environ.get('IP_URL')

res = requests.get(IP_URL)
ip_data = res.json()[0]
ID = ip_data['id']
INTERNALIP = ip_data['internalipaddress']

b = Bridge(INTERNALIP,ID)
b.connect()
bridge = b.get_api()