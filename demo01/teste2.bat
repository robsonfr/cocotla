@echo off
..\as09\as09.exe -l -c demo2.s
ren demo2.bin demo2.rom
c:\python27\python ..\casconv.py -w demo2.rom
