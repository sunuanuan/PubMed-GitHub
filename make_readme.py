#!/usr/bin/env python3

import math
from collections import defaultdict

template = """# PubMed-GitHub

A collection of GitHub repositories that in PubMed abstract.

## Top 20 Authors

| Rank | Author | Count | Stars | Score |
| ---: | -----: | ----: | ----: | ----: |
{top20_authors_text}

***Note: only count repositories with stars not less than top 1000 threshold ({top1000_stars}).***

## Top 1000 Repositories

***Format: description, language, created date, updated date.***

{top1000_repos_text}

"""


def get_top1000_repos(file):
    repos = []
    header = ["author", "name", "pmids", "stars", "language", "description"]
    with open(file) as f:
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
        pmids = "; ".join(f"[{pmid}](https://pubmed.ncbi.nlm.nih.gov/{pmid})" for pmid in repo["pmids"].split(";"))
        row.append(f"{i}. [{author}/{name}](https://github.com/{author}/{name}) (⭐{stars} · {language})")
        row.append(f"{description} ({pmids})")
        rows.append(" ".join(row))
    text = "\n".join(rows)
    return text


def main(input, output):
    top1000_repos, top1000_stars = get_top1000_repos(input)
    top20_authors = get_top20_authors(top1000_repos)
    top20_authors_text = get_to20_authors_text(top20_authors)
    top1000_repos_text = get_top1000_repos_text(top1000_repos)
    with open(output, "w") as f:
        f.write(template.format(
            top1000_stars=top1000_stars,
            top20_authors_text=top20_authors_text,
            top1000_repos_text=top1000_repos_text,
        ))


if __name__ == "__main__":
    main("repo_github.txt", "README.md")
