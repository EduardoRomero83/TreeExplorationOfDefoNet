#!/usr/bin/python3

"""
Created on Sat Mar 18 17:05:13 2023

@author: Eduardo Romero
"""

import cgi, os
import cgitb; cgitb.enable()
import zipfile

UPLOAD_DIR = "/opt/bitnami/apache2/cgi-bin/"

print("Content-Type: text/html")
print()

print("<html>")
print("<head>")
print("<title>Upload ZIP File</title>")
print("</head>")
print("<body>")

print("<h1>Upload ZIP File</h1>")
print("<form method='post' enctype='multipart/form-data'>")
print("<input type='file' name='file'>")
print("<input type='submit' value='Upload'>")
print("</form>")

form = cgi.FieldStorage()

# Check if the file was uploaded
if "file" not in form:
    print("<p>No file was uploaded.</p>")
else:
    # Get the file and filename
    file = form["file"]
    filename = os.path.basename(file.filename)

    # Check if the file is a ZIP archive
    if not zipfile.is_zipfile(file.file):
        print("<p>File is not a ZIP archive.</p>")
    else:
        # Save the file to the upload directory
        with open(os.path.join(UPLOAD_DIR, filename), "wb") as f:
            f.write(file.file.read())
        print("<p>File uploaded successfully.</p>")

print("</body>")
print("</html>")
