#!/usr/bin/python3
"""
Created on Sat Mar 18 17:05:13 2023

@author: Eduardo Romero
"""

import cgi
import cgitb
import os
import zipfile
import subprocess

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
print("<input type='text' name='link' placeholder='Enter a link to the file'>")
print("<input type='submit' name='upload' value='Upload'>")
print("</form>")

form = cgi.FieldStorage()
state = str(form.getvalue("state"))
state = state.replace("@","DAB")
unzipDirectory = UNZIP_DIR + state + "/"
fileDownloaded = False
filename = unzipDirectory + "dataset.zip"

if not os.path.isdir(unzipDirectory):
    os.mkdir(unzipDirectory)


if "link" in form and "upload" in form:
    # Get the file and filename
    link = form["link"].value
    cmd = ["wget", "-O", filename, link]
    
    # Check if the link is valid
    if not link:
       print("<p>Invalid link.</p>")
    else:
        # Download the file from the link in the background
        with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p1:
            stdout, stderr = p1.communicate()
            print("<p>Download started.</p>")

            # Check if the download is finished
            if p1.returncode == 0:
                fileDownloaded = True
                with zipfile.ZipFile(filename, 'r') as zip_ref:
                    zip_ref.extractall(unzipDirectory)
                print("<p>File unzipped successfully.</p>")
            else:
                print(f"Download failed. Error code: {p1.returncode}")
                print(stderr.decode("utf-8"))

print("</body>")
print("</html>")