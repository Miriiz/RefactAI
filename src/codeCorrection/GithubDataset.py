import time

import requests
import pandas as pd
import csv
from define import github_token
from tqdm import tqdm
from datetime import datetime, timedelta


# issue
class GithubDataset:
    def __init__(self, language, number_of_repo, searching_words, day_since, today_remove=0):
        self.headers = {'Authorization': f'token {github_token}'}
        self.language = language
        self.number_of_repo = number_of_repo
        self.searching_words = searching_words
        self.data = []
        self.page = 1
        self.day_since = day_since
        self.repo_per_page = 20
        self.today_remove = today_remove
        if number_of_repo < 20:
            self.repo_per_page = number_of_repo

    def load_commits(self, start_at=1):
        i = 0
        self.page = start_at

        number_of_pages = int(self.number_of_repo / self.repo_per_page)
        for i in tqdm(range(number_of_pages)):
            commits = self.get_all_commits(self.page)
            for commit in commits:
                detailed_commit = self.get_commit(commit['repository']['owner']['login'], commit['repository']['name'], commit['sha'])
                if detailed_commit is None:
                    print("commit not found")
                    continue
                for file in detailed_commit['files']:
                    if 'patch' in file:
                        #if 'def' not in file['patch']:
                         #   continue
                        data_before, data_after = self.clear_file_content(file['patch'])
                        self.data.append(
                            ["KO", str(self.page), commit['repository']['owner']['login'], commit['repository']['name'], commit['sha'],
                             commit['commit']['message'], data_before])
                        self.data.append(
                            ["OK", str(self.page), commit['repository']['owner']['login'], commit['repository']['name'], commit['sha'],
                             commit['commit']['message'], data_after])
            self.page += 1

    def load_from_commits(self, start_at=1):
        i = 0
        self.page = start_at

        number_of_pages = int(self.number_of_repo / self.repo_per_page)
        for i in tqdm(range(number_of_pages)):
            repos = self.get_all_repo(self.page)
            for repo in repos:
                commits = self.get_all_commits(repo['owner']['login'], repo['name'])

                if not isinstance(commits, list):
                    print("commits not found")
                    continue
                for commit in commits:
                    can_get_commit = True
                    for searching_word in self.searching_words:
                        if searching_word not in commit['commit']['message']:
                            can_get_commit = False

                    if can_get_commit:
                        detailed_commit = self.get_commit(repo['owner']['login'], repo['name'], commit['sha'])
                        if detailed_commit is None:
                            continue
                        for file in detailed_commit['files']:
                            if 'patch' in file:
                                data_before, data_after = self.clear_file_content(file['patch'])
                                self.data.append(
                                    ["KO", str(self.page), repo['owner']['login'], repo['name'], commit['sha'],
                                     commit['commit']['message'], data_before])
                                self.data.append(
                                    ["OK", str(self.page), repo['owner']['login'], repo['name'], commit['sha'],
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
        today = datetime.today() - timedelta(days=self.today_remove)
        data = {'items': []}
        i = 0
        while until < today:
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

    def get_all_commits(self, page):
        # On peut monter plus haut si on veut + de repos ( jusqu'a 365 mais un des repos pose problème )
        since = datetime.today() - timedelta(days=self.day_since)  # X jours en arriere
        until = since + timedelta(days=1)  # X + 1 jour en arriere
        today = datetime.today() - timedelta(days=self.today_remove)
        data = {'items': []}
        i = 0
        print("+".join(self.searching_words))
        while until < today:
            url = f'https://api.github.com/search/commits?q=message:{"+".join(self.searching_words)} committer-date:SINCE..UNTIL&order' \
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
        return data['items']

    def get_repo(self, owner, name):
        url = f'https://api.github.com/repos/{owner}/{name}'
        r = requests.get(url, headers=self.headers)
        r.raise_for_status()
        data = r.json()
        return data

    def get_all_commits(self, owner, name):
        url = f'https://api.github.com/repos/{owner}/{name}/commits'
        r = requests.get(url, headers=self.headers)
        try:
            r.raise_for_status()
            data = r.json()
            return data
        except requests.exceptions.HTTPError:
            print(f"commits not found")
            return None

    def get_commit(self, owner, name, commit_sha):
        url = f'https://api.github.com/repos/{owner}/{name}/commits/{commit_sha}'
        r = requests.get(url, headers=self.headers)
        try:
            r.raise_for_status()
            data = r.json()
            return data
        except requests.exceptions.HTTPError:
            print(f"commit {commit_sha} not found")
            return None

    # Récupérer tous les fichiers
    # https://api.github.com/repos/chriskiehl/Gooey/contents
    def get_repo_files(self, owner, name):
        return

    # -> url : Récupérer un fichier
    # https://api.github.com/repos/chriskiehl/Gooey/contents/pip_deploy.py?ref=master
    # -> git_url : https://api.github.com/repos/chriskiehl/Gooey/git/blobs/3a8710f0319f5d8ad3bf1199906bb4958781dfda

    # issues https://api.github.com/repos/chriskiehl/Gooey/issues
    # https://api.github.com/repos/chriskiehl/Gooey/issues/816 /
    # https://api.github.com/repos/chriskiehl/Gooey/issues/816/comments compare
    # https://api.github.com/repos/chriskiehl/Gooey/compare/4990377cc32fabcfc047a5b543625875f247724d
    # ...be4b11b8f27f500e7326711641755ad44576d408
    def save(self, location):
        with open(location, 'w', newline='', encoding="utf-8") as saving_file:
            writer = csv.writer(saving_file, delimiter=';')
            writer.writerow(['Label', 'Page', 'Username', 'Repo', 'Commit', 'Bug', 'Code'])
            for data in self.data:
                writer.writerow(data)

    def load_from_file(self, location):
        file = open(location, encoding="utf-8")
        csvreader = csv.DictReader(file, delimiter=';')
        # header = next(csvreader)
        result = {}
        x_train = []
        y_train = []
        for row in csvreader:
            for column, value in row.items():
                result.setdefault(column, []).append(value)
        file.close()
        indices_without_labels = []
        it = 0
        for label in result['Label']:
            if label == 'OK':
                y_train.append(1)
            elif label == 'KO':
                y_train.append(0)
            else:
                indices_without_labels.append(it)
            it += 1
        it = 0
        for code in result['Code']:
            if it not in indices_without_labels:
                x_train.append(code)
            it += 1
        return x_train, y_train

    def clean_code_from_file(self, location):
        file = open(location, encoding="utf-8")
        csvreader = csv.DictReader(file, delimiter=';')
        # header = next(csvreader)
        result = {}
        for row in csvreader:
            for column, value in row.items():
                result.setdefault(column, []).append(value)
        file.close()

        clean_code = []
        for code in result['Code']:
            code_array = code.split("\n")
            clean_code_array = []
            for line_code in code_array:
                new_line = list(line_code)
                if len(new_line) != 0:
                    if new_line[0] == '-' or new_line[0] == '+':
                        new_line[0] = ' '
                    elif new_line[0] == '@':
                        start_indice = line_code.find("@@", 4, len(line_code)) + 3
                        new_line = new_line[start_indice:]

                clean_code_array.append(''.join(new_line))
            clean_code.append('\n'.join(clean_code_array))

        data = []
        for i in range(len(result['Username'])):
            data.append([result['Label'][i], result['Page'][i], result['Username'][i], result['Repo'][i],
                         result['Commit'][i], result['Bug'][i], clean_code[i]])

        with open(location, 'w', newline='', encoding="utf-8") as saving_file:
            writer = csv.writer(saving_file, delimiter=';')
            writer.writerow(['Label', 'Page', 'Username', 'Repo', 'Commit', 'Bug', 'Code'])
            for d in data:
                writer.writerow(d)


# dataset = GithubDataset('python', 900, ['memory', 'error'], 100, 90)
# dataset.clean_code_from_file('output\\dataset_all_v2.csv')

j = 4
for i in range(0, 100, 10):
     dataset = GithubDataset('python', 50, ['memory', 'error', 'python'], 10 + i, 0 + i)
     dataset.load_from_commits()
     dataset.save('output\\dataset_{j}.csv'.format(j=j))
     j += 1

# x = []
# for i in range(1, 10):
#     x.append('output\\dataset_{i}.csv'.format(i=i))
#
# li = []
# x.append('output\\dataset_all.csv')
# for filename in x:
#     df = pd.read_csv(filename, index_col=None, sep=";", header=0)
#     li.append(df)
#
# frame = pd.concat(li, axis=0, ignore_index=True)
# # check pd doublon
# frame.drop_duplicates(inplace=True)
# frame.to_csv('output\\dataset_all_v2.csv', sep=';', index=False)
