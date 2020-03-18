# VHbuster
A python program to find virtual hosts.

# Usage:
```
usage: vhbuster.py [-h] [-t 5] [-o /path/to/outfile] [--timeout TIMEOUT]
                   [--http_only] [--https_only]
                   127.0.0.1,ipfile.txt domains

Find virtual hosts on a list or single ip address.

positional arguments:
  127.0.0.1,ipfile.txt  List of ip addresses or ip files, seperated by commas.
  domains               Location of file containing potential virtual hosts.

optional arguments:
  -h, --help            show this help message and exit
  -t 5                  Amount of threads to run at once.
  -o /path/to/outfile   Outfile
  --timeout TIMEOUT     Time in seconds to wait for a response.
  --http_only           Only send http requests.
  --https_only          Only send https requests.
```
