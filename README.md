A script that fetches ASN information and ip ranges from [Hurricane Electric](https://bgp.he.net.).

**Usage**
```
python heASNs.py /path/to/org/names/file.txt 
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

|
|__ASNs
|  |_google.txt
|  |_yahoo.txt
|  |_dell.txt
|__Ranges
|  |_google.txt
|  |_yahoo.txt
|  |_dell.txt