from manimlib.imports import *
from PrimoCreature import *
import copy
class Demo(GraphScene):
    def construct(_):
        _.init()
        t = _.gbit(_.encd("Demo"))
        _.wait()
        _.play(Write(_.drawGrid(t,21,21)))
        _.wait()

    def drawGrid(_,src,ii,jj):
        vg = VGroup()
        for i in range(ii):
            for j in range(jj):
                if src[i][j]==False:
                    s = Rectangle(width=0.3,height=0.3,stroke_width=0,fill_color=WHITE,fill_opacity=1).shift(0.3*i*DOWN+0.3*j*RIGHT).shift(3*LEFT+3*UP)
                    vg.add(s)
                else:
                    s = Rectangle(width=0.3,height=0.3,stroke_width=0,fill_color=BLACK,fill_opacity=1).shift(0.3*i*DOWN+0.3*j*RIGHT).shift(3*LEFT+3*UP)
                    vg.add(s)
        return vg
        
    def init(_):
        _.DARK=0
        _.LIGHT=1
        _._gfExp = [0] * 512
        _._gfLog = [0] * 256
        _._gfPrim = 0x11d

        _x = 1

        for i in range(255):
            _._gfExp[i] = _x
            _._gfLog[_x] = i
            _x = _.GFMul(_x, 2)

        for i in range(255, 512):
            _._gfExp[i] = _._gfExp[i-255]

        _._finder = _.copyFrom(
                _.copyFrom(
                    [[_.DARK for i in range(3)] for j in range(3)],
                    [[_.LIGHT for i in range(5)] for j in range(5)],
                    1, 1
                ),
                [[_.DARK for i in range(7)] for j in range(7)], 1, 1
            )


        # Alignment pattern. Not used in version 1.
        _align = _.copyFrom(
            _.copyFrom(
                [[_.DARK]],
                [[_.LIGHT for i in range(3)] for j in range(3)], 1, 1
            ),
            [[_.DARK for i in range(5)] for j in range(5)], 1, 1
        )

        # Version 1 QR code template with finder patterns and timing sequences.
        _.ver1Temp = [[_.LIGHT for i in range(21)] for j in range(21)]
        _.ver1Temp = _.copyFrom(_._finder, _.ver1Temp, 0, 0)
        _.ver1Temp = _.copyFrom(_._finder, _.ver1Temp, 14, 0)
        _.ver1Temp = _.copyFrom(_._finder, _.ver1Temp, 0, 14)
        _.ver1Temp = _.copyFrom(_._timSeq(5), _.ver1Temp, 6, 8)
        _.ver1Temp = _.copyFrom(_._timSeq(5, vertical=True), _.ver1Temp, 8, 6)
        _.ver1Temp = _.copyFrom([[_.DARK]], _.ver1Temp, 13, 8)

        # Data area mask to avoid applying masks to functional area.
        _._dataAreaMask = [[_.DARK for i in range(21)] for j in range(21)]
        _._dataAreaMask = _.copyFrom([[_.LIGHT for i in range(9)] for j in range(9)],
                                _._dataAreaMask, 0, 0)
        _._dataAreaMask = _.copyFrom([[_.LIGHT for i in range(9)] for j in range(8)],
                                _._dataAreaMask, 13, 0)
        _._dataAreaMask = _.copyFrom([[_.LIGHT for i in range(8)] for j in range(9)],
                                _._dataAreaMask, 0, 13)
        _._dataAreaMask = _.copyFrom([[_.LIGHT for i in range(4)]], _._dataAreaMask, 6, 9)
        _._dataAreaMask = _.copyFrom([[_.LIGHT] for i in range(4)], _._dataAreaMask, 9, 6)
        _._maskList = [
                [
                    [
                        _.DARK if _.mdk(c, i, j)
                        else _.LIGHT for i in range(21)
                    ] for j in range(21)
                ] for c in range(8)
            ]
        _.dataMasks = [_.logicAnd(_._dataAreaMask, mask) for mask in _._maskList]

    def mdk(_,idxes, i, j):
        if idxes == 0:
            poli = (i+j) % 2
        elif idxes == 1:
            poli = j % 2
        elif idxes == 2:
            poli = i % 3
        elif idxes == 3:
            poli = (i+j) % 3
        elif idxes == 4:
            poli = (j//2 + i//3) % 2
        elif idxes == 5:
            poli = (i*j) % 2+(i*j) % 3
        elif idxes == 6:
            poli = ((i*j) % 2+(i*j) % 3) % 2
        elif idxes == 7:
            poli = ((i+j) % 2+(i*j) % 3) % 2
        return poli == 0

    def GFMul(_,x=2, y=2, prim=0x11d, field_charac_full=256, carryless=True):
        '''Galois field GF(2^8) multiplication.'''
        rr = 0
        while y:
            if y & 1:
                rr = rr ^ x if carryless else rr + x
            y = y >> 1
            x = x << 1
            if prim > 0 and x & field_charac_full:
                x = x ^ prim
        return rr

    def RSEnc(_,bitstring, nsym):
        '''Encode bitstring with nsym EC bits using RS algorithm.'''
        gen = _._rsGenPoly(nsym)
        res = [0] * (len(bitstring) + len(gen) - 1)
        res[:len(bitstring)] = bitstring
        for i in range(len(bitstring)):
            coef = res[i]
            if coef != 0:
                for j in range(1, len(gen)):
                    res[i+j] ^= _._gfMul(gen[j], coef)
        res[:len(bitstring)] = bitstring
        return res

    def _gfMul(_,x, y):
        '''Simplified GF multiplication.'''
        if x == 0 or y == 0:
            return 0
        return _._gfExp[_._gfLog[x] + _._gfLog[y]]

    def transpose(_,mat):
        '''Transpose a matrix'''
        res = [[mat[j][i] for j in range(len(mat))] for i in range(len(mat[0]))]
        return res

    def _timSeq(_,len, vertical=False):
        '''
        Generate a horizontal, unless specified vertical
        timing sequence with alternating dark and light
        pixels with length len.
        '''
        res = [[i % 2 for i in range(len)]]
        if vertical:
            res = _.transpose(res)
        return res

    def _gfPolyMul(_,p, q):
        '''GF polynomial multiplication.'''
        r = [0] * (len(p) + len(q) - 1)
        for j in range(len(q)):
            for i in range(len(p)):
                r[i+j] ^= _._gfMul(p[i], q[j])
        return r

    def _gfPolyDiv(_,dividend, divisor):
        '''GF polynomial division.'''
        res = list(dividend)
        for i in range(len(dividend) - len(divisor) + 1):
            coef = res[i]
            if coef != 0:
                for j in range(1, len(divisor)):
                    if divisor[j] != 0:
                        res[i+j] ^= _gfMul(divisor[j], coef)
        sep = -(len(divisor) - 1)
        return res[:sep], res[sep:]

    def _gfPow(_,x, pow):
        '''GF power.'''
        return _._gfExp[(_._gfLog[x] * pow) % 255]

    def _rsGenPoly(_,nsym):
        '''Generate generator polynomial for RS algorithm.'''
        g = [1]
        for i in range(nsym):
            g = _._gfPolyMul(g, [1, _._gfPow(2, i)])
        return g

    def _fmtEncode(_,fmt):
        '''Encode the 15-bit format code using BCH code.'''
        g = 0x537
        code = fmt << 10
        for i in range(4, -1, -1):
            if code & (1 << (i+10)):
                code ^= g << i
        return ((fmt << 10) ^ code) ^ 0b101010000010010

    def encd(_,data):
        '''
        Encode the input data stream.
        Add mode prefix, encode data using ISO-8859-1,
        group data, add padding suffix, and call RS encoding method.
        '''
        if len(data) > 17:
            print('Error: Version 1 QR code encodes no more than 17 characters.')
        # Byte mode prefix 0100.
        bitstring = '0100'
        # Character count in 8 binary bits.
        bitstring += '{:08b}'.format(len(data))
        # Encode every character in ISO-8859-1 in 8 binary bits.
        for c in data:
            bitstring += '{:08b}'.format(ord(c.encode('iso-8859-1')))
        # Terminator 0000.
        bitstring += '0000'
        res = list()
        # Convert string to byte numbers.
        while bitstring:
            res.append(int(bitstring[:8], 2))
            bitstring = bitstring[8:]
        # Add padding pattern.
        while len(res) < 19:
            res.append(int('11101100', 2))
            res.append(int('00010001', 2))
        # Slice to 19 bytes for V1-L.
        res = res[:19]
        # Call RSEnc to add 7 EC bits.
        return _.RSEnc(res, 7)
    
    def fillbt(_,byte, downwards=False):
        '''
        Fill a byte into a 2 by 4 matrix upwards,
        unless specified downwards.
        Upwards:    Downwards:
            0|1         6|7
            -+-         -+-
            2|3         4|5
            -+-         -+-
            4|5         2|3
            -+-         -+-
            6|7         0|1
        '''
        bytestr = '{:08b}'.format(byte)
        res = [[0, 0] for i in range(4)]
        for i in range(8):
            
            res[i // 2][i % 2] = not int(bytestr[7-i])
        if downwards:
            res = res[::-1]
        return res

    def copyFrom(_,src, dst, top, left):
        '''
        Copy the content of matrix src into matrix dst.
        The top-left corner of src is positioned at (left, top)
        in dst.
        '''
        res = copy.deepcopy(dst)
        for j in range(len(src)):
            for i in range(len(src[0])):
                res[top+j][left+i] = src[j][i]
        return res

    def _fillData(_,bitstream):
        '''Fill the encoded data into the template QR code matrix'''
        res = copy.deepcopy(_.ver1Temp)
        for i in range(15):
            res = _.copyFrom(_.fillbt(bitstream[i], (i//3) % 2 != 0),
                        res,
                        21-4*((i % 3-1)*(-1)**((i//3) % 2)+2),
                        21-2*(i//3+1))
            _.play(Write(_.drawGrid(res,21,21)))
        tmp = _.fillbt(bitstream[15])
        res = _.copyFrom(tmp[2:], res, 7, 11)
        _.play(Write(_.drawGrid(res,21,21)))
        res = _.copyFrom(tmp[:2], res, 4, 11)
        _.play(Write(_.drawGrid(res,21,21)))
        tmp = _.fillbt(bitstream[16])
        res = _.copyFrom(tmp, res, 0, 11)
        _.play(Write(_.drawGrid(res,21,21)))
        tmp = _.fillbt(bitstream[17], True)
        res = _.copyFrom(tmp, res, 0, 9)
        _.play(Write(_.drawGrid(res,21,21)))
        tmp = _.fillbt(bitstream[18], True)
        res = _.copyFrom(tmp[:2], res, 4, 9)
        _.play(Write(_.drawGrid(res,21,21)))
        res = _.copyFrom(tmp[2:], res, 7, 9)
        _.play(Write(_.drawGrid(res,21,21)))
        for i in range(3):
            res = _.copyFrom(_.fillbt(bitstream[19+i], True),
                        res, 9+4*i, 9)
            _.play(Write(_.drawGrid(res,21,21)))
        tmp = _.fillbt(bitstream[22])
        res = _.copyFrom(tmp, res, 9, 7)
        _.play(Write(_.drawGrid(res,21,21)))
        for i in range(3):
            res = _.copyFrom(_.fillbt(bitstream[23+i], i % 2 == 0),
                        res, 9, 4-2*i)
            _.play(Write(_.drawGrid(res,21,21)))
        # Generate image after filling data for debug use.
        
       
        return res

    def _fillInfo(_,arg):
        '''
        Fill the encoded format code into the masked QR code matrix.
        arg: (masked QR code matrix, mask number).
        '''
        mat, mask = arg
        # 01 is the format code for L error control level,
        # concatenated with mask id and passed into _fmtEncode
        # to get the 15 bits format code with EC bits.
        fmt = _._fmtEncode(int('01'+'{:03b}'.format(mask), 2))
        fmtarr = [[not int(c)] for c in '{:015b}'.format(fmt)]
        mat = _.copyFrom(_.transpose(fmtarr[7:]), mat, 8, 13)
        mat = _.copyFrom(fmtarr[9:][::-1], mat, 0, 8)
        mat = _.copyFrom(fmtarr[7:9][::-1], mat, 7, 8)
        mat = _.copyFrom(fmtarr[:7][::-1], mat, 14, 8)
        mat = _.copyFrom(_.transpose(fmtarr[:6]), mat, 8, 0)
        mat = _.copyFrom([fmtarr[6]], mat, 8, 7)
        return mat

    def _penalty(_,mat):
        '''
        Calculate penalty score for a masked matrix.
        N1: penalty for more than 5 consecutive pixels in row/column,
            3 points for each occurrence of such pattern,
            and extra 1 point for each pixel exceeding 5
            consecutive pixels.
        N2: penalty for blocks of pixels larger than 2x2.
            3*(m-1)*(n-1) points for each block of mxn
            (larger than 2x2).
        N3: penalty for patterns similar to the finder pattern.
            40 points for each occurrence of 1:1:3:1:1 ratio
            (dark:light:dark:light:dark) pattern in row/column,
            preceded of followed by 4 consecutive light pixels.
        N4: penalty for unbalanced dark/light ratio.
            10*k points where k is the rating of the deviation of
            the proportion of dark pixels from 50% in steps of 5%.
        '''
        # Initialize.
        n1 = n2 = n3 = n4 = 0
        # Calculate N1.

        def getN1(mat, strategy):
            n1 = 0
            for j in range(len(mat)):
                count = 1
                adj = False
                for i in range(1, len(mat)):
                    if strategy == "j":
                        compare = mat[j][i-1]
                    elif strategy == "i":
                        i, j = j, i
                        compare = mat[j-1][i]
                    if mat[j][i] == compare:
                        count += 1
                    else:
                        count = 1
                        adj = False
                    if count >= 5:
                        if not adj:
                            adj = True
                            n1 += 3
                        else:
                            n1 += 1
            return n1

        n1 = getN1(mat, "i") + getN1(mat, "j")

        # Calculate N2.
        m = n = 1
        for j in range(1, len(mat)):
            for i in range(1, len(mat)):
                if (mat[j][i] == mat[j-1][i] and mat[j][i] == mat[j][i-1] and
                    mat[j][i] == mat[j-1][i-1]):
                    if mat[j][i] == mat[j-1][i]:
                        m += 1
                    if mat[j][i] == mat[j][i-1]:
                        n += 1
                else:
                    n2 += 3 * (m-1) * (n-1)
                    m = n = 1

        # Calculate N3.
        count = 0

        def getCount(mat):
            count = 0
            for row in mat:
                rowstr = ''.join(str(e) for e in row)
                occurrences = []
                begin = 0
                while rowstr.find('0100010', begin) != -1:
                    begin = rowstr.find('0100010', begin) + 7
                    occurrences.append(begin)
                for begin in occurrences:
                    if (rowstr.count('00000100010', begin-4) != 0 or
                        rowstr.count('01000100000', begin) != 0):
                        count += 1
            return count

        transposedMat = _.transpose(mat)
        n3 += 40 * (getCount(mat)+getCount(transposedMat))

        # Calculate N4.
        dark = sum(row.count(_.DARK) for row in mat)
        percent = int((float(dark) / float(len(mat)**2)) * 100)
        pre = percent - percent % 5
        nex = percent + 5 - percent % 5
        n4 = min(abs(pre-50)//5, abs(nex-50)//5) * 10

        # Return final penalty score.
        return n1 + n2 + n3 + n4

    def logicAnd(_,mat1, mat2):
        '''
        Matrix-wise and.
        Dark and dark -> dark
        Light and light -> light
        Dark and light -> light
        Light and dark -> light
        '''
        res = [[True for i in range(len(mat1[0]))] for j in range(len(mat1))]
        for j in range(len(mat1)):
            for i in range(len(mat1[0])):
                res[j][i] = mat1[j][i] or mat2[j][i]
        return res

    def logicOr(_,mat1, mat2):
        """
        B + B -> B
        B + W -> B
        W + W -> W
        """
        res = [[False for i in range(len(mat1[0]))] for j in range(len(mat1))]
        for j in range(len(mat1)):
            for i in range(len(mat1[0])):
                res[j][i] = mat1[j][i] and mat2[j][i]
        return res

    def logicNot(_,mat1):
        res = [[False for i in range(len(mat1[0]))] for j in range(len(mat1))]
        for j in range(len(mat1)):
            for i in range(len(mat1[0])):
                res[j][i] = not mat1[j][i]
        return res

    def logicXor(_,mat1, mat2):
        '''
        Matrix-wise xor.
        Dark xor dark -> light
        Light xor light -> light
        Dark xor light -> dark
        Light xor dark -> dark
        '''
        res = [[True for i in range(len(mat1[0]))] for j in range(len(mat1))]
        for j in range(len(mat1)):
            for i in range(len(mat1[0])):
                res[j][i] = mat1[j][i] == mat2[j][i]
        return res

    def _mask(_,mat):
        '''
        Mask the data QR code matrix with all 8 masks,
        call _penalty to calculate penalty scores for each
        and select the best mask.
        Return tuple(selected masked matrix, number of selected mask).
        '''
        maskeds = [_.logicXor(mat, dataMask) for dataMask in _.dataMasks]
        penalty = [0] * 8
        for i, masked in enumerate(maskeds):
            penalty[i] = _._penalty(masked)
            # Print penalty scores for debug use.
            if True:
                print('penalty for mask {}: {}'.format(i, penalty[i]))
        # Find the id of the best mask.
        selected = penalty.idxes(min(penalty))
        # Print selected mask and penalty score,
        # and generate image for masked QR code for debug use.
        if True:
            print('mask {} selected with penalty {}'.format(selected,
                                                            penalty[selected]))
            
        return maskeds[selected], selected

    def gbit(_,bitstream):
        '''
        Take in the encoded data stream and generate the
        final QR code bitmap.
        '''
        return _._fillInfo(_._mask(_._fillData(bitstream)))


class FillDataDemo(GraphScene):
    def construct(_):
        _.ia = 0
        _.ja=0
        _.gr = VGroup()
        _.init()
        t = _.gbit(_.encd("Demo"))
        _.wait(3)

    def drawGrid(_,src,ii,jj):
        vg = VMobject()
        for i in range(ii):
            for j in range(jj):
                if src[i][j]==False:
                    s = Rectangle(width=0.3,height=0.3,stroke_width=0,fill_color=WHITE,fill_opacity=1).shift(0.3*i*DOWN+0.3*j*RIGHT).shift(3*LEFT+3*UP)
                    vg.add(s)
                else:
                    s = Rectangle(width=0.3,height=0.3,stroke_width=0,fill_color=BLACK,fill_opacity=1).shift(0.3*i*DOWN+0.3*j*RIGHT).shift(3*LEFT+3*UP)
                    vg.add(s)
        return vg
        
    def init(_):
        _.DARK=0
        _.LIGHT=1
        _._gfExp = [0] * 512
        _._gfLog = [0] * 256
        _._gfPrim = 0x11d

        _x = 1

        for i in range(255):
            _._gfExp[i] = _x
            _._gfLog[_x] = i
            _x = _.GFMul(_x, 2)

        for i in range(255, 512):
            _._gfExp[i] = _._gfExp[i-255]

        _._finder = _.copyFrom(
                _.copyFrom(
                    [[_.DARK for i in range(3)] for j in range(3)],
                    [[_.LIGHT for i in range(5)] for j in range(5)],
                    1, 1
                ),
                [[_.DARK for i in range(7)] for j in range(7)], 1, 1
            )


        # Alignment pattern. Not used in version 1.
        _align = _.copyFrom(
            _.copyFrom(
                [[_.DARK]],
                [[_.LIGHT for i in range(3)] for j in range(3)], 1, 1
            ),
            [[_.DARK for i in range(5)] for j in range(5)], 1, 1
        )

        # Version 1 QR code template with finder patterns and timing sequences.
        _.ver1Temp = [[_.LIGHT for i in range(21)] for j in range(21)]
        _.ver1Temp = _.copyFrom(_._finder, _.ver1Temp, 0, 0)
        _.ver1Temp = _.copyFrom(_._finder, _.ver1Temp, 14, 0)
        _.ver1Temp = _.copyFrom(_._finder, _.ver1Temp, 0, 14)
        _.ver1Temp = _.copyFrom(_._timSeq(5), _.ver1Temp, 6, 8)
        _.ver1Temp = _.copyFrom(_._timSeq(5, vertical=True), _.ver1Temp, 8, 6)
        _.ver1Temp = _.copyFrom([[_.DARK]], _.ver1Temp, 13, 8)

        # Data area mask to avoid applying masks to functional area.
        _._dataAreaMask = [[_.DARK for i in range(21)] for j in range(21)]
        _._dataAreaMask = _.copyFrom([[_.LIGHT for i in range(9)] for j in range(9)],
                                _._dataAreaMask, 0, 0)
        _._dataAreaMask = _.copyFrom([[_.LIGHT for i in range(9)] for j in range(8)],
                                _._dataAreaMask, 13, 0)
        _._dataAreaMask = _.copyFrom([[_.LIGHT for i in range(8)] for j in range(9)],
                                _._dataAreaMask, 0, 13)
        _._dataAreaMask = _.copyFrom([[_.LIGHT for i in range(4)]], _._dataAreaMask, 6, 9)
        _._dataAreaMask = _.copyFrom([[_.LIGHT] for i in range(4)], _._dataAreaMask, 9, 6)
        _._maskList = [
                [
                    [
                        _.DARK if _.mdk(c, i, j)
                        else _.LIGHT for i in range(21)
                    ] for j in range(21)
                ] for c in range(8)
            ]
        _.dataMasks = [_.logicAnd(_._dataAreaMask, mask) for mask in _._maskList]

    def mdk(_,idxes, i, j):
        if idxes == 0:
            poli = (i+j) % 2
        elif idxes == 1:
            poli = j % 2
        elif idxes == 2:
            poli = i % 3
        elif idxes == 3:
            poli = (i+j) % 3
        elif idxes == 4:
            poli = (j//2 + i//3) % 2
        elif idxes == 5:
            poli = (i*j) % 2+(i*j) % 3
        elif idxes == 6:
            poli = ((i*j) % 2+(i*j) % 3) % 2
        elif idxes == 7:
            poli = ((i+j) % 2+(i*j) % 3) % 2
        return poli == 0

    def GFMul(_,x=2, y=2, prim=0x11d, field_charac_full=256, carryless=True):
        '''Galois field GF(2^8) multiplication.'''
        rr = 0
        while y:
            if y & 1:
                rr = rr ^ x if carryless else rr + x
            y = y >> 1
            x = x << 1
            if prim > 0 and x & field_charac_full:
                x = x ^ prim
        return rr

    def RSEnc(_,bitstring, nsym):
        '''Encode bitstring with nsym EC bits using RS algorithm.'''
        gen = _._rsGenPoly(nsym)
        res = [0] * (len(bitstring) + len(gen) - 1)
        res[:len(bitstring)] = bitstring
        for i in range(len(bitstring)):
            coef = res[i]
            if coef != 0:
                for j in range(1, len(gen)):
                    res[i+j] ^= _._gfMul(gen[j], coef)
        res[:len(bitstring)] = bitstring
        return res

    def _gfMul(_,x, y):
        '''Simplified GF multiplication.'''
        if x == 0 or y == 0:
            return 0
        return _._gfExp[_._gfLog[x] + _._gfLog[y]]

    def transpose(_,mat):
        '''Transpose a matrix'''
        res = [[mat[j][i] for j in range(len(mat))] for i in range(len(mat[0]))]
        return res

    def _timSeq(_,len, vertical=False):
        '''
        Generate a horizontal, unless specified vertical
        timing sequence with alternating dark and light
        pixels with length len.
        '''
        res = [[i % 2 for i in range(len)]]
        if vertical:
            res = _.transpose(res)
        return res

    def _gfPolyMul(_,p, q):
        '''GF polynomial multiplication.'''
        r = [0] * (len(p) + len(q) - 1)
        for j in range(len(q)):
            for i in range(len(p)):
                r[i+j] ^= _._gfMul(p[i], q[j])
        return r

    def _gfPolyDiv(_,dividend, divisor):
        '''GF polynomial division.'''
        res = list(dividend)
        for i in range(len(dividend) - len(divisor) + 1):
            coef = res[i]
            if coef != 0:
                for j in range(1, len(divisor)):
                    if divisor[j] != 0:
                        res[i+j] ^= _gfMul(divisor[j], coef)
        sep = -(len(divisor) - 1)
        return res[:sep], res[sep:]

    def _gfPow(_,x, pow):
        '''GF power.'''
        return _._gfExp[(_._gfLog[x] * pow) % 255]

    def _rsGenPoly(_,nsym):
        '''Generate generator polynomial for RS algorithm.'''
        g = [1]
        for i in range(nsym):
            g = _._gfPolyMul(g, [1, _._gfPow(2, i)])
        return g

    def _fmtEncode(_,fmt):
        '''Encode the 15-bit format code using BCH code.'''
        g = 0x537
        code = fmt << 10
        for i in range(4, -1, -1):
            if code & (1 << (i+10)):
                code ^= g << i
        return ((fmt << 10) ^ code) ^ 0b101010000010010

    def encd(_,data):
        '''
        Encode the input data stream.
        Add mode prefix, encode data using ISO-8859-1,
        group data, add padding suffix, and call RS encoding method.
        '''
        if len(data) > 17:
            print('Error: Version 1 QR code encodes no more than 17 characters.')
        # Byte mode prefix 0100.
        bitstring = '0100'
        # Character count in 8 binary bits.
        bitstring += '{:08b}'.format(len(data))
        # Encode every character in ISO-8859-1 in 8 binary bits.
        for c in data:
            bitstring += '{:08b}'.format(ord(c.encode('iso-8859-1')))
        # Terminator 0000.
        bitstring += '0000'
        res = list()
        # Convert string to byte numbers.
        while bitstring:
            res.append(int(bitstring[:8], 2))
            bitstring = bitstring[8:]
        # Add padding pattern.
        while len(res) < 19:
            res.append(int('11101100', 2))
            res.append(int('00010001', 2))
        # Slice to 19 bytes for V1-L.
        res = res[:19]
        # Call RSEnc to add 7 EC bits.
        return _.RSEnc(res, 7)
    
    def fillbt(_,byte, downwards=False):
        '''
        Fill a byte into a 2 by 4 matrix upwards,
        unless specified downwards.
        Upwards:    Downwards:
            0|1         6|7
            -+-         -+-
            2|3         4|5
            -+-         -+-
            4|5         2|3
            -+-         -+-
            6|7         0|1
        '''
        _.ia=_.ia+1
        if _.ia+1>5:
            _.ia=0
            _.ja=_.ja+1
        
        bytestr = '{:08b}'.format(byte)
        res = [[0, 0] for i in range(4)]
        for i in range(8):
            
            res[i // 2][i % 2] = not int(bytestr[7-i])
        if downwards:
            res = res[::-1]
        _.gr.add(_.drawGrid(res,4,2).shift(_.ia*1*RIGHT+_.ja*1.5*DOWN))
        _.add(_.gr)
        _.wait(0.3)
        _.remove(_.gr)
        return res

    def copyFrom(_,src, dst, top, left):
        '''
        Copy the content of matrix src into matrix dst.
        The top-left corner of src is positioned at (left, top)
        in dst.
        '''
        res = copy.deepcopy(dst)
        for j in range(len(src)):
            for i in range(len(src[0])):
                res[top+j][left+i] = src[j][i]
        return res

    def _fillData(_,bitstream):
        '''Fill the encoded data into the template QR code matrix'''
        res = copy.deepcopy(_.ver1Temp)
        for i in range(15):
            res = _.copyFrom(_.fillbt(bitstream[i], (i//3) % 2 != 0),
                        res,
                        21-4*((i % 3-1)*(-1)**((i//3) % 2)+2),
                        21-2*(i//3+1))
        tmp = _.fillbt(bitstream[15])
        res = _.copyFrom(tmp[2:], res, 7, 11)
        res = _.copyFrom(tmp[:2], res, 4, 11)
        tmp = _.fillbt(bitstream[16])
        res = _.copyFrom(tmp, res, 0, 11)
        tmp = _.fillbt(bitstream[17], True)
        res = _.copyFrom(tmp, res, 0, 9)
        tmp = _.fillbt(bitstream[18], True)
        res = _.copyFrom(tmp[:2], res, 4, 9)
        res = _.copyFrom(tmp[2:], res, 7, 9)
        for i in range(3):
            res = _.copyFrom(_.fillbt(bitstream[19+i], True),
                        res, 9+4*i, 9)
        tmp = _.fillbt(bitstream[22])
        res = _.copyFrom(tmp, res, 9, 7)
        for i in range(3):
            res = _.copyFrom(_.fillbt(bitstream[23+i], i % 2 == 0),
                        res, 9, 4-2*i)
        _.play(Transform(_.gr,_.drawGrid(res,21,21)))
        # Generate image after filling data for debug use.
        
       
        return res

    def _fillInfo(_,arg):
        '''
        Fill the encoded format code into the masked QR code matrix.
        arg: (masked QR code matrix, mask number).
        '''
        mat, mask = arg
        # 01 is the format code for L error control level,
        # concatenated with mask id and passed into _fmtEncode
        # to get the 15 bits format code with EC bits.
        fmt = _._fmtEncode(int('01'+'{:03b}'.format(mask), 2))
        fmtarr = [[not int(c)] for c in '{:015b}'.format(fmt)]
        mat = _.copyFrom(_.transpose(fmtarr[7:]), mat, 8, 13)
        mat = _.copyFrom(fmtarr[9:][::-1], mat, 0, 8)
        mat = _.copyFrom(fmtarr[7:9][::-1], mat, 7, 8)
        mat = _.copyFrom(fmtarr[:7][::-1], mat, 14, 8)
        mat = _.copyFrom(_.transpose(fmtarr[:6]), mat, 8, 0)
        mat = _.copyFrom([fmtarr[6]], mat, 8, 7)
        return mat

    def _penalty(_,mat):
        '''
        Calculate penalty score for a masked matrix.
        N1: penalty for more than 5 consecutive pixels in row/column,
            3 points for each occurrence of such pattern,
            and extra 1 point for each pixel exceeding 5
            consecutive pixels.
        N2: penalty for blocks of pixels larger than 2x2.
            3*(m-1)*(n-1) points for each block of mxn
            (larger than 2x2).
        N3: penalty for patterns similar to the finder pattern.
            40 points for each occurrence of 1:1:3:1:1 ratio
            (dark:light:dark:light:dark) pattern in row/column,
            preceded of followed by 4 consecutive light pixels.
        N4: penalty for unbalanced dark/light ratio.
            10*k points where k is the rating of the deviation of
            the proportion of dark pixels from 50% in steps of 5%.
        '''
        # Initialize.
        n1 = n2 = n3 = n4 = 0
        # Calculate N1.

        def getN1(mat, strategy):
            n1 = 0
            for j in range(len(mat)):
                count = 1
                adj = False
                for i in range(1, len(mat)):
                    if strategy == "j":
                        compare = mat[j][i-1]
                    elif strategy == "i":
                        i, j = j, i
                        compare = mat[j-1][i]
                    if mat[j][i] == compare:
                        count += 1
                    else:
                        count = 1
                        adj = False
                    if count >= 5:
                        if not adj:
                            adj = True
                            n1 += 3
                        else:
                            n1 += 1
            return n1

        n1 = getN1(mat, "i") + getN1(mat, "j")

        # Calculate N2.
        m = n = 1
        for j in range(1, len(mat)):
            for i in range(1, len(mat)):
                if (mat[j][i] == mat[j-1][i] and mat[j][i] == mat[j][i-1] and
                    mat[j][i] == mat[j-1][i-1]):
                    if mat[j][i] == mat[j-1][i]:
                        m += 1
                    if mat[j][i] == mat[j][i-1]:
                        n += 1
                else:
                    n2 += 3 * (m-1) * (n-1)
                    m = n = 1

        # Calculate N3.
        count = 0

        def getCount(mat):
            count = 0
            for row in mat:
                rowstr = ''.join(str(e) for e in row)
                occurrences = []
                begin = 0
                while rowstr.find('0100010', begin) != -1:
                    begin = rowstr.find('0100010', begin) + 7
                    occurrences.append(begin)
                for begin in occurrences:
                    if (rowstr.count('00000100010', begin-4) != 0 or
                        rowstr.count('01000100000', begin) != 0):
                        count += 1
            return count

        transposedMat = _.transpose(mat)
        n3 += 40 * (getCount(mat)+getCount(transposedMat))

        # Calculate N4.
        dark = sum(row.count(_.DARK) for row in mat)
        percent = int((float(dark) / float(len(mat)**2)) * 100)
        pre = percent - percent % 5
        nex = percent + 5 - percent % 5
        n4 = min(abs(pre-50)//5, abs(nex-50)//5) * 10

        # Return final penalty score.
        return n1 + n2 + n3 + n4

    def logicAnd(_,mat1, mat2):
        '''
        Matrix-wise and.
        Dark and dark -> dark
        Light and light -> light
        Dark and light -> light
        Light and dark -> light
        '''
        res = [[True for i in range(len(mat1[0]))] for j in range(len(mat1))]
        for j in range(len(mat1)):
            for i in range(len(mat1[0])):
                res[j][i] = mat1[j][i] or mat2[j][i]
        return res

    def logicOr(_,mat1, mat2):
        """
        B + B -> B
        B + W -> B
        W + W -> W
        """
        res = [[False for i in range(len(mat1[0]))] for j in range(len(mat1))]
        for j in range(len(mat1)):
            for i in range(len(mat1[0])):
                res[j][i] = mat1[j][i] and mat2[j][i]
        return res

    def logicNot(_,mat1):
        res = [[False for i in range(len(mat1[0]))] for j in range(len(mat1))]
        for j in range(len(mat1)):
            for i in range(len(mat1[0])):
                res[j][i] = not mat1[j][i]
        return res

    def logicXor(_,mat1, mat2):
        '''
        Matrix-wise xor.
        Dark xor dark -> light
        Light xor light -> light
        Dark xor light -> dark
        Light xor dark -> dark
        '''
        res = [[True for i in range(len(mat1[0]))] for j in range(len(mat1))]
        for j in range(len(mat1)):
            for i in range(len(mat1[0])):
                res[j][i] = mat1[j][i] == mat2[j][i]
        return res

    def _mask(_,mat):
        '''
        Mask the data QR code matrix with all 8 masks,
        call _penalty to calculate penalty scores for each
        and select the best mask.
        Return tuple(selected masked matrix, number of selected mask).
        '''
        maskeds = [_.logicXor(mat, dataMask) for dataMask in _.dataMasks]
        penalty = [0] * 8
        for i, masked in enumerate(maskeds):
            penalty[i] = _._penalty(masked)
            # Print penalty scores for debug use.
            if True:
                print('penalty for mask {}: {}'.format(i, penalty[i]))
        # Find the id of the best mask.
        selected = penalty.idxes(min(penalty))
        # Print selected mask and penalty score,
        # and generate image for masked QR code for debug use.
        if True:
            print('mask {} selected with penalty {}'.format(selected,
                                                            penalty[selected]))
            
        return maskeds[selected], selected

    def gbit(_,bitstream):
        '''
        Take in the encoded data stream and generate the
        final QR code bitmap.
        '''
        return _._fillInfo(_._mask(_._fillData(bitstream)))


class ShowTextAndSayMode(GraphScene):
    def construct(_):
        _.gr = VGroup()
        _.init()
        ss = VGroup()
        t = _.encd("Demo")
        
        t0=TextMobject("D","e","m","o");
        t1=TextMobject("0100","00000100","01000100","01100101","01101101","01101111","0000").scale(0.8)
        vgg = VGroup(t0,t1)
        vgg.arrange(DOWN).shift(2*UP)
        t1.shift(DOWN)
        _.play(Write(t0))
        _.play(t0[0].set_color,BLUE,t0[2].set_color,BLUE)
        t1[2].set_color(BLUE)
        t1[4].set_color(BLUE)
        t1[0].set_color(YELLOW)
        t1[1].set_color(GREEN)
        t1[6].set_color(YELLOW)
        _.play(Write(t1[0]))
        _.play(ShowCreationThenDestructionAround(t1[0]))
        _.wait()
        text=Text("len=4",font="Consolas").scale(0.5)
        _.play(Write(text))
        _.wait()
        _.play(ReplacementTransform(text,t1[1]))
        _.play(ReplacementTransform(t0[0].copy(),t1[2]))
        _.play(ReplacementTransform(t0[1].copy(),t1[3]))
        _.play(ReplacementTransform(t0[2].copy(),t1[4]))
        _.play(ReplacementTransform(t0[3].copy(),t1[5]))
        _.play(Write(t1[6]))
        _.play(ShowCreationThenDestructionAround(t1[6]))
        _.wait()
        t3=TextMobject("01000000","01000100","01000110","01010110","11010110","11110000").scale(0.8).shift(0.7*UP)
        t3[0].set_color(RED)
        t3[1].set_color(GREEN)
        t3[2].set_color(YELLOW)
        t3[4].set_color(BLUE)
        _.play(FadeOut(t1),FadeIn(t3))
        t4=TextMobject("[","64,","68,","70,","86,","214,","240,","236,","17,","236,","17,","236,","17,","236,","17,","236,","17,","236,","17,","236]").scale(0.5)
        for i in range(0,6):
            _.play(ReplacementTransform(t3[i].copy(),t4[i+1]))
        _.play(Write(t4[0]))
        _.wait()
        s1 =Text("11101100",font="Consolas").shift(2*DOWN).scale(0.3)
        s2 =Text("00010001",font="Consolas").shift(2*DOWN+2*RIGHT).scale(0.3)
        _.play(Write(s1),Write(s2))
        _.wait()
        _.play(ReplacementTransform(s1,t4[7])) 
        _.play(ReplacementTransform(s2,t4[8])) 
        for i in range(9,len(t4)):
            _.play(Write(t4[i])) 
        t5=TextMobject("[","64,","68,","70,","86,","214,","240,","236,","17,","236,","17,","236,","17,","236,","17,","236,","17,","236,","17,","236, 17, 236, 17, 236, 145, 154, 132, 52, 230, 111, 236]").scale(0.6)
        _.wait()
        _.play(ReplacementTransform(t4,t5),run_time=5)
        _.wait()
    def drawGrid(_,src,ii,jj):
        vg = VMobject()
        for i in range(ii):
            for j in range(jj):
                if src[i][j]==False:
                    s = Rectangle(width=0.3,height=0.3,fill_color=GREEN,fill_opacity=1).shift(0.3*i*DOWN+0.3*j*RIGHT).shift(3*LEFT+3*UP)
                    vg.add(s)
                else:
                    s = Rectangle(width=0.3,height=0.3,fill_color=WHITE,fill_opacity=1).shift(0.3*i*DOWN+0.3*j*RIGHT).shift(3*LEFT+3*UP)
                    vg.add(s)
        return vg
        
    def init(_):
        _.DARK=0
        _.LIGHT=1
        _._gfExp = [0] * 512
        _._gfLog = [0] * 256
        _._gfPrim = 0x11d

        _x = 1

        for i in range(255):
            _._gfExp[i] = _x
            _._gfLog[_x] = i
            _x = _.GFMul(_x, 2)

        for i in range(255, 512):
            _._gfExp[i] = _._gfExp[i-255]

        _._finder = _.copyFrom(
                _.copyFrom(
                    [[_.DARK for i in range(3)] for j in range(3)],
                    [[_.LIGHT for i in range(5)] for j in range(5)],
                    1, 1
                ),
                [[_.DARK for i in range(7)] for j in range(7)], 1, 1
            )


        # Alignment pattern. Not used in version 1.
        _align = _.copyFrom(
            _.copyFrom(
                [[_.DARK]],
                [[_.LIGHT for i in range(3)] for j in range(3)], 1, 1
            ),
            [[_.DARK for i in range(5)] for j in range(5)], 1, 1
        )

        # Version 1 QR code template with finder patterns and timing sequences.
        _.ver1Temp = [[_.LIGHT for i in range(21)] for j in range(21)]
        _.ver1Temp = _.copyFrom(_._finder, _.ver1Temp, 0, 0)
        _.ver1Temp = _.copyFrom(_._finder, _.ver1Temp, 14, 0)
        _.ver1Temp = _.copyFrom(_._finder, _.ver1Temp, 0, 14)
        _.ver1Temp = _.copyFrom(_._timSeq(5), _.ver1Temp, 6, 8)
        _.ver1Temp = _.copyFrom(_._timSeq(5, vertical=True), _.ver1Temp, 8, 6)
        _.ver1Temp = _.copyFrom([[_.DARK]], _.ver1Temp, 13, 8)

        # Data area mask to avoid applying masks to functional area.
        _._dataAreaMask = [[_.DARK for i in range(21)] for j in range(21)]
        _._dataAreaMask = _.copyFrom([[_.LIGHT for i in range(9)] for j in range(9)],
                                _._dataAreaMask, 0, 0)
        _._dataAreaMask = _.copyFrom([[_.LIGHT for i in range(9)] for j in range(8)],
                                _._dataAreaMask, 13, 0)
        _._dataAreaMask = _.copyFrom([[_.LIGHT for i in range(8)] for j in range(9)],
                                _._dataAreaMask, 0, 13)
        _._dataAreaMask = _.copyFrom([[_.LIGHT for i in range(4)]], _._dataAreaMask, 6, 9)
        _._dataAreaMask = _.copyFrom([[_.LIGHT] for i in range(4)], _._dataAreaMask, 9, 6)
        _._maskList = [
                [
                    [
                        _.DARK if _.mdk(c, i, j)
                        else _.LIGHT for i in range(21)
                    ] for j in range(21)
                ] for c in range(8)
            ]
        _.dataMasks = [_.logicAnd(_._dataAreaMask, mask) for mask in _._maskList]

    def mdk(_,idxes, i, j):
        if idxes == 0:
            poli = (i+j) % 2
        elif idxes == 1:
            poli = j % 2
        elif idxes == 2:
            poli = i % 3
        elif idxes == 3:
            poli = (i+j) % 3
        elif idxes == 4:
            poli = (j//2 + i//3) % 2
        elif idxes == 5:
            poli = (i*j) % 2+(i*j) % 3
        elif idxes == 6:
            poli = ((i*j) % 2+(i*j) % 3) % 2
        elif idxes == 7:
            poli = ((i+j) % 2+(i*j) % 3) % 2
        return poli == 0

    def GFMul(_,x=2, y=2, prim=0x11d, field_charac_full=256, carryless=True):
        '''Galois field GF(2^8) multiplication.'''
        rr = 0
        while y:
            if y & 1:
                rr = rr ^ x if carryless else rr + x
            y = y >> 1
            x = x << 1
            if prim > 0 and x & field_charac_full:
                x = x ^ prim
        return rr

    def RSEnc(_,bitstring, nsym):
        '''Encode bitstring with nsym EC bits using RS algorithm.'''
        gen = _._rsGenPoly(nsym)
        res = [0] * (len(bitstring) + len(gen) - 1)
        res[:len(bitstring)] = bitstring
        for i in range(len(bitstring)):
            coef = res[i]
            if coef != 0:
                for j in range(1, len(gen)):
                    res[i+j] ^= _._gfMul(gen[j], coef)
        res[:len(bitstring)] = bitstring
        return res

    def _gfMul(_,x, y):
        '''Simplified GF multiplication.'''
        if x == 0 or y == 0:
            return 0
        return _._gfExp[_._gfLog[x] + _._gfLog[y]]

    def transpose(_,mat):
        '''Transpose a matrix'''
        res = [[mat[j][i] for j in range(len(mat))] for i in range(len(mat[0]))]
        return res

    def _timSeq(_,len, vertical=False):
        '''
        Generate a horizontal, unless specified vertical
        timing sequence with alternating dark and light
        pixels with length len.
        '''
        res = [[i % 2 for i in range(len)]]
        if vertical:
            res = _.transpose(res)
        return res

    def _gfPolyMul(_,p, q):
        '''GF polynomial multiplication.'''
        r = [0] * (len(p) + len(q) - 1)
        for j in range(len(q)):
            for i in range(len(p)):
                r[i+j] ^= _._gfMul(p[i], q[j])
        return r

    def _gfPolyDiv(_,dividend, divisor):
        '''GF polynomial division.'''
        res = list(dividend)
        for i in range(len(dividend) - len(divisor) + 1):
            coef = res[i]
            if coef != 0:
                for j in range(1, len(divisor)):
                    if divisor[j] != 0:
                        res[i+j] ^= _gfMul(divisor[j], coef)
        sep = -(len(divisor) - 1)
        return res[:sep], res[sep:]

    def _gfPow(_,x, pow):
        '''GF power.'''
        return _._gfExp[(_._gfLog[x] * pow) % 255]

    def _rsGenPoly(_,nsym):
        '''Generate generator polynomial for RS algorithm.'''
        g = [1]
        for i in range(nsym):
            g = _._gfPolyMul(g, [1, _._gfPow(2, i)])
        return g

    def _fmtEncode(_,fmt):
        '''Encode the 15-bit format code using BCH code.'''
        g = 0x537
        code = fmt << 10
        for i in range(4, -1, -1):
            if code & (1 << (i+10)):
                code ^= g << i
        return ((fmt << 10) ^ code) ^ 0b101010000010010

    def encd(_,data):
        '''
        Encode the input data stream.
        Add mode prefix, encode data using ISO-8859-1,
        group data, add padding suffix, and call RS encoding method.
        '''
        if len(data) > 17:
            print('Error: Version 1 QR code encodes no more than 17 characters.')
        # Byte mode prefix 0100.
        bitstring = '0100'
        print(bitstring)
        # Character count in 8 binary bits.
        bitstring += '{:08b}'.format(len(data))
        print(bitstring)
        # Encode every character in ISO-8859-1 in 8 binary bits.
        for c in data:
            bitstring += '{:08b}'.format(ord(c.encode('iso-8859-1')))
            print(bitstring)
        # Terminator 0000.
        bitstring += '0000'
        print(bitstring)
        res = list()
        # Convert string to byte numbers.
        while bitstring:
            res.append(int(bitstring[:8], 2))
            bitstring = bitstring[8:]
        # Add padding pattern.
        while len(res) < 19:
            res.append(int('11101100', 2))
            res.append(int('00010001', 2))
        # Slice to 19 bytes for V1-L.
        res = res[:19]
        print(res)
        # Call RSEnc to add 7 EC bits.
        print(_.RSEnc(res, 7))
        return _.RSEnc(res, 7)
    
    def fillbt(_,byte, downwards=False):
        '''
        Fill a byte into a 2 by 4 matrix upwards,
        unless specified downwards.
        Upwards:    Downwards:
            0|1         6|7
            -+-         -+-
            2|3         4|5
            -+-         -+-
            4|5         2|3
            -+-         -+-
            6|7         0|1
        '''
        bytestr = '{:08b}'.format(byte)
        res = [[0, 0] for i in range(4)]
        for i in range(8):
            
            res[i // 2][i % 2] = not int(bytestr[7-i])
        if downwards:
            res = res[::-1]
        _.gr.add(_.drawGrid(res,4,2))
        _.play(FadeInFromDown(_.gr))
        _.wait(0.2)
        _.play(FadeOutAndShift(_.gr,direction=UP))
        return res

    def copyFrom(_,src, dst, top, left):
        '''
        Copy the content of matrix src into matrix dst.
        The top-left corner of src is positioned at (left, top)
        in dst.
        '''
        res = copy.deepcopy(dst)
        for j in range(len(src)):
            for i in range(len(src[0])):
                res[top+j][left+i] = src[j][i]
        return res

    def _fillData(_,bitstream):
        '''Fill the encoded data into the template QR code matrix'''
        res = copy.deepcopy(_.ver1Temp)
        for i in range(15):
            res = _.copyFrom(_.fillbt(bitstream[i], (i//3) % 2 != 0),
                        res,
                        21-4*((i % 3-1)*(-1)**((i//3) % 2)+2),
                        21-2*(i//3+1))
        tmp = _.fillbt(bitstream[15])
        res = _.copyFrom(tmp[2:], res, 7, 11)
        res = _.copyFrom(tmp[:2], res, 4, 11)
        tmp = _.fillbt(bitstream[16])
        res = _.copyFrom(tmp, res, 0, 11)
        tmp = _.fillbt(bitstream[17], True)
        res = _.copyFrom(tmp, res, 0, 9)
        tmp = _.fillbt(bitstream[18], True)
        res = _.copyFrom(tmp[:2], res, 4, 9)
        res = _.copyFrom(tmp[2:], res, 7, 9)
        for i in range(3):
            res = _.copyFrom(_.fillbt(bitstream[19+i], True),
                        res, 9+4*i, 9)
        tmp = _.fillbt(bitstream[22])
        res = _.copyFrom(tmp, res, 9, 7)
        for i in range(3):
            res = _.copyFrom(_.fillbt(bitstream[23+i], i % 2 == 0),
                        res, 9, 4-2*i)
        _.play(Transform(_.gr,_.drawGrid(res,21,21)))
        # Generate image after filling data for debug use.
        
       
        return res

    def _fillInfo(_,arg):
        '''
        Fill the encoded format code into the masked QR code matrix.
        arg: (masked QR code matrix, mask number).
        '''
        mat, mask = arg
        # 01 is the format code for L error control level,
        # concatenated with mask id and passed into _fmtEncode
        # to get the 15 bits format code with EC bits.
        fmt = _._fmtEncode(int('01'+'{:03b}'.format(mask), 2))
        fmtarr = [[not int(c)] for c in '{:015b}'.format(fmt)]
        mat = _.copyFrom(_.transpose(fmtarr[7:]), mat, 8, 13)
        mat = _.copyFrom(fmtarr[9:][::-1], mat, 0, 8)
        mat = _.copyFrom(fmtarr[7:9][::-1], mat, 7, 8)
        mat = _.copyFrom(fmtarr[:7][::-1], mat, 14, 8)
        mat = _.copyFrom(_.transpose(fmtarr[:6]), mat, 8, 0)
        mat = _.copyFrom([fmtarr[6]], mat, 8, 7)
        return mat

    def _penalty(_,mat):
        '''
        Calculate penalty score for a masked matrix.
        N1: penalty for more than 5 consecutive pixels in row/column,
            3 points for each occurrence of such pattern,
            and extra 1 point for each pixel exceeding 5
            consecutive pixels.
        N2: penalty for blocks of pixels larger than 2x2.
            3*(m-1)*(n-1) points for each block of mxn
            (larger than 2x2).
        N3: penalty for patterns similar to the finder pattern.
            40 points for each occurrence of 1:1:3:1:1 ratio
            (dark:light:dark:light:dark) pattern in row/column,
            preceded of followed by 4 consecutive light pixels.
        N4: penalty for unbalanced dark/light ratio.
            10*k points where k is the rating of the deviation of
            the proportion of dark pixels from 50% in steps of 5%.
        '''
        # Initialize.
        n1 = n2 = n3 = n4 = 0
        # Calculate N1.

        def getN1(mat, strategy):
            n1 = 0
            for j in range(len(mat)):
                count = 1
                adj = False
                for i in range(1, len(mat)):
                    if strategy == "j":
                        compare = mat[j][i-1]
                    elif strategy == "i":
                        i, j = j, i
                        compare = mat[j-1][i]
                    if mat[j][i] == compare:
                        count += 1
                    else:
                        count = 1
                        adj = False
                    if count >= 5:
                        if not adj:
                            adj = True
                            n1 += 3
                        else:
                            n1 += 1
            return n1

        n1 = getN1(mat, "i") + getN1(mat, "j")

        # Calculate N2.
        m = n = 1
        for j in range(1, len(mat)):
            for i in range(1, len(mat)):
                if (mat[j][i] == mat[j-1][i] and mat[j][i] == mat[j][i-1] and
                    mat[j][i] == mat[j-1][i-1]):
                    if mat[j][i] == mat[j-1][i]:
                        m += 1
                    if mat[j][i] == mat[j][i-1]:
                        n += 1
                else:
                    n2 += 3 * (m-1) * (n-1)
                    m = n = 1

        # Calculate N3.
        count = 0

        def getCount(mat):
            count = 0
            for row in mat:
                rowstr = ''.join(str(e) for e in row)
                occurrences = []
                begin = 0
                while rowstr.find('0100010', begin) != -1:
                    begin = rowstr.find('0100010', begin) + 7
                    occurrences.append(begin)
                for begin in occurrences:
                    if (rowstr.count('00000100010', begin-4) != 0 or
                        rowstr.count('01000100000', begin) != 0):
                        count += 1
            return count

        transposedMat = _.transpose(mat)
        n3 += 40 * (getCount(mat)+getCount(transposedMat))

        # Calculate N4.
        dark = sum(row.count(_.DARK) for row in mat)
        percent = int((float(dark) / float(len(mat)**2)) * 100)
        pre = percent - percent % 5
        nex = percent + 5 - percent % 5
        n4 = min(abs(pre-50)//5, abs(nex-50)//5) * 10

        # Return final penalty score.
        return n1 + n2 + n3 + n4

    def logicAnd(_,mat1, mat2):
        '''
        Matrix-wise and.
        Dark and dark -> dark
        Light and light -> light
        Dark and light -> light
        Light and dark -> light
        '''
        res = [[True for i in range(len(mat1[0]))] for j in range(len(mat1))]
        for j in range(len(mat1)):
            for i in range(len(mat1[0])):
                res[j][i] = mat1[j][i] or mat2[j][i]
        return res

    def logicOr(_,mat1, mat2):
        """
        B + B -> B
        B + W -> B
        W + W -> W
        """
        res = [[False for i in range(len(mat1[0]))] for j in range(len(mat1))]
        for j in range(len(mat1)):
            for i in range(len(mat1[0])):
                res[j][i] = mat1[j][i] and mat2[j][i]
        return res

    def logicNot(_,mat1):
        res = [[False for i in range(len(mat1[0]))] for j in range(len(mat1))]
        for j in range(len(mat1)):
            for i in range(len(mat1[0])):
                res[j][i] = not mat1[j][i]
        return res

    def logicXor(_,mat1, mat2):
        '''
        Matrix-wise xor.
        Dark xor dark -> light
        Light xor light -> light
        Dark xor light -> dark
        Light xor dark -> dark
        '''
        res = [[True for i in range(len(mat1[0]))] for j in range(len(mat1))]
        for j in range(len(mat1)):
            for i in range(len(mat1[0])):
                res[j][i] = mat1[j][i] == mat2[j][i]
        return res

    def _mask(_,mat):
        '''
        Mask the data QR code matrix with all 8 masks,
        call _penalty to calculate penalty scores for each
        and select the best mask.
        Return tuple(selected masked matrix, number of selected mask).
        '''
        maskeds = [_.logicXor(mat, dataMask) for dataMask in _.dataMasks]
        penalty = [0] * 8
        for i, masked in enumerate(maskeds):
            penalty[i] = _._penalty(masked)
            # Print penalty scores for debug use.
            if True:
                print('penalty for mask {}: {}'.format(i, penalty[i]))
        # Find the id of the best mask.
        selected = penalty.idxes(min(penalty))
        # Print selected mask and penalty score,
        # and generate image for masked QR code for debug use.
        if True:
            print('mask {} selected with penalty {}'.format(selected,
                                                            penalty[selected]))
            
        return maskeds[selected], selected

    def gbit(_,bitstream):
        '''
        Take in the encoded data stream and generate the
        final QR code bitmap.
        '''
        return _._fillInfo(_._mask(_._fillData(bitstream)))


class Des(Scene):
    def construct(_):
        ori = TextMobject("0","0","1","0","1","1","0","0")
        primo = PrimoCreature(color=BLUE).shift(2*DOWN+4*LEFT).look_at(ori)
        _.play(FadeIn(primo))
        _.play(Write(ori))
        _.wait()
        _.wait()
        _.play(ApplyWave(ori))
        _.play(ori.shift,2*UP,)
        primo.look_at(ori)

        ve = Arrow(2*UP,0.2*UP,color=YELLOW)
        _.play(Write(ve))
        _.wait()
        trans = TextMobject("0","1","1","0","0","1","0","0")
        _.play(ReplacementTransform(ori.copy(),trans),run_time=3)
        _.wait()
        _.play(ori.shift,2*RIGHT)
        oriii = TextMobject("???").shift(2*UP)
        _.play(Rotate(ve,PI))
        _.play(Write(oriii))
        _.wait()

        _.play(FadeOut(oriii),FadeOut(trans))
        _.play(Rotate(ve,PI))
        _.play(ori.shift,2*LEFT)
        oriiii = TextMobject("XXXX")
        oriiii.next_to(ori)
        _.play(Write(oriiii))
        _.wait()

        palabras_ale = TextMobject("Pause and pounder...")
        _.play(PrimoCreatureSays(
            primo, palabras_ale,
            bubble_kwargs={"height": 2, "width": 3},
            target_mode="plain"
        ))

        palabras_ale = TextMobject("Jump out of 0-1 bits!")
        _.play(PrimoCreatureSays(
            primo, palabras_ale,
            bubble_kwargs={"height": 2, "width": 3},
            target_mode="plain"
        ))


class func(GraphScene):
    CONFIG = {
        "x_min" : -5,
        "x_max" : 5,
        "y_min" : -3,
        "y_max" : 3,
        "graph_origin" : ORIGIN ,
        "function_color" : RED ,
        "axes_color" : GREEN,
        "x_labeled_nums" :range(-3,3,2),
        "y_labeled_nums" :range(-3,3,1),
    }
    def construct(_):
        _.setup_axes(animate=True)
         
        f1 = _.get_graph(lambda x : x+1)
        f1.get_point_from_function(0)
        e=Dot(np.array([0,1,0]))
        f=Dot(np.array([0.9,2,0]))
        _.play(FadeInFromLarge(e))
        _.play(Write(f1))
        _.play(Rotate(f1,PI),run_time=3)
        _.play(Rotate(f1,-PI),run_time=3)
        _.play(FadeInFromLarge(f))
        _.play(Rotate(f1,PI/18),run_time=0.2)
        _.play(Rotate(f1,-PI/18),run_time=0.2)
        _.wait()

        _.play(FadeOut(f1))

        v = ValueTracker(value=1)

        

        def g2(obj):
            obj.become(_.get_graph(lambda x: v.get_value()*x**2+(1-v.get_value())*x+1,color=YELLOW)) 
        f2 = _.get_graph(lambda x : x**2+1).add_updater(g2)
        f2.color=YELLOW
        _.play(Write(f2))
        _.play(v.increment_value,5.0,rate_func=wiggle,run_time=3)
        _.play(v.increment_value,-3.0,rate_func=wiggle,run_time=5)
        g=Dot(np.array([-0.9,2,0]))
        _.play(FadeInFromLarge(g))
        _.play(v.increment_value,0.1,rate_func=wiggle,run_time=1)

        h = TexMobject("f(x)= \\sum _{i=1}^{n}y_i\\prod _{j=1,j \\neq i}^n \\frac{x-x_j}{x_i-x_j}")\
            .shift(2*DOWN).add_background_rectangle()
        
        _.play(Write(h),run_time=5)

        _.wait()
        _.play(FadeOut(h))
        n1=Dot(np.array([-0.5,(0.25+1+0.05),0]),color=YELLOW)
        n2=Dot(np.array([0.5,(0.25+1+0.05),0]),color=YELLOW)
        _.play(FadeInFromLarge(n1),FadeInFromLarge(n2))
        _.wait()
        _.play(FadeOut(f2))

        _.play(g.shift,UP)
        _.wait(3)
        f3 = _.get_graph(lambda x : (3/2)*x**2+(-1/2)*x+1)
        _.play(Write(f3))
        t = Text("Matched 3 points...",font="Consolas").scale(0.5).shift(2*DOWN).add_background_rectangle()
        _.play(Write(t))
        _.wait()
        _.play(e.scale,0.5,
                f.scale,0.5,
                g.scale,0.5,
                n1.scale,0.5,
                n2.scale,0.5,)
        _.wait()
        _.play(FadeOutAndShiftDown(f3))
        _.wait()
        _.play(Write(f2))
        _.wait()
        _.play(FadeOut(t))
        _.play(e.scale,2,
                f.scale,2,
                g.scale,2,
                n1.scale,2,
                n2.scale,2,)
        t = Text("Matched 4 points!!!",font="Consolas").scale(0.5).shift(2*DOWN).add_background_rectangle()
        _.play(Write(t))
        _.wait()
        _.play(FadeOut(t))
        _.play(g.shift,DOWN)


class xordesc(ThreeDScene):
    def construct(_):
        _.begin_ambient_camera_rotation(rate=0.2)
        _.move_camera(phi=45*DEGREES,theta=80*DEGREES,gamma=0*DEGREES,run_time=3)
        _.wait()
        _.init()
        t = _.drawGrid(_._fillData(_.encd("Demo")),21,21)
        tt = _.drawGrid(_._maskList[2],21,21)
        _.play(Write(t))
        _.play(Write(tt.shift(np.array([0,0,1]))))
        _.move_camera(phi=25*DEGREES,theta=50*DEGREES,gamma=0*DEGREES,run_time=3)

        _.move_camera(phi=80*DEGREES,theta=80*DEGREES,gamma=0*DEGREES,run_time=3)
        _.wait(3)

        _.play(tt.shift,(np.array([0,0,-1])))

        ttt = _.drawGrid(_.gbit(_.encd("Demo")),21,21)
        _.play(Write(ttt))
        _.move_camera(phi=45*DEGREES,theta=80*DEGREES,gamma=0*DEGREES,run_time=3)
        

    def drawGrid(_,src,ii,jj):
        vg = VGroup()
        for i in range(ii):
            for j in range(jj):
                if src[i][j]==False:
                    s = Rectangle(width=0.3,height=0.3,stroke_width=0,fill_color=WHITE,fill_opacity=1).shift(0.3*i*DOWN+0.3*j*RIGHT).shift(3*LEFT+3*UP)
                    vg.add(s)
                else:
                    s = Rectangle(width=0.3,height=0.3,stroke_width=0,fill_color=GREY,fill_opacity=1).shift(0.3*i*DOWN+0.3*j*RIGHT).shift(3*LEFT+3*UP)
                    vg.add(s)
        return vg
        
    def init(_):
        _.DARK=0
        _.LIGHT=1
        _._gfExp = [0] * 512
        _._gfLog = [0] * 256
        _._gfPrim = 0x11d

        _x = 1

        for i in range(255):
            _._gfExp[i] = _x
            _._gfLog[_x] = i
            _x = _.GFMul(_x, 2)

        for i in range(255, 512):
            _._gfExp[i] = _._gfExp[i-255]

        _._finder = _.copyFrom(
                _.copyFrom(
                    [[_.DARK for i in range(3)] for j in range(3)],
                    [[_.LIGHT for i in range(5)] for j in range(5)],
                    1, 1
                ),
                [[_.DARK for i in range(7)] for j in range(7)], 1, 1
            )


        # Alignment pattern. Not used in version 1.
        _align = _.copyFrom(
            _.copyFrom(
                [[_.DARK]],
                [[_.LIGHT for i in range(3)] for j in range(3)], 1, 1
            ),
            [[_.DARK for i in range(5)] for j in range(5)], 1, 1
        )

        # Version 1 QR code template with finder patterns and timing sequences.
        _.ver1Temp = [[_.LIGHT for i in range(21)] for j in range(21)]
        _.ver1Temp = _.copyFrom(_._finder, _.ver1Temp, 0, 0)
        _.ver1Temp = _.copyFrom(_._finder, _.ver1Temp, 14, 0)
        _.ver1Temp = _.copyFrom(_._finder, _.ver1Temp, 0, 14)
        _.ver1Temp = _.copyFrom(_._timSeq(5), _.ver1Temp, 6, 8)
        _.ver1Temp = _.copyFrom(_._timSeq(5, vertical=True), _.ver1Temp, 8, 6)
        _.ver1Temp = _.copyFrom([[_.DARK]], _.ver1Temp, 13, 8)

        # Data area mask to avoid applying masks to functional area.
        _._dataAreaMask = [[_.DARK for i in range(21)] for j in range(21)]
        _._dataAreaMask = _.copyFrom([[_.LIGHT for i in range(9)] for j in range(9)],
                                _._dataAreaMask, 0, 0)
        _._dataAreaMask = _.copyFrom([[_.LIGHT for i in range(9)] for j in range(8)],
                                _._dataAreaMask, 13, 0)
        _._dataAreaMask = _.copyFrom([[_.LIGHT for i in range(8)] for j in range(9)],
                                _._dataAreaMask, 0, 13)
        _._dataAreaMask = _.copyFrom([[_.LIGHT for i in range(4)]], _._dataAreaMask, 6, 9)
        _._dataAreaMask = _.copyFrom([[_.LIGHT] for i in range(4)], _._dataAreaMask, 9, 6)
        _._maskList = [
                [
                    [
                        _.DARK if _.mdk(c, i, j)
                        else _.LIGHT for i in range(21)
                    ] for j in range(21)
                ] for c in range(8)
            ]
        _.dataMasks = [_.logicAnd(_._dataAreaMask, mask) for mask in _._maskList]

    def mdk(_,idxes, i, j):
        if idxes == 0:
            poli = (i+j) % 2
        elif idxes == 1:
            poli = j % 2
        elif idxes == 2:
            poli = i % 3
        elif idxes == 3:
            poli = (i+j) % 3
        elif idxes == 4:
            poli = (j//2 + i//3) % 2
        elif idxes == 5:
            poli = (i*j) % 2+(i*j) % 3
        elif idxes == 6:
            poli = ((i*j) % 2+(i*j) % 3) % 2
        elif idxes == 7:
            poli = ((i+j) % 2+(i*j) % 3) % 2
        return poli == 0

    def GFMul(_,x=2, y=2, prim=0x11d, field_charac_full=256, carryless=True):
        '''Galois field GF(2^8) multiplication.'''
        rr = 0
        while y:
            if y & 1:
                rr = rr ^ x if carryless else rr + x
            y = y >> 1
            x = x << 1
            if prim > 0 and x & field_charac_full:
                x = x ^ prim
        return rr

    def RSEnc(_,bitstring, nsym):
        '''Encode bitstring with nsym EC bits using RS algorithm.'''
        gen = _._rsGenPoly(nsym)
        res = [0] * (len(bitstring) + len(gen) - 1)
        res[:len(bitstring)] = bitstring
        for i in range(len(bitstring)):
            coef = res[i]
            if coef != 0:
                for j in range(1, len(gen)):
                    res[i+j] ^= _._gfMul(gen[j], coef)
        res[:len(bitstring)] = bitstring
        return res

    def _gfMul(_,x, y):
        '''Simplified GF multiplication.'''
        if x == 0 or y == 0:
            return 0
        return _._gfExp[_._gfLog[x] + _._gfLog[y]]

    def transpose(_,mat):
        '''Transpose a matrix'''
        res = [[mat[j][i] for j in range(len(mat))] for i in range(len(mat[0]))]
        return res

    def _timSeq(_,len, vertical=False):
        '''
        Generate a horizontal, unless specified vertical
        timing sequence with alternating dark and light
        pixels with length len.
        '''
        res = [[i % 2 for i in range(len)]]
        if vertical:
            res = _.transpose(res)
        return res

    def _gfPolyMul(_,p, q):
        '''GF polynomial multiplication.'''
        r = [0] * (len(p) + len(q) - 1)
        for j in range(len(q)):
            for i in range(len(p)):
                r[i+j] ^= _._gfMul(p[i], q[j])
        return r

    def _gfPolyDiv(_,dividend, divisor):
        '''GF polynomial division.'''
        res = list(dividend)
        for i in range(len(dividend) - len(divisor) + 1):
            coef = res[i]
            if coef != 0:
                for j in range(1, len(divisor)):
                    if divisor[j] != 0:
                        res[i+j] ^= _gfMul(divisor[j], coef)
        sep = -(len(divisor) - 1)
        return res[:sep], res[sep:]

    def _gfPow(_,x, pow):
        '''GF power.'''
        return _._gfExp[(_._gfLog[x] * pow) % 255]

    def _rsGenPoly(_,nsym):
        '''Generate generator polynomial for RS algorithm.'''
        g = [1]
        for i in range(nsym):
            g = _._gfPolyMul(g, [1, _._gfPow(2, i)])
        return g

    def _fmtEncode(_,fmt):
        '''Encode the 15-bit format code using BCH code.'''
        g = 0x537
        code = fmt << 10
        for i in range(4, -1, -1):
            if code & (1 << (i+10)):
                code ^= g << i
        return ((fmt << 10) ^ code) ^ 0b101010000010010

    def encd(_,data):
        '''
        Encode the input data stream.
        Add mode prefix, encode data using ISO-8859-1,
        group data, add padding suffix, and call RS encoding method.
        '''
        if len(data) > 17:
            print('Error: Version 1 QR code encodes no more than 17 characters.')
        # Byte mode prefix 0100.
        bitstring = '0100'
        # Character count in 8 binary bits.
        bitstring += '{:08b}'.format(len(data))
        # Encode every character in ISO-8859-1 in 8 binary bits.
        for c in data:
            bitstring += '{:08b}'.format(ord(c.encode('iso-8859-1')))
        # Terminator 0000.
        bitstring += '0000'
        res = list()
        # Convert string to byte numbers.
        while bitstring:
            res.append(int(bitstring[:8], 2))
            bitstring = bitstring[8:]
        # Add padding pattern.
        while len(res) < 19:
            res.append(int('11101100', 2))
            res.append(int('00010001', 2))
        # Slice to 19 bytes for V1-L.
        res = res[:19]
        # Call RSEnc to add 7 EC bits.
        return _.RSEnc(res, 7)
    
    def fillbt(_,byte, downwards=False):
        '''
        Fill a byte into a 2 by 4 matrix upwards,
        unless specified downwards.
        Upwards:    Downwards:
            0|1         6|7
            -+-         -+-
            2|3         4|5
            -+-         -+-
            4|5         2|3
            -+-         -+-
            6|7         0|1
        '''
        bytestr = '{:08b}'.format(byte)
        res = [[0, 0] for i in range(4)]
        for i in range(8):
            
            res[i // 2][i % 2] = not int(bytestr[7-i])
        if downwards:
            res = res[::-1]
        return res

    def copyFrom(_,src, dst, top, left):
        '''
        Copy the content of matrix src into matrix dst.
        The top-left corner of src is positioned at (left, top)
        in dst.
        '''
        res = copy.deepcopy(dst)
        for j in range(len(src)):
            for i in range(len(src[0])):
                res[top+j][left+i] = src[j][i]
        return res

    def _fillData(_,bitstream):
        '''Fill the encoded data into the template QR code matrix'''
        res = copy.deepcopy(_.ver1Temp)
        for i in range(15):
            res = _.copyFrom(_.fillbt(bitstream[i], (i//3) % 2 != 0),
                        res,
                        21-4*((i % 3-1)*(-1)**((i//3) % 2)+2),
                        21-2*(i//3+1))
        tmp = _.fillbt(bitstream[15])
        res = _.copyFrom(tmp[2:], res, 7, 11)
        res = _.copyFrom(tmp[:2], res, 4, 11)
        tmp = _.fillbt(bitstream[16])
        res = _.copyFrom(tmp, res, 0, 11)
        tmp = _.fillbt(bitstream[17], True)
        res = _.copyFrom(tmp, res, 0, 9)
        tmp = _.fillbt(bitstream[18], True)
        res = _.copyFrom(tmp[:2], res, 4, 9)
        res = _.copyFrom(tmp[2:], res, 7, 9)
        for i in range(3):
            res = _.copyFrom(_.fillbt(bitstream[19+i], True),
                        res, 9+4*i, 9)
        tmp = _.fillbt(bitstream[22])
        res = _.copyFrom(tmp, res, 9, 7)
        for i in range(3):
            res = _.copyFrom(_.fillbt(bitstream[23+i], i % 2 == 0),
                        res, 9, 4-2*i)
        # Generate image after filling data for debug use.
        
       
        return res

    def _fillInfo(_,arg):
        '''
        Fill the encoded format code into the masked QR code matrix.
        arg: (masked QR code matrix, mask number).
        '''
        mat, mask = arg
        # 01 is the format code for L error control level,
        # concatenated with mask id and passed into _fmtEncode
        # to get the 15 bits format code with EC bits.
        fmt = _._fmtEncode(int('01'+'{:03b}'.format(mask), 2))
        fmtarr = [[not int(c)] for c in '{:015b}'.format(fmt)]
        mat = _.copyFrom(_.transpose(fmtarr[7:]), mat, 8, 13)
        mat = _.copyFrom(fmtarr[9:][::-1], mat, 0, 8)
        mat = _.copyFrom(fmtarr[7:9][::-1], mat, 7, 8)
        mat = _.copyFrom(fmtarr[:7][::-1], mat, 14, 8)
        mat = _.copyFrom(_.transpose(fmtarr[:6]), mat, 8, 0)
        mat = _.copyFrom([fmtarr[6]], mat, 8, 7)
        return mat

    def _penalty(_,mat):
        '''
        Calculate penalty score for a masked matrix.
        N1: penalty for more than 5 consecutive pixels in row/column,
            3 points for each occurrence of such pattern,
            and extra 1 point for each pixel exceeding 5
            consecutive pixels.
        N2: penalty for blocks of pixels larger than 2x2.
            3*(m-1)*(n-1) points for each block of mxn
            (larger than 2x2).
        N3: penalty for patterns similar to the finder pattern.
            40 points for each occurrence of 1:1:3:1:1 ratio
            (dark:light:dark:light:dark) pattern in row/column,
            preceded of followed by 4 consecutive light pixels.
        N4: penalty for unbalanced dark/light ratio.
            10*k points where k is the rating of the deviation of
            the proportion of dark pixels from 50% in steps of 5%.
        '''
        # Initialize.
        n1 = n2 = n3 = n4 = 0
        # Calculate N1.

        def getN1(mat, strategy):
            n1 = 0
            for j in range(len(mat)):
                count = 1
                adj = False
                for i in range(1, len(mat)):
                    if strategy == "j":
                        compare = mat[j][i-1]
                    elif strategy == "i":
                        i, j = j, i
                        compare = mat[j-1][i]
                    if mat[j][i] == compare:
                        count += 1
                    else:
                        count = 1
                        adj = False
                    if count >= 5:
                        if not adj:
                            adj = True
                            n1 += 3
                        else:
                            n1 += 1
            return n1

        n1 = getN1(mat, "i") + getN1(mat, "j")

        # Calculate N2.
        m = n = 1
        for j in range(1, len(mat)):
            for i in range(1, len(mat)):
                if (mat[j][i] == mat[j-1][i] and mat[j][i] == mat[j][i-1] and
                    mat[j][i] == mat[j-1][i-1]):
                    if mat[j][i] == mat[j-1][i]:
                        m += 1
                    if mat[j][i] == mat[j][i-1]:
                        n += 1
                else:
                    n2 += 3 * (m-1) * (n-1)
                    m = n = 1

        # Calculate N3.
        count = 0

        def getCount(mat):
            count = 0
            for row in mat:
                rowstr = ''.join(str(e) for e in row)
                occurrences = []
                begin = 0
                while rowstr.find('0100010', begin) != -1:
                    begin = rowstr.find('0100010', begin) + 7
                    occurrences.append(begin)
                for begin in occurrences:
                    if (rowstr.count('00000100010', begin-4) != 0 or
                        rowstr.count('01000100000', begin) != 0):
                        count += 1
            return count

        transposedMat = _.transpose(mat)
        n3 += 40 * (getCount(mat)+getCount(transposedMat))

        # Calculate N4.
        dark = sum(row.count(_.DARK) for row in mat)
        percent = int((float(dark) / float(len(mat)**2)) * 100)
        pre = percent - percent % 5
        nex = percent + 5 - percent % 5
        n4 = min(abs(pre-50)//5, abs(nex-50)//5) * 10

        # Return final penalty score.
        return n1 + n2 + n3 + n4

    def logicAnd(_,mat1, mat2):
        '''
        Matrix-wise and.
        Dark and dark -> dark
        Light and light -> light
        Dark and light -> light
        Light and dark -> light
        '''
        res = [[True for i in range(len(mat1[0]))] for j in range(len(mat1))]
        for j in range(len(mat1)):
            for i in range(len(mat1[0])):
                res[j][i] = mat1[j][i] or mat2[j][i]
        return res

    def logicOr(_,mat1, mat2):
        """
        B + B -> B
        B + W -> B
        W + W -> W
        """
        res = [[False for i in range(len(mat1[0]))] for j in range(len(mat1))]
        for j in range(len(mat1)):
            for i in range(len(mat1[0])):
                res[j][i] = mat1[j][i] and mat2[j][i]
        return res

    def logicNot(_,mat1):
        res = [[False for i in range(len(mat1[0]))] for j in range(len(mat1))]
        for j in range(len(mat1)):
            for i in range(len(mat1[0])):
                res[j][i] = not mat1[j][i]
        return res

    def logicXor(_,mat1, mat2):
        '''
        Matrix-wise xor.
        Dark xor dark -> light
        Light xor light -> light
        Dark xor light -> dark
        Light xor dark -> dark
        '''
        res = [[True for i in range(len(mat1[0]))] for j in range(len(mat1))]
        for j in range(len(mat1)):
            for i in range(len(mat1[0])):
                res[j][i] = mat1[j][i] == mat2[j][i]
        return res

    def _mask(_,mat):
        '''
        Mask the data QR code matrix with all 8 masks,
        call _penalty to calculate penalty scores for each
        and select the best mask.
        Return tuple(selected masked matrix, number of selected mask).
        '''
        maskeds = [_.logicXor(mat, dataMask) for dataMask in _.dataMasks]
        penalty = [0] * 8
        for i, masked in enumerate(maskeds):
            penalty[i] = _._penalty(masked)
            # Print penalty scores for debug use.
            if True:
                print('penalty for mask {}: {}'.format(i, penalty[i]))
        # Find the id of the best mask.
        selected = penalty.idxes(min(penalty))
        # Print selected mask and penalty score,
        # and generate image for masked QR code for debug use.
        if True:
            print('mask {} selected with penalty {}'.format(selected,
                                                            penalty[selected]))
            
        return maskeds[selected], selected

    def gbit(_,bitstream):
        '''
        generate thefinal QR code bitmap.
        '''
        return _._fillInfo(_._mask(_._fillData(bitstream)))
