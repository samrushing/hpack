HPACK
=====

An implementation of [HPACK](http://http2.github.io/http2-spec/compression.html) in Python/Cython.

Status
------

Decoder and encoder work.  The encoder makes use of the dynamic table,
and detects variable headers (like 'Date:') and limits their number of
values to avoid flooding the dynamic table.

There are some requirements around the 'cookie' header I haven't
looked at yet.

Purpose
-------

I plan on writing a fast implementation in Cython for
[Shrapnel](https://github.com/ironport/shrapnel).  The python code is
a prototype for that code.  Hopefully the result (and ASCII huffman
table) are simple enough that people can translate it to C/C++ without
too much trouble.
