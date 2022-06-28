from GithubDataset import GithubDataset
from Model import *
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
from matplotlib import pyplot as plt

max_token = 500
encoder = layers.experimental.preprocessing.TextVectorization(output_mode='int', output_sequence_length=100,
                                                              max_tokens=max_token)
test_percent = 5 / 100


def vectorize_text(text, label):
    text = tf.expand_dims(text, -1)
    label = tf.reshape(label, [int(tf.size(label)), 1])
    return encoder(text) / max_token, label


def split_dataset(x):
    test_size = int(len(x) * test_percent)
    return x[test_size:len(x)], x[0:test_size]


def prepare_dataset(x, y):
    assert(len(x) == len(y))
    dx = tf.data.Dataset.from_tensor_slices(np.array(x)).shuffle(len(x))
    dy = tf.data.Dataset.from_tensor_slices(np.array(y)).shuffle(len(y))
    dcomb = tf.data.Dataset.zip((dx, dy)).batch(len(x))
    encoder.adapt(dcomb.map(lambda text, label: text))
    return dcomb.map(vectorize_text)


def save_plot_accuracy(log, filename, title="model accuracy"):
    plt.plot(log.history['accuracy'])
    plt.plot(log.history['val_accuracy'])
    plt.title(title)
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'val'], loc='upper left')
    plt.savefig(f'plots/{filename}.png')


if __name__ == '__main__':
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    dataset = GithubDataset('python', 900, 'memory', 5)
    x_train, y_train = dataset.load_from_file("output\\dataset_all_v2.csv")
    x_train, x_test = split_dataset(x_train)
    y_train, y_test = split_dataset(y_train)

    train = prepare_dataset(x_train, y_train)
    test = prepare_dataset(x_test, y_test)
    # valu, label = next(iter(train))
    # for i in range(len(valu)):
        # print(valu[i])

    #model = create_base_model(linear_mod)
    model = create_base_model(add_mlp_layers2, encoder)
    # model = create_base_model(add_mlp_layers)
    # model = create_base_model(add_lstm_layers)

    # forest = create_base_model(forest_mod)
    logs = train_model(model, train, test)
    save_plot_accuracy(logs, "mlp2Adam2")
