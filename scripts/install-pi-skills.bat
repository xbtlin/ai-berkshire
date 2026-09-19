@echo off
setlocal

for %%I in ("%~dp0..") do set "ROOT=%%~fI"

if defined PI_SKILLS_DIR (
  set "DEST=%PI_SKILLS_DIR%"
) else (
  set "DEST=%USERPROFILE%\.pi\agent\skills"
)

where py >nul 2>nul
if %ERRORLEVEL%==0 (
  set "PY=py -3"
) else (
  set "PY=python"
)

REM Pi uses the Agent Skills package format, so reuse the generated packages
REM that are also installed for Codex. The source workflows remain skills/*.md.
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

echo Installed Pi skills to %DEST%
echo Restart Pi to discover the new skills.
