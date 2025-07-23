# 📦 Hướng dẫn cài đặt TTS Tool Vietnamese

> 👨‍💻 **Phát triển bởi**: Nguyễn Vĩnh Bảo  
> 📞 **Liên hệ**: [Facebook](https://fb.com/ngvinhbao14081) | [Telegram](https://t.me/nvb1408)  
> 💖 **Ủng hộ**: VPBank - 0567546604

## 🎯 Chọn phương pháp cài đặt

| Phương pháp | Phù hợp cho | Thời gian | Độ khó | Khuyến nghị |
|-------------|-------------|-----------|--------|-------------|
| **🚀 Executable** | Người dùng cuối | 2 phút | ⭐ | ✅ Khuyến nghị |
| **💻 Source Code** | Developers | 5 phút | ⭐⭐ | 🔧 Dev/Test |
| **🏗️ Build từ đầu** | Contributors | 15 phút | ⭐⭐⭐ | 🛠️ Advanced |

---

## 🚀 Phương pháp 1: Download Executable (Khuyến nghị)

### 📥 Bước 1: Download
```
🌐 Truy cập: https://github.com/ngvinhbao/tts-tool-vietnamese/releases/latest
📁 Download: TTS_Tool_Vietnamese_v1.0.0.zip
📊 Kích thước: ~20-30MB
```

### 📂 Bước 2: Giải nén và cài đặt
```bash
# 1. Giải nén file ZIP
📁 Chọn thư mục: C:\TTS_Tool_Vietnamese\ (hoặc bất kỳ đâu)
🔓 Giải nén toàn bộ

# 2. Cấu trúc thư mục sau khi giải nén:
TTS_Tool_Vietnamese_v1.0.0_Release/
├── TTS_Tool_Vietnamese_v1.0.0.exe    # File chính
├── README.md                          # Hướng dẫn
├── RELEASE_NOTES.txt                  # Ghi chú phiên bản
├── config.json                        # Cấu hình
└── assets/                            # Tài nguyên (nếu có)
```

### ▶️ Bước 3: Chạy ứng dụng
```
🖱️ Double-click: TTS_Tool_Vietnamese_v1.0.0.exe
⏱️ Lần đầu: 10-15 giây khởi động (tải giọng nói)
🛡️ Windows Defender: Chọn "More info" → "Run anyway"
```

### 🔧 Xử lý Windows Defender
```
⚠️ Nếu Windows Defender chặn:

Cách 1: Tạm thời cho phép
1. Click "More info"
2. Click "Run anyway"
3. Ứng dụng sẽ chạy bình thường

Cách 2: Thêm vào exception (Khuyến nghị)
1. Windows Security → Virus & threat protection
2. Manage settings → Add or remove exclusions
3. Add an exclusion → Folder
4. Chọn thư mục chứa TTS Tool
```

### ✅ Hoàn thành!
```
🎉 Ứng dụng đã sẵn sàng!
📁 Thư mục output: Tự động tạo khi convert
🎤 Giọng nói: HoaiMy (nữ), NamMinh (nam)
📞 Hỗ trợ: fb.com/ngvinhbao14081
```

---

## 💻 Phương pháp 2: Chạy từ Source Code

### 🐍 Bước 1: Cài đặt Python
```bash
# Download Python 3.8+ từ https://python.org
# ✅ QUAN TRỌNG: Check "Add Python to PATH"

# Kiểm tra cài đặt
python --version          # Kết quả: Python 3.8.0+
pip --version            # Kết quả: pip 21.0+
```

### 📂 Bước 2: Clone Repository
```bash
# Cách 1: HTTPS (Khuyến nghị)
git clone https://github.com/ngvinhbao/tts-tool-vietnamese.git

# Cách 2: SSH (Nếu có setup SSH key)
git clone git@github.com:ngvinhbao/tts-tool-vietnamese.git

# Cách 3: Download ZIP
# https://github.com/ngvinhbao/tts-tool-vietnamese/archive/main.zip
```

### 🌍 Bước 3: Setup Virtual Environment
```bash
cd tts-tool-vietnamese

# Tạo virtual environment (KHUYẾN NGHỊ)
python -m venv venv

# Kích hoạt virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Kiểm tra virtual environment
which python             # Phải trỏ về venv/
pip list                # Danh sách package trong venv
```

### 📦 Bước 4: Cài đặt Dependencies
```bash
# Upgrade pip trước
python -m pip install --upgrade pip

# Cài đặt từ requirements.txt
pip install -r requirements.txt

# Hoặc cài đặt thủ công từng package
pip install edge-tts>=6.1.0
pip install gTTS>=2.3.0
pip install pyttsx3>=2.90
pip install pygame>=2.1.0
```

### ▶️ Bước 5: Chạy ứng dụng
```bash
# Chạy từ source
python src/tts_app.py

# Hoặc install package và chạy
pip install -e .
tts-tool
```

### 🧪 Bước 6: Test tính năng
```python
# Test script đơn giản
python -c "
import edge_tts
import asyncio

async def test():
    tts = edge_tts.Communicate('Xin chào Việt Nam!', 'vi-VN-HoaiMyNeural')
    await tts.save('test.mp3')
    print('✅ Test thành công!')

asyncio.run(test())
"
```

---

## 🏗️ Phương pháp 3: Build từ Source

### 🔨 Bước 1: Setup Build Environment
```bash
# Cài đặt build tools
pip install pyinstaller>=5.0

# Windows: Cài Inno Setup (optional, cho installer)
# Download: https://jrsoftware.org/isdl.php

# macOS: Cài create-dmg (optional)
brew install create-dmg

# Linux: Cài AppImage tools (optional)
```

### 🏗️ Bước 2: Build Executable
```bash
# Chạy build script
python scripts/build_exe.py

# Hoặc build manual
python -m PyInstaller \
  --name "TTS_Tool_Vietnamese_v1.0.0" \
  --onefile \
  --windowed \
  --icon assets/icon.ico \
  src/tts_app.py
```

### 📊 Bước 3: Kiểm tra Build
```bash
# Kiểm tra file executable
ls -la dist/
# TTS_Tool_Vietnamese_v1.0.0.exe (~40-60MB)

# Test executable
./dist/TTS_Tool_Vietnamese_v1.0.0.exe

# Kiểm tra dependencies
ldd ./dist/TTS_Tool_Vietnamese_v1.0.0.exe  # Linux
otool -L ./dist/TTS_Tool_Vietnamese_v1.0.0  # macOS
```

### 📦 Bước 4: Tạo Release Package
```bash
# Script tự động tạo package
python scripts/create_release.py

# Kết quả:
# - release/TTS_Tool_Vietnamese_v1.0.0_Release.zip
# - release/TTS_Tool_Vietnamese_v1.0.0_Release/
```

---

## 🔧 Khắc phục sự cố cài đặt

### ❌ **Python không được nhận diện**
```bash
# Windows: Thêm Python vào PATH
1. Gỡ cài đặt Python
2. Tải lại từ python.org
3. ✅ Check "Add Python to PATH" khi cài

# Hoặc thêm manual:
# Thêm vào Environment Variables:
# C:\Users\YourName\AppData\Local\Programs\Python\Python39\
# C:\Users\YourName\AppData\Local\Programs\Python\Python39\Scripts\
```

### ❌ **"pip không được nhận diện"**
```bash
# Cài lại pip
python -m ensurepip --upgrade
python -m pip install --upgrade pip

# Hoặc download get-pip.py
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

### ❌ **"edge-tts cài đặt thất bại"**
```bash
# Cách 1: Upgrade setuptools
pip install --upgrade setuptools wheel

# Cách 2: Cài từ source
pip install git+https://github.com/rany2/edge-tts.git

# Cách 3: Sử dụng conda
conda install -c conda-forge edge-tts
```

### ❌ **"pygame không có âm thanh"**
```bash
# Windows: Cài lại pygame
pip uninstall pygame
pip install pygame

# macOS: Cài SDL2
brew install sdl2 sdl2_mixer sdl2_ttf

# Linux: Cài audio libs
sudo apt-get install python3-pygame
sudo apt-get install pulseaudio alsa-utils
```

### ❌ **"Git không được nhận diện"**
```bash
# Windows: Download Git for Windows
# https://git-scm.com/download/win

# macOS: Cài Xcode Command Line Tools
xcode-select --install

# Linux: Cài git
sudo apt-get install git       # Ubuntu/Debian
sudo yum install git           # CentOS/RHEL
```

### ❌ **"Build thất bại với PyInstaller"**
```bash
# Xóa cache và thử lại
rmdir /s build dist            # Windows
rm -rf build dist              # macOS/Linux

# Cài phiên bản cụ thể
pip install pyinstaller==5.7.0

# Build với verbose để debug
pyinstaller --log-level DEBUG src/tts_app.py
```

### ❌ **"Thiếu dependencies khi chạy executable"**
```bash
# Thêm hidden imports khi build
pyinstaller \
  --hidden-import edge_tts \
  --hidden-import gtts \
  --hidden-import pyttsx3 \
  --hidden-import pygame \
  --collect-all edge_tts \
  src/tts_app.py
```

---

## 🖥️ Cài đặt theo hệ điều hành

### 🪟 Windows 10/11

#### Yêu cầu:
- Windows 10 version 1903+ hoặc Windows 11
- 4GB RAM (khuyến nghị 8GB+)
- 1GB dung lượng trống
- Windows Defender/Antivirus updated

#### Hướng dẫn:
```powershell
# 1. Download và giải nén
# 2. Right-click → "Run as Administrator" (nếu cần)
# 3. Nếu SmartScreen cảnh báo:
#    - Click "More info"
#    - Click "Run anyway"

# Tạo shortcut (optional)
# Right-click executable → "Create shortcut"
# Kéo shortcut ra Desktop
```

### 🍎 macOS 10.14+

#### Yêu cầu:
- macOS Mojave 10.14+
- 4GB RAM
- 1GB dung lượng trống

#### Hướng dẫn:
```bash
# 1. Download .dmg file (nếu có) hoặc .zip
# 2. Nếu macOS block app:
#    System Preferences → Security & Privacy
#    Click "Open Anyway"

# Hoặc chạy từ Terminal:
chmod +x TTS_Tool_Vietnamese_v1.0.0
./TTS_Tool_Vietnamese_v1.0.0

# Tạo alias (optional)
echo 'alias tts-tool="/path/to/TTS_Tool_Vietnamese_v1.0.0"' >> ~/.zshrc
source ~/.zshrc
```

### 🐧 Ubuntu/Linux

#### Yêu cầu:
- Ubuntu 18.04+ hoặc equivalent
- Python 3.8+
- Audio system (PulseAudio/ALSA)

#### Hướng dẫn:
```bash
# 1. Cài dependencies hệ thống
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv
sudo apt-get install -y portaudio19-dev python3-pyaudio
sudo apt-get install -y espeak espeak-data libespeak1 libespeak-dev

# 2. Download và cài đặt
wget https://github.com/ngvinhbao/tts-tool-vietnamese/releases/latest/download/TTS_Tool_Vietnamese_v1.0.0_Linux.tar.gz
tar -xzf TTS_Tool_Vietnamese_v1.0.0_Linux.tar.gz
cd TTS_Tool_Vietnamese_v1.0.0_Release/

# 3. Make executable
chmod +x TTS_Tool_Vietnamese_v1.0.0
./TTS_Tool_Vietnamese_v1.0.0

# 4. Tạo desktop entry (optional)
cat > ~/.local/share/applications/tts-tool.desktop << EOF
[Desktop Entry]
Name=TTS Tool Vietnamese
Comment=Vietnamese Text-to-Speech Tool
Exec=/path/to/TTS_Tool_Vietnamese_v1.0.0
Icon=/path/to/assets/icon.png
Type=Application
Categories=AudioVideo;Audio;
EOF
```

---

## 🚀 Tự động hóa cài đặt

### 📜 Windows Batch Script
```batch
@echo off
echo TTS Tool Vietnamese - Auto Installer
echo =====================================

REM Download (requires curl hoặc wget for Windows)
echo Downloading TTS Tool Vietnamese...
curl -L -o TTS_Tool.zip https://github.com/ngvinhbao/tts-tool-vietnamese/releases/latest/download/TTS_Tool_Vietnamese_v1.0.0.zip

REM Extract
echo Extracting...
powershell -command "Expand-Archive -Path 'TTS_Tool.zip' -DestinationPath 'TTS_Tool_Vietnamese'"

REM Run
echo Starting TTS Tool...
cd TTS_Tool_Vietnamese
start TTS_Tool_Vietnamese_v1.0.0.exe

echo Installation complete!
pause
```

### 🐚 Linux/macOS Shell Script
```bash
#!/bin/bash
# TTS Tool Vietnamese - Auto Installer

echo "🎤 TTS Tool Vietnamese - Auto Installer"
echo "======================================="

# Check dependencies
command -v python3 >/dev/null 2>&1 || { echo "❌ Python3 required but not installed."; exit 1; }
command -v pip3 >/dev/null 2>&1 || { echo "❌ pip3 required but not installed."; exit 1; }

# Download
echo "📥 Downloading TTS Tool Vietnamese..."
wget -O tts-tool.zip https://github.com/ngvinhbao/tts-tool-vietnamese/releases/latest/download/TTS_Tool_Vietnamese_v1.0.0.zip

# Extract
echo "📂 Extracting..."
unzip tts-tool.zip
cd TTS_Tool_Vietnamese_v1.0.0_Release/

# Make executable
chmod +x TTS_Tool_Vietnamese_v1.0.0

# Run
echo "🚀 Starting TTS Tool..."
./TTS_Tool_Vietnamese_v1.0.0

echo "✅ Installation complete!"
```

---

## 📋 Checklist sau khi cài đặt

### ✅ Kiểm tra cơ bản
- [ ] Ứng dụng khởi động không lỗi
- [ ] Giao diện hiển thị đầy đủ
- [ ] Menu và buttons hoạt động
- [ ] Có thể nhập text tiếng Việt

### ✅ Kiểm tra TTS engine
- [ ] Edge TTS: Có 2 giọng HoaiMy, NamMinh
- [ ] Google TTS: Backup option
- [ ] System TTS: Fallback option

### ✅ Kiểm tra audio
- [ ] Convert text thành công
- [ ] File MP3 được tạo trong thư mục output/
- [ ] Play button phát được âm thanh
- [ ] Export function hoạt động

### ✅ Kiểm tra tính năng
- [ ] Load/Save text file
- [ ] Điều chỉnh speed và pitch
- [ ] Character counter
- [ ] Settings được lưu

---

## 📞 Hỗ trợ cài đặt

### 🆘 Nếu gặp khó khăn
```
📧 Email: Liên hệ qua Facebook hoặc Telegram
📘 Facebook: https://fb.com/ngvinhbao14081
💬 Telegram: https://t.me/nvb1408
🐛 GitHub Issues: https://github.com/ngvinhbao/tts-tool-vietnamese/issues
```

### 💡 Thông tin cần cung cấp khi báo lỗi
```
🖥️ Hệ điều hành: Windows 10/11, macOS, Ubuntu...
🐍 Phiên bản Python: python --version
📦 Phương pháp cài đặt: Executable, Source, Build
❌ Error message: Copy toàn bộ lỗi
📸 Screenshot: Nếu có lỗi giao diện
```

### 💖 Ủng hộ tác giả
```
Nếu ứng dụng hữu ích, đừng quên ủng hộ tác giả nhé!

🏦 VPBank: 0567546604
₿ Crypto: TULbGQbBGLL4VNrUYob7eWJUDup2ixkUT4
⭐ Star trên GitHub
📢 Share cho bạn bè
```

---

<div align="center">

**🎉 Chúc bạn sử dụng TTS Tool Vietnamese vui vẻ! 🎉**

**Made with ❤️ in Vietnam 🇻🇳**

[⬆ Về đầu trang](#-hướng-dẫn-cài-đặt-tts-tool-vietnamese)

</div>