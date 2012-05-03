#!/usr/bin/env python2.7 

from time import time
import os
import optparse
import subprocess

DEFAULT_URL = "http://mirror.cse.iitk.ac.in/archlinux/pool/packages/\
wxgtk-2.8.12.1-3-i686.pkg.tar.xz"

def cb(option, opt_str, value, parser):
    args=[]
    for arg in parser.rargs:
        if arg[0] != "-":
            args.append(arg)
	else:
            del parser.rargs[:len(args)]
	    break
    if getattr(parser.values, option.dest):
        args.extend(getattr(parser.values, option.dest))
    setattr(parser.values, option.dest, args)

def test_dwnld(p, u, t, f):
    url = ""
    os.environ.update({'http_proxy':p})
    try:
        with open(os.devnull, 'wb') as devnull:
            start = time()
            subprocess.check_call(['wget', '-T', str(t), "-t", str(1), 
                                   "-O", f, u], stdout=devnull, 
                                  stderr=subprocess.STDOUT)
        end = time()
    except subprocess.CalledProcessError:
        return -1
    if(os.path.isfile(f)):
        os.remove(f)
    return end - start

def main():
    usage = "./find-fatest-proxy.py [options] -p proxy1 proxy2 ..."
    parser = optparse.OptionParser(usage)
    parser.add_option("-u", "--url", dest="url",
                     help="use URL for comparisons",
                     type="string", default=DEFAULT_URL)
    parser.add_option("-t", "--timeout", dest="timeout",
                     help="timeout for individual attempt",
                     type="int", default=5)
    parser.add_option("-f", "--filename", dest="filename",
                     help='''Name and optionally the full path to which to\
 download the test file. `tempdwldfile` by default.''',
                     type="string", default="tempdwldfile")
    parser.add_option("-p", "--proxies",
        action="callback", callback=cb, dest="proxies", help="proxies to be \
compared")
    parser.add_option("-l", "--list", action="store_true", dest="listproxies",
		      help="List all proxies with times. Only the fastest shown\
 by default")
    parser.add_option("-r", "--read", dest="proxyfile", default="~/.proxyfile",
                      help="Read proxies from a file. Default file is ~/.proxyfile")
    (options, args) = parser.parse_args()
    if options.proxyfile[0]=='~':
        print "here"
        options.proxyfile = os.environ.get('HOME') + options.proxyfile.lstrip('~')
        print options.proxyfile
    if not options.proxies and not os.path.isfile(options.proxyfile):
        parser.error("No proxies provided")
    tlist = []
    if options.proxies:
        for proxy in options.proxies:
            td = test_dwnld(proxy, options.url, options.timeout, options.filename)
            tlist.append((proxy, td))
    if os.path.isfile(options.proxyfile):
        pf = open(options.proxyfile)
        proxies = pf.readlines()
        for proxy in proxies:
            proxy=proxy.strip()
            td = test_dwnld(proxy, options.url, options.timeout, options.filename)
            tlist.append((proxy, td))
        pf.close()
    tlist = sorted(tlist, key=lambda x:x[1])
    if not options.listproxies:
	    print tlist[0][0]
    else:
	    for i in tlist:
		    print i[0] + " " + str(i[1]) + "s"

if __name__ == "__main__":
    main()
