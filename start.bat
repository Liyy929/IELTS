@echo off
cd /d %~dp0
title IELTS Vocab Workflow
chcp 65001 >nul

:: 设置我的 Python 路径
set PYTHON_EXE=D:\python_app\python.exe

:: 加载密钥配置
if exist config.env (
    for /f "tokens=1,2 delims==" %%a in (config.env) do set %%a=%%b
)

echo =========================================
echo  Starting IELTS Workflow Backend Service
echo =========================================
echo.

:: 启动 Flask 服务，并保持窗口不关闭
start "Flask Server - Do NOT close" cmd /k ""%PYTHON_EXE%" server.py"

echo Service started successfully.
echo You can now go to the website and highlight words.
echo.
timeout /t 5 >nul