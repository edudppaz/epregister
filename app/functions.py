import requests
import json
import urllib3
from netaddr import *

## Disable SSL warnings ##
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


## Define functions to use ##


def check_ep_exists(ise_url, ep_mac, username, password):
    headers= {'Accept': 'application/json', 'Content-Type': 'application/json'}
    url = ise_url + "endpoint/?filter=mac.EQ."+ep_mac
    payload = {}
    response = requests.get(url, auth=(username, password), headers=headers, data=payload, verify=False)
    data = response.json()
    return data

def register_ep_ise(ise_url, ep_mac, ise_chosen_group_id, username, password):
    headers= {'Accept': 'application/json', 'Content-Type': 'application/json'}
    url = ise_url + "endpoint"
    payload = json.dumps({"ERSEndPoint" : {"name" : ep_mac,"description" : "ERS API-added endpoint","mac" : ep_mac,"staticGroupAssignment" : True, "groupId" : ise_chosen_group_id}})
    response = requests.post(url, auth=(username, password), headers=headers, data=payload, verify=False)
    data = response.headers
    result = (f"Endpoint with mac {ep_mac} has been registered\n\n\n")
    return data, result

def update_ep_ise(ise_url, mac, endpoint_id, ise_chosen_group_id, username, password):
    headers= {'Accept': 'application/json', 'Content-Type': 'application/json'}
    url = ise_url + "endpoint/"+endpoint_id
    payload = json.dumps({"ERSEndPoint" : {"staticGroupAssignment" : True, "groupId" : ise_chosen_group_id}})
    response = requests.put(url, auth=(username, password), headers=headers, data=payload, verify=False)
    data = response.headers
    result = (f"Endpoint with mac {mac} has been added to the chosen group\n\n\n")
    return data, result

def get_mac_address():
    class mac_custom(mac_unix): pass
    mac_custom.word_fmt = '%.2X'
    valid_mac = False
    while valid_mac == False:
        try:
            raw_eui = EUI(input("Please enter the endpoint mac-address\n"), dialect=mac_custom)
            valid_mac = True
        except:
            print(f"Invalid MAC Address, please enter a valid mac")
    mac = str(raw_eui)
    return mac

def get_ipam_token(IPAM_URL, IPAM_APP, username, password):
    print("Logging into IPAM and fetching token...\n")
    response = requests.post(IPAM_URL + "/api/" + IPAM_APP + "/user/", auth=(username,password),verify=False )
    if response.status_code is not 200:
      print("Error retreiving token from PHPIPAM, response was:")
      print(response.json())
      exit(1);

    # Retreive Token if succesful
    return response.json()['data']['token']
