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

print("<h1>Upload dataset</h1>")
print("<p>Please upload a dataset to be tested. The dataset should have the following format:</p>")
print("<p>There should be one file called 'data_result_train.txt'</p>")
print("<p>This file should have two columns. For each row, the first column has" 
     + " a path to an image file and the second column should contain a value between 0 and 1"
     +" indicating the classification of the model on that image.</p>")
print("<p>For example: </p>")
print("<p>nn_Data_Set_Cropped/training/0/DJI_0004_hw_0_0.jpg 0.3466 </p>")
print("<p>Indicates that the image on the first column is classified as class 0 by the neural model. </p>")
print("<p>The dataset should contain a similar file called  'data_result_test.txt' that follows a similar format.</p>")
print("<p>Finally the dataset should contain a folder containing all the images in the path specified in the previous two files. </p>")
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
        
        # Reset the file position before extracting
        file.file.seek(0)
        print("<p>File uploaded successfully. Please unzip it now</p>")
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
