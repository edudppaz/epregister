#!/usr/bin/env python3

#from pypsrp.client import Client
from integration_info import *
from functions import *
from flask import Flask, render_template, request, session
from flask_bootstrap import Bootstrap
from os import environ
import config
import getpass
## Main script body ##


app = Flask(__name__)
app.config.from_object('config.Config')

Bootstrap(app)
@app.route("/", methods=["GET", "POST"])
def main():
    print(f"Username: {username}")
    return render_template("main.html", ise_groups=ise_groups, ipam_subnet=ipam_subnet)


@app.route("/check-endpoint", methods=["POST"])
def check():
    endpoint_mac = request.form.get("endpoint_mac")
    ise_chosen_group_id = request.form.get("ise_group_id")
    ep_on_ise = check_ep_exists(ise_url, endpoint_mac, username, password)
    ## If endpoint does not exist, we register a new endpoint on the correct group #
    if ep_on_ise['SearchResult']['total'] == 0:
        register_ep, result = register_ep_ise (ise_url, endpoint_mac, ise_chosen_group_id, username, password)
    elif ep_on_ise['SearchResult']['total'] == 1:
        endpoint_id = ep_on_ise['SearchResult']['resources'][0]['id']
        updated_response, result = update_ep_ise (ise_url, endpoint_mac, endpoint_id, ise_chosen_group_id, username, password)
    return render_template("check-endpoint.html", ep_data=json.dumps(ep_on_ise, indent=10), result=result)

if __name__ == '__main__':
    username = environ.get('FLASK_APP_USERNAME')
    password = environ.get('FLASK_APP_PASSWORD')
    app.run()