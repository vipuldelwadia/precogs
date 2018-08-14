#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 12:36:37 2018

@author: rologan
"""

import os
import sys
import json
import requests
import tempfile
from io import BytesIO
from PIL import Image


def makeFolder(newpath):
    if not os.path.exists(newpath):
        os.makedirs(newpath)
        
makeFolder('./dataset/with_logos')
makeFolder('./dataset/no_logos')

file = open('firebase_database_export.json','r') 

data = json.load(file)

file.close() 

images = data['images']

imageCount = len(images)

def downloadImage(imageUrl):
    buffer = tempfile.SpooledTemporaryFile(max_size=1e9)
    response = requests.get(randomImageUrl, stream=True)
    
    if response.status_code == 200:
        downloaded = 0
        #filesize = int(response.headers['content-length'])
        
        for chunk in response.iter_content():
            downloaded += len(chunk)
            buffer.write(chunk)
            
        buffer.seek(0)
        return Image.open(BytesIO(buffer.read()))

for index, imageId in enumerate(images):
    # If labelled as yes or no logos then download and put into
    # correct dataset folder.
    image = images[imageId]
    
    if image['label'] == 'yes':
        randomImageUrl = image['url']
        img = downloadImage(randomImageUrl)
        img.save("dataset/with_logos/" + imageId + ".jpg")
    elif image['label'] == 'no':
        randomImageUrl = image['url']
        response = requests.get(randomImageUrl)
        img = downloadImage(randomImageUrl)
        img.save("dataset/no_logos/" + imageId + ".jpg")
        
    sys.stdout.write('\r')
    sys.stdout.write(str(index) + "/" + str(imageCount) + " images downloaded")
    sys.stdout.flush()
        
        
        
