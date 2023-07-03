#!/usr/bin/python3
"""
Created on Sun Mar 12 16:18:25 2023
@author: Eduardo Romero
"""
import cgi
import cgitb
import dns.resolver
import subprocess

cgitb.enable()
with open('/etc/resolv.kube', 'r') as f:
    kubedns = str(f.read()).strip()
res = dns.resolver.Resolver(configure=False)
res.nameservers = [ kubedns ]

form = cgi.FieldStorage()
numPixels = str(form.getvalue("p1"))
if numPixels == "None":
    numPixels = "4"
state = str(form.getvalue("state"))
state = state.replace("@","DAB")
# The full DNS name is default.svc.cluster.local
cmd = ["python3", "executeTree.py", numPixels, state]
with open("/opt/bitnami/apache/htdocs/"+state+"treeOutput.txt", "wb") as f:
    subprocess.Popen(cmd, stdout=f, shell=False, close_fds=True)
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
