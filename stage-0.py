import requests
import json
from pprint import pprint
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from utils.auth import IntersightAuth, get_authenticated_aci_session
from env import config

auth=IntersightAuth(secret_key_filename=config['INTERSIGHT_CERT'],
                      api_key_id=config['INTERSIGHT_API_KEY'])

BASE_URL='https://www.intersight.com/api/v1/'

url = f"{BASE_URL}ntp/Policies"

try:
    response = requests.get(url, auth=auth)
    response.raise_for_status()
    pprint(response.json()["Results"], indent = 4)
except Exception as e:
    print(e)
