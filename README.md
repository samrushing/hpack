HPACK
=====

An implementation of [HPACK](http://http2.github.io/http2-spec/compression.html) in Python/Cython.

Status
------

Decoder and encoder work.  The encoder makes use of the dynamic table,
but is not incredibly sophisticated.  The encoder could detect usage
patterns in headers - e.g., a header like 'Date' that changes its value
often might flood the dynamic table - this could probably be detected
and avoided.

There are some requirements around the 'cookie' header I haven't
looked at yet.

Purpose
-------

I plan on writing a fast implementation in Cython for
[Shrapnel](https://github.com/ironport/shrapnel).  The python code is
a prototype for that code.  Hopefully the result (and ASCII huffman
table) are simple enough that people can translate it to C/C++ without
too much trouble.
