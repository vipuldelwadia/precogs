'''
new_dataset_maker.py

This file will take a KITTI Dataset which has images that contain multiple 
vehicles and separate the vehicles 
into separate image and label files.
'''


from PIL import Image
import glob
import os
import shutil
import math

 #Dataset used for creating our more refined dataset.
arrayOfLabelPaths = glob.glob("./Dataset/labels/*.txt")
KITTIImageDir = "/Users/rologan/Documents/Machine_learning/Datasets/cars/KITTI/training/images/"
imageDir = "Dataset/images"

minImageWidth = 50
minImageHeight = 50
paddingPercentage = .10

print("Starting...")
totalImagesCreated = 0

# delete images dir if exists.
if os.path.exists(imageDir):
    shutil.rmtree(imageDir)

for i, file in enumerate(arrayOfLabelPaths):
    fo = open(file, "r")
    label = fo.readline()
    fo.close()
    
    data = label.split(",")
    imagePath = KITTIImageDir + str(data[0]) + ".png"
    boundingBox = list(map(float, [data[3], data[4], data[5], data[6]]))
    
    # Don't add this image if it is too small.
    if boundingBox[2] - boundingBox[0] < minImageWidth or boundingBox[3] - boundingBox[1] < minImageHeight:
        continue
    
    # We pad the image so we don't clip the bounds too close to the vehicle.
    boundingBox[0] = boundingBox[0] - (boundingBox[0] * paddingPercentage)
    boundingBox[1] = boundingBox[1] - (boundingBox[1] * paddingPercentage)
    boundingBox[2] = boundingBox[2] + (boundingBox[2] * paddingPercentage)
    boundingBox[3] = boundingBox[3] + (boundingBox[3] * paddingPercentage)
    
    image = Image.open(imagePath)
    cropped = image.crop(boundingBox)
    
    radians = float(data[2])
    degrees = int(math.degrees(radians))
    
    # Bucket the different angles of the vehicles into front, side, back or other.
    angleDescription = "other"
    
    if degrees in range(-100,-79):
        angleDescription = "back"
    if degrees in range(165,181):
        angleDescription = "side"
    if degrees in range(-180,-164):
        angleDescription = "side"
    if degrees in range(-15,16):
        angleDescription = "side"
    if degrees in range(75,106):
        angleDescription = "front"
        
        
    # Split our images into trainging and validation groups.
    dirName = "training" if i % 3 == 0 else "validation"
    
    outputDir = imageDir + "/" + dirName + "/" + angleDescription + "/"
    
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
        
    newfilename = outputDir + data[0] + "_" + str(data[1]) + ".png"
    cropped.save(newfilename)
    
    totalImagesCreated = totalImagesCreated + 1

   
print("all done, " + str(totalImagesCreated) + " images created")