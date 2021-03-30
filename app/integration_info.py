## IPAM VARS ##
IPAM_URL = "https://ipam.atea.svg"
IPAM_APP = "TESTAPI"
ipam_subnet = {
    "api_test1": {
        "Atea SVG": {"subnet": "1.1.1.0/24", "id": "89"},
        "Atea BRG": {"subnet": "2.2.2.0/24", "id": "90"},
    },
    "api_test2": {"Jorgen": {"subnet": "3.3.3.0/24", "id": "91"}},
}
IPAM_API_TAG = "5"

## ISE VARS ##
ise_ip = "10.11.10.67"
ise_url = "https://" + ise_ip + ":9060/ers/config/"