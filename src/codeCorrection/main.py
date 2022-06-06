from GithubDataset import GithubDataset
from Model import *

if __name__ == '__main__':
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

    '''
    dataset = GithubDataset('python', 100, 'memory')
    print(dataset.load_commits())
    dataset.save("output\\test2.csv")
    '''
    model_linear = create_base_model(linear_mod)

    # model_mlp = create_base_model(add_mlp_layers)
