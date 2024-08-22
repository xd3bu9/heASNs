#!/usr/bin/env python

from argparse import ArgumentParser
from bs4 import BeautifulSoup
import os
import re
import requests
import json
import sys

requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning
)

resultlist = []
ranges_pattern = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}/\d{1,2}\b")
asn_pattern = re.compile(r"\bAS\d{5}\b")


def get_args():
    parser = ArgumentParser()
    parser.add_argument("-i", metavar="INPUT", help="organization name or input file.")
    return parser.parse_args()


def req(org):
    parameters = {"search[search]": org.strip(), "commit": "Search"}
    x = requests.get(
        "https://bgp.he.net/search",
        params=parameters,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
        },
    )
    html = BeautifulSoup(x.text, "html.parser")
    table = html.find("table", attrs={"class": "w100p"})
    atags = table.find_all("a")
    return atags


def parse(links, org):
    ipRanges = list(set(re.findall(ranges_pattern, str(links))))
    asns = list(set(re.findall(asn_pattern, str(links))))
    item = {"name": org, "data": {"asns": asns, "ranges": ipRanges}}
    resultlist.append(item)


def file_exists(file):
    return os.path.isfile(file)


def bgp(userInput):
    if file_exists(file=userInput):
        with open(userInput.strip(), "r") as file:
            for line in file:
                parse(req(line), org=line)
    else:
        parse(req(userInput), org=userInput)


def main():
    args = get_args()
    if args.i == None:
        print("-i is a required argument.")
        exit(1)
    bgp(userInput=args.i)
    output = {"results": resultlist}
    print(json.dumps(output))


if __name__ == "__main__":
    main()
