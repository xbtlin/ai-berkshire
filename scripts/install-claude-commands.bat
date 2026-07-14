@echo off
setlocal

for %%I in ("%~dp0..") do set "ROOT=%%~fI"

if defined CLAUDE_COMMANDS_DIR (
  set "DEST=%CLAUDE_COMMANDS_DIR%"
) else (
  set "DEST=%USERPROFILE%\.claude\commands"
)

if not exist "%DEST%" mkdir "%DEST%"
if errorlevel 1 exit /b %ERRORLEVEL%

copy /Y "%ROOT%\skills\*.md" "%DEST%\" >nul
if errorlevel 1 exit /b %ERRORLEVEL%

echo Installed Claude Code commands to %DEST%
