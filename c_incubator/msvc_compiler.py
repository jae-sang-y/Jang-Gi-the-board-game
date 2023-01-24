import enum
import itertools
import os
from typing import List


class TargetType(enum.Enum):
    EXE = 'EXE'
    DLL = ' DLL'


class MSVCCompiler:
    msvc_bin_path = r'C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\bin\Hostx64\x64'
    msvc_include_path = r'C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\include'
    msvc_lib_path = r'C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.34.31933\lib\x64'
    win_kits_ucrt_include_path = r'C:\Program Files (x86)\Windows Kits\10\Include\10.0.22000.0\ucrt'
    win_kits_ucrt_lib_path = r'C:\Program Files (x86)\Windows Kits\10\Lib\10.0.22000.0\ucrt\x64'
    win_kits_um_lib_path = r'C:\Program Files (x86)\Windows Kits\10\Lib\10.0.22000.0\um\x64'

    def __init__(self):
        self.target_file: str = None
        self.target_type: TargetType = TargetType.EXE
        self.additional_lib_path_list: List[str] = list()
        self.additional_compiler_args: List[str] = [
            '/MD', '/EHsc', '/utf-8'
        ]
        self.additional_import_lib_list: List[str] = list()
        self.additional_include_path_list: List[str] = list()

    def compile(self):
        print('cwd:', os.getcwd())

        os.environ['PATH'] = r'{};{}'.format(os.environ['PATH'], self.msvc_bin_path)

        include_path_list = [
            self.msvc_include_path,
            self.win_kits_ucrt_include_path
        ]
        lib_path_list = [
            self.msvc_lib_path,
            self.win_kits_ucrt_lib_path,
            self.win_kits_um_lib_path
        ]

        compile_args = ['cl.exe']
        for include_path in itertools.chain(include_path_list, self.additional_include_path_list):
            compile_args.append('-I')
            compile_args.append(f'"{include_path}"')
        compile_args.append(self.target_file)

        if self.target_type == TargetType.DLL:
            compile_args.append('/LD')

        compile_args += self.additional_compiler_args

        compile_args.append('/link')
        for lib_path in itertools.chain(lib_path_list, self.additional_lib_path_list):
            compile_args.append(f'/LIBPATH:"{lib_path}"')
        for lib_path in self.additional_import_lib_list:
            compile_args.append(f'/DEFAULTLIB:"{lib_path}"')
        compile_cmd = ' '.join(compile_args)
        print('compile_cmd:', compile_cmd)
        rc = os.system(compile_cmd)
        assert rc == 0, rc
        self.after_compile()

    def after_compile(self):
        target_file_name = self.target_file.split('.')[0]
        for suffix in [
            '.exp',
            '.obj'
        ]:
            outfile_path = f'{target_file_name}{suffix}'
            if os.path.isfile(outfile_path):
                os.remove(outfile_path)
        for suffix in [
            '.dll', '.exe'
        ]:
            out_file_path = f'{target_file_name}{suffix}'
            if os.path.isfile(out_file_path):
                print('move file', out_file_path, '-> ../bin')
                os.system('move /Y {} {}'.format(out_file_path, '../bin'))
        lib_file_path = f'{target_file_name}.lib'
        if os.path.isfile(lib_file_path):
            print('move file', out_file_path, '-> ../lib')
            os.system('move /Y {} {}'.format(lib_file_path, '../lib'))

    def run_executable(self, *args):
        target_file_name = self.target_file.split('.')[0]
        os.chdir('../bin')
        rc = os.system(f'{target_file_name}.exe ' + ' '.join(map(str, args)))
        assert rc == 0, rc
