from cffi import FFI
ffibuilder = FFI()

# cdef() expects a single string declaring the C types, functions and
# globals needed to use the shared object. It must be in valid C syntax.
ffibuilder.cdef("""

extern uint32_t GetQHYCCDSDKVersion(uint32_t *year,uint32_t *month,uint32_t *day,uint32_t *subday);
extern uint32_t SetQHYCCDLogLevel(uint8_t logLevel);
extern uint32_t InitQHYCCDResource(void);
""")

# set_source() gives the name of the python extension module to
# produce, and some C source code as a string.  This C code needs
# to make the declarated functions, types and globals available,
# so it is often just the "#include".
ffibuilder.set_source("_qhyccd_cffi",
"""
#include "libqhy/config.h"
extern uint32_t GetQHYCCDSDKVersion(uint32_t *year,uint32_t *month,uint32_t *day,uint32_t *subday);
extern uint32_t SetQHYCCDLogLevel(uint8_t logLevel);
extern uint32_t InitQHYCCDResource(void);
""",
     libraries=['qhyccd'])   # library name, for the linker

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)

