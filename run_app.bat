@echo off
chcp 65001 >nul
title TTS Tool Vietnamese - Quick Start

echo.
echo ████████╗████████╗███████╗    ████████╗ ██████╗  ██████╗ ██╗     
echo ╚══██╔══╝╚══██╔══╝██╔════╝    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     
echo    ██║      ██║   ███████╗       ██║   ██║   ██║██║   ██║██║     
echo    ██║      ██║   ╚════██║       ██║   ██║   ██║██║   ██║██║     
echo    ██║      ██║   ███████║       ██║   ╚██████╔╝╚██████╔╝███████╗
echo    ╚═╝      ╚═╝   ╚══════╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝
echo.
echo 🎤 TTS Tool Vietnamese - Chuyển văn bản thành giọng nói
echo 👨‍💻 Phát triển bởi: Nguyễn Vĩnh Bảo
echo 📞 Liên hệ: fb.com/ngvinhbao14081 ^| t.me/nvb1408
echo 💖 Ủng hộ: VPBank - 0567546604
echo ===============================================================
echo.

REM Kiểm tra Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python chưa được cài đặt hoặc không có trong PATH
    echo 📥 Vui lòng download Python từ: https://python.org
    echo ✅ Nhớ check "Add Python to PATH" khi cài đặt
    echo.
    pause
    exit /b 1
)

echo ✅ Python đã được cài đặt: 
python --version

REM Kiểm tra pip
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip chưa được cài đặt
    echo 🔧 Đang cài đặt pip...
    python -m ensurepip --upgrade
)

echo ✅ pip đã sẵn sàng:
pip --version

REM Kiểm tra virtual environment
if not exist "venv" (
    echo 🌍 Tạo virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ❌ Không thể tạo virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment đã được tạo
)

REM Kích hoạt virtual environment
echo 🔄 Kích hoạt virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ❌ Không thể kích hoạt virtual environment
    pause
    exit /b 1
)

echo ✅ Virtual environment đã được kích hoạt

REM Kiểm tra requirements.txt
if not exist "requirements.txt" (
    echo 📝 Tạo requirements.txt...
    echo edge-tts^>=6.1.0> requirements.txt
    echo gTTS^>=2.3.0>> requirements.txt
    echo pyttsx3^>=2.90>> requirements.txt
    echo pygame^>=2.1.0>> requirements.txt
    echo pyinstaller^>=5.0>> requirements.txt
    echo pillow^>=9.0.0>> requirements.txt
    echo requests^>=2.28.0>> requirements.txt
    echo ✅ requirements.txt đã được tạo
)

REM Kiểm tra dependencies
echo 🔍 Kiểm tra dependencies...
pip show edge-tts >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 Cài đặt dependencies...
    echo ⏱️  Quá trình này có thể mất vài phút...
    pip install --upgrade pip
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Cài đặt dependencies thất bại
        echo 🔧 Thử cài đặt thủ công:
        echo    pip install edge-tts gTTS pyttsx3 pygame
        pause
        exit /b 1
    )
    echo ✅ Dependencies đã được cài đặt thành công
) else (
    echo ✅ Dependencies đã sẵn sàng
)

REM Kiểm tra file chính
if not exist "src\tts_app.py" (
    echo ❌ Không tìm thấy src\tts_app.py
    echo 📁 Vui lòng đảm bảo cấu trúc thư mục đúng:
    echo    TTS_Tool_Vietnamese\
    echo    ├── src\
    echo    │   └── tts_app.py
    echo    ├── requirements.txt
    echo    └── run_app.bat
    pause
    exit /b 1
)

REM Kiểm tra config.json
if not exist "config.json" (
    echo 📝 Tạo config.json mặc định...
    echo {> config.json
    echo   "app_name": "TTS Tool Vietnamese",>> config.json
    echo   "version": "1.0.0",>> config.json
    echo   "author": "Nguyễn Vĩnh Bảo",>> config.json
    echo   "description": "Công cụ chuyển văn bản thành giọng nói tiếng Việt">> config.json
    echo }>> config.json
    echo ✅ config.json đã được tạo
)

REM Tạo thư mục output
if not exist "output" (
    mkdir output
    echo ✅ Thư mục output đã được tạo
)

echo.
echo 🚀 Khởi động TTS Tool Vietnamese...
echo ⏱️  Lần đầu chạy có thể mất 10-15 giây...
echo 📁 File audio sẽ được lưu trong thư mục 'output'
echo.

REM Chạy ứng dụng
python src\tts_app.py

REM Kiểm tra kết quả
if %errorlevel% neq 0 (
    echo.
    echo ❌ Ứng dụng gặp lỗi khi chạy
    echo 🐛 Có thể là do:
    echo    - Thiếu dependencies
    echo    - Lỗi trong code
    echo    - Không có quyền ghi file
    echo.
    echo 📞 Liên hệ hỗ trợ:
    echo    Facebook: fb.com/ngvinhbao14081
    echo    Telegram: t.me/nvb1408
    echo.
) else (
    echo.
    echo 🎉 Cảm ơn bạn đã sử dụng TTS Tool Vietnamese!
    echo 💖 Nếu thấy hữu ích, đừng quên ủng hộ tác giả:
    echo    🏦 VPBank: 0567546604
    echo    ₿ Crypto: TULbGQbBGLL4VNrUYob7eWJUDup2ixkUT4
    echo.
)

pause