from phue import Bridge
import os
from dotenv import load_dotenv
import requests
load_dotenv()

from Phillipfy.Phillipfy import Phillipfy

app = Phillipfy(room='Bedroom')

if __name__ == '__main__':
    app.run()


