#!/usr/bin/python3
"""
Created on Sun Mar 12 16:18:25 2023

@author: Eduardo Romero
"""

import cgi
import cgitb
import os
import dns.resolver

cgitb.enable()
with open('/etc/resolv.kube', 'r') as f:
    kubedns = str(f.read()).strip()
res = dns.resolver.Resolver(configure=False)
res.nameservers = [ kubedns ]


form = cgi.FieldStorage()
item = str(form.getvalue("ms"))
port = str(form.getvalue("port"))
numPixels = str(form.getvalue("numpixels"))
# The full DNS name is default.svc.cluster.local
item = item + ".default.svc.cluster.local"
r = res.resolve(item, 'A')
ipaddr = str(r[0])
os.popen("python3 executeTree.py > ../htdocs/treeOutput.txt " + numPixels + " &")
fileURL = 'http://'+ipaddr+':'+port+'/treeOutput.txt'
linkToFile = "<a href=" + fileURL + "> click here</a>"

print ("Content-type: text/html")
print ("")
print("<html>")
print("<head>")
print("<title>Test dataset and model</title>")
print("</head>")
print("<body>")
print("<h1>Test dataset and model</h1>")
print ("<p>The output will be ready in a few minutes: " + linkToFile + "</p>")
print("</body>")
print("</html>")
