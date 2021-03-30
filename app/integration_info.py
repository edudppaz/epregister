## IPAM VARS ##
ipam_url = "https://ipam.atea.svg"
ipam_app = "TESTAPI"
ipam_subnet = {
    "TEST_API_V1": {
        "Atea SVG": {"subnet": "1.1.1.0/24", "id": "89"},
        "Atea BRG": {"subnet": "2.2.2.0/24", "id": "90"},
    },
    "TEST_API_V2": {"Jorgen": {"subnet": "3.3.3.0/24", "id": "91"}},
}
ipam_api_tag = "5"

## ISE VARS ##
ise_ip = "10.11.10.67"
ise_url = "https://" + ise_ip + ":9060/ers/config/"