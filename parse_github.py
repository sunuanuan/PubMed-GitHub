#!/usr/bin/env python3

import sys

import github


def get_repos(input: str) -> list:
    repos = []
    with open(input) as f:
        for line in f:
            author, name, pmids = line.strip().split("\t")
            repos.append((author, name, pmids))
    return repos


def download_repos(user, password, repos: set, output: str) -> None:
    g = github.Github(auth=github.Auth.Login(user, password))
    with open(output, "w") as f:
        for i, (author, name, pmids) in enumerate(repos, start=1):
            print(i, author, name)
            try:
                repo = g.get_repo(author + "/" + name)
            except github.UnknownObjectException:
                continue
            print(author, name, pmids, repo.stargazers_count, repo.language, repo.description, sep="\t", file=f, flush=True)


def main(user, password):
    repos = get_repos("repo_pubmed.txt")
    download_repos(user, password, repos, "repo_github.txt")


if __name__ == "__main__":
    user, password = sys.argv[1:]
    main(user, password)
