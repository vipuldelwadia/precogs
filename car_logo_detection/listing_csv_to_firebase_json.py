#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 10:23:25 2018

@author: rologan
"""

file = open('to_upload_to_firebase.json','w') 
 
file.write('{\n')
file.write('\t"config" : {\n')
file.write('\t\t"question" : "Does this image have any logos or branding text on it?",\n')
file.write('\t\t"question_type" : 0\n')
file.write('\t},\n')
file.write('\t"images" : {\n')
 

fo = open('./listing_photos_dataset.csv', "r")
lines = fo.readlines()

lineCount = len(lines)

for index, line in enumerate(lines):
    line = line.rstrip()
    url = 'https://trademe.test2.tmcdn.co.nz/photoserver/full/' + line + '.jpg'
    file.write('\t\t"' + line + '" : {\n')
    file.write('\t\t\t"label" : "",\n')
    file.write('\t\t\t"url" : "' + url + '"\n')
    
    if index >= (lineCount - 1):
        file.write('\t\t}\n')
    else:
        file.write('\t\t},\n')
        
file.write('\t}\n')
file.write('}')
    

fo.close()
file.close() 