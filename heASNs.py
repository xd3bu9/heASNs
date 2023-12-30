#!/usr/bin/env python

from argparse import ArgumentParser
from bs4 import BeautifulSoup
import os
import re
import requests
import sys

def get_args():
	parser = ArgumentParser()
	parser.add_argument('orgs', help='input file with a list of organization names.')
	parser.add_argument('o', help='output directory.')
	return parser.parse_args()

def save_output(directory, filename, output):
    path = os.path.join(directory, '{}.txt'.format(filename))
    with open(path, 'w') as out_file:
        for value in output:
            out_file.write(value + '\n')

def server(host):
    curlServer = "/usr/bin/curl --location --head "
    os.execl(curlServer+"host")

def bgp(inputfile, outputdir):
    ranges_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}/\d{1,2}\b')
    asn_pattern = re.compile(r'\bAS\d{5}\b')
    asn_dir = "{}/ASNs/".format(outputdir)
    ranges_dir = "{}/ipRanges/".format(outputdir)
    os.makedirs(asn_dir)
    os.makedirs(ranges_dir)
    with open(inputfile.strip(), "r") as file:
        for line in file:
            parameters = {"search[search]": line.strip(), "commit": "Search"}
            x = requests.get("https://bgp.he.net/search", params=parameters)
            html = BeautifulSoup(x.text, 'html.parser')
            table = html.find('table', attrs={'class': 'w100p'})
            atags = table.find_all('a')
            ipRanges = list(set(re.findall(ranges_pattern, str(atags))))
            asns = list(set(re.findall(asn_pattern, str(atags))))
            save_output(asn_dir, '{}'.format(line.replace('\n', '')), asns)
            save_output(ranges_dir, '{}'.format(line.replace('\n', '')), ipRanges)

if len(sys.argv) != 3:
    print("Usage: python heASNs.py -orgs /path/to/org/names/file.txt -o /path/to/output/dir/")
    sys.exit(1)

def main():
    args = get_args()
    orgsFilePath = args.orgs
    outputDir = args.o
    bgp(inputfile=orgsFilePath, outputdir=outputDir)

if __name__ == '__main__':
	main()