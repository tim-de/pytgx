#!/usr/bin/pypy3

import sys

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
        print("Please provide a path")
        exit(-1)
    path = sys.argv[1]
    num = getNumber(path)
    print(f"{path} => 0x{num:08x}")
