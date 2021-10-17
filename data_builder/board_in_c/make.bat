@echo off
SET CWD="%cd%"
echo It's running on %cwd%
SET PATH=%path%;C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.29.30133\bin\Hostx64\x64;

cl.exe /nologo board_in_c.cpp "/IC:\Users\YJS-ATX\AppData\Local\Programs\Python\Python39\include" "/IC:\Program Files (x86)\Windows Kits\10\Include\10.0.19041.0\ucrt" "/IC:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.29.30133\include" "/IC:\Program Files (x86)\Windows Kits\10\Include\10.0.19041.0\shared" /link /NOLOGO "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.29.30133\lib\x64" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\Lib\10.0.19041.0\um\x64" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\Lib\10.0.19041.0\ucrt\x64" "/LIBPATH:C:\Users\YJS-ATX\AppData\Local\Programs\Python\Python39\libs" /DLL /OUT:board_in_c.dll
