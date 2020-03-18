# VHbuster
A python program to find virtual hosts.

# Usage:
```
usage: vhbuster.py [-h] [-iL /path/to/ip/file] [-i 127.0.0.1] [-t 5]
                   [-o /path/to/outfile] [--timeout TIMEOUT] [--http_only]
                   [--https_only]
                   domains

Find virtual hosts on a list or single ip address.

positional arguments:
  domains               Location of file containing potential virtual hosts.

optional arguments:
  -h, --help            show this help message and exit
  -iL /path/to/ip/file  Location of file containing ip addresses.
  -i 127.0.0.1          List of ip addresses, seperated by commas.
  -t 5                  Amount of threads to run at once.
  -o /path/to/outfile   Outfile
  --timeout TIMEOUT     Time in seconds to wait for a response.
  --http_only           Only send http requests.
  --https_only          Only send https requests.

```
