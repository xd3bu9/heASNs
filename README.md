A script that fetches ASN information and ip ranges from [Hurricane Electric](https://bgp.he.net.).

**Usage**
```
python heASNs.py -orgs /path/to/org/names/file.txt -o /path/to/output/dir
```
**Input**

A list of org names.

`cat sample.txt`
```
google
yahoo
dell
```

**Output**

```
.
├──ASNs
   ├──dell.txt
   ├──google.txt
   └──yahoo.txt
├──ipRanges
   ├──dell.txt
   ├──google.com
   └──yahoo.txt
```