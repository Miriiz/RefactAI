import tensorflow as tf
# import tensorflow_decision_forests as tfdf
import os
from tensorflow.keras import Model, Sequential
from tensorflow.python.keras.layers import Flatten
from ModelParam import *

train_size = 0
val_size = 0


def create_base_model(add_custom_layers_func, encoder=None) -> Model:
    m = Sequential()
    if encoder is not None:
        add_custom_layers_func(m, encoder)
    else:
        add_custom_layers_func(m)
    m.add(Flatten())
    m.add(tf.keras.layers.Dense(1, activation="sigmoid"))  # tf.keras.activations.softmax))
    #
    # optimizer = 'adam'
    optimizer = tf.keras.optimizers.Adam(1e-4)
    m.compile(tf.keras.optimizers.SGD(learning_rate=ref_lr / ref_batch_size * batch_size), #
              # tf.keras.optimizers.SGD(learning_rate=ref_lr / ref_batch_size * batch_size),
              loss=tf.keras.losses.BinaryCrossentropy(from_logits=True)
              # loss='sparse_categorical_crossentropy'
              ,
              metrics=["accuracy"])
    # m.build()
    # m.summary()

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
    # tfdf et non tf
    return model


def add_mlp_layers(model):
    model.add(tf.keras.layers.Flatten())
    for _ in range(5):
        model.add(tf.keras.layers.Dense(2048, activation=tf.keras.activations.linear))
        model.add(tf.keras.layers.BatchNormalization())
        model.add(tf.keras.layers.Activation(activation=tf.keras.activations.tanh))


def classic_layers(model):
    model.add(tf.keras.layers.Embedding(10000 + 1, 16))
    model.add(tf.keras.layers.Dropout(0.2))
    model.add(tf.keras.layers.GlobalAveragePooling1D())
    model.add(tf.keras.layers.Dropout(0.2))
    model.add(tf.keras.layers.Dense(1, activation=tf.keras.activations.sigmoid))


def add_mlp_layers2(model, encoder):
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(
            input_dim=len(encoder.get_vocabulary()),
            output_dim=64,
            # Use masking to handle the variable sequence lengths
            mask_zero=True),
        tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),
        tf.keras.layers.Dense(64),
        tf.keras.layers.Dense(1),
        tf.keras.layers.Activation('sigmoid')
    ])


def add_mlp_layers3(model, encoder):
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(len(encoder.get_vocabulary()), 64, mask_zero=True),
        tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, return_sequences=True)),
        tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(32)),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(1)
    ])




def add_lstm_layers(model, encoder):
    embedding_dim = 64
    model = tf.keras.Sequential([
        # Add an Embedding layer expecting input vocab of size 5000, and output embedding dimension of size 64 we set
        # at the top
        tf.keras.layers.Embedding(len(encoder.get_vocabulary()), embedding_dim, mask_zero=True),
        tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(embedding_dim, return_sequences=True)),
        tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(32)),
        tf.keras.layers.Dense(embedding_dim, activation='relu'),
        tf.keras.layers.Dense(6, activation='softmax')
    ])


# Function to train model
def train_model(m: Model, dataset, dataset_test):
    train_size = sum(1 for _ in dataset.unbatch())
    val_size = sum(1 for _ in dataset_test.unbatch())
    print(train_size)
    print(val_size)
    model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath='model\mlp3',
        save_weights_only=True,
        monitor='val_accuracy',
        mode='max',
        save_best_only=True)

    log = m.fit(
        dataset,
        validation_data=dataset_test,
        # steps_per_epoch=train_size // batch_size,
        # validation_steps=val_size // batch_size,
        epochs=epch,
        batch_size=batch_size,
        callbacks=[
            model_checkpoint_callback
            # tf.keras.callbacks.TensorBoard(log_dir='./logs', histogram_freq=0, write_graph=True, write_images=True)
        ]
    )
    return log


# Function to predict
def predict(model, x_iterator):
    return model.predict(x_iterator)
