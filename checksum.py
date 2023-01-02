#!/usr/bin/pypy3

import struct

def checksum_32(filename, blocksize=2048):
    blocksize += blocksize % 4 # ensure blocks are 32 bit aligned
    eof = False
    checksum = 0
    with open(filename, "rb") as infilehandle:
        while not eof:
            buf = infilehandle.read(blocksize)
            if len(buf) < blocksize:
                # if buf is shorter than blocksize then we've reached the end of the file
                blocksize = len(buf)
                if blocksize < 4:
                    if blocksize == 0:
                        break
                    buf += b'\0' * (4 - blocksize)
                else:
                    buf += b'\0' * (blocksize % 4) # ensure buf is 32 bit aligned
                eof = True
            u32vals = struct.unpack("<{0}I".format(blocksize//4), buf)
            for u32value in u32vals:
                checksum ^= u32value
    return(checksum)

if __name__ == "__main__":
    print("0x{0:08x}".format(checksum_32("/home/timot/.wine/drive_c/Program Files (x86)/Kohan Ahrimans Gift/Kohan_AG.tgw"), 512))
