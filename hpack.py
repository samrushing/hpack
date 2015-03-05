# -*- Mode: Python -*-

static_table = [
    (None, None),
    (':authority', None),
    (':method', 'GET'),
    (':method', 'POST'),
    (':path', '/'),
    (':path', '/index.html'),
    (':scheme', 'http'),
    (':scheme', 'https'),
    (':status', '200'),
    (':status', '204'),
    (':status', '206'),
    (':status', '304'),
    (':status', '400'),
    (':status', '404'),
    (':status', '500'),
    ('accept-charset', None),
    ('accept-encoding', 'gzip, deflate'),
    ('accept-language', None),
    ('accept-ranges', None),
    ('accept', None),
    ('access-control-allow-origin', None),
    ('age', None),
    ('allow', None),
    ('authorization', None),
    ('cache-control', None),
    ('content-disposition', None),
    ('content-encoding', None),
    ('content-language', None),
    ('content-length', None),
    ('content-location', None),
    ('content-range', None),
    ('content-type', None),
    ('cookie', None),
    ('date', None),
    ('etag', None),
    ('expect', None),
    ('expires', None),
    ('from', None),
    ('host', None),
    ('if-match', None),
    ('if-modified-since', None),
    ('if-none-match', None),
    ('if-range', None),
    ('if-unmodified-since', None),
    ('last-modified', None),
    ('link', None),
    ('location', None),
    ('max-forwards', None),
    ('proxy-authenticate', None),
    ('proxy-authorization', None),
    ('range', None),
    ('referer', None),
    ('refresh', None),
    ('retry-after', None),
    ('server', None),
    ('set-cookie', None),
    ('strict-transport-security', None),
    ('transfer-encoding', None),
    ('user-agent', None),
    ('vary', None),
    ('via', None),
    ('www-authenticate', None),
]

nstatic = len(static_table)

def from_ascii (s, pos=0):
    if s[pos] == '.':
        pos += 1
        l, pos = from_ascii (s, pos)
        r, pos = from_ascii (s, pos)
        return [l, r], pos
    elif s[pos] == 'Z':
        return 256, pos + 1
    else:
        return int (s[pos:pos+2], 16), pos + 2

# source: see huffman.py
huffman_table, _ = from_ascii (
    '.....3031.3261..6365.696f...7374..2025.2d2e...2f33.3435..3637.3839.....3d41.5f62'
    '..6466.6768...6c6d.6e70..7275..3a42.4344.....4546.4748..494a.4b4c...4d4e.4f50..'
    '5152.5354....5556.5759..6a6b.7176...7778.797a...262a.2c3b..585a...2122.2829..3f.'
    '272b..7c.233e...0024.405b..5d7e..5e7d..3c60.7b....5cc3.d0.8082...83a2.b8c2..e0e2'
    '..99a1.a7ac.....b0b1.b3d1..d8d9.e3e5...e6.8184..8586.8892...9a9c.a0a3..a4a9.aaad'
    '.....b2b5.b9ba..bbbd.bec4...c6e4.e8e9...0187.898a..8b8c.8d8f.....9395.9697..989b'
    '.9d9e...a5a6.a8ae..afb4.b6b7....bcbf.c5e7..ef.098e..9091.949f....abce.d7e1..eced'
    '..c7cf.eaeb.....c0c1.c8c9..cacd.d2d5...dadb.eef0..f2f3.ff.cbcc.....d3d4.d6dd..de'
    'df.f1f4...f5f6.f7f8..fafb.fcfd....fe.0203..0405.0607...080b.0c0e..0f10.1112....1'
    '314.1517..1819.1a1b...1c1d.1e1f..7fdc.f9..0a0d.16Z'
)

class DynamicTable:

    def __init__ (self):
        self.table = []
        self.size = 0
        self.max_size = 1024

    def __getitem__ (self, index):
        if index < nstatic:
            return static_table[index]
        else:
            return self.table[index-nstatic]

    def entry_size (self, name, val):
        return len(name) + len(val) + 32

    def __setitem__ (self, name, val):
        self.table.append ((name, val))
        self.size += self.entry_size (name, val)

    def set_size (self, size):
        # eviction, etc..
        import pdb; pdb.set_trace()

class Decoder:

    def __init__ (self, data, table):
        self.data = data
        self.pos = 0
        # used when pulling off huffman-encoded bits.
        self.bpos = 0
        self.dyn = table
        
    @property
    def done (self):
        return self.pos >= len(self.data)

    @property
    def byte (self):
        return ord(self.data[self.pos])

    def next_byte (self):
        self.pos += 1
        self.bpos = 7

    def get_bytes (self, n):
        result = self.data[self.pos:self.pos+n]
        self.pos += n
        assert (len(result) == n)
        return result

    masks = {i : (1<<i)-1 for i in (4,5,6,7)}
        
    def get_integer (self, nbits):
        # fetch an integer from the lower <nbits> of
        #   the current byte.
        mask = self.masks[nbits]
        r = self.byte & mask
        if r == mask:
            # more octets
            r = 0
            while 1:
                self.next_byte()
                r <<= 7
                r |= self.byte & 0x7f
                if self.byte & 0x80:
                    break
            self.next_byte()
            return r + mask
        else:
            self.next_byte()
            return r

    def get_bit (self):
        r = (self.byte & (1 << self.bpos)) != 0
        self.bpos -= 1
        if self.bpos < 0:
            self.next_byte()
        return r

    def get_pair0 (self, index):
        if index == 0:
            name = self.get_literal()
        else:
            name = self.dyn[index][0]
        val  = self.get_literal()
        return name, val

    def get_header (self):
        if self.byte >> 7 == 0x1:
            # index name and value
            index = self.get_integer (7)
            assert index != 0
            return self.dyn[index]
        elif self.byte >> 6 == 0b01:
            # literal with incremental indexing.
            index = self.get_integer (6)
            name, val = self.get_pair0 (index)
            self.dyn[name] = val
            return name, val
        elif self.byte >> 4 in (0b0000, 0b0001):
            never = self.byte >> 4 & 0b0001
            # literal without indexing
            index = self.get_integer (4)
            name, val = self.get_pair0 (index)
            return name, val
        elif self.byte >> 5 == 0b001:
            self.dyn.set_size (self.get_integer (5))

    def get_literal (self):
        is_huffman = self.byte & 0b10000000
        lit_len = self.get_integer (7)
        if is_huffman:
            return self.get_huffman (lit_len)
        else:
            return self.get_bytes (lit_len)

    def get_huffman (self, nbytes):
        r = []
        stop = self.pos + nbytes
        while 1:
            t = huffman_table
            while 1:
                b = self.get_bit()
                t = t[b]
                if isinstance (t, int):
                    r.append (chr (t))
                    break
                if self.pos == stop:
                    return ''.join (r)
        return ''.join (r)
