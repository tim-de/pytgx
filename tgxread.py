#!/usr/bin/python

import struct
import os
from pathlib import Path

class FileIdentifier:
    low = 0
    high = 0

    def __str__(self):
        return f'{self.low}.{self.high}'
    
    def __eq__(self, other):
        return self.high == other.high and self.low == other.low
    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.low, self.high))
    
class SubFile:
    filepath = ""
    checksum = 0
    filelen = 0
    startoffset = 0
    endoffset = 0

    def __init__(self, buf):
        self.ident = FileIdentifier()
        (bytepath,
         self.checksum,
         self.filelen,
         self.ident.low, self.ident.high) = struct.unpack("80s I I II 8x", buf)
        self.filepath = Path(bytepath.decode('ascii').replace("\\", "/").replace("\0", ""))

    def __str__(self):
        return f'\
        path => {self.filepath}\n\
        checksum => 0x{self.checksum:04x}\n\
        length => {self.filelen}\n\
        ident => {self.ident}\n\
        start => 0x{self.startoffset:04x}, end => 0x{self.endoffset:04x}\n'

    def dump(self, infilehandle, rootdirname, blocksize=1024):
        writepath = Path(".", rootdirname, self.filepath)
        print(writepath)
        writedir = Path("/".join(writepath.parts[:-1]))
        writedir.mkdir(mode=0o777, parents=True, exist_ok=True)
        infilehandle.seek(self.startoffset)
        position = self.startoffset
        with writepath.open("wb") as outfilehandle:
            while position < self.endoffset:
                if self.endoffset - position < blocksize:
                    blocksize = self.endoffset - position
                buf = infilehandle.read(blocksize)
                outfilehandle.write(buf)
                position += blocksize

class LenSpec:
    length = 0

    def __init__(self, buf):
        self.ident = FileIdentifier()
        (self.length,
         self.ident.low, self.ident.high) = struct.unpack("8x I II", buf)
        
class Header:
    version = 0
    checksum = 0
    filelen = 0
    filecount = 0
    subfiles = {}
    def parsefile(self, filename):
        self.filename = Path(filename.replace("\\", "/"))
        with self.filename.open(mode="rb") as fh:
            buf = fh.read(116)
            #print(buf)
            (self.version,
             self.checksum,
             self.filelen,
             self.filecount) = struct.unpack("12x I I I 40x I 48x", buf)
            for index in range(self.filecount):
                buf = fh.read(104)
                tempsubfilehdr = SubFile(buf)
                self.subfiles[tempsubfilehdr.ident]=tempsubfilehdr

            lengthspecs = []
            for index in range(self.filecount):
                buf = fh.read(20)
                lengthspecs.append(LenSpec(buf))
                
            for lspec in lengthspecs:
                buf = fh.read(8)
                (self.subfiles[lspec.ident].startoffset,
                 self.subfiles[lspec.ident].endoffset) = struct.unpack("I I", buf)

    def dump(self):
        with self.filename.open(mode="rb") as infilehandle:
            basedirname = self.filename.parts[-1].split(".")[0]
            for ident in self.subfiles:
                self.subfiles[ident].dump(infilehandle, basedirname)

if __name__ == "__main__":
    print("This is a library file, intended to be imported by another python program")
