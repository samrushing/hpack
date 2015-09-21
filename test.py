# -*- Mode: Python -*-

from hpack import *
import sys

W = sys.stderr.write

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
    # with eviction (& huffman)
    ['488264025885aec3771a4b6196d07abe941054d444a8200595040b8166e082a62d1bff6e919d29ad171863c78f0b97c8e9ae82ae43d3',
     '4883640effc1c0bf',
     '88c16196d07abe941054d444a8200595040b8166e084a62d1bffc05a839bd9ab77ad94e7821dd7f2e6c7b335dfdfcd5b3960d5af27087f3672c1ab270fb5291f9587316065c003ed4ee5b1063d5007',
 ]
]

class HeaderSet (dict):
    def __iter__ (self):
        for k, v in self.iteritems():
            yield k, v

def t0 (headers):
    dt = DynamicTable (max_size=256)
    for header in headers:
        d = Decoder (dt)
        d.feed (HD (header))
        while not d.done:
            W ('%r: %r\n' % d.get_header())

def t1():
    for test in tests:
        t0 (test)

def t2():
    h = HuffmanEncoder()
    h.encode ('www.example.com')
    W ('%s\n' % (h.done().encode('hex'),))
    h = HuffmanEncoder()
    h.encode ('2398423942342')
    W ('%s\n' % (h.done().encode('hex'),))

def t3():
    e = Encoder()
    hs = HeaderSet ([
        ('thing1', ['value of thing1']),
        ('thing2', ['2398423942342']),
        (':method', [b'GET'])
        ])
    encoded = e (hs)
    d = Decoder()
    W ('%r\n' % (encoded,))
    d.feed (encoded)
    while not d.done:
        W ('%r: %r\n' % d.get_header())

def t4():
    e = Encoder()
    hs = HeaderSet ([
        ('last-modified', ['Thu, 17 Sep 2015 21:05:27 GMT']),
        ('content-type', ['text/x-python']),
        (':version', ['HTTP/1.1']),
        (':status', ['200 OK']),
        ])
    encoded = e (hs)
    encoded = '\x0f\x1d\x96\xdf=\xbfJ\x05\xd57\x16\xb5\x04\x00\xb6\xa0\x83p\r\xdc\x13\xaab\xd1\xbf\x0f\x10\x8aI|\xa5\x8f+W\xe93\x9e\xaf\x00\x86\xb9\xdc\xb6 \xc7\xab\x87\xc7\xbf~\xb6\x02\xb8\x7f\x00\x85\xb8\x84\x8d6\xa3\x85\x10\x00\xa6\xac\xdf'
    d = Decoder()
    d.feed (encoded)
    while not d.done:
        print d.get_header()

t1()
t2()
t3()
t4()


