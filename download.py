#!/usr/bin/env python3

import gzip
import re
import sys
from pathlib import Path

import github


def get_repos(input: str) -> list:
    repos = set()
    pattern = re.compile("github.com/([a-zA-Z0-9]+)/([a-zA-Z0-9-]+)")
    for file in Path(input).glob("abstract-github.com-set.*.txt.gz"):
        with gzip.open(file, "rt", encoding="utf-8") as f:
            findall = pattern.findall(f.read())
            repos.update(set(findall))
    return sorted(list(repos))


def download_repos(user, password, repos: set, output: str) -> None:
    g = github.Github(auth=github.Auth.Login(user, password))
    with open(output, "w") as f:
        for i, (author, name) in enumerate(repos, start=1):
            print(i, author, name)
            try:
                repo = g.get_repo(author + "/" + name)
            except github.UnknownObjectException:
                continue
            print(author,
                  name,
                  repo.stargazers_count,
                  repo.created_at,
                  repo.updated_at,
                  repo.language,
                  repo.description,
                  sep="\t",
                  file=f,
                  flush=True)


def main(user, password):
    repos = get_repos("data/")
    download_repos(user, password, repos, "repos.txt")


if __name__ == "__main__":
    user, password = sys.argv[1:]
    main(user, password)
