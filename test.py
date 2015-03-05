# -*- Mode: Python -*-

from hpack import *

def t0 (headers):
    print '--------------'
    dt = DynamicTable()
    for header in headers:
        d = Decoder (HD (header), dt)
        while not d.done:
            print d.get_header()
        print '****'
        print 'dt.size', dt.size

def HD(s):
    return s.decode ('hex')

tests = [
    # without huffman coding
    ['040c2f73616d706c652f70617468'],
    ['400a637573746f6d2d6b65790d637573746f6d2d686561646572'],
    ['828684410f7777772e6578616d706c652e636f6d',
     '828684be58086e6f2d6361636865',
     '828785bf400a637573746f6d2d6b65790c637573746f6d2d76616c7565'],
    # with huffman coding
    ['828684418cf1e3c2e5f23a6ba0ab90f4ff', 
     '828684be5886a8eb10649cbf',
     '828785bf408825a849e95ba97d7f8925a849e95bb8e8b4bf'],
    # responses
    ['4803333032580770726976617465611d4d6f6e2c203231204f637420323031332032303a31333a323120474d546e1768747470733a2f2f7777772e6578616d706c652e636f6d'],
]

def t1():
    for test in tests:
        t0 (test)

t1()
