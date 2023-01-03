#!/usr/bin/python

import struct
import os
from pathlib import Path

class FileIdentifier:
    """A class to contain the file index that specifies a file's place within the
    .TGX/.TGW file"""           # Not fully understood as of 01/02/23 --- timoT
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
    """A class to represent a file contained within a .TGX or .TGW archive file"""
    filepath = ""
    checksum = 0
    filelen = 0
    startoffset = 0
    endoffset = 0,

    def __init__(self, buf):
        self.ident = FileIdentifier()
        (bytepath,
         self.checksum,
         self.filelen,
         self.ident.low, self.ident.high,
         self.p1, self.p2) = struct.unpack("80s I I II II", buf)
        self.filepath = Path(bytepath.decode('ascii').replace("\\", "/").replace("\0", ""))
        # Comment out the line above, and uncomment the one below to use the last two words of the
        # filespec to determine the subdirectory rather than the filepath listed in the header.
        #self.filepath = Path(str(self.p1), bytepath.decode('ascii').replace("\0", "").split("\\")[-1])

    def __str__(self):
        return f'\
        path => {self.filepath}\n\
        checksum => 0x{self.checksum:04x}\n\
        length => {self.filelen}\n\
        ident => {self.ident}\n\
        start => 0x{self.startoffset:04x}, end => 0x{self.endoffset:04x}\n'

    def dump(self, infilehandle, rootdirname, blocksize=1024, verbosity=1):
        """ Dump the contents of a subfile into the correct subdirectory under
        'rootdirname', copying 'blocksize' bytes at a time to not use too much
        RAM when copying large files"""
        if verbosity > 0:
            if verbosity == 1:
                printline = f"\rDumping {self.filepath}"
                print(printline + (" " * (80-len(printline))), end="")
            else:
                print(f"Dumping {self.filepath}")
        writepath = Path(".", rootdirname, self.filepath)
        writedir = writepath.parents[0]
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
    # Could probably replace with a function, but what would code in an
    # object-oriented language be without a little class-explosion
    length = 0

    def __init__(self, buf):
        self.ident = FileIdentifier()
        (self.length,
         self.ident.low, self.ident.high) = struct.unpack("8x I II", buf)
        
class Header:
    """A class to represent the header information at the start of
    a .TGX/.TGW file. It contains a dictionary of subfiles, referenced
    by the identifier given to them within the archive file, so that
    their offsets may be correctly retreived from the source file as
    needed."""
    version = 0
    checksum = 0
    filelen = 0
    filecount = 0
    subfiles = {}
    def parsefile(self, filename, verbosity=1):
        self.filename = Path(filename.replace("\\", "/"))
        with self.filename.open(mode="rb") as fh:
            if verbosity > 0:
                print(f"Reading file {self.filename}")
            buf = fh.read(116)
            #print(buf)
            (version,
             self.checksum,
             self.filelen,
             byteshortname,
             self.filecount) = struct.unpack("12x I I I 12x 2s 26x I 48x", buf)
            self.version = unpack_version_number(version)
            self.shortname = byteshortname.decode("ascii")
            if verbosity > 0:
                print(f"Parsed header for {self.filename} ({self.shortname})\nVersion => {self.version}\nChecksum => {self.checksum:08x}\nLength => {self.filelen}B\nSubfiles => {self.filecount}")
                print("Parsing subfile headers")
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
                if verbosity == 2:
                    print(self.subfiles[lspec.ident])
            if verbosity > 0:
                print("All headers parsed")

    def dump(self, basedirname, verbosity=1):
        """Dumps all the subfiles by calling the Subfile.dump method on each of them."""
        with self.filename.open(mode="rb") as infilehandle:
            if basedirname == "":
                basedirname = ".".join(self.filename.parts[-1].split(".")[:-1])
            if verbosity > 0:
                print(f"Dumping {self.filecount} subfiles")
            for ident in self.subfiles:
                self.subfiles[ident].dump(infilehandle, basedirname, verbosity=verbosity)
            if verbosity > 0:
                if verbosity == 1:
                    print("\33[2K\r", end="")
                print("Done!")

def unpack_version_number(packed_version):
    """Unpacks the version number of the file from the form it appears in within the file."""
    unpacked_version = f"{packed_version % 100}"
    packed_version = int(packed_version / 100)
    while packed_version != 0:
        unpacked_version = f"{packed_version % 100}.{unpacked_version}"
        packed_version = int(packed_version / 100)
    return unpacked_version
    
                
if __name__ == "__main__":
    pass
