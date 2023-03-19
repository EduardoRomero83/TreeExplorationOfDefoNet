#!/usr/bin/python3

"""
Created on Sat Mar 18 17:05:13 2023

@author: Eduardo Romero
"""
#!/usr/bin/env python
import cgi
import os
import zipfile
import io
import shutil

UPLOAD_DIR = "/path/to/upload/directory"
UNZIP_DIR = "/path/to/unzip/directory"

print("Content-Type: text/html")
print()

print("<html>")
print("<head>")
print("<title>Upload and Unzip ZIP File</title>")
print("</head>")
print("<body>")

print("<h1>Upload and Unzip ZIP File</h1>")
print("<form method='post' enctype='multipart/form-data'>")
print("<input type='file' name='file'>")
print("<input type='submit' value='Upload and Unzip'>")
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
        
        # Reset the file position before extracting
        file.file.seek(0)
        
        # Unzip the file into the specified directory
        with zipfile.ZipFile(io.BytesIO(file.file.read())) as zip_ref:
            zip_ref.extractall(UNZIP_DIR)
        
        print("<p>File uploaded and unzipped successfully.</p>")

print("</body>")
print("</html>")
