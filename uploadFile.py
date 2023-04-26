#!/usr/bin/python3

#!/usr/bin/python3

"""
Created on Sat Mar 18 17:05:13 2023

@author: Eduardo Romero
"""

import cgi
import cgitb
import os
import zipfile
import io

UPLOAD_DIR = "/opt/bitnami/apache2/cgi-bin/"
UNZIP_DIR = "/opt/bitnami/apache2/cgi-bin/"

cgitb.enable()

print("Content-Type: text/html")
print()

print("<html>")
print("<head>")
print("<title>Upload and Unzip ZIP file</title>")
print("</head>")
print("<body>")

print("<h1>Upload and Unzip ZIP file</h1>")
print("<p>Please select a ZIP file to upload:</p>")
print("<form method='post' enctype='multipart/form-data'>")
print("<input type='file' name='file'>")
print("<input type='submit' name='upload' value='Upload'>")
print("</form>")

form = cgi.FieldStorage()

if "file" in form and "upload" in form:
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
        print("<form method='post' enctype='multipart/form-data'>")
        print("<input type='hidden' name='filename' value='" + filename + "'>")
        print("<input type='submit' name='unzip' value='Unzip'>")
        print("</form>")

if "filename" in form and "unzip" in form:
    filename = form["filename"].value
    # Unzip the file into the specified directory
    with zipfile.ZipFile(os.path.join(UPLOAD_DIR, filename), 'r') as zip_ref:
        zip_ref.extractall(UNZIP_DIR)
    print("<p>File unzipped successfully.</p>")

print("</body>")
print("</html>")
