#!/usr/bin/env /usr/bin/python3
# -*- coding: utf-8 -*-

def init():
  global GIT_CMD_ALIASES
  GIT_CMD_ALIASES = {
    "g": "git",
    "ga": "git add",
    "gb": "git branch",
    "gbD": "git branch -D",
    "gc": "git clone",
    "gcan": "git commit --amend --no-edit",
    "gcb": "git checkout -b",
    "gd": "git diff",
    "gf": "git fetch",
    "gl": "git log --oneline -5",
    "gst": "git status",
  }
