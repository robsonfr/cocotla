@echo off
..\as09\as09.exe -l -c demo1.s
copy /b demo1.bin + /b demo01.raw demo1.rom
c:\python27\python ..\casconv.py %1 demo1.rom
