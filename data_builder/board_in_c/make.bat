@echo off
SET CWD="%cd%"
echo It's running on %cwd%

SET PLATFOM=x64
SET PATH=%path%;C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.29.30133\bin\Host%PLATFOM%\%PLATFOM%;

cl.exe /nologo /utf-8 /std:c++20 /EHsc board_in_c.cpp "/IC:\Users\YJS-ATX\AppData\Local\Programs\Python\Python39\include" "/IC:\Program Files (x86)\Windows Kits\10\Include\10.0.19041.0\ucrt" "/IC:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.29.30133\include" "/IC:\Program Files (x86)\Windows Kits\10\Include\10.0.19041.0\shared" /link /NOLOGO "/LIBPATH:C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.29.30133\lib\%PLATFOM%" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\Lib\10.0.19041.0\um\x64" "/LIBPATH:C:\Program Files (x86)\Windows Kits\10\Lib\10.0.19041.0\ucrt\%PLATFOM%" "/LIBPATH:C:\Users\YJS-ATX\AppData\Local\Programs\Python\Python39\libs" /DLL /OUT:board_in_c.dll
