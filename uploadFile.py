#!/usr/bin/python3

"""
Created on Sat Mar 18 17:05:13 2023

@author: Eduardo Romero
"""

#!/usr/bin/env python

import cgi
import os
import requests

# Get the form data
form = cgi.FieldStorage()
link = form.getvalue('link')


url = 'https://graph.microsoft.com/v1.0/shares/u!{}/root'.format(link)

# Retrieve the file using the Microsoft Graph API
response = requests.get(url)

# Save the file to disk
with open('dataset.zip', 'wb') as f:
    f.write(response.content)

print('Content-Type: text/html')
print()
print('<html><body>')
print('<h2>File uploaded successfully!</h2>')
print('</body></html>')
