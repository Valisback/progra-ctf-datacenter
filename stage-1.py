import requests
import json
from pprint import pprint
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from utils.auth import IntersightAuth, get_authenticated_aci_session
from env import config

auth=IntersightAuth(secret_key_filename=config['INTERSIGHT_CERT'],
                      api_key_id=config['INTERSIGHT_API_KEY'])

BASE_URL='https://www.intersight.com/api/v1/'

alarm_url = f"{BASE_URL}cond/Alarms"
summary_infra_url = f"{BASE_URL}compute/PhysicalSummaries"
hcl_url = f"{BASE_URL}cond/HclStatuses"
kubernetes_cluster_url = f"{BASE_URL}kubernetes/Clusters"
kubernetes_deployment_url = f"{BASE_URL}kubernetes/Deployments"


def get_alarms(url):
    try:
        response = requests.get(url, auth=auth)
        response.raise_for_status()
        i = 0
        print("\n=========== ALARMS ===========")
        for alarm in response.json()["Results"]:
            i+=1
            print("| => (", i, "): ", alarm["Description"])
        print("\n")

    except Exception as e:
        print(e)

def get_summary_infra(url):
    try:
        response = requests.get(url, auth=auth)
        response.raise_for_status()
        print("\n=========== SUMMARY INFRASTRUCTURE ===========")
        for resource in response.json()["Results"]:
            print("- Name: ", resource["Name"])
            print("| => Management Mode: ", resource["ManagementMode"])
            print("| => Management IP: ", resource["MgmtIpAddress"])
            print("| => Firmware: ", resource["Firmware"])
            print("| => CPUs: ", resource["NumCpus"])
            print("| => Cores: ", resource["NumCpuCores"])
            print("| => PowerState: ", resource["OperPowerState"])
            print("| => Model: ", resource["Model"])
            print("| => Serial: ", resource["Serial"])
            print("| => License Tier: ", resource["PlatformType"])
            print("\n")

    except Exception as e:
        print(e)

def get_HCL(url):
    try:
        response = requests.get(url, auth=auth)
        response.raise_for_status()
        print("\n=========== HCL ===========")
        for resource in response.json()["Results"]:
            print("- Model: ", resource["HclModel"])
            print("| => OS Vendor: ", resource["HclOsVendor"])
            print("| => OS Version: ", resource["HclOsVersion"])
            print("\n")

    except Exception as e:
        print(e)


def get_Kubernetes(url, request_type):
    try:
        response = requests.get(url, auth=auth)
        response.raise_for_status()
        nbDeployments = 0
        if request_type == "cluster":
            print("\n=========== Kubernetes Cluster ===========")
        elif request_type == "deployment":
            print("\n=========== Kubernetes Deployments ===========")
        for resource in response.json()["Results"]:
            print("| => ", resource["Name"])
            nbDeployments += 1
        if request_type == "deployment":
            print("\n-- Total Kubernetes Deployments: ", nbDeployments)
    except Exception as e:
        print(e)

get_alarms(alarm_url)
get_summary_infra(summary_infra_url)
get_HCL(hcl_url)
get_Kubernetes(kubernetes_cluster_url, "cluster")
get_Kubernetes(kubernetes_deployment_url, "deployment")