#!/usr/bin/python

import tgxread

if __name__ == "__main__":
    infilename = "/home/timot/.wine/drive_c/Program Files (x86)/Kohan Ahrimans Gift/Kohan_AG.tgw"
    tgxhdr = tgxread.Header()
    tgxhdr.parsefile(infilename)
    tgxhdr.dump()
