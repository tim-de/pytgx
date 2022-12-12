#!/usr/bin/python

import tgxread
import argparse

if __name__ == "__main__":
    cmdparse = argparse.ArgumentParser(description="Unpack a .TGX asset archive file")
    
    cmdparse.add_argument("filename", type=str, nargs="?", default="",
                          help="The path to a .tgx file to unpack")
    cmdparse.add_argument("-o", "--outfile", nargs="?", required=False, default="", dest= "outfile",
                          help="The name of the directory to store the output")
    
    verbage = cmdparse.add_mutually_exclusive_group()
    verbage.add_argument("-v", "--verbose", action="store_const", required=False, const=2, default=1, dest="verbosity",
                          help="Display more information about the extracted files")
    verbage.add_argument("-q", "--quiet", action="store_const", required=False, const=0, default=1, dest="verbosity",
                          help="Suppress console output")

    args = cmdparse.parse_args()
    
    if args.filename == "":
        cmdparse.print_usage()
        exit()
    tgxhdr = tgxread.Header()
    tgxhdr.parsefile(args.filename, args.verbosity)
    tgxhdr.dump(args.outfile, args.verbosity)
