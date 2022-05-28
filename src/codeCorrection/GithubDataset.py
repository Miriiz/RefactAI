import base64
import json
import requests
import os


class GithubDataset():
    def __init__(self, language, number_of_repo):
        self.authentification()
        self.language = language
        self.number_of_repo = number_of_repo

    def authentification(self):
        return

    # Récupération des repos publics en python
    # https://api.github.com/legacy/repos/search/Python?language=Python&page=1&per_page=100
    # https://api.github.com/search/repositories?q=language:python&order=desc
    def get_all_repo(self):
        url = f'https://api.github.com/search/repositories?q=language:{self.language}&order=desc'
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()
        return data['repositories']

    def get_all_repo_2(self):
        url = f'https://api.github.com/legacy/repos/search/Python?language=Python&page=1&per_page=100'
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()
        return data['repositories']

    # Contenu d'un repo
    # https://api.github.com/repos/chriskiehl/Gooey
    def get_repo(self, owner, name):
        return

    # Récupérer tout les fichiers
    # https://api.github.com/repos/chriskiehl/Gooey/contents
    def get_repo_files(self, owner, name):
        return

    # -> url : Récupérer un fichier
    # https://api.github.com/repos/chriskiehl/Gooey/contents/pip_deploy.py?ref=master
    # -> git_url : https://api.github.com/repos/chriskiehl/Gooey/git/blobs/3a8710f0319f5d8ad3bf1199906bb4958781dfda

    # commits
    # https://api.github.com/repos/chriskiehl/Gooey/commits

    # issues
    # https://api.github.com/repos/chriskiehl/Gooey/issues
    # https://api.github.com/repos/chriskiehl/Gooey/issues/816 / https://api.github.com/repos/chriskiehl/Gooey/issues/816/comments


'''
def github_read_file(username, repository_name, file_path, github_token=None):
    headers = {}
    if github_token:
        headers['Authorization'] = f"token {github_token}"

    url = f'https://api.github.com/repos/%7Busername%7D/%7Brepository_name%7D/contents/%7Bfile_path%7D'
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    data = r.json()
    file_content = data['content']
    file_content_encoding = data.get('encoding')
    if file_content_encoding == 'base64':
        file_content = base64.b64decode(file_content).decode()

    return file_content


def main():
    github_token = os.environ['GITHUB_TOKEN']
    username = 'airbnb'
    repository_name = 'javascript'
    file_path = 'package.json'
    file_content = github_read_file(username, repository_name, file_path, github_token=github_token)
    data = json.loads(file_content)
    print(data['name'])
'''