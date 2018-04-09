#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2018  Mate Soos
#                     Many thanks to Ivica Nikolic

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


import sys
import optparse

parser = optparse.OptionParser()
parser.add_option("--num", "-n", dest="n", metavar="NUM", type=int,
                  default=6, help="Size of S-box")
parser.add_option("--hb", dest="helpb", metavar="HELP", type=int,
                  default=0, help="Number of help boxes of the only known solution for N value 6. ONLY works for 6-bit s-box.")
parser.add_option("--onlyhelp", action="store_true", default=False,
                  dest="onlyhelp", help="Only output help bits as per only currently known solution")
parser.add_option("--symmbreak", action="store_true", default=False,
                  dest="symmbreak", help="Give help bits that break symmetry. This CONFLICTS WITH --hb")
parser.add_option("--verbose", "-v", action="store_true", default=False,
                  dest="verbose", help="Print more output")

(options, args) = parser.parse_args()


global perms
global var
perms = []
var = 1
for i in range(2**options.n):
    val = []
    for _ in range(options.n):
        val.append(var)
        var += 1
    perms.append(val)


def gen_problem():
    global perms
    global var
    n = options.n
    print("c Num bits: %d" % n)

    # we now have:
    # perms[0000] -> [bits it maps to, as variable numbers]
    # perms[0001] -> [bits it maps to, as variable numbers]

    out = "c num vars: %d\n" % (var-1)

    # it's a permutation, so any 2 XOR is non-zero
    for i in range(2**n-1):
        out += "c -- perm for %d -- \n" % i
        for i2 in range(i+1, 2**n):
            out += "c -- perm for %d vs %d-- \n" % (i, i2)
            one_must_be_true = []
            for a, b in zip(perms[i], perms[i2]):
                out += "x -%d " % var
                one_must_be_true.append(var)
                var += 1
                out += " %d %d 0\n" % (a, b)

            out += "c one must be true.\n"
            for x in one_must_be_true:
                out += "%d " % x
            out += "0\n"

    out + "c ---- cut ----"
    print(out.strip())
    out = ""

    for i in range(2**(4*n)):
        vals = []
        myxor = 0
        for i2 in range(4):
            val = i >> (n*i2)
            val &= (2**(n)-1)
            vals.append(val)

        OK = True
        for i2 in range(3):
            if vals[i2] <= vals[i2+1]:
                OK = False
                break

        if not OK:
            continue

        out += "c vals are: "
        for x in vals:
            out += "%d " % x
        out += "\n"

        # check if the original is all-zero
        xor_them = 0
        for x in vals:
            xor_them ^= x
        out += "c their XOR is %d" % xor_them
        if xor_them != 0:
            out += " -> Not interesting, not 0\n"
            continue
        out += "\n"
        print(out.strip())
        out = ""

        # XOR each bit
        ind_bits = []
        for bitno in range(n):
            out += "c bit no. %d -> XOR mapped to var %d\n" % (bitno, var)

            ind_bits.append(var)
            out += "x -%d " % (var)
            var += 1
            for y in range(4):
                out += "%d " % perms[vals[y]][bitno]
            out += "0\n"

        out += "c at least one 1 among these: "
        for x in ind_bits:
            out += "%d " % x
        out += "\n"

        # non-zero, so at least one bit is a 1
        for x in ind_bits:
            out +="%d " % x
        out += "0\n"

    print(out.strip())
    out = ""

    # fixed values
    out += "c setting val %d for s(%d)\n" % (0, 0)
    out += "-%d 0\n" % perms[0][0]
    out += "-%d 0\n" % perms[0][1]
    out += "-%d 0\n" % perms[0][2]
    out += "-%d 0\n" % perms[0][3]


def symmbreak():
    for i in range(1, n+1):
        left_val = 2**(i-1)
        val = 2**(i-1)

        out += "c setting val %d for s(%d)\n" % (left_val, val)
        for bit in range(n):
            if ((val >> bit) & 1) == 0:
                out += "-%d 0\n" % perms[left_val][bit]
            else:
                out += "%d 0\n" % perms[left_val][bit]

    print(out.strip())


def gen_helpboxes():
    if options.helpb == 0 or options.n != 6:
        return

    sbox = [0, 54, 48, 13, 15, 18, 53, 35,
            25, 63, 45, 52,  3, 20, 41, 33,
            59, 36,  2, 34, 10,  8, 57, 37,
            60, 19, 42, 14, 50, 26, 58, 24,
            39, 27, 21, 17, 16, 29,  1, 62,
            47, 40, 51, 56,  7, 43, 44, 38,
            31, 11,  4, 28, 61, 46,  5, 49,
            9,  6, 23, 32, 30, 12, 55, 22]
    out = ""
    for x in range(options.helpb):
        out += "c help %d\n" % x
        for i in range(6):
            val = (sbox[x] >> i) % 2
            if val == 0:
                out += "-"
            out += "%d 0\n" % perms[x][i]

    print(out.strip())


if __name__ == "__main__":
    if options.helpb > 0 and options.symmbreak:
        print("ERROR: Symmetry breaking is not consistent with help boxes. Use only one or the other.")
        exit(-1)

    if options.helpb > 0 and options.n != 6:
        print("ERROR : the --hb option only makes sense with -n 6")
        exit(-1)

    if options.helpb > 64:
        print("ERROR: There are only 2**6 == 64 boxes... the --hb option cannot be larger than that")
        exit(-1)

    if not options.onlyhelp:
        gen_problem()

    if options.symmbreak:
        symmbreak()

    if options.helpb > 0:
        gen_helpboxes()
