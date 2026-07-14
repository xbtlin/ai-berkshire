@echo off
setlocal

for %%I in ("%~dp0..") do set "ROOT=%%~fI"

if defined CODEX_HOME (
  set "DEST=%CODEX_HOME%\prompts"
) else (
  set "DEST=%USERPROFILE%\.codex\prompts"
)

where py >nul 2>nul
if %ERRORLEVEL%==0 (
  set "PY=py -3"
) else (
  set "PY=python"
)

%PY% "%ROOT%\scripts\sync-codex-prompts.py"
if errorlevel 1 exit /b %ERRORLEVEL%

if not exist "%DEST%" mkdir "%DEST%"
if errorlevel 1 exit /b %ERRORLEVEL%

copy /Y "%ROOT%\codex-prompts\*.md" "%DEST%\" >nul
if errorlevel 1 exit /b %ERRORLEVEL%

echo Installed Codex slash prompts to %DEST%
echo Restart Codex to pick up new slash prompts.
