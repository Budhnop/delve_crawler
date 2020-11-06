"""
TODO
"""
import os
import requests
import urllib3
import certifi
import json
import math
import colorama
from colorama import Fore
import urllib.parse

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", "*")
API_BASE_URL = os.getenv("API_BASE_URL", "*")
headers = dict(authorization=f"Bearer {ACCESS_TOKEN}", accept="application/json")

colorama.init(autoreset=True)

#MAXIMUM NUMBERS OF ITEM RETURNED IN A SINGLE PASS
REQUEST_LIMIT = 500


def conn_status():
    # https://urllib3.readthedocs.io/en/latest/user-guide.html#ssl
    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where()
    )

    print(Fore.GREEN + "Check if certs is still valid...")
    try:
        http.request('GET', API_BASE_URL)
    except urllib3.exceptions as e:
        print("BAD CERTS, quitting...")
        exit(666)


def get_data(url, params="", stream=None):
    return requests.get(f"{API_BASE_URL}/" + url,
                        params=params,
                        headers=headers,
                        verify=True)


def write_to_json(filename, data):
    print(Fore.GREEN + "\n--------------------------------------")
    print(Fore.GREEN + f'Writing to file output/{filename}.json\n')
    with open(f'output\{filename}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def get_server(team_id, team_name):
    print(Fore.CYAN + "[{}] : ".format(
        team_name
    ), end=" ")

    response = get_data("servers?limit=1&offset=0&q=%7B%22team%22%3A%20%7B%22id%22%3A%20%22{}%22%7D%7D".format(team_id))
    total_servers = response.json()["totalItems"]
    print("Got {} servers : ".format(total_servers), end=" ")

    current_offset = 0
    server_list = {"servers": []}

    for x in range(math.ceil(total_servers / REQUEST_LIMIT)):
        print(Fore.YELLOW + ".", end="")
        response = get_data("servers?limit={}&offset={}&q=%7B%22team%22%3A%20%7B%22id%22%3A%20%22{}%22%7D%7D".format(REQUEST_LIMIT, (x * REQUEST_LIMIT), team_id))
        servers = response.json()["items"]
        tmp_server = server_list["servers"]
        for server in servers:
            tmp_server.append(server)

        server_list.update({"servers": tmp_server})

    print("")
    return server_list["servers"]


def get_server_per_teams(teams):
    print(Fore.CYAN + "-------------------------------------------------")
    print(Fore.CYAN + "Fetching servers per teams...")
    print(Fore.CYAN + "-------------------------------------------------")

    servers = {"server": []}
    for team in teams:
        new_server = get_server(team["id"], team["name"])
        tmp_server = servers["server"]
        for server in new_server:
            tmp_server.append(server)

        servers.update({"server": tmp_server})

    write_to_json("servers", servers)


def get_server_stats():
    print(Fore.CYAN + "Fetching server stats...".format())
    response = get_data("servers/distribution")
    write_to_json("server_stats", response.json())


def get_website(team_id, team_name):
    print(Fore.CYAN + "[{}] : ".format(
        team_name
    ), end=" ")

    response = get_data("websites?limit=1&offset=0&q=%7B%22team%22%3A%20%7B%22id%22%3A%20%22{}%22%7D%7D".format(
        team_id))
    total_websites = response.json()["totalItems"]
    print("Got {} websites : ".format(total_websites), end=" ")

    current_offset = 0
    website_list = {"websites": []}

    for x in range(math.ceil(total_websites / REQUEST_LIMIT)):
        print(Fore.YELLOW + ".", end="")
        response = get_data("websites?limit={}&offset={}&q=%7B%22team%22%3A%20%7B%22id%22%3A%20%22{}%22%7D%7D".format(
            REQUEST_LIMIT, (x * REQUEST_LIMIT), team_id))
        websites = response.json()["items"]
        tmp_website = website_list["websites"]
        for website in websites:
            tmp_website.append(website)

        website_list.update({"websites": tmp_website})

    print("")
    return website_list["websites"]


def get_website_per_teams(teams):
    print(Fore.CYAN + "-------------------------------------------------")
    print(Fore.CYAN + "Fetching websites per teams...")
    print(Fore.CYAN + "-------------------------------------------------")

    websites = {"website": []}
    for team in teams:
        new_website = get_website(team["id"], team["name"])
        tmp_server = websites["website"]
        for website in new_website:
            tmp_server.append(website)

        websites.update({"website": tmp_server})

    write_to_json("websites", websites)


def get_website_stats():
    print(Fore.CYAN + "Fetching website stats...".format())
    response = get_data("websites/distribution")
    write_to_json("website_stats", response.json())


def get_teams():
    print(Fore.CYAN + "Fetching teams...", end=" ")
    response = get_data("teams?limit=1000&offset=0")
    print("Got {} teams".format(
        response.json()["currentItemCount"])
    )
    write_to_json("teams", response.json()["items"])
    return response.json()["items"]


def get_users():
    print(Fore.CYAN + "Fetching user list...", end=" ")
    response = get_data("users?limit=1000&offset=0")
    print("Got {} users".format(
        response.json()["currentItemCount"])
    )
    write_to_json("users", response.json()["items"])


def get_remediation_plans():
    print(Fore.CYAN + "Fetching remediation plans...", end=" ")
    response = get_data("remediation-plans?limit=1000&offset=0")
    print("Got {} plans".format(response.json()["currentItemCount"]))
    write_to_json("rem_plans", response.json()["items"])


def get_vuln_byplan():
    print("Fetching vulns by remediation plans...")


def get_range(team_id, team_name):
    print(Fore.CYAN + "[{}] : ".format(
        team_name
    ), end=" ")

    response = get_data("ranges?limit=1&offset=0&q=%7B%22team%22%3A%20%7B%22id%22%3A%20%22{}%22%7D%7D".format(team_id))
    total_ranges = response.json()["totalItems"]
    print("Got {} ranges".format(total_ranges), end=" ")

    current_offset = 0
    range_list = {"ranges": []}

    for x in range(math.ceil(total_ranges / REQUEST_LIMIT)):
        print(Fore.YELLOW + ".", end="")
        response = get_data(
            "ranges?limit={}&offset={}&q=%7B%22team%22%3A%20%7B%22id%22%3A%20%22{}%22%7D%7D".format(REQUEST_LIMIT, (
                        x * REQUEST_LIMIT), team_id))
        ranges = response.json()["items"]
        tmp_server = range_list["ranges"]
        for server in ranges:
            tmp_server.append(server)

        range_list.update({"ranges": tmp_server})

    print("")
    return range_list["ranges"]


def get_range_per_team(teams):
    print(Fore.CYAN + "-------------------------------------------------")
    print(Fore.CYAN + "Fetching ranges per teams...")
    print(Fore.CYAN + "-------------------------------------------------")

    ranges = {"range": []}
    for team in teams:
        new_server = get_range(team["id"], team["name"])
        tmp_server = ranges["range"]
        for server in new_server:
            tmp_server.append(server)

        ranges.update({"range": tmp_server})

    write_to_json("ranges", ranges)


def get_vuln_group():
    print(Fore.CYAN + "----------------------------------")
    print(Fore.CYAN + "Fetching vulnerabilities groups...")
    print(Fore.CYAN + "----------------------------------")

    vuln_type = ["critical", "medium"]  # vuln type we wanna get back from the API

    vuln_list = {"vuln": []}
    vuld_id = []

    for x in range(len(vuln_type)):
        str_url = 'vulnerability-groups?limit=1&offset=0&q=*'
        str_param = urllib.parse.quote('{"severity": {"level": "*"}}'.replace("*", vuln_type[x]))
        str_url = str_url.replace("*", str_param)

        response = get_data(str_url)

        total_vulns = response.json()["totalItems"]
        print(Fore.CYAN + "Got {} {} vulnerabilities".format(total_vulns, vuln_type[x]), end="")

        current_offset = 0

        for y in range(math.ceil(total_vulns / REQUEST_LIMIT)):
            print(Fore.YELLOW + ".", end="")
            str_url = 'vulnerability-groups?limit={}&offset={}&q=*'.format(
                REQUEST_LIMIT, (y * REQUEST_LIMIT))
            str_param = urllib.parse.quote('{"severity": {"level": "*"}}'.replace("*", vuln_type[x]))
            str_url = str_url.replace("*", str_param)

            response = get_data(str_url)

            vulns = response.json()["items"]
            tmp_vuln = vuln_list["vuln"]
            for vuln in vulns:
                tmp_vuln.append(vuln)
                vuld_id.append(vuln["id"])  # Build up of ID to return

            vuln_list.update({"vuln": tmp_vuln})
        print("")

    write_to_json("all_vulns_group", vuln_list)
    return vuld_id


def get_vulns(vuln_group_id):
    # Need to use SESSION for no connection spam
    # Or use threading??

    print(Fore.CYAN + "----------------------------------")
    print(Fore.CYAN + "Fetching {} vulnerabilities...".format(len(vuln_group_id)))
    print(Fore.CYAN + "----------------------------------")

    vuln_list = {"vuln": []}
    current_vuln = 0
    for vuln in vuln_group_id:
        current_vuln += 1
        #str = current_vuln / len(vuln_group_id) * 100

        print("{}% Completed\r".format(current_vuln / len(vuln_group_id) * 100), end="")

        str_url = 'vulnerability-groups/{}'.format(vuln)

        response = get_data(str_url)
        tmp_vuln = vuln_list["vuln"]
        tmp_vuln.append(response.json())
        vuln_list.update({"vuln": tmp_vuln})

    print("")
    write_to_json("all_vulns", vuln_list)


def merge_servers_and_websites():
    print(Fore.CYAN + "----------------------------------")
    print(Fore.CYAN + "Merging servers and websites")
    print(Fore.CYAN + "----------------------------------")
    fServer = open('output/servers.json', )
    fWebsite = open('output/websites.json', )
    jServer = json.load(fServer)["server"]
    jWebsite = json.load(fWebsite)["website"]

    #create massive json file with all matching fields from servers and websites to create a single asset file
    all_assets = []
    keys = {"creationDate":"", "id":"", "isActive":"", "isNew":"", "kind":"", "lastFailedScanId":"", "lastScanId":"", "teamId":""}

    for server in jServer:
        asset = keys
        asset["creationDate"] = server["creationDate"]
        asset["id"] = server["id"]
        asset["isActive"] = server["isActive"]
        asset["kind"] = server["kind"]
        asset["teamId"] = server["teamId"]
        asset["isNew"] = server["isNew"] if "isNew" in server else False
        asset["lastFailedScanId"] = server["lastFailedScanId"] if "lastFailedScanId" in server else None
        asset["lastScanId"] = server["lastScanId"] if "lastScanId" in server else None

        all_assets.append(asset)

    for website in jWebsite:
        asset = keys
        asset["creationDate"] = website["creationDate"]
        asset["id"] = website["id"]
        asset["isActive"] = website["isActive"]
        asset["kind"] = website["kind"]
        asset["teamId"] = website["teamId"]
        asset["isNew"] = website["isNew"] if "isNew" in website else False
        asset["lastFailedScanId"] = website["lastFailedScanId"] if "lastFailedScanId" in website else None
        asset["lastScanId"] = website["lastScanId"] if "lastScanId" in website else None

        all_assets.append(asset)

    write_to_json("assets", all_assets)


def main():
    conn_status()
    get_users()
    teams = get_teams()
    get_vuln_group()
    get_server_per_teams(teams)
    get_website_per_teams(teams)
    merge_servers_and_websites()
    get_range_per_team(teams)
    get_website_stats()
    get_server_stats()
    get_remediation_plans()


if __name__ == '__main__':
    main()

