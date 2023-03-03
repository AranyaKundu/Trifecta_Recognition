import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import pathlib
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense, Dropout


def create_model(data_augmentation):
     # set normalization layer scale
    normalization_layer = layers.experimental.preprocessing.Rescaling(1./255)

    model = Sequential([
        data_augmentation,
        layers.experimental.preprocessing.Rescaling(1./255, input_shape = (img_height, img_width, 3)),
        layers.Conv2D(16, 3, padding = 'same', activation = 'relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(32, 3, padding = 'same', activation = 'relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, padding = 'same', activation = 'relu'),
        layers.MaxPooling2D(),
        layers.Dropout(0.2),
        layers.Flatten(),
        layers.Dense(128, activation = 'relu'),
        layers.Dense(num_classes)
        ])

    model.compile(optimizer = 'adam',
                loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits = True),
                metrics=['accuracy'])
    
    return model

if __name__ == "__main__":
    
    directory = "path/to/images"
    img_height, img_width, batch_size = 180, 180, 16
    classnames = os.listdir(directory)
    data_dir = pathlib.Path(directory)
    num_classes = len(classnames)
    # Set training data
    train_data = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        class_names = classnames,
        seed = 42,
        image_size = (img_height, img_width),
        batch_size = batch_size
    )

    # set buffer size
    autotune = tf.data.AUTOTUNE
    # apply buffer size to train data
    train_data = train_data.cache().shuffle(1000).prefetch(buffer_size = autotune)

    data_augmentation = keras.Sequential([
            layers.experimental.preprocessing.RandomFlip("horizontal", input_shape = (img_height, img_width, 3)),
            layers.experimental.preprocessing.RandomRotation(0.1),
            layers.experimental.preprocessing.RandomZoom(0.1)
        ])

    model = create_model(data_augmentation)

    history = model.fit(train_data, epochs = 30)
    
    model.save("face_recognition_model.h5")
