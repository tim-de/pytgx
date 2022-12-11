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
    
class TgxSubFile:
    filepath = ""
    checksum = 0
    filelen = 0
    ident = TgxFileIdentifier()
    startoffset = 0
    endoffset = 0

    def __init__(self, buf):
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
    ident = TgxFileIdentifier()
    length = 0

    def __init__(self, buf):
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
                self.subfiles[str(TgxSubFile(buf).ident)]=TgxSubFile(buf)
                print(TgxSubFile(buf))

            for ident in self.subfiles:
                print(ident, self.subfiles[ident])
            lengthspecs = []
            for index in range(self.filecount):
                buf = fh.read(20)
                templspec = TgxLenSpec(buf)
                print(str(templspec.ident))
                lengthspecs.append(templspec)
            print([str(lspec.ident) for lspec in lengthspecs])
                
            for lspec in lengthspecs:
                print(lspec.length, lspec.ident)
                ident = str(lspec.ident)

                buf = fh.read(8)
                (self.subfiles[ident].startoffset,
                 self.subfiles[ident].endoffset) = struct.unpack("I I", buf)

if __name__ == "__main__":
    infile = "/home/timot/.wine/drive_c/Program Files (x86)/Kohan Ahrimans Gift/Terst.tgx"
    tgxhdr = TgxHeader()
    tgxhdr.parsefile(infile)
    print(tgxhdr.version, tgxhdr.filelen, tgxhdr.filecount)
    for ix in tgxhdr.subfiles:
        print(ix)
        print(tgxhdr.subfiles[ix])
