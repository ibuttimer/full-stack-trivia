@echo off
REM Copyright (c) 2012-2020, EnterpriseDB Corporation.  All rights reserved

REM PostgreSQL server psql runner script for Windows

chcp 1252

SET server=localhost
SET /P server="Server [%server%]: "

SET database=trivia
SET /P database="Database [%database%]: "

SET port=5432
SET /P port="Port [%port%]: "

SET username=dbowner
SET /P username="Username [%username%]: "

for /f "delims=" %%a in ('chcp ^|find /c "932"') do @ SET CLIENTENCODING_JP=%%a
if "%CLIENTENCODING_JP%"=="1" SET PGCLIENTENCODING=SJIS
if "%CLIENTENCODING_JP%"=="1" SET /P PGCLIENTENCODING="Client Encoding [%PGCLIENTENCODING%]: "

REM Run psql
"C:\Program Files\PostgreSQL\13\bin\psql.exe" -h %server% -U %username% -d %database% -p %port% < trivia.psql

