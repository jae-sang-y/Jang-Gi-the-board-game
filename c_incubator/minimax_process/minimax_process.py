from c_incubator.msvc_compiler import MSVCCompiler

if __name__ == '__main__':
    msvc_compiler = MSVCCompiler()
    msvc_compiler.target_file = 'minimax_process.cpp'
    msvc_compiler.additional_lib_path_list.append('../lib')
    msvc_compiler.additional_import_lib_list.append('board_util.lib')
    msvc_compiler.additional_import_lib_list.append('board.lib')
    msvc_compiler.additional_import_lib_list.append('actor.lib')
    msvc_compiler.additional_import_lib_list.append('evaluator.lib')
    msvc_compiler.compile()
    msvc_compiler.run_executable(2, 0)
