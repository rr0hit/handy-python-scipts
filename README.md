handy-python-scipts
===================

A collection of a few few handy python scripts.

find-fastest-proxy
------------------

A script that finds the fastest proxy from a given list by comparing the times
taken to download contents from a URL.

Usage: ./find-fatest-proxy.py [options] -p proxy1 proxy2 ...

Options:
  -h, --help            show this help message and exit
  -u URL, --url=URL     use URL for comparisons
  -t TIMEOUT, --timeout=TIMEOUT
                        timeout for individual attempt
  -f FILENAME, --filename=FILENAME
                        Name and optionally the full path to which to download
                        the test file. `tempdwldfile` by default.
  -p, --proxies         proxies to be compared
  -l, --list            List all proxies with times. Only the fastest shown by
                        default

