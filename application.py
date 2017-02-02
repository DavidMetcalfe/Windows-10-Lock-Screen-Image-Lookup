import winreg
import os.path
import webbrowser
import sys

import requests

'''
A simple script that will fetch the currently displayed Lock Screen 
wallpaper being used by Windows 10 and do a Google image search 
to help identify it. Resulting search will pop up in your default browser.

David Metcalfe, Feb 1 2017
'''
try:
    # Connect to registry, set appropriate key.
    reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    reg = winreg.OpenKey(reg,
        r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Lock Screen\\Creative")

    # Fetch Registry value (file path) for LandscapeAssetPath.
    regKey = winreg.QueryValueEx(reg, 'LandscapeAssetPath')[0]

    # Normalize filepath.
    imgDir = os.path.normpath(regKey)
except:
    sys.exit('Something went wrong relating to the filesystem.')

try:
    # Hand-off file to Google Images for a reverse image search.
    filePath = imgDir
    searchUrl = 'http://www.google.hr/searchbyimage/upload'
    multipart = {'encoded_image': (filePath, open(filePath, 'rb')), 'image_content': ''}
    response = requests.post(searchUrl, files=multipart, allow_redirects=False)
    fetchUrl = response.headers['Location']
    webbrowser.open(fetchUrl)
except:
    sys.exit('Something went wrong while searching the image.')