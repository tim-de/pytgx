#!/usr/bin/python

import tgxread
import argparse

if __name__ == "__main__":
    cmdparse = argparse.ArgumentParser(description="Unpack a .TGX asset archive file")
    
    cmdparse.add_argument("filename", type=str, nargs="?", default="",
                          help="The path to a .tgx file to unpack")
    cmdparse.add_argument("-o", "--outfile", nargs="?", required=False, default="", dest= "outfile",
                          help="The name of the directory to store the output")
    cmdparse.add_argument("-v", "--verbose", action="store_true", required=False, default=False, dest="verbose",
                               help="Display information about the extraction")

    args = cmdparse.parse_args()
    
    if args.filename == "":
        cmdparse.print_usage()
        exit()
    tgxhdr = tgxread.Header()
    tgxhdr.parsefile(args.filename, args.verbose)
    tgxhdr.dump(args.outfile, args.verbose)
