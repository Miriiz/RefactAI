from GithubDataset import GithubDataset

dataset = GithubDataset('python', 100, 'memory')
print(dataset.load_commits())
dataset.save("output\\test2.csv")