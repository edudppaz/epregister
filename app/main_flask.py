#!/usr/bin/env python3

# from pypsrp.client import Client
from integration_info import *
from functions import *
from flask import Flask, render_template, request, session
from flask_bootstrap import Bootstrap
from os import environ
import config
import getpass
import pprint

"""
The Following environment variables need to be set for the
proper integration with ISE and IPAM:
ISE ERS app:
FLASK_APP_ERS_USERNAME
FLASK_APP_ERS_PASSWORD

Example (macosx):
export FLASK_APP_ERS_USERNAME="username123"
export FLASK_APP_ERS_PASSWORD="password123"

"""
app = Flask(__name__)
app.config.from_object("config.Config")

Bootstrap(app)


@app.route("/", methods=["GET", "POST"])
def main():
    return render_template("main.html", ise_groups=ise_db)


@app.route("/register-endpoint", methods=["POST"])
def register():
    endpoint_mac = request.form.get("endpoint_mac")
    ise_chosen_group = request.form.get("ise_group_id")
    ise_chosen_group_id = ise_db[ise_chosen_group]
    session["endpoint_mac"] = endpoint_mac
    session["ise_chosen_group"] = ise_chosen_group
    ep_on_ise = check_ep_exists(ise_url, endpoint_mac, username, password)
    ## If endpoint does not exist, we register a new endpoint on the correct group #
    if ep_on_ise["SearchResult"]["total"] == 0:
        register_ep, result = register_ep_ise(
            ise_url, endpoint_mac, ise_chosen_group_id, username, password
        )
    elif ep_on_ise["SearchResult"]["total"] == 1:
        endpoint_id = ep_on_ise["SearchResult"]["resources"][0]["id"]
        updated_response, result = update_ep_ise(
            ise_url, endpoint_mac, endpoint_id, ise_chosen_group_id, username, password
        )
    ipam_data = ipam_subnet[ise_chosen_group]
    print(json.dumps(ipam_data, indent=5))
    return render_template(
        "register-endpoint.html",
        ep_data=json.dumps(ep_on_ise, indent=10),
        ipam_data=ipam_data,
        ise_chosen_group=ise_chosen_group,
        result=result,
    )


@app.route("/ipam-reservation", methods=["POST"])
def ipam():
    location_choice = request.form.get("location_choice")
    ise_chosen_group = session["ise_chosen_group"]
    print(f"The ise chosen group is {ise_chosen_group}")
    print(f"The location choice is {location_choice}")
    location_id = ipam_subnet[ise_chosen_group][location_choice]["id"]
    print(f"The location id is {location_id}")
    subnet = ipam_subnet[ise_chosen_group][location_choice]["subnet"]
    ipam_token = get_ipam_token(ipam_url, ipam_app, username, password)
    reserved_ipam_ip, subnet, result = ipam_reserve_ip(
        location_id,
        session["endpoint_mac"],
        subnet,
        ipam_url,
        ipam_app,
        ipam_api_tag,
        ipam_token,
    )
    # location_id =
    return render_template(
        "ipam-reservation.html",
        reserved_ipam_ip=reserved_ipam_ip,
        subnet=subnet,
        result=result,
    )


if __name__ == "__main__":
    username = environ.get("FLASK_APP_ERS_USERNAME")
    password = environ.get("FLASK_APP_ERS_PASSWORD")
    ise_db = get_api_groups(ise_url, username, password)
    pprint.pprint(ise_db)
    app.run()