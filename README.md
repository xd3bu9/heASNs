A script that fetches ASN information and ip ranges from [Hurricane Electric](https://bgp.he.net.).

### Usage
Input should be either a single organization name, or a new line delimited file of organization names.

**Single target**
```
python heASNs.py -i <target>
```

**Multiple targets**
```
python heASNs.py -i </path/to/org/names/file.txt>
```


#### Note: Verify results from the script as no valdation is done to confirm ownership.
