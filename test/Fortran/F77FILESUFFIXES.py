#!/usr/bin/env python
#
# __COPYRIGHT__
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

__revision__ = "__FILE__ __REVISION__ __DATE__ __DEVELOPER__"

import os
import string
import sys
import TestSCons

from common import write_fake_link

_python_ = TestSCons._python_
_exe   = TestSCons._exe

test = TestSCons.TestSCons()

write_fake_link(test)

test.write('myfortran.py', r"""
import getopt
import sys
comment = '#' + sys.argv[1]
opts, args = getopt.getopt(sys.argv[2:], 'co:')
for opt, arg in opts:
    if opt == '-o': out = arg
infile = open(args[0], 'rb')
outfile = open(out, 'wb')
for l in infile.readlines():
    if l[:len(comment)] != comment:
        outfile.write(l)
sys.exit(0)
""")

# Test default file suffix: .f77/.F77 for F77
test.write('SConstruct', """
env = Environment(LINK = r'%(_python_)s mylink.py',
                  LINKFLAGS = [],
                  F77 = r'%(_python_)s myfortran.py g77',
                  FORTRAN = r'%(_python_)s myfortran.py fortran')
env.Program(target = 'test01', source = 'test01.f')
env.Program(target = 'test02', source = 'test02.F')
env.Program(target = 'test03', source = 'test03.for')
env.Program(target = 'test04', source = 'test04.FOR')
env.Program(target = 'test05', source = 'test05.ftn')
env.Program(target = 'test06', source = 'test06.FTN')
env.Program(target = 'test07', source = 'test07.fpp')
env.Program(target = 'test08', source = 'test08.FPP')
env.Program(target = 'test09', source = 'test09.f77')
env.Program(target = 'test10', source = 'test10.F77')
env.Program(target = 'test11', source = 'test11.f90')
env.Program(target = 'test12', source = 'test12.F90')
env.Program(target = 'test13', source = 'test13.f95')
env.Program(target = 'test14', source = 'test14.F95')
""" % locals())

test.write('test01.f',   "This is a .f file.\n#link\n#fortran\n")
test.write('test02.F',   "This is a .F file.\n#link\n#fortran\n")
test.write('test03.for', "This is a .for file.\n#link\n#fortran\n")
test.write('test04.FOR', "This is a .FOR file.\n#link\n#fortran\n")
test.write('test05.ftn', "This is a .ftn file.\n#link\n#fortran\n")
test.write('test06.FTN', "This is a .FTN file.\n#link\n#fortran\n")
test.write('test07.fpp', "This is a .fpp file.\n#link\n#fortran\n")
test.write('test08.FPP', "This is a .FPP file.\n#link\n#fortran\n")
test.write('test09.f77', "This is a .f77 file.\n#link\n#g77\n")
test.write('test10.F77', "This is a .F77 file.\n#link\n#g77\n")
test.write('test11.f90', "This is a .f90 file.\n#link\n#fortran\n")
test.write('test12.F90', "This is a .F90 file.\n#link\n#fortran\n")
test.write('test13.f95', "This is a .f95 file.\n#link\n#fortran\n")
test.write('test14.F95', "This is a .F95 file.\n#link\n#fortran\n")

test.run(arguments = '.', stderr = None)

test.must_match('test01' + _exe, "This is a .f file.\n")
test.must_match('test02' + _exe, "This is a .F file.\n")
test.must_match('test03' + _exe, "This is a .for file.\n")
test.must_match('test04' + _exe, "This is a .FOR file.\n")
test.must_match('test05' + _exe, "This is a .ftn file.\n")
test.must_match('test06' + _exe, "This is a .FTN file.\n")
test.must_match('test07' + _exe, "This is a .fpp file.\n")
test.must_match('test08' + _exe, "This is a .FPP file.\n")
test.must_match('test09' + _exe, "This is a .f77 file.\n")
test.must_match('test10' + _exe, "This is a .F77 file.\n")
test.must_match('test11' + _exe, "This is a .f90 file.\n")
test.must_match('test12' + _exe, "This is a .F90 file.\n")
test.must_match('test13' + _exe, "This is a .f95 file.\n")
test.must_match('test14' + _exe, "This is a .F95 file.\n")

test.pass_test()

# Test non-default file suffix: .f/.F for F77

test2 = TestSCons.TestSCons()

write_fake_link(test2)

test2.write('myfortran.py', r"""
import getopt
import sys
comment = '#' + sys.argv[1]
opts, args = getopt.getopt(sys.argv[2:], 'co:')
for opt, arg in opts:
    if opt == '-o': out = arg
infile = open(args[0], 'rb')
outfile = open(out, 'wb')
for l in infile.readlines():
    if l[:len(comment)] != comment:
        outfile.write(l)
sys.exit(0)
""")

test2.write('SConstruct', """
env = Environment(LINK = r'%(_python_)s mylink.py',
                  LINKFLAGS = [],
                  F77 = r'%(_python_)s myfortran.py g77',
                  FORTRAN = r'%(_python_)s myfortran.py fortran')
                  #F77FILESUFFIXES = ['.f', '.F'])
env.Program(target = 'test01', source = 'test01.f')
env.Program(target = 'test02', source = 'test02.F')
env.Program(target = 'test03', source = 'test03.f77')
env.Program(target = 'test04', source = 'test04.F77')
env.Program(target = 'test05', source = 'test05.f95')
env.Program(target = 'test06', source = 'test06.F95')
""" % locals())

test2.write('test01.f',   "This is a .f file.\n#link\n#g77\n")
test2.write('test02.F',   "This is a .F file.\n#link\n#g77\n")
test2.write('test03.f77', "This is a .for file.\n#link\n#fortran\n")
test2.write('test04.F77', "This is a .FOR file.\n#link\n#fortran\n")
test2.write('test05.f95', "This is a .ftn file.\n#link\n#fortran\n")
test2.write('test06.F95', "This is a .FTN file.\n#link\n#fortran\n")

test2.run(arguments = '.', stderr = None)

test2.must_match('test01' + _exe, "This is a .f file.\n")
test2.must_match('test02' + _exe, "This is a .F file.\n")
test2.must_match('test03' + _exe, "This is a .f77 file.\n")
test2.must_match('test04' + _exe, "This is a .F77 file.\n")
test2.must_match('test05' + _exe, "This is a .f95 file.\n")
test2.must_match('test06' + _exe, "This is a .F95 file.\n")

test2.pass_test()
