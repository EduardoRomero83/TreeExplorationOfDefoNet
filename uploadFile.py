#!/usr/bin/python3
"""
@author: Eduardo Romero
"""
import cgi
import cgitb
import os
import subprocess

UNZIP_DIR = "/opt/bitnami/apache2/cgi-bin/"

cgitb.enable()

print("Content-Type: text/html")
print()
form = cgi.FieldStorage()
state = str(form.getvalue("state"))
state = state.replace("@","DAB")
unzipDirectory = UNZIP_DIR + state + "/"
fileDownloaded = False
filename = unzipDirectory + "dataset.zip"

if not os.path.isdir(unzipDirectory):
    os.mkdir(unzipDirectory)
    
    
if not "p1" in form:
    print("<html>")
    print("<head>")
    print("<title>Upload and Unzip ZIP file</title>")
    print("</head>")
    print("<body>")
    print("<h1>Upload dataset</h1>")
    print("<p>Please upload a dataset to be tested. The dataset should be given as a link.</p>")
    print("<p>The link should be a download link to a zip file.</p>")
    print("<p>Inside the zip file, the dataset should have the following format:</p>")
    print("<p>There should be one file called 'data_result_train.txt'</p>")
    print("<p>This file should have two columns. For each row, the first column has"
          + " a path to an image file and the second column should contain a value between 0 and 1"
          +" indicating the classification of the model on that image.</p>")
    print("<p>For example: </p>")
    print("<p>nn_Data_Set_Cropped/training/0/DJI_0004_hw_0_0.jpg 0.3466 </p>")
    print("<p>Indicates that the image on the first column is classified as class 0 by the neural model. </p>")
    print("<p>The dataset should contain a similar file called  'data_result_test.txt' that follows a similar format.</p>")
    print("<p>Finally the dataset should contain a folder containing all the images in the path specified in the previous two files. </p>")
    print("<p>For example: in the example given above, there should be a folder called nn_Data_Set_Cropped with all image files.</p>")
    print('<form method="get" action="/cgi-bin/uploadFile.py" enctype="multipart/form-data">')
    print('<input type = "hidden" name = "ms" value = "i44445treeinterpretability">')
    print('<input type = "hidden" name = "port" value = "44445">')
    print('<input type = "hidden" name = "path" value = "/cgi-bin/">')
    print('<input type = "hidden" name = "page" value = "uploadFile.py">')	 
    print("<input type='text' name='p1' placeholder='Enter a link to the file'>")
    print("<input type='submit' name='upload' value='Upload'>")
    print("</form>")
else:
    print("<html>")
    print("<head>")
    print("<title>Dowloading from URL</title>")
    print("</head>")
    print("<body>")
    # Get the file and filename
    link = form["p1"].value
    cmd = ["wget", "-O", filename, link]
    # Check if the link is valid
    if not link:
        print("<p>Invalid link.</p>")
    else:
        # Download the file from the link
        p1 = subprocess.Popen(cmd)
        print("<p>Download started.</p>")
        print("<p>Please allow a few minutes for the download to complete.</p>")
        cmd = ["python3", "unzip.py", str(p1.pid), filename, unzipDirectory]
        subprocess.Popen(cmd)

print("</body>")
print("</html>")