# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 16:18:25 2023

@author: Eduardo Romero
"""

import cgi
import cgitb
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
r = res.query(item, 'A')
ipaddr = str(r[0])
with urllib.request.urlopen('http://'+ipaddr+':'+port+'/cgi-bin/executeTree.py') as response:
   html = response.read()

print ("Content-type: text/html")
print ("")
print (html)
