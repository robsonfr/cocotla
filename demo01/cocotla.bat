@echo off
as09.exe -o%1.rom -c -l %1.s
c:\python27\python ..\casconv.py -w %1.rom demo1.rom
