#!/usr/bin/python3
"""
Created on Sun Mar 12 16:18:25 2023
@author: Eduardo Romero
"""
import cgi
import cgitb
import dns.resolver
import os

cgitb.enable()
with open('/etc/resolv.kube', 'r') as f:
    kubedns = str(f.read()).strip()
res = dns.resolver.Resolver(configure=False)
res.nameservers = [ kubedns ]

form = cgi.FieldStorage()
numPixels = str(form.getvalue("p1"))
state = str(form.getvalue("state"))
state = state.replace("@","DAB")
# The full DNS name is default.svc.cluster.local

cmdString = "python3 executeTree.py " + numPixels + " " + state 
fileOutput = "/opt/bitnami/apache/htdocs/"+state+"treeOutput.txt"
cmdString = cmdString + " > " + fileOutput + " & < /dev/null"
os.system(cmdString)
fileURL = "/"+state+"treeOutput.txt"
linkToFile = "<a href=\"" + fileURL + "\"> click here</a>"

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
