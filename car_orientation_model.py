"""
Created on Wed May  2 08:36:20 2018

@author: rologan
"""

'''
```
data/
    train/
        dogs/
            dog001.jpg
            dog002.jpg
            ...
        cats/
            cat001.jpg
            cat002.jpg
            ...
    validation/
        dogs/
            dog001.jpg
            dog002.jpg
            ...
        cats/
            cat001.jpg
            cat002.jpg
            ...
```
'''

from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K




# dimensions of our images.
img_width, img_height = 150, 150

train_data_dir = '/Users/rologan/Documents/Machine_learning/Datasets/catdog/train'
validation_data_dir = '/Users/rologan/Documents/Machine_learning/Datasets/catdog/test'

cars_images_dir = '/Users/rologan/Documents/Machine_learning/Datasets/cars/KITTI/training/images'
car_labels_dir = '/Users/rologan/Documents/Machine_learning/Datasets/cars/KITTI/training/labels'

'''
Example of label for image.
Car 0.00 0 -1.75 683.34 170.98 803.44 257.43 1.49 1.56 4.34 2.51 1.49 14.75 -1.59
Car 0.00 0 -1.31 262.97 182.23 469.76 318.00 1.42 1.53 4.12 -3.06 1.56 9.79 -1.61
Car 0.99 1 -2.37 910.25 159.81 1241.00 374.00 1.59 1.59 3.89 2.61 1.55 2.39 -1.60
Car 0.00 0 -1.58 641.55 172.79 681.44 206.29 1.38 1.64 3.51 2.22 1.40 31.72 -1.51
Van 0.00 2 -1.24 683.63 153.82 724.01 183.67 2.59 1.98 5.33 8.59 0.95 65.64 -1.11

Type: van
Truncated: 0.00
Occluded: 3
Alpha: 2.06 -> 120 degrees
Box: 16.35, 117.65, 314.78, 314.78
Dimensions: 2.72, 1.90, 5.78
Location: -7.39, 1.99, 12.90
rotation_y: 1.55 -> 88 

!!!USE ALPHA VALUE FOR ROTATION OF CAR!!!
who knows what the fuck rotation_y does?

Data Format Description
=======================

The data for training and testing can be found in the corresponding folders.
The sub-folders are structured as follows:

  - image_02/ contains the left color camera images (png)
  - label_02/ contains the left color camera label files (plain text files)
  - calib/ contains the calibration for all four cameras (plain text file)

The label files contain the following information, which can be read and
written using the matlab tools (readLabels.m, writeLabels.m) provided within
this devkit. All values (numerical or strings) are separated via spaces,
each row corresponds to one object. The 15 columns represent:

#Values    Name      Description
----------------------------------------------------------------------------
   1    type         Describes the type of object: 'Car', 'Van', 'Truck',
                     'Pedestrian', 'Person_sitting', 'Cyclist', 'Tram',
                     'Misc' or 'DontCare'
   1    truncated    Float from 0 (non-truncated) to 1 (truncated), where
                     truncated refers to the object leaving image boundaries
   1    occluded     Integer (0,1,2,3) indicating occlusion state:
                     0 = fully visible, 1 = partly occluded
                     2 = largely occluded, 3 = unknown
   1    alpha        Observation angle of object, ranging [-pi..pi]
   4    bbox         2D bounding box of object in the image (0-based index):
                     contains left, top, right, bottom pixel coordinates
   3    dimensions   3D object dimensions: height, width, length (in meters)
   3    location     3D object location x,y,z in camera coordinates (in meters)
   1    rotation_y   Rotation ry around Y-axis in camera coordinates [-pi..pi]
   1    score        Only for results: Float, indicating confidence in
                     detection, needed for p/r curves, higher is better.
                     
                     
    0.79 radians in a new segment.
                     
'''


nb_train_samples = 200
nb_validation_samples = 40
epochs = 50
batch_size = 16

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
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

# this is the augmentation configuration we will use for training
train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

# this is the augmentation configuration we will use for testing:
# only rescaling
test_datagen = ImageDataGenerator(rescale=1. / 255)

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

model.fit_generator(
    train_generator,
    steps_per_epoch=nb_train_samples // batch_size,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=nb_validation_samples // batch_size)

model.save_weights('catdog_weights.h5')
model.save('catdog_model.h5')