@echo off
setlocal

REM Install AI Berkshire WorkBuddy skills into the local WorkBuddy skill dir.
REM Default destination: %WORKBUDDY_HOME%\skills  or  %USERPROFILE%\.workbuddy\skills
REM Override with: set WORKBUDDY_HOME=D:\somewhere

for %%I in ("%~dp0..") do set "ROOT=%%~fI"

if defined WORKBUDDY_SKILLS_DIR (
  set "DEST=%WORKBUDDY_SKILLS_DIR%"
) else if defined WORKBUDDY_HOME (
  set "DEST=%WORKBUDDY_HOME%\skills"
) else (
  set "DEST=%USERPROFILE%\.workbuddy\skills"
)

where py >nul 2>nul
if %ERRORLEVEL%==0 (
  set "PY=py -3"
) else (
  set "PY=python"
)

if defined WORKBUDDY_SKILL_PREFIX (
  %PY% "%ROOT%\scripts\sync-workbuddy-skills.py" --prefix "%WORKBUDDY_SKILL_PREFIX%"
) else (
  %PY% "%ROOT%\scripts\sync-workbuddy-skills.py"
)
if errorlevel 1 exit /b %ERRORLEVEL%

if not exist "%DEST%" mkdir "%DEST%"
if errorlevel 1 exit /b %ERRORLEVEL%

for /d %%D in ("%ROOT%\workbuddy-skills\*") do (
  if exist "%DEST%\%%~nxD" rmdir /s /q "%DEST%\%%~nxD"
  if errorlevel 1 exit /b 1
  xcopy "%%~fD" "%DEST%\%%~nxD\" /E /I /Y >nul
  if errorlevel 1 exit /b 1
)

echo Installed WorkBuddy skills to %DEST%
echo Restart WorkBuddy (or reload skills) to pick up new skills.
endlocal
