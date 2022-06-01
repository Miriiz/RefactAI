import base64
import json
import requests
import os
import csv
from define import github_token


# issue
class GithubDataset:
    def __init__(self, language, number_of_repo, searching_word):
        self.headers = {'Authorization': f'token {github_token}'}
        self.language = language
        self.number_of_repo = number_of_repo
        self.searching_word = searching_word
        self.data = []
        self.page = 1

    def load_commits(self):
        repos = self.get_all_repo(self.page)
        i = 0
        while i < self.number_of_repo:
            for repo in repos:
                commits = self.get_all_commits(repo['owner']['login'], repo['name'])
                for commit in commits:
                    if self.searching_word in commit['commit']['message']:
                        print("found " + str(len(self.data)))
                        detailed_commit = self.get_commit(repo['owner']['login'], repo['name'], commit['sha'])
                        for file in detailed_commit['files']:
                            self.data.append([repo['owner']['login'], repo['name'], commit['sha'], commit['commit']['message'],
                                              file['patch']])
                i += 1
                if i == self.number_of_repo:
                    break
            self.page += 1

    def get_all_repo(self, page):
        url = f'https://api.github.com/search/repositories?q=language:{self.language}&order=desc&page={page}'
        r = requests.get(url, headers=self.headers)
        r.raise_for_status()
        data = r.json()
        return data['items']

    def get_all_repo_2(self, page):
        url = f'https://api.github.com/legacy/repos/search/Python?language={self.language}&page={page}&per_page=100'
        r = requests.get(url, headers=self.headers)
        r.raise_for_status()
        data = r.json()
        return data['repositories']

    def get_repo(self, owner, name):
        url = f'https://api.github.com/repos/{owner}/{name}'
        r = requests.get(url, headers=self.headers)
        r.raise_for_status()
        data = r.json()
        return data

    def get_all_commits(self, owner, name):
        url = f'https://api.github.com/repos/{owner}/{name}/commits'
        r = requests.get(url, headers=self.headers)
        r.raise_for_status()
        data = r.json()
        return data

    def get_commit(self, owner, name, commit_sha):
        url = f'https://api.github.com/repos/{owner}/{name}/commits/{commit_sha}'
        r = requests.get(url, headers=self.headers)
        r.raise_for_status()
        data = r.json()
        return data

    # Récupérer tout les fichiers
    # https://api.github.com/repos/chriskiehl/Gooey/contents
    def get_repo_files(self, owner, name):
        return

    # -> url : Récupérer un fichier
    # https://api.github.com/repos/chriskiehl/Gooey/contents/pip_deploy.py?ref=master
    # -> git_url : https://api.github.com/repos/chriskiehl/Gooey/git/blobs/3a8710f0319f5d8ad3bf1199906bb4958781dfda

    # issues
    # https://api.github.com/repos/chriskiehl/Gooey/issues
    # https://api.github.com/repos/chriskiehl/Gooey/issues/816 / https://api.github.com/repos/chriskiehl/Gooey/issues/816/comments
    # compare
    # https://api.github.com/repos/chriskiehl/Gooey/compare/4990377cc32fabcfc047a5b543625875f247724d...be4b11b8f27f500e7326711641755ad44576d408
    def save(self, location):
        with open(location, 'w', newline='') as saving_file:
            writer = csv.writer(saving_file)
            writer.writerow(['Username', 'Repo', 'Commit', 'Bug', 'Code'])
            for data in self.data:
                writer.writerow(data)


'''
    url = f'https://api.github.com/repos/%7Busername%7D/%7Brepository_name%7D/contents/%7Bfile_path%7D'
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    data = r.json()
    file_content = data['content']
    file_content_encoding = data.get('encoding')
    if file_content_encoding == 'base64':
        file_content = base64.b64decode(file_content).decode()
'''
