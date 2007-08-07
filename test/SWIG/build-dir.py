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

"""
Make sure SWIG works when a BuildDir (or build_dir) is used.

Test case courtesy Joe Maruszewski.
"""

import TestSCons

test = TestSCons.TestSCons()

test.subdir(['build'],
            ['source'])

test.write(['SConstruct'], """\
import distutils.sysconfig

#
# Create the build environment.
#
env = Environment(CPPPATH = [".", distutils.sysconfig.get_python_inc()],
                  CPPDEFINES = "NDEBUG",
                  SWIGFLAGS = ["-python", "-c++"],
                  SWIGCXXFILESUFFIX = "_wrap.cpp")
Export("env")

#
# Build the libraries.
#
SConscript("source/SConscript", build_dir = "build")
""")

test.write(['source', 'SConscript'], """\
Import("env")
lib = env.SharedLibrary("_linalg",
                        "linalg.i",
                        SHLIBPREFIX = "",
                        SHLIBSUFFIX = ".pyd")
""")

test.write(['source', 'Vector.hpp'], """\
class Vector
{
 public:
  Vector(int size = 0) : _size(size)
  {
    _v = new double[_size];
    for (int i = 0; i < _size; ++i)
      _v[i] = 0.0;
  }

  ~Vector() { delete [] _v; }

  int size() const { return _size; }

  double&        operator[](int key)       { return _v[key]; }
  double  const& operator[](int key) const { return _v[key]; }

 private:
  int _size;
  double* _v;
};
""")

test.write(['source', 'linalg.i'], """\
%module linalg
%{
#include <sstream>
#include "Vector.hpp"
%}


class Vector
{
public:
  Vector(int n = 0);
  ~Vector();
  
  %extend
  {
    const char* __str__() { return "linalg.Vector()"; }
    int __len__() { return $self->size(); }
    double __getitem__(int key) { return $self->operator[](key); }
    void __setitem__(int key, double value) { $self->operator[](key) = value; }
    
    %pythoncode %{
    def __iter__(self):
        for i in xrange(len(self)):
            yield self[i]
    %}
  }
};
""")

test.write(['source', 'test.py'], """\
#!/usr/bin/env python
import linalg


x = linalg.Vector(5)
print x

x[1] = 99.5
x[3] = 8.3
x[4] = 11.1


for i, v in enumerate(x):
    print "\tx[%d] = %g" % (i, v)

""")

test.run(arguments = '.')

test.up_to_date(arguments = '.')

test.pass_test()
