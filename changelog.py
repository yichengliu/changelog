#!/usr/bin/env python3
from git import Repo
import sys
import os
import argparse
import re

parser = argparse.ArgumentParser(description='Generate change log')
parser.add_argument('f', metavar='from_tag', type=str, help='from tag')
parser.add_argument('t', metavar='to_tag', type=str, help='to tag')
parser.add_argument('--markdown', dest='markdown', action='store_true', help='enable markdown for ticket number')
parser.set_defaults(markdown=False)


args = parser.parse_args()

commit_map = []

def bfs(commit, adding):
    q = [commit]
    visited = []

    while (q):
        top = q.pop(0)

        if adding:
            commit_map.append(top)
        else:
            commit_map.remove(top)

        for p in top.parents:
            if p not in visited:
                q.append(p)
                visited.append(p)

repo = Repo(os.getcwd())

assert not repo.bare

new = repo.commit(args.t)
old = repo.commit(args.f)

bfs(new, True)
bfs(old, False)

for node in commit_map:
    message = node.message
    print('* ' + message.replace('\n', ''))
