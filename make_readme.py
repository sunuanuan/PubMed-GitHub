#!/usr/bin/env python3

import math
from collections import defaultdict
from datetime import date

template = """# PubMed-GitHub

***update {dt}***

A collection of GitHub repositories that appear in PubMed abstract.

## Top 20 Authors

| Rank | Author | Count | Stars | Score |
| ---: | -----: | ----: | ----: | ----: |
{top20_authors_text}

***Note: only count repositories with stars not less than top 1000 threshold ({top1000_stars}).***

## Top 1000 Repositories

***Format: description, language, created date, updated date.***

{top1000_repos_text}

"""


def get_top1000_repos(repo_info_file):
    repos = []
    header = ["author", "name", "stars", "create", "update", "language", "description"]
    with open(repo_info_file) as f:
        for line in f:
            row = line.strip().split("\t")
            cell = dict(zip(header, row))
            cell["stars"] = int(cell["stars"])
            repos.append(cell)
    top1000_repos = sorted(repos, key=lambda x: x["stars"], reverse=True)[:1000]
    top1000_stars = top1000_repos[-1]["stars"]
    return top1000_repos, top1000_stars


def get_top20_authors(repos):
    authors = defaultdict(dict)
    for repo in repos:
        author = repo["author"]
        if author in authors:
            authors[author]["count"] += 1
            authors[author]["stars"] += repo["stars"]
            authors[author]["score"] += math.log2(repo["stars"])
            authors[author]["score"] = round(authors[author]["score"], 2)
        else:
            authors[author]["count"] = 1
            authors[author]["stars"] = repo["stars"]
            authors[author]["score"] = math.log2(repo["stars"])
    return sorted(authors.items(), key=lambda t: t[1]["score"], reverse=True)[:20]


def get_to20_authors_text(authors):
    text = ""
    for rank, (author, cell) in enumerate(authors, start=1):
        score = f"{cell['score']:.2f}"
        text += f"| {rank} | [{author}](https://github.com/{author}) | {cell['count']} | {cell['stars']} | {score} |\n"
    return text


def get_top1000_repos_text(repos):
    rows = []
    for i, repo in enumerate(repos, start=1):
        row = []
        author, name, language, stars, description = repo["author"], repo["name"], repo["language"], repo["stars"], repo["description"]
        create_date = repo["create"].split()[0]
        update_date = repo["update"].split()[0]
        row.append(f"{i}. [{author}/{name}](https://github.com/{author}/{name}) ({stars} stars)")
        row.append(f"{description} ({language}, {create_date}, {update_date})")
        rows.append("\n".join(row))
    text = "\n".join(rows)
    return text


def main():
    top1000_repos, top1000_stars = get_top1000_repos("repos.txt")
    top20_authors = get_top20_authors(top1000_repos)
    top20_authors_text = get_to20_authors_text(top20_authors)
    top1000_repos_text = get_top1000_repos_text(top1000_repos)
    with open("README.md", "w") as f:
        f.write(
            template.format(
                dt=date.today(),
                top1000_stars=top1000_stars,
                top20_authors_text=top20_authors_text,
                top1000_repos_text=top1000_repos_text,
            ))


if __name__ == "__main__":
    main()
