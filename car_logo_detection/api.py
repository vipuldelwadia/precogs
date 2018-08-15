from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
from keras.preprocessing import image

import tensorflow as tf

from PIL import Image

import numpy as np
from flask import Flask, request, jsonify

# dimensions of our images.
img_width, img_height = 100, 100
target_size = (img_width, img_height)

model = None

def invoke(model, input_file):
    img = Image.open(input_file)

    if img.size != target_size:
        img = img.resize(target_size)

    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)

    with graph.as_default():
        return model.predict(x)

def load_model(weights_file):
    if K.image_data_format() == 'channels_first':
        input_shape = (3, img_width, img_height)
    else:
        input_shape = (img_width, img_height, 3)

    global model
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

    model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

    model.load_weights(weights_file)

    global graph
    graph = tf.get_default_graph()

load_model('weights.h5')

app = Flask(__name__)

@app.route('/v1/predict', methods=['POST'])
def _predict():
    upload = request.files['image']
    result = invoke(model=model, input_file=upload)
    return jsonify({
        'filename': upload.filename,
        'hasLogo': True if int(result[0][0]) == 1 else False # convert numpy float to python float
    })

app.run(debug=True, port=5000, host='0.0.0.0')