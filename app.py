# app.py
# Developer: Nicolas Fuchs

#######################
import requests
import urllib
import subprocess
import json
import shutil
#######################

# Unsplash Application Key
api_access_key = 'application key here'

# Setting the filepath for this file (already inside this directory)
filepath = 'tmp/background.jpeg'
# Full filepath is required for osascript
full_filepath = "/Users/nicolasfuchs/Desktop/backgroundImage/tmp/background.jpeg"

# Change the Background script
cmd = """/usr/bin/osascript<<END
tell application "Finder"
set desktop picture to POSIX file "%s"
end tell
END"""

# Using Unsplash API to grab random image from Unsplash
url = 'https://api.unsplash.com/photos/random?client_id=' + api_access_key

# requests 'GET' request for the webpage
response = requests.get(url)
# Stores the reponse content
json_string = response.content

# Uses JSON to load the content to 'parsed_json'
parsed_json = json.loads(json_string)
# 'photo' is a link to the image
photo = parsed_json['urls']['full']

# Open the url image, set stream to True, this will return the stream content.
r = requests.get(photo, stream = True)

# Check if the image was retrieved successfully
if r.status_code == 200:
    # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
    r.raw.decode_content = True
    
    # Open a local file with wb ( write binary ) permission.
    with open(filepath,'wb') as f:
        shutil.copyfileobj(r.raw, f)
        
    print('Image sucessfully Downloaded: ',filepath)
else:
    print('Image Couldn\'t be retreived')

# Running osascript using subprocess
try:
	subprocess.Popen(cmd%full_filepath, shell=True)
	subprocess.call(["killall Dock"], shell=True)
except:
	print("Your computer didn't allow this!")
