from bs4 import BeautifulSoup
import os
import re
import requests
import sys

if len(sys.argv) != 2:
    print("Usage: python heASNs.py /path/to/org/names/file.txt")
    sys.exit(1)

filePath = sys.argv[1]
pwd = os.getcwd()
ranges_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}/\d{1,2}\b')
asn_pattern = re.compile(r'\bAS\d{5}\b')
asn_dir = "{}/ASNs/".format(pwd)
ranges_dir = "{}/ipRanges/".format(pwd)

os.makedirs(asn_dir)
os.makedirs(ranges_dir)

def save_output(directory, filename, output):
    path = os.path.join(directory, '{}.txt'.format(filename))
    with open(path, 'w') as out_file:
        for value in output:
            out_file.write(value + '\n')

with open(filePath.strip(), "r") as file:
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