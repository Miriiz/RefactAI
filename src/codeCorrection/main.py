from GithubDataset import GithubDataset
from  Model import  *

if __name__ == '__main__':
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

    # dataset = GithubDataset('python', 100)
    # print(dataset.get_all_repo_2())
    model_linear = create_base_model(linear_mod)
    model_mlp = create_base_model(add_mlp_layers)
