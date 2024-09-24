#!/usr/bin/python3
# -*- coding: utf-8; -*-
"""
Randomly indent block
"""

import shutil
import os.path
from getopt import getopt, GetoptError
from shlex import quote
from typing import Optional
from sys import argv, stdin, stdout, stderr
from random import randrange


help_msg = """\
Usage: evilindent [Option...] [FILE...]
Randomly indent block

Option:
    -i, --in-place      edit files in place
    -b, --backup=<SUFFIX>
                        in place and makes backup
    -h, --help          show this help
    -v, --version       show version
"""

version = "0.1.0"

bak: Optional[str] = None

try:
    optlist, files = getopt(argv[1:], "ib:hv", longopts=[
        "in-place",
        "bak",
        "help",
        "version",
    ])
except GetoptError as e:
    print("Error:", e, file=stderr)
    exit(2)

for opt, arg in optlist:
    match opt:
        case "-i" | "--in-place":
            bak = ""
        case "-b" | "--backup":
            bak = arg
        case "-h" | "--help":
            print(end=help_msg)
            exit()
        case "-v" | "--version":
            print(version)
            exit()


def set_list(lst: list, index: int, elem, default = None) -> None:
    for _ in range(len(lst), index):
        lst.append(default)
    if len(lst) - 1 == index:
        lst[index] = elem
    else:
        assert len(lst) == index, f"{lst=!r}, {index=}, {elem=!r}"
        lst.append(elem)


def get_indent(line: str) -> tuple[int, str]:
    solid = line.lstrip(" \t")
    return len(line) - len(solid), solid


def check_path(path: str) -> None:
    if bak is None and path == "-":
        return

    if not os.path.exists(path):
        print("Error:", f"{quote(path)} file does not exists", file=stderr)
        exit(2)

    if not os.path.isfile(path):
        print("Error:", f"{quote(path)} is not a file", file=stderr)
        exit(2)



def with_out_file(path: str, f):
    if bak is None:
        if path == "-":
            f(stdin, stdout)
        else:
            with open(path) as file:
                f(file, stdout)
        return

    assert isinstance(bak, str), f"{type(bak)=!r}, {bak=!r}"
    bak_path = path + (bak or ".bak")
    shutil.move(path, bak_path)

    with open(bak_path) as file, open(path, "w") as out_file:
        f(file, out_file)

    if not bak:
        os.remove(bak_path)


def run_file(file, out_file) -> None:
    prev_indent = 0
    indent_map = [""]
    for line in file:
        indent, solid = get_indent(line)

        if indent or solid:
            if indent+1 > len(indent_map):
                new_indent = (len(indent_map[prev_indent])
                              + randrange(7) + 1)
                set_list(indent_map, indent, " " * new_indent)

            indent_map[indent+1:] = ()

            prev_indent = indent
        print(indent_map[indent], end=solid, file=out_file)


for path in files:
    check_path(path)
    with_out_file(path, run_file)
