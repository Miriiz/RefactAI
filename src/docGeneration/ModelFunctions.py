import tensorflow as tf
import os
from tensorflow.keras import Model, Sequential
from tensorflow.python.keras.layers import Flatten

train_size = 0
val_size = 0
epch = 300
ref_lr = 0.000001
batch_size = 32

encoder = tf.keras.layers.experimental.preprocessing.TextVectorization(output_mode='int', output_sequence_length=100,
                                                              max_tokens=500)


def add_mlp_layers2(model, encoder):
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(
            input_dim=len(encoder.get_vocabulary()),
            output_dim=64,
            # Use masking to handle the variable sequence lengths
            mask_zero=True),
        tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(1)
    ])


def create_base_model(add_custom_layers_func, encoder=None) -> Model:
    m = Sequential()
    if encoder is not None:
        add_custom_layers_func(m, encoder)
    else:
        add_custom_layers_func(m)
    m.add(Flatten())
    m.add(tf.keras.layers.Dense(1, activation="sigmoid"))  # tf.keras.activations.softmax))

    m.compile(optimizer=tf.keras.optimizers.Adam(1e-4),
              # tf.keras.optimizers.SGD(learning_rate=ref_lr / ref_batch_size * batch_size),
              loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              metrics=["accuracy"])
    # m.build()
    # m.summary()

    return m
