# =======================================================================================================
# PROBLEM C3
#
# Build a CNN based classifier for Cats vs Dogs dataset.
# Your input layer should accept 150x150 with 3 bytes color as the input shape.
# This is unlabeled data, use ImageDataGenerator to automatically label it.
# Don't use lambda layers in your model.
#
# The dataset used in this problem is originally published in https://www.kaggle.com/c/dogs-vs-cats/data
#
# Desired accuracy and validation_accuracy > 72%
# ========================================================================================================
import urllib

import urllib.request
import zipfile
import tensorflow as tf
import os
from keras_preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Activation, Dense, Flatten, Dropout


def solution_C3():
    data_url = 'https://github.com/dicodingacademy/assets/raw/main/Simulation/machine_learning/cats_and_dogs.zip'
    urllib.request.urlretrieve(data_url, 'cats_and_dogs.zip')
    local_file = 'cats_and_dogs.zip'
    zip_ref = zipfile.ZipFile(local_file, 'r')
    zip_ref.extractall('data/')
    zip_ref.close()

    BASE_DIR = 'data/cats_and_dogs_filtered'
    train_dir = os.path.join(BASE_DIR, 'train')
    validation_dir = os.path.join(BASE_DIR, 'validation')

    train_datagen =  ImageDataGenerator(
        rotation_range=30,
        brightness_range=[0.2,1.0],
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode="nearest",
        rescale=1./255,
        validation_split=0.4
    )


    # YOUR IMAGE SIZE SHOULD BE 150x150
    # Make sure you used "binary"
    train_generator =  train_datagen.flow_from_directory(BASE_DIR,
                                                         batch_size=12,
                                                         class_mode='binary',
                                                         shuffle=False,
                                                         target_size=(150,150),
                                                         subset="training")
    validation_generator = train_datagen.flow_from_directory(BASE_DIR,
                                                             batch_size=12,
                                                             class_mode='binary',
                                                             shuffle=False,
                                                             target_size=(150,150),
                                                             subset="validation")
    model = tf.keras.models.Sequential([
        # YOUR CODE HERE, end with a Neuron Dense, activated by 'sigmoid'
        Conv2D(32, (3,3), strides = (1,1), activation="relu", input_shape=(150,150,3)),
        MaxPooling2D(pool_size=(2,2), padding='valid'),
        Conv2D(32, (3,3), strides = (1,1), activation='relu'),
        MaxPooling2D(pool_size=(2,2), padding='valid'),
        Conv2D(64, (3,3), strides = (1,1), activation='relu'),
        MaxPooling2D(pool_size=(2,2), padding='valid'),
        Flatten(),
        Dropout(0.2),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(
        train_generator,
        steps_per_epoch=8,
        epochs=8,
        verbose=1,
        validation_data=validation_generator,
        validation_steps=8
    )
    return model


# The code below is to save your model as a .h5 file.
# It will be saved automatically in your Submission folder.
if __name__ == '__main__':
    # DO NOT CHANGE THIS CODE
    model = solution_C3()
    model.save("model_C3.h5")
