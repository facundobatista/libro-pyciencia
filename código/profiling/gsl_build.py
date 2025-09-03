from cffi import FFI
ffi = FFI()
ffi.cdef("""
    double gsl_hypot(const double x, const double y);
""")

ffi.set_source("gsl", """
    #include "gsl/gsl_math.h"   // the C header of the library
""", libraries=['gsl'])

ffi.compile(verbose=True)

# Copyright 2020-2025 Facundo Batista y Manuel Carlevaro
# Licencia CC BY-NC-SA 4.0
# Para más info visitar https://github.com/facundobatista/libro-pyciencia/
