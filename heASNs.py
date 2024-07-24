#!/usr/bin/env python

from argparse import ArgumentParser
from bs4 import BeautifulSoup
import os
import re
import requests
import sys
import mmh3
import requests
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
    parser.add_argument("-o", help="output directory.")
    return parser.parse_args()


# save output
def save_output(directory, filename, output):
    path = os.path.join(directory, "{}.txt".format(filename))
    with open(path, "w") as out_file:
        for value in output:
            out_file.write(value + "\n")


def req(domain):
    parameters = {"search[search]": domain.strip(), "commit": "Search"}
    x = requests.get("https://bgp.he.net/search", params=parameters)
    html = BeautifulSoup(x.text, "html.parser")
    table = html.find("table", attrs={"class": "w100p"})
    atags = table.find_all("a")
    return atags


def parse(links, line, dir):
    ipRanges = list(set(re.findall(ranges_pattern, str(links))))
    asns = list(set(re.findall(asn_pattern, str(links))))
    save_output(dir, "{}".format(line.replace("\n", "")), asns)
    save_output(dir, "{}".format(line.replace("\n", "")), ipRanges)


def file_exists(file):
    return os.path.isfile(file)


# passive
def bgp(userInput, outdir):
    os.makedirs(outdir)
    if file_exists(file=userInput):
        with open(userInput.strip(), "r") as file:
            for line in file:
                parse(req(line), line=line, dir=outdir)
    else:
        parse(req(userInput), userInput, outdir)


def main():
    args = get_args()
    userinput = args.i
    outputdir = args.o
    out = "{}/out/".format(outputdir)
    bgp(userInput=userinput, outdir=out)


if __name__ == "__main__":
    main()
