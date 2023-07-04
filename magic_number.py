#!/usr/bin/pypy3

import sys
import os

def getNumber(path: str) -> int:
    if path == "":
        return 0

    path = path.upper()

    result = ord(path[0]) << 8
    for count, char in enumerate(path[1:]):
        result += ((result >> 4) * ord(char)) + count
        result &= 0xffffffff
    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide at least one path")
        exit(-1)
    pathlist = sys.argv[1:]
    pathlist.sort(key=lambda p: getNumber(p.replace("/", "\\")))
    for path in pathlist:
        num = getNumber(path.replace("/", "\\"))
        length = os.stat(path).st_size
        print(f"{path:15s} \t=> l: 0x{length:08x} id: 0x{num:08x}")
