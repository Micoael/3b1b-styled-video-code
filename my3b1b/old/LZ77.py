from manimlib.imports import *
from PrimoCreature import *

class LZ77:
    """
    A simplified implementation of LZ77 algorithm
    """

    def __init__(self, window_size):
        self.window_size = window_size
        self.buffer_size = 4

    def longest_match(self, data, cursor):
        """
        find the longest match between in dictionary and lookahead-buffer
        """
        end_buffer = min(cursor + self.buffer_size, len(data))

        p = -1
        l = -1
        c = ''

        for j in range(cursor+1, end_buffer+1):
            start_index = max(0, cursor - self.window_size + 1)
            substring = data[cursor + 1:j + 1]

            for i in range(start_index, cursor+1):
                repetition = len(substring) / (cursor - i + 1)
                last = len(substring) % (cursor - i + 1)
                matchedstring = data[i:cursor + 1] * repetition + data[i:i + last]

                if matchedstring == substring and len(substring) > l:
                    p = cursor - i + 1
                    l = len(substring)
                    c = data[j+1]

        # unmatched string between the two
        if p == -1 and l == -1:
            return 0, 0, data[cursor + 1]
        return p, l, c

    def compress(self, message):
        """
        compress message
        :return: tuples (p, l, c)
        """
        i = -1
        out = []

        # the cursor move until it reaches the end of message
        while i < len(message)-1:
            (p, l, c) = self.longest_match(message, i)
            out.append((p, l, c))
            i += (l+1)
        return out

    def decompress(self, compressed):
        """
        decompress the compressed message
        :param compressed: tuples (p, l, c)
        :return: decompressed message
        """
        cursor = -1
        out = ''

        for (p, l, c) in compressed:
            # the initialization
            if p == 0 and l == 0:
                out += c
            elif p >= l:
                out += (out[cursor-p+1:cursor+1] + c)

            # the repetition of dictionary
            elif p < l:
                repetition = l / p
                last = l % p
                out += (out[cursor-p+1:cursor+1] * repetition + out[cursor-p+1:last] + c)
            cursor += (l + 1)

        return out


 

class Demostrate(Scene):
    def construct(self):
        compressor = LZ77(6)
        origin = list('aacaacabcabaaac')
        pack = compressor.compress(origin)
    