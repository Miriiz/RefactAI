from GithubDataset import GithubDataset
from Model import *
import numpy as np
import tensorflow as tf

from tensorflow.keras import layers

#Code Correction
#0 Créer un énorme dataset sur numpy
#1 Modeles

#Rapport
#rapport permettant d'identifier les bugs et de rajouter une ligne
#Table des matières
#Memory error


def custom_standardization(input_data):
    return tf.strings.lower(input_data)


if __name__ == '__main__':
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    dataset = GithubDataset('python', 900, 'memory', 5)
    x_train, y_train = dataset.load_from_file("output\\dataset_all.csv")
    print(x_train[0])

    model_linear = create_base_model(linear_mod)
    '''
    max_features = 10000
    sequence_length = 250
    vectorize_layer = layers.experimental.preprocessing.TextVectorization(
        standardize=custom_standardization,
        max_tokens=max_features,
        output_mode='int',
        output_sequence_length=sequence_length)
    print(vectorize_layer(x_train[0]))
    '''
    VOCAB_SIZE = 1000
    x = tf.data.Dataset.from_tensor_slices(np.array(x_train))

    encoder = layers.experimental.preprocessing.TextVectorization(
        max_tokens=VOCAB_SIZE)
    encoder.adapt(x.map(lambda text, label: text))

    train_model(model_linear, x_train, y_train)

    #model_mlp = create_base_model(add_mlp_layers)


