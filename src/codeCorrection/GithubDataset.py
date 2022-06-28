import time
import requests
import pandas as pd
import csv
from define import github_token
from tqdm import tqdm
from datetime import datetime, timedelta


def load_github_dataset(location):
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


def clean_line(line):
    new_line = list(line)
    if len(new_line) != 0:
        if new_line[0] == '-' or new_line[0] == '+':
            new_line[0] = ' '
        elif new_line[0] == '@':
            start_indice = line.find("@@", 4, len(line)) + 3
            new_line = new_line[start_indice:]

    return ''.join(new_line)


def clear_file_content(file_content):
    content_file_before = []
    content_file_after = []
    start_indice = file_content.find("@@", 4, len(file_content)) + 3
    for line in file_content[start_indice:].split('\n'):
        if line[0] == '+':
            content_file_after.append(clean_line(line))
        elif line[0] == '-':
            content_file_before.append(clean_line(line))
        else:
            content_file_after.append(clean_line(line))
            content_file_before.append(clean_line(line))
    return '\n'.join(content_file_before), '\n'.join(content_file_after)


class GithubDataset:
    def __init__(self, searching_words):
        self.headers = {'Authorization': f'token {github_token}'}
        self.searching_words = searching_words
        self.data = []

    def load_from_commits(self, number_of_month, start_year=2001):
        for month in tqdm(range(number_of_month)):
            commits = self.get_all_commits_from(month, start_year)
            for commit in commits:
                detailed_commit = self.get_commit(commit['repository']['owner']['login'], commit['repository']['name'],
                                                  commit['sha'])
                if detailed_commit is None:
                    continue
                for file in detailed_commit['files']:
                    if 'patch' in file:
                        # if 'def' not in file['patch']:
                        #   continue
                        data_before, data_after = clear_file_content(file['patch'])
                        self.data.append(
                            ["KO", commit['repository']['owner']['login'], commit['repository']['name'],
                             commit['sha'],
                             commit['commit']['message'], data_before])
                        self.data.append(
                            ["OK", commit['repository']['owner']['login'], commit['repository']['name'],
                             commit['sha'],
                             commit['commit']['message'], data_after])

    def get_all_commits_from(self, month_passed, year_start):
        # On peut monter plus haut si on veut + de repos ( jusqu'a 365 mais un des repos pose problème )
        since = datetime.strptime(f'{str(year_start)}-01-01', '%Y-%m-%d') + timedelta(days=30*month_passed) # X jours en arriere
        until = since + timedelta(days=30)  # X + 1 jour en arriere
        data = {'items': []}

        for page in range(1, 21):
            url = f'https://api.github.com/search/commits?q=message:{"+".join(self.searching_words)} committer-date:SINCE..UNTIL&order' \
                  f'=desc&page={page}' \
                  f'&per_page={50}'
            url = url.replace('SINCE', since.strftime('%Y-%m-%dT%H:%M:%SZ')).replace('UNTIL', until.strftime(
                '%Y-%m-%dT%H:%M:%SZ'))
            r = requests.get(url)
            r.raise_for_status()
            tmp = r.json()

            if len(tmp["items"]) == 0:
                break
            if page == 1:
                data = {**data, **tmp}
            else:
                data["items"].extend(tmp["items"])
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
            print(f"commit {owner}/{name}/commits/{commit_sha} not found")
            return None

    def save(self, location):
        with open(location, 'w', newline='', encoding="utf-8") as saving_file:
            writer = csv.writer(saving_file, delimiter=';')
            writer.writerow(['Label', 'Username', 'Repo', 'Commit', 'Bug', 'Code'])
            for data in self.data:
                writer.writerow(data)


# dataset = GithubDataset('python', 900, ['memory', 'error'], 100, 90)
# dataset.clean_code_from_file('output\\dataset_all_v2.csv')

starting_year = 2002
end_year = starting_year + 1
for year in range(starting_year, end_year):
    dataset = GithubDataset(['memory', 'error', 'python'])
    dataset.load_from_commits(4, year)
    dataset.save(f'output\\dataset_{year}.csv')

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
