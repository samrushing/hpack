HPACK
=====

An implementation of [HPACK](http://http2.github.io/http2-spec/compression.html) in Python/Cython.

Status
------

Decoder works.  Encoder works, but does not yet make use of the
DynamicTable.  This code is being tested with shrapnel's h2 server.

Purpose
-------

I plan on writing a fast implementation in Cython for
[Shrapnel](https://github.com/ironport/shrapnel).  The python code is
a prototype for that code.  Hopefully the result (and ASCII huffman
table) are simple enough that people can translate it to C/C++ without
too much trouble.
