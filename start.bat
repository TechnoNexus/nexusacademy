@echo off
title Pega Academy Practice Exam Launcher
echo Starting Pega Academy Practice Exam Web Server on port 8080...
start "" "http://localhost:8080"
python -m http.server 8080
pause
