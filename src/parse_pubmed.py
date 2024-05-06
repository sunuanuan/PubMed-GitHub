#!/usr/bin/env python3

import gzip
import re
from collections import defaultdict
from pathlib import Path


def parse_file(file: Path, repos: dict):
    pattern = re.compile("github.com/([a-zA-Z0-9]+)/([a-zA-Z0-9-]+)")
    with gzip.open(file, "rt", encoding="utf-8") as f:
        repo_list = set()
        pmid = journal = "None"
        for line in f:
            line = line.strip()
            if line:
                if line.startswith("PMID- "):
                    pmid = line.replace("PMID- ", "")
                elif line.startswith("JT  - "):
                    journal = line.replace("JT  - ", "")
                else:
                    findall = pattern.findall(line)
                    if findall:
                        repo_list.update(set(findall))
            else:
                for author, name in repo_list:
                    if not journal.startswith(("IEEE", "bioRxiv")):
                        repos[(author, name)].add(pmid)
                repo_list.clear()
                pmid = journal = "None"
        for author, name in repo_list:
            for author, name in repo_list:
                if not journal.startswith("IEEE"):
                    repos[(author, name)].add(pmid)
    return repos


def main(input: str, output: str) -> list:
    repos = defaultdict(set)
    for file in Path(input).glob("pubmed-github.com-set.*.txt.gz"):
        repos = parse_file(file, repos)
    with open(output, "w") as f:
        for (author, name), array in sorted(repos.items()):
            pmids = ";".join([pmid for pmid in sorted(array)])
            print(author, name, pmids, sep="\t", file=f)


if __name__ == "__main__":
    main("../downloads/", "../downloads/repo_pubmed.txt")
