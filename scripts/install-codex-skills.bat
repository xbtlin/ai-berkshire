@echo off
setlocal

for %%I in ("%~dp0..") do set "ROOT=%%~fI"

if defined CODEX_HOME (
  set "DEST=%CODEX_HOME%\skills"
) else (
  set "DEST=%USERPROFILE%\.codex\skills"
)

where py >nul 2>nul
if %ERRORLEVEL%==0 (
  set "PY=py -3"
) else (
  set "PY=python"
)

%PY% "%ROOT%\scripts\sync-codex-skills.py"
if errorlevel 1 exit /b %ERRORLEVEL%

if not exist "%DEST%" mkdir "%DEST%"
if errorlevel 1 exit /b %ERRORLEVEL%

for /d %%D in ("%ROOT%\codex-skills\*") do (
  if exist "%DEST%\%%~nxD" rmdir /s /q "%DEST%\%%~nxD"
  if errorlevel 1 exit /b 1
  xcopy "%%~fD" "%DEST%\%%~nxD\" /E /I /Y >nul
  if errorlevel 1 exit /b 1
)

echo Installed Codex skills to %DEST%
echo Run .\scripts\install-codex-prompts.bat if you want slash-command prompts.
echo Restart Codex to pick up new skills.
