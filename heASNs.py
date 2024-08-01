#!/usr/bin/env python

from argparse import ArgumentParser
from bs4 import BeautifulSoup
import os
import re
import requests
import sys
import mmh3
import codecs
from requests.exceptions import ProxyError, ReadTimeout, ConnectTimeout

requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning
)

ranges_pattern = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}/\d{1,2}\b")
asn_pattern = re.compile(r"\bAS\d{5}\b")


def get_args():
    parser = ArgumentParser()
    parser.add_argument("-i", help="organization name or input file.")
    return parser.parse_args()


def req(domain):
    parameters = {"search[search]": domain.strip(), "commit": "Search"}
    x = requests.get("https://bgp.he.net/search", params=parameters)
    html = BeautifulSoup(x.text, "html.parser")
    table = html.find("table", attrs={"class": "w100p"})
    atags = table.find_all("a")
    return atags


def print_output(lst, line):
    if len(lst) < 1:
        return
    print("----- " + line.strip() + " -----")
    for item in lst:
        print(item)


def parse(links, line):
    ipRanges = list(set(re.findall(ranges_pattern, str(links))))
    asns = list(set(re.findall(asn_pattern, str(links))))
    print_output(asns, line=line)
    print_output(ipRanges, line=line)


def file_exists(file):
    return os.path.isfile(file)


def bgp(userInput):
    if file_exists(file=userInput):
        with open(userInput.strip(), "r") as file:
            for line in file:
                parse(req(line), line=line)
    else:
        parse(req(userInput), userInput)


def main():
    args = get_args()
    bgp(userInput=args.i)


if __name__ == "__main__":
    main()
