from GithubDataset import GithubDataset
from Model import *

#Code Correction
#0 Créer un énorme dataset + améliorer la récupération (memory, error)
#1 Modeles
#2 vérifier les commentaires sur du code -> Créer un dataset + modèles
#3 rapport permettant d'identifier les bugs et de rajouter une ligne sur le code

#Lier les 2 rapports?

#Documentation -> améliorer le format
if __name__ == '__main__':
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    dataset = GithubDataset('python', 900, 'memory', 5)
    x_train, y_train = dataset.load_from_file("output\\test.csv")
    print(x_train)
    print(y_train)

    model_linear = create_base_model(linear_mod)
    train_model(model_linear, x_train, y_train)

    #model_mlp = create_base_model(add_mlp_layers)


