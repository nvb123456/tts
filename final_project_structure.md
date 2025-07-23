# 🚀 TTS Tool Vietnamese - Project Hoàn Chỉnh

> 👨‍💻 **Phát triển bởi**: Nguyễn Vĩnh Bảo  
> 📞 **Liên hệ**: [Facebook](https://fb.com/ngvinhbao14081) | [Telegram](https://t.me/nvb1408)  
> 💖 **Ủng hộ**: VPBank - 0567546604 | Crypto: TULbGQbBGLL4VNrUYob7eWJUDup2ixkUT4

## 📁 Cấu trúc project hoàn chỉnh

```
TTS_Tool_Vietnamese/                 # Thư mục gốc
├── 📁 src/                          # Source code
│   └── tts_app.py                   # [FILE 1] Main application
├── 📁 assets/                       # Tài nguyên
│   ├── icon.ico                     # Icon ứng dụng
│   ├── logo.png                     # Logo
│   └── banner.png                   # Banner
├── 📁 docs/                         # Tài liệu
│   ├── README.md                    # [FILE 5] Documentation chính
│   ├── INSTALL.md                   # [FILE 6] Hướng dẫn cài đặt
│   └── CHANGELOG.md                 # Lịch sử thay đổi
├── 📁 scripts/                      # Scripts tiện ích
│   ├── build_exe.py                 # [FILE 4] Build executable
│   ├── installer.iss                # Inno Setup script
│   └── deploy.py                    # Deploy script
├── 📁 tests/                        # Unit tests
│   ├── __init__.py
│   ├── test_tts.py
│   └── test_gui.py
├── requirements.txt                 # [FILE 2] Dependencies
├── config.json                      # [FILE 3] Cấu hình app
├── setup.py                        # [FILE 10] Python setup
├── LICENSE                          # [FILE 8] License
├── .gitignore                       # [FILE 9] Git ignore
├── run_app.bat                      # [FILE 7] Windows quick start
├── run_app.sh                       # Linux/macOS quick start
└── README.md                        # Project overview

📁 output/                           # (Tự tạo) Audio files
📁 build/                            # (Tự tạo) Build artifacts  
📁 dist/                             # (Tự tạo) Distribution files
📁 release/                          # (Tự tạo) Release packages
```

## 🛠️ Cách tạo project từ đầu

### Bước 1: Tạo cấu trúc thư mục
```bash
# Tạo thư mục chính
mkdir TTS_Tool_Vietnamese
cd TTS_Tool_Vietnamese

# Tạo các thư mục con
mkdir src assets docs scripts tests
mkdir build dist release output

# Tạo files rỗng
touch src/__init__.py
touch tests/__init__.py
```

### Bước 2: Copy các files từ artifacts

#### 📄 FILE 1: src/tts_app.py
```python
# Copy toàn bộ nội dung từ [FILE 1: src/tts_app.py] ở trên
```

#### 📄 FILE 2: requirements.txt
```text
# Copy nội dung từ [FILE 2: requirements.txt]
```

#### 📄 FILE 3: config.json
```json
// Copy nội dung từ [FILE 3: config.json]
```

#### 📄 FILE 4: scripts/build_exe.py
```python
# Copy nội dung từ [FILE 4: scripts/build_exe.py]
```

#### 📄 FILE 5: docs/README.md
```markdown
# Copy nội dung từ [FILE 5: docs/README.md]
```

#### 📄 FILE 6: docs/INSTALL.md
```markdown
# Copy nội dung từ [FILE 6: docs/INSTALL.md]
```

#### 📄 FILE 7: run_app.bat
```batch
REM Copy nội dung từ [FILE 7: run_app.bat]
```

#### 📄 FILE 8: LICENSE
```text
Copy nội dung từ [FILE 8: LICENSE]
```

#### 📄 FILE 9: .gitignore
```text
# Copy nội dung từ [FILE 9: .gitignore]
```

#### 📄 FILE 10: setup.py
```python
# Copy nội dung từ [FILE 10: setup.py]
```

### Bước 3: Tạo các files bổ sung

#### 📄 run_app.sh (Linux/macOS)
```bash
#!/bin/bash
# TTS Tool Vietnamese - Quick Start Script (Linux/macOS)

echo "🎤 TTS Tool Vietnamese - Quick Start"
echo "👨‍💻 Phát triển bởi: Nguyễn Vĩnh Bảo"
echo "📞 Liên hệ: fb.com/ngvinhbao14081 | t.me/nvb1408"
echo "💖 Ủng hộ: VPBank - 0567546604"
echo "=================================================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 chưa được cài đặt"
    echo "📥 Vui lòng cài đặt Python3 trước"
    exit 1
fi

echo "✅ Python3 đã sẵn sàng: $(python3 --version)"

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 chưa được cài đặt"
    exit 1
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "🌍 Tạo virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Kích hoạt virtual environment..."
source venv/bin/activate

# Install dependencies
if [ ! -f "venv/.deps_installed" ]; then
    echo "📦 Cài đặt dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    touch venv/.deps_installed
    echo "✅ Dependencies đã được cài đặt"
fi

# Create output directory
mkdir -p output

echo "🚀 Khởi động TTS Tool Vietnamese..."
python src/tts_app.py

echo "🎉 Cảm ơn bạn đã sử dụng TTS Tool Vietnamese!"
```

#### 📄 docs/CHANGELOG.md
```markdown
# 📋 Changelog - TTS Tool Vietnamese

All notable changes to this project will be documented in this file.

## [1.0.0] - 2024-12-22

### ✨ Added
- Ứng dụng TTS đầu tiên với giọng Việt Neural
- Giao diện GUI thân thiện với Tkinter
- Hỗ trợ 2 giọng: HoaiMy (nữ) và NamMinh (nam)
- Điều chỉnh tốc độ và cao độ giọng nói
- Xuất file MP3/WAV chất lượng cao
- Load/Save file văn bản
- Auto-save settings
- Character counter
- Progress bar với thông tin ủng hộ

### 🔧 Technical
- Sử dụng Microsoft Edge TTS API
- Fallback với Google TTS và System TTS
- Async processing để không block GUI
- Virtual environment support
- Build script với PyInstaller
- Cross-platform compatibility

### 📚 Documentation
- README.md với hướng dẫn chi tiết
- INSTALL.md với 3 phương pháp cài đặt
- Release notes tự động
- License MIT
- Git ignore hoàn chỉnh

### 🏗️ Build System
- PyInstaller build script
- Inno Setup installer (Windows)
- Release packaging automation
- GitHub Actions ready (future)

## [Unreleased]

### 🔮 Planned Features
- Batch processing GUI
- Voice effects (echo, reverb)
- Subtitle generation with timing
- Voice cloning (AI)
- Web app version
- Mobile apps
- Cloud sync
- API service

---

👨‍💻 **Phát triển bởi**: Nguyễn Vĩnh Bảo  
📞 **Liên hệ**: fb.com/ngvinhbao14081 | t.me/nvb1408  
💖 **Ủng hộ**: VPBank - 0567546604
```

#### 📄 tests/test_tts.py
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TTS Tool Vietnamese - Unit Tests
Test cases for TTS functionality
"""

import unittest
import asyncio
import tempfile
import os
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

class TestTTSEngines(unittest.TestCase):
    """Test TTS engines functionality"""
    
    def setUp(self):
        self.test_text = "Xin chào, đây là test TTS Tool Vietnamese."
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        # Clean up temp files
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @unittest.skipUnless(EDGE_TTS_AVAILABLE, "Edge TTS not available")
    def test_edge_tts_vietnamese(self):
        """Test Edge TTS with Vietnamese voice"""
        async def run_test():
            output_file = os.path.join(self.temp_dir, "test_edge.mp3")
            
            communicate = edge_tts.Communicate(
                self.test_text, 
                "vi-VN-HoaiMyNeural"
            )
            await communicate.save(output_file)
            
            # Check if file was created and has content
            self.assertTrue(os.path.exists(output_file))
            self.assertGreater(os.path.getsize(output_file), 1000)  # At least 1KB
        
        asyncio.run(run_test())
    
    @unittest.skipUnless(GTTS_AVAILABLE, "gTTS not available")
    def test_google_tts_vietnamese(self):
        """Test Google TTS with Vietnamese"""
        output_file = os.path.join(self.temp_dir, "test_gtts.mp3")
        
        tts = gTTS(text=self.test_text, lang='vi', slow=False)
        tts.save(output_file)
        
        # Check if file was created and has content
        self.assertTrue(os.path.exists(output_file))
        self.assertGreater(os.path.getsize(output_file), 1000)  # At least 1KB
    
    def test_text_processing(self):
        """Test text processing functions"""
        # Test character counting
        char_count = len(self.test_text)
        self.assertGreater(char_count, 0)
        
        # Test text validation
        self.assertTrue(self.test_text.strip())
        
        # Test Vietnamese characters
        vietnamese_text = "Tiếng Việt có dấu: áàảãạ êéèẻẽẹ"
        self.assertIn('ệ', vietnamese_text)

class TestConfigFile(unittest.TestCase):
    """Test configuration file handling"""
    
    def test_config_loading(self):
        """Test loading config.json"""
        config_path = Path(__file__).parent.parent / 'config.json'
        
        if config_path.exists():
            import json
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Check required fields
            self.assertIn('app_name', config)
            self.assertIn('version', config)
            self.assertIn('author', config)
            self.assertEqual(config['author'], 'Nguyễn Vĩnh Bảo')

class TestFileOperations(unittest.TestCase):
    """Test file operations"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_text_file_operations(self):
        """Test loading and saving text files"""
        test_content = "Đây là nội dung test file tiếng Việt.\nDòng thứ hai."
        test_file = os.path.join(self.temp_dir, "test.txt")
        
        # Test saving
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        # Test loading
        with open(test_file, 'r', encoding='utf-8') as f:
            loaded_content = f.read()
        
        self.assertEqual(test_content, loaded_content)

if __name__ == '__main__':
    print("🧪 Running TTS Tool Vietnamese Tests")
    print("👨‍💻 Phát triển bởi: Nguyễn Vĩnh Bảo")
    print("=" * 50)
    
    # Run tests
    unittest.main(verbosity=2)
```

## 🚀 Cách sử dụng sau khi tạo project

### 1. Cài đặt và chạy
```bash
# Windows
run_app.bat

# Linux/macOS
chmod +x run_app.sh
./run_app.sh

# Hoặc manual
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
python src/tts_app.py
```

### 2. Build executable
```bash
python scripts/build_exe.py
```

### 3. Run tests
```bash
python -m pytest tests/
# Hoặc
python tests/test_tts.py
```

### 4. Install as package
```bash
pip install -e .
tts-tool
```

## 📦 Phân phối và chia sẻ

### GitHub Repository
```bash
git init
git add .
git commit -m "🎉 Initial release v1.0.0 - TTS Tool Vietnamese"
git branch -M main
git remote add origin https://github.com/ngvinhbao/tts-tool-vietnamese.git
git push -u origin main

# Tạo release
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

### Release Package
```bash
# Tự động tạo release package
python scripts/build_exe.py

# Kết quả:
# release/TTS_Tool_Vietnamese_v1.0.0_Release.zip
```

## 🎯 Checklist hoàn thành project

- [ ] ✅ Tạo tất cả 10 files chính
- [ ] ✅ Copy code từ các artifacts
- [ ] ✅ Cài đặt dependencies
- [ ] ✅ Test chạy ứng dụng
- [ ] ✅ Build executable thành công
- [ ] ✅ Test trên máy khác
- [ ] ✅ Tạo GitHub repository
- [ ] ✅ Upload release package
- [ ] ✅ Viết README và documentation
- [ ] ✅ Marketing và chia sẻ

## 💖 Lời cảm ơn

**Dự án này được phát triển với ❤️ bởi Nguyễn Vĩnh Bảo**

📞 **Liên hệ**: [Facebook](https://fb.com/ngvinhbao14081) | [Telegram](https://t.me/nvb1408)  
💰 **Ủng hộ**: VPBank - 0567546604 | Crypto: TULbGQbBGLL4VNrUYob7eWJUDup2ixkUT4

**Nếu project hữu ích, đừng quên:**
- ⭐ Star trên GitHub  
- 📢 Share cho bạn bè
- 💰 Ủng hộ tác giả
- 🐛 Báo lỗi nếu có
- 💡 Đề xuất tính năng mới

---

**🇻🇳 Made with ❤️ in Vietnam 🇻🇳**