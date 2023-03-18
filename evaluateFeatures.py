#!/usr/bin/python3
"""
Created on Sun Mar 12 16:18:25 2023

@author: Eduardo Romero
"""

import cgi
import cgitb
import os
import urllib.request
import dns.resolver

cgitb.enable()
with open('/etc/resolv.kube', 'r') as f:
    kubedns = str(f.read()).strip()
res = dns.resolver.Resolver(configure=False)
res.nameservers = [ kubedns ]


form = cgi.FieldStorage()
item = str(form.getvalue("ms"))
port = str(form.getvalue("port"))
# The full DNS name is default.svc.cluster.local
item = item + ".default.svc.cluster.local"
r = res.resolve(item, 'A')
ipaddr = str(r[0])
# os.command)wget ...) & run execute...
os.popen("python3 executeTree.py > treeOutput.txt &")
#with urllib.request.urlopen('http://'+ipaddr+':'+port+'/cgi-bin/executeTree.py') as response:
#   html = response.read()
fileURL = 'http://'+ipaddr+':'+port+'/cgi-bin/treeOutput.txt'
linkToFile = "<a href=" + fileURL + "> click here</a>"

print ("Content-type: text/html")
print ("")
print ("The output will be ready in a few minutes: " + linkToFile)
