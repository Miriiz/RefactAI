import tensorflow as tf
import os
from tensorflow.keras import Model, Sequential
from tensorflow.python.keras.layers import Flatten
from ModelParam import *


def create_base_model(add_custom_layers_func) -> Model:
    m = Sequential()
    add_custom_layers_func(m)
    m.add(Flatten())
    m.add(tf.keras.layers.Dense(2, tf.keras.activations.softmax))

    m.compile(optimizer=tf.keras.optimizers.SGD(learning_rate=ref_lr / ref_batch_size * batch_size),
              loss=tf.keras.losses.categorical_crossentropy,
              metrics=["categorical_accuracy"])

    return m


def linear_mod(Seq):
    pass


def add_mlp_layers(model):
    model.add(tf.keras.layers.Flatten())
    for _ in range(5):
        model.add(tf.keras.layers.Dense(2048, activation=tf.keras.activations.linear))
        model.add(tf.keras.layers.BatchNormalization())
        model.add(tf.keras.layers.Activation(activation=tf.keras.activations.tanh))
