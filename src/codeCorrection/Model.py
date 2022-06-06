import tensorflow as tf
import os
from tensorflow.keras import Model, Sequential
from tensorflow.python.keras.layers import Flatten
from ModelParam import *

train_size = 0
val_size = 0
class_w = 0


def create_base_model(add_custom_layers_func) -> Model:
    m = Sequential()
    add_custom_layers_func(m)
    m.add(Flatten())
    m.add(tf.keras.layers.Dense(2, tf.keras.activations.softmax))

    m.compile(optimizer=tf.keras.optimizers.SGD(learning_rate=ref_lr / ref_batch_size * batch_size),
              loss=tf.keras.losses.categorical_crossentropy,
              metrics=["categorical_accuracy"])

    return m


# Create Dataset Iterator
def create_dataset_iterator(x_train, y_train, x_val, y_val):
    train_dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train))
    train_dataset = train_dataset.shuffle(train_size).batch(batch_size)

    val_dataset = tf.data.Dataset.from_tensor_slices((x_val, y_val))
    val_dataset = val_dataset.shuffle(val_size).batch(batch_size)

    return train_dataset, val_dataset


def linear_mod(Seq):
    pass


def forest_mod(model):
    model = tf.keras.RandomForestModel()
    return model


def add_mlp_layers(model):
    model.add(tf.keras.layers.Flatten())
    for _ in range(5):
        model.add(tf.keras.layers.Dense(2048, activation=tf.keras.activations.linear))
        model.add(tf.keras.layers.BatchNormalization())
        model.add(tf.keras.layers.Activation(activation=tf.keras.activations.tanh))


# Function to train model
def train_model(m: Model, x_iterator, y_iterator):
    log = m.fit(
        x_iterator,
        validation_data=y_iterator,
        epochs=epch,
        callbacks=[
            tf.keras.callbacks.TensorBoard(log_dir='./logs', histogram_freq=1, write_graph=True, write_images=True)
        ]
    )
    return log


# Function to predict
def predict(model, x_iterator):
    return model.predict(x_iterator)
