#!/usr/bin/python

import struct

class TgxFileIdentifier:
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
    
class TgxSubFile:
    filepath = ""
    checksum = 0
    filelen = 0
    startoffset = 0
    endoffset = 0

    def __init__(self, buf):
        self.ident = TgxFileIdentifier()
        (bytepath,
         self.checksum,
         self.filelen,
         self.ident.low, self.ident.high) = struct.unpack("80s I I II 8x", buf)
        self.filepath = bytepath.decode('ascii')

    def __str__(self):
        return f'\
        path => {self.filepath}\n\
        checksum => 0x{self.checksum:04x}\n\
        length => {self.filelen}\n\
        ident => {self.ident}\n\
        start => 0x{self.startoffset:04x}, end => 0x{self.endoffset:04x}\n'

class TgxLenSpec:
    length = 0

    def __init__(self, buf):
        self.ident = TgxFileIdentifier()
        (self.length,
         self.ident.low, self.ident.high) = struct.unpack("8x I II", buf)
        
class TgxHeader:
    version = 0
    checksum = 0
    filelen = 0
    filecount = 0
    subfiles = {}
    def parsefile(self, filename):
        with open(filename, mode="rb") as fh:
            buf = fh.read(116)
            #print(buf)
            (self.version,
             self.checksum,
             self.filelen,
             self.filecount) = struct.unpack("12x I I I 40x I 48x", buf)
            for index in range(self.filecount):
                buf = fh.read(104)
                tempsubfilehdr = TgxSubFile(buf)
                self.subfiles[tempsubfilehdr.ident]=tempsubfilehdr

            lengthspecs = []
            for index in range(self.filecount):
                buf = fh.read(20)
                lengthspecs.append(TgxLenSpec(buf))
                
            for lspec in lengthspecs:
                buf = fh.read(8)
                (self.subfiles[lspec.ident].startoffset,
                 self.subfiles[lspec.ident].endoffset) = struct.unpack("I I", buf)

if __name__ == "__main__":
    infile = "/home/timot/.wine/drive_c/Program Files (x86)/Kohan Ahrimans Gift/Terst.tgx"
    tgxhdr = TgxHeader()
    tgxhdr.parsefile(infile)
    print(tgxhdr.version, tgxhdr.filelen, tgxhdr.filecount)
    for index in tgxhdr.subfiles:
        print(index)
        print(tgxhdr.subfiles[index])
