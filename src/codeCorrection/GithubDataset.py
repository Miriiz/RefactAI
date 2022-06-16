import time

import requests
import csv
from define import github_token
from tqdm import tqdm
from datetime import datetime, timedelta


# issue
class GithubDataset:
    def __init__(self, language, number_of_repo, searching_word, day_since):
        self.headers = {'Authorization': f'token {github_token}'}
        self.language = language
        self.number_of_repo = number_of_repo
        self.searching_word = searching_word
        self.data = []
        self.page = 1
        self.day_since = day_since
        self.repo_per_page = 20
        if number_of_repo < 20:
            self.repo_per_page = number_of_repo

    def load_commits(self, start_at=1):
        i = 0
        self.page = start_at
        number_of_pages = int(self.number_of_repo / self.repo_per_page)
        for i in tqdm(range(number_of_pages)):
            repos = self.get_all_repo(self.page)
            for repo in repos:
                commits = self.get_all_commits(repo['owner']['login'], repo['name'])
                if isinstance(commits, list):
                    continue
                for commit in commits:
                    if self.searching_word in commit['commit']['message']:
                        detailed_commit = self.get_commit(repo['owner']['login'], repo['name'], commit['sha'])
                        for file in detailed_commit['files']:
                            if 'patch' in file:
                                data_before, data_after = self.clear_file_content(file['patch'])
                                self.data.append(["KO", str(self.page), repo['owner']['login'], repo['name'], commit['sha'],
                                                  commit['commit']['message'], data_before])
                                self.data.append(["OK", str(self.page), repo['owner']['login'], repo['name'], commit['sha'],
                                                  commit['commit']['message'], data_after])
            self.page += 1

    def clear_file_content(self, file_content):
        content_file_before = []
        content_file_after = []
        start_indice = file_content.find("@@", 4, len(file_content)) + 3
        for line in file_content[start_indice:].split('\n'):
            if line[0] == '+':
                content_file_after.append(line)
            elif line[0] == '-':
                content_file_before.append(line)
            else:
                content_file_after.append(line)
                content_file_before.append(line)
        return '\n'.join(content_file_before), '\n'.join(content_file_after)

    def get_all_repo(self, page):
        # On peut monter plus haut si on veut + de repos ( jusqu'a 365 mais un des repos pose problème )
        since = datetime.today() - timedelta(days=self.day_since)  # X jours en arriere
        until = since + timedelta(days=1)  # X + 1 jour en arriere
        today = datetime.today()   # X + 1 jour en arriere
        data = {'items': []}
        i = 0
        while tqdm(until < today):
            url = f'https://api.github.com/search/repositories?q=language:{self.language} created:SINCE..UNTIL&order' \
                  f'=desc&page={page}' \
                  f'&per_page={self.repo_per_page}'
            url = url.replace('SINCE', since.strftime('%Y-%m-%dT%H:%M:%SZ')).replace('UNTIL', until.strftime(
                '%Y-%m-%dT%H:%M:%SZ'))
            r = requests.get(url)
            r.raise_for_status()
            tmp = r.json()
            if i == 0:
                data = {**data, **tmp}
                i += 1
            else:
                data["items"].extend(tmp["items"])
            since = until
            until = since + timedelta(days=1)
            time.sleep(10)

        return data['items']

    def get_all_repo_2(self, page):
        url = f'https://api.github.com/legacy/repos/search/Python?language={self.language}&page={page}&per_page=20'
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

    # Récupérer tous les fichiers
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
        with open(location, 'w', newline='', encoding="utf-8") as saving_file:
            writer = csv.writer(saving_file, delimiter=';')
            writer.writerow(['Label', 'Page', 'Username', 'Repo', 'Commit', 'Bug', 'Code'])
            for data in self.data:
                writer.writerow(data)

    def load_from_file(self, location):
        file = open(location)
        csvreader = csv.reader(file)
        header = next(csvreader)
        rows = []
        for row in csvreader:
            rows.append(row)
        file.close()
        return rows


dataset = GithubDataset('python', 900, 'memory', 60)
dataset.load_commits()
dataset.save("output\\test4.csv")
# print(dataset.load_from_file("output\\memory.csv"))

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
