# -*- Mode: Python -*-

import unittest
import hpack

def HD (s):
    return s.decode ('hex')

# decoder tests are from rfc7541

class TestDecoder (unittest.TestCase):

    def _tdecode (self, encs, exps):
        t = hpack.DynamicTable()
        d = hpack.Decoder (t)
        r = []
        for enc in encs:
            r.append (d.decode (HD (enc)))
        self.assertEquals (r, exps)

    def test_c_2_1 (self):
        # Literal Header Field with Indexing
        self._tdecode (
            ['400a637573746f6d2d6b65790d637573746f6d2d686561646572'],
            [[('custom-key', 'custom-header')]]
        )

    def test_c_2_2 (self):
        # Literal Header Field without Indexing
        self._tdecode (['040c2f73616d706c652f70617468'], [[(':path', '/sample/path')]])

    def test_c_2_3 (self):
        # Literal Header Field Never Indexed
        self._tdecode (['100870617373776f726406736563726574'], [[('password', 'secret')]])

    def test_c_2_4 (self):
        # Indexed Header Field
        self._tdecode (['82'], [[(':method', 'GET')]])

    def test_c_3 (self):
        # Request Examples without Huffman Coding
        encs = [
            '828684410f7777772e6578616d706c652e636f6d',
            '828684be58086e6f2d6361636865',
            '828785bf400a637573746f6d2d6b65790c637573746f6d2d76616c7565'
        ]
        exp0 = [
            (':method', 'GET'),
            (':scheme', 'http'),
            (':path', '/'),
            (':authority', 'www.example.com'),
        ]
        exp1 = [
            (':method', 'GET'),
            (':scheme', 'http'),
            (':path', '/'),
            (':authority', 'www.example.com'),
            ('cache-control', 'no-cache'),
        ]
        exp2 = [
            (':method', 'GET'),
            (':scheme', 'https'),
            (':path', '/index.html'),
            (':authority', 'www.example.com'),
            ('custom-key', 'custom-value'),
        ]
        self._tdecode (encs, [exp0, exp1, exp2])
        #['828684410f7777772e6578616d706c652e636f6d',
        # '828684be58086e6f2d6361636865',
        # '828785bf400a637573746f6d2d6b65790c637573746f6d2d76616c7565'],


    def test_c_3 (self):
        # Request Examples without Huffman Coding
        enc0 = '828684410f7777772e6578616d706c652e636f6d'
        enc1 = '828684be58086e6f2d6361636865'
        enc2 = '828785bf400a637573746f6d2d6b65790c637573746f6d2d76616c7565'
        exp0 = [
            (':method', 'GET'),
            (':scheme', 'http'),
            (':path', '/'),
            (':authority', 'www.example.com'),
        ]
        exp1 = [
            (':method', 'GET'),
            (':scheme', 'http'),
            (':path', '/'),
            (':authority', 'www.example.com'),
            ('cache-control', 'no-cache'),
        ]
        exp2 = [
            (':method', 'GET'),
            (':scheme', 'https'),
            (':path', '/index.html'),
            (':authority', 'www.example.com'),
            ('custom-key', 'custom-value'),
        ]
        t = hpack.DynamicTable()
        d = hpack.Decoder (t)
        self.assertEquals (d.decode (HD (enc0)), exp0)
        self.assertEquals (t.size, 57)
        self.assertEquals (d.decode (HD (enc1)), exp1)
        self.assertEquals (t.size, 110)
        self.assertEquals (d.decode (HD (enc2)), exp2)
        self.assertEquals (t.size, 164)

    def test_c_4 (self):
        # Request Examples with Huffman Coding
        enc0 = '828684418cf1e3c2e5f23a6ba0ab90f4ff'
        enc1 = '828684be5886a8eb10649cbf'
        enc2 = '828785bf408825a849e95ba97d7f8925a849e95bb8e8b4bf'
        exp0 = [
            (':method', 'GET'),
            (':scheme', 'http'),
            (':path', '/'),
            (':authority', 'www.example.com'),
        ]
        exp1 = [
            (':method', 'GET'),
            (':scheme', 'http'),
            (':path', '/'),
            (':authority', 'www.example.com'),
            ('cache-control', 'no-cache'),
        ]
        exp2 = [
            (':method', 'GET'),
            (':scheme', 'https'),
            (':path', '/index.html'),
            (':authority', 'www.example.com'),
            ('custom-key', 'custom-value'),
        ]
        t = hpack.DynamicTable()
        d = hpack.Decoder (t)
        self.assertEquals (d.decode (HD (enc0)), exp0)
        self.assertEquals (t.size, 57)
        self.assertEquals (d.decode (HD (enc1)), exp1)
        self.assertEquals (t.size, 110)
        self.assertEquals (d.decode (HD (enc2)), exp2)
        self.assertEquals (t.size, 164)

    def test_c_5 (self):
        # Response Examples without Huffman Coding
        enc0 = (
            '488264025885aec3771a4b6196d07abe941054d444a8200595'
            '040b8166e082a62d1bff6e919d29ad171863c78f0b97c8e9ae82ae43d3'
        )
        enc1 = '4883640effc1c0bf'
        enc2 = (
            '88c16196d07abe941054d444a8200595040b8166e084a62d1b'
            'ffc05a839bd9ab77ad94e7821dd7f2e6c7b335dfdfcd5b3960'
            'd5af27087f3672c1ab270fb5291f9587316065c003ed4ee5b1063d5007'
        )
        exp0 = [
            (':status', '302'),
            ('cache-control', 'private'),
            ('date', 'Mon, 21 Oct 2013 20:13:21 GMT'),
            ('location', 'https://www.example.com'),
        ]
        exp1 = [
            (':status', '307'),
            ('cache-control', 'private'),
            ('date', 'Mon, 21 Oct 2013 20:13:21 GMT'),
            ('location', 'https://www.example.com'),
        ]
        exp2 = [
            (':status', '200'),
            ('cache-control', 'private'),
            ('date', 'Mon, 21 Oct 2013 20:13:22 GMT'),
            ('location', 'https://www.example.com'),
            ('content-encoding', 'gzip'),
            ('set-cookie', 'foo=ASDJKHQKBZXOQWEOPIUAXQWEOIU; max-age=3600; version=1'),
        ]
        t = hpack.DynamicTable (max_size=256)
        d = hpack.Decoder (t)
        self.assertEquals (d.decode (HD (enc0)), exp0)
        self.assertEquals (t.size, 222)
        self.assertEquals (d.decode (HD (enc1)), exp1)
        self.assertEquals (t.size, 222)
        self.assertEquals (d.decode (HD (enc2)), exp2)
        self.assertEquals (t.size, 215)

    def test_c_6 (self):
        enc0 = (
            '488264025885aec3771a4b6196d07abe941054d444a8200595'
            '040b8166e082a62d1bff6e919d29ad171863c78f0b97c8e9ae82ae43d3'
        )
        exp0 = [
            (':status', '302'),
            ('cache-control', 'private'),
            ('date', 'Mon, 21 Oct 2013 20:13:21 GMT'),
            ('location', 'https://www.example.com'),
        ]
        enc1 = '4883640effc1c0bf'
        exp1 = [
            (':status', '307'),
            ('cache-control', 'private'),
            ('date', 'Mon, 21 Oct 2013 20:13:21 GMT'),
            ('location', 'https://www.example.com'),
        ]
        enc2 = (
            '88c16196d07abe941054d444a8200595040b8166e084a62d1b'
            'ffc05a839bd9ab77ad94e7821dd7f2e6c7b335dfdfcd5b3960'
            'd5af27087f3672c1ab270fb5291f9587316065c003ed4ee5b1063d5007'
        )
        exp2 = [
            (':status', '200'),
            ('cache-control', 'private'),
            ('date', 'Mon, 21 Oct 2013 20:13:22 GMT'),
            ('location', 'https://www.example.com'),
            ('content-encoding', 'gzip'),
            ('set-cookie', 'foo=ASDJKHQKBZXOQWEOPIUAXQWEOIU; max-age=3600; version=1'),
        ]
        t = hpack.DynamicTable (max_size=256)
        d = hpack.Decoder (t)
        self.assertEquals (d.decode (HD (enc0)), exp0)
        self.assertEquals (t.size, 222)
        self.assertEquals (d.decode (HD (enc1)), exp1)
        self.assertEquals (t.size, 222)
        self.assertEquals (d.decode (HD (enc2)), exp2)
        self.assertEquals (t.size, 215)

    def test_endian (self):
        # test for correct multi-digit endian behavior.
        d = hpack.Decoder()
        d.data = '\x0f\x83\x01'
        assert d.get_integer (4) == 146


