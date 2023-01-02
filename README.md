# tgxlib

## Tools for working with .TGX game asset files

This is where I intend to document what I can discern
about the .tgx/tgw files used in TimeGate games such as
KIS and KAG.

Currently it's little more than a placeholder, don't hate <3

### FILES:
+ **tgxlib.py**
  This is just a library that contains all the abstractions and
  handles the heavy lifting for finding and accessing the different
  files contained within a .tgx or .tgw file.
+ **tgxdumper.py**
  This takes a path to a .tgx file as argument and extracts all the
  subfiles into a directory, creating a subdirectory structure that
  mirrors the directories given within the header of the source file.
+ **checksum.py**
  Takes a file as argument, and returns the 32-bit XOR checksum of the
  file. This doesn't seem essential as Kohan doesn't seem to care if the
  checksum is valid before loading but I think it's nice to have anyway.
  Slow in its current implementation
  