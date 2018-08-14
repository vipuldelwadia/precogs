#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 16:15:31 2018

@author: rologan
"""

from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
from sklearn.metrics import confusion_matrix
from PIL import Image

import matplotlib.pyplot as plt
import itertools
import numpy as np
import glob

# dimensions of our images.
img_width, img_height = 100, 100
target_size = (img_width, img_height)

if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)

model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=input_shape))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.8))
model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

model.load_weights('weights.h5')

model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

arrayOfLogoImagePaths = glob.glob('./dataset/test/with_logos/*jpg')
arrayOfNoLogoImagePaths = glob.glob('./dataset/test/no_logos/*jpg')

y_true = [1] * len(arrayOfLogoImagePaths) + [0] * len(arrayOfNoLogoImagePaths)
y_pred = []

for i, imagePath in enumerate(arrayOfLogoImagePaths + arrayOfNoLogoImagePaths):

    img = Image.open(imagePath)
    
    if img.size != target_size:
        img = img.resize(target_size)

    x = np.asanyarray(img)
    x = np.expand_dims(x, axis=0)
    
    prediction = model.predict(x)
    y_pred.append(int(prediction[0][0]))
    
cnf_matrix = confusion_matrix(y_true, y_pred, labels=[1, 0])

classes = ["Logo", "no Logo"]

plt.figure()
plt.imshow(cnf_matrix, interpolation='nearest', cmap=plt.cm.Blues)
plt.title("Confusion matrix")
plt.colorbar()
tick_marks = np.arange(len(classes))
plt.xticks(tick_marks, classes, rotation=45)
plt.yticks(tick_marks, classes)

fmt = 'd'
thresh = cnf_matrix.max() / 2.
for i, j in itertools.product(range(cnf_matrix.shape[0]), range(cnf_matrix.shape[1])):
    plt.text(j, i, format(cnf_matrix[i, j], fmt),
             horizontalalignment="center",
             color="white" if cnf_matrix[i, j] > thresh else "black")

plt.tight_layout()
plt.ylabel('True label')
plt.xlabel('Predicted label')

# Print out stats to do with confustion matrix.
total = len(y_pred)
real_true = len(arrayOfLogoImagePaths)
real_false = len(arrayOfNoLogoImagePaths)

true_pos = cnf_matrix[0][0]
true_neg = cnf_matrix[1][1]
false_pos = cnf_matrix[1][0]
false_neg = cnf_matrix[0][1]

newline = "\n"

print("Overall, how often is the classifier correct?")
print("Accuracy: " + str((true_pos+true_neg)/total))
print(newline);

print("Overall, how often is it wrong?")
print("Misclassification rate: " + str((false_pos+false_neg)/total))
print(newline)

print("When it's actually yes, how often does it predict yes?")
print("true pos rate sensitivity: " + str((true_pos / real_true)))
print(newline)

print("When it's actually no, how often does it predict yes?")
print("false pos rate (recall): " + str((false_pos/real_false)))
print(newline)

print("When it's actually no, how often does it predict no?")
print("Specificity: " + str((true_neg/real_false)))
print(newline)

print("When it predicts yes, how often is it correct?")
print("precision: " + str((true_pos/(true_pos + false_pos))))
print(newline)

print("How often does the yes condition actually occur in our sample?")
print("prevalance: " + str((real_true/total)))
print(newline)