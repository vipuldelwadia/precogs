#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  2 08:36:20 2018

@author: rologan
"""
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
import matplotlib.pyplot as plt
import numpy as np
from keras.preprocessing import image
from PIL import Image


# dimensions of our images.
img_width, img_height = 100, 100

train_data_dir = './dataset/test'
validation_data_dir = './dataset/test'

nb_train_samples = 1511
nb_validation_samples = 298
epochs = 30
batch_size = 16

def preprocess_image(x):
    #return x
    crop_height = int(img_height/6)
    half_height = int(img_height/2)
    
    img = image.array_to_img(x)

    top = img.crop((0, 0, img_width, crop_height))
    bottom = img.crop((0, (img_height - crop_height), img_width, img_height))
    
    top = top.resize((img_width, half_height))
    bottom = bottom.resize((img_width, half_height))
    
    new = Image.new('RGB', (img_width, img_height))

    new.paste(top, (0,0))
    new.paste(bottom, (0,half_height))
    
    x = np.asanyarray(new)
    x.setflags(write=1)

    return x * (1. / 255)

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

# this is the augmentation configuration we will use for training
train_datagen = ImageDataGenerator(
    horizontal_flip=True,
    rescale=1. / 255)
    #preprocessing_function=preprocess_image)

# this is the augmentation configuration we will use for testing:
# only rescaling
test_datagen = ImageDataGenerator(
    rescale=1. / 255)
    #preprocessing_function=preprocess_image)

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary')

validation_generator = test_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary')

H = model.fit_generator(
    train_generator,
    steps_per_epoch=nb_train_samples // batch_size,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=nb_validation_samples // batch_size)

model.save_weights('weights.h5')
model.save('model.h5')

# plot the training loss and accuracy
plt.style.use("ggplot")
plt.figure()
N = epochs
plt.plot(np.arange(0, N), H.history["loss"], label="train_loss")
plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss")
plt.plot(np.arange(0, N), H.history["acc"], label="train_acc")
plt.plot(np.arange(0, N), H.history["val_acc"], label="val_acc")
plt.title("Training Loss and Accuracy on Logo/No Logo")
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend(loc="lower left")
plt.savefig("plot")