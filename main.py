from phue import Bridge
import os
from dotenv import load_dotenv
import requests
load_dotenv()

from lib.Phillipfy import Phillipfy

app = Phillipfy()

app.run()


