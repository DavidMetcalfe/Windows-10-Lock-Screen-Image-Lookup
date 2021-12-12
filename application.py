import winreg
import os
import pathlib
import webbrowser
import sys
import requests
import subprocess as sp

import PIL.Image
def check_landscape(fn):
    try:
        img=PIL.Image.open(fn)
        w,h=img.size
        if w>1000 and w>h:
            #print("%s: %d x %d"%(fn,w,h))
            return True
    except Exception as e:
        print("Error:",str(e))
        return False

'''
A simple script that will fetch the currently displayed Lock Screen
wallpaper being used by Windows 10 and do a Google image search
to help identify it. Resulting search will pop up in your default browser.

David Metcalfe, Feb 1 2017

Modified to use the 'HotSpotImageFolderPath' and search for the latest 
large landscape image, since the previous version didn't show the most 
recently displayed lock image.

jdpipe 2021
'''
try:
    # Connect to registry, set appropriate key.
    reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    reg = winreg.OpenKey(
        reg,
        r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Lock Screen\\Creative")

    # Fetch Registry value (file path) for LandscapeAssetPath.
    regKey = winreg.QueryValueEx(reg, 'HotSpotImageFolderPath')[0]

    # Normalize filepath.
    imgDir = os.path.normpath(regKey)
except Exception as e:
    print("{}".format(e.message))
    sys.exit('Something went wrong relating to the filesystem.')

try:
    ls = pathlib.Path(imgDir).glob('*')
    ls = [str(i) for i in ls if check_landscape(i)]
    ls = sorted(ls,key=os.path.getmtime)
    ls.reverse()
    #print("\n".join([repr((i,os.path.getmtime(i))) for i in ls]))
    #sp.run("ls -lahS %s"%(imgDir,),shell=True,check=True)
except Exception as e:
    print("{}".format(e.message))
    sys.exit('Something went wrong searching for the newest image')

if len(ls) == 0:
    sys.exit("No images found")
filePath=ls[0]
print(filePath)

try:
    # Hand-off file to Google Images for a reverse image search.
    #filePath = imgDir
    searchUrl = 'http://www.google.com.au/searchbyimage/upload'
    multipart = {'encoded_image': (filePath, open(filePath, 'rb')), 'image_content': ''}
    response = requests.post(searchUrl, files=multipart, allow_redirects=False)
    fetchUrl = response.headers['Location']
    webbrowser.open(fetchUrl)
except Exception as e:
    print("{}".format(e.message))
    sys.exit('Something went wrong while searching the image.')

# vim: ts=4:sw=4:et
