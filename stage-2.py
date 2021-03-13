import requests
import json
import acitoolkit.acitoolkit as aci
from acitoolkit import HealthScore
from pprint import pprint
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from utils.auth import IntersightAuth, get_authenticated_aci_session
from env import config
from datetime import datetime
import csv

requests.packages.urllib3.disable_warnings() # Disable warning message

# Check for ACI simulator access
#aci_session = get_authenticated_aci_session(config['ACI_USER'], config['ACI_PASSWORD'], config['ACI_BASE_URL'])
BASE_URL = config['ACI_BASE_URL']

#url = f"{BASE_URL}/api/class/fabricHealthTotal.json"
session = aci.Session(BASE_URL, config['ACI_USER'], config['ACI_PASSWORD'])

fault_count = {"total": 0, "critical": 0}

resp = session.login()
if not resp.ok:
    print('%% Could not login to APIC')
    sys.exit(1)

healthScore_obj = HealthScore()

hScores = healthScore_obj.get_all(session)    # To get all health scores from the APIC

totHealthScore = 0
totNbScores = 0
maxSeverity = 100
dateTimeObj = datetime.now()

for score in hScores:
    score_val = int(score.__str__())
    if score_val < maxSeverity:
        maxSeverity = score_val
    totNbScores+=1
    totHealthScore += score_val

totHealthScore = totHealthScore / totNbScores
print("\nAt: ", dateTimeObj)
print("| => Total Health Score: ", totHealthScore)
print("| => Max Severity: ", maxSeverity, "\n")

with open('health_report.csv', mode='a') as outfile:
    outfile_writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    outfile_writer.writerow([dateTimeObj, totHealthScore, maxSeverity])