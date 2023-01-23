import os

from c_incubator.msvc_compiler import MSVCCompiler, TargetType

if __name__ == '__main__':
    msvc_compiler = MSVCCompiler()
    msvc_compiler.target_file = 'board.cpp'
    msvc_compiler.target_type = TargetType.DLL
    msvc_compiler.compile()
