import os

from c_incubator.msvc_compiler import MSVCCompiler, TargetType

if __name__ == '__main__':
    msvc_compiler = MSVCCompiler()
    msvc_compiler.target_file = 'board_util.cpp'
    msvc_compiler.target_type = TargetType.DLL
    msvc_compiler.additional_lib_path_list.append('../lib')
    msvc_compiler.additional_import_lib_list.append('actor.lib')
    msvc_compiler.additional_import_lib_list.append('board.lib')
    msvc_compiler.compile()