getty = (
    "Four score and seven years ago our fathers brought forth on this continent, a new nation,"
    " conceived in Liberty, and dedicated to the proposition that all men are created equal."
    "Now we are engaged in a great civil war, testing whether that nation, or any nation so"
    " conceived and so dedicated, can long endure. We are met on a great battle-field of that"
    " war. We have come to dedicate a portion of that field, as a final resting place for those"
    " who here gave their lives that that nation might live. It is altogether fitting and proper"
    " that we should do this."
).split()

class TestEncoder (unittest.TestCase):

    def _tencode (self, headers):
        e = hpack.Encoder()
        for k, v in headers:
            e.emit_header (k, v)
        encoded = e.flush()
        d = hpack.Decoder()
        decoded = d.decode (encoded)
        self.assertEquals (headers, decoded)

    def _tencode_many (self, headers_list):
        e = hpack.Encoder()
        d = hpack.Decoder()
        for headers in headers_list:
            for k, v in headers:
                e.emit_header (k, v)
            encoded = e.flush()
            decoded = d.decode (encoded)
            self.assertEquals (headers, decoded)

    def test_0 (self):
        # tests dynamic table with repeated key/val pairs, and
        #   repeated key with new values.
        headers = [
            ('a', 'b'),
            ('b', 'b'),
            ('c', 'b'),
            ('a', 'b'),
            ('b', 'b'),
            ('c', 'b'),
            ('a', 'x'),
            ('b', 'y'),
            ('c', 'z'),
        ]
        self._tencode (headers)

    def test_1 (self):
        exp0 = [
            (':status', '302'),
            ('cache-control', 'private'),
            ('date', 'Mon, 21 Oct 2013 20:13:21 GMT'),
            ('location', 'https://www.example.com'),
        ]
        exp1 = [
            (':status', '307'),
            ('cache-control', 'private'),
            ('date', 'Mon, 21 Oct 2013 20:13:21 GMT'),
            ('location', 'https://www.example.com'),
        ]
        exp2 = [
            (':status', '200'),
            ('cache-control', 'private'),
            ('date', 'Mon, 21 Oct 2013 20:13:22 GMT'),
            ('location', 'https://www.example.com'),
            ('content-encoding', 'gzip'),
            ('set-cookie', 'foo=ASDJKHQKBZXOQWEOPIUAXQWEOIU; max-age=3600; version=1'),
        ]
        self._tencode_many ([exp0, exp1, exp2])

    def test_2 (self):
        import random
        random.seed (314159)
        # randomly-generated header content
        e = hpack.Encoder()
        d = hpack.Decoder()
        for i in range (100):
            # 20 lines in each header.
            pairs = []
            for j in range (20):
                # pick header names from the first 20 words.
                name = getty[random.randrange (0, 20)].lower()
                val  = getty[random.randrange (20, len(getty))]
                pairs.append ((name, val))
                e.emit_header (name, val)
            encoded = e.flush()
            self.assertEquals (d.decode (encoded), pairs)

if __name__ == '__main__':
    unittest.main()
