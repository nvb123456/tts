#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TTS Tool Vietnamese - Build Script
Script tự động build executable file
Tác giả: Nguyễn Vĩnh Bảo
"""

import os
import sys
import json
import shutil
import subprocess
import zipfile
from datetime import datetime
from pathlib import Path

class TTSToolBuilder:
    def __init__(self):
        self.root_dir = Path.cwd().parent  # Lên 1 cấp từ scripts/
        self.build_dir = self.root_dir / "build"
        self.dist_dir = self.root_dir / "dist"
        self.release_dir = self.root_dir / "release"
        
        # Load config
        self.config = self.load_config()
        self.app_name = self.config['app_name'].replace(' ', '_')
        self.version = self.config['version']
        
    def load_config(self):
        """Load configuration from config.json"""
        config_file = self.root_dir / "config.json"
        if not config_file.exists():
            print(f"❌ Không tìm thấy config.json tại: {config_file}")
            sys.exit(1)
            
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def setup_directories(self):
        """Create necessary directories"""
        directories = [
            self.build_dir,
            self.dist_dir,
            self.release_dir
        ]
        
        for directory in directories:
            directory.mkdir(exist_ok=True)
            print(f"📁 Đã tạo thư mục: {directory}")
    
    def install_dependencies(self):
        """Install required dependencies"""
        print("📦 Đang cài đặt dependencies...")
        
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "--upgrade", "pip"
            ], check=True)
            
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", str(self.root_dir / "requirements.txt")
            ], check=True)
            
            print("✅ Dependencies đã được cài đặt thành công")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Cài đặt dependencies thất bại: {e}")
            return False
    
    def build_executable(self):
        """Build standalone executable using PyInstaller"""
        print(f"🔨 Đang build {self.app_name} v{self.version}...")
        
        # Ensure tts_app.py exists
        main_script = self.root_dir / "src" / "tts_app.py"
        if not main_script.exists():
            print(f"❌ Không tìm thấy file chính: {main_script}")
            print("Vui lòng đảm bảo tts_app.py có trong thư mục src/")
            return False
        
        # PyInstaller command
        exe_name = f"TTS_Tool_Vietnamese_v{self.version}"
        
        cmd = [
            sys.executable, "-m", "PyInstaller",
            str(main_script),
            "--name", exe_name,
            "--onefile",
            "--windowed",
            "--clean",
            "--noconfirm",
            f"--distpath={self.dist_dir}",
            f"--workpath={self.build_dir}",
            "--hidden-import", "edge_tts",
            "--hidden-import", "gtts", 
            "--hidden-import", "pyttsx3",
            "--hidden-import", "pygame",
            "--exclude-module", "matplotlib",
            "--exclude-module", "numpy",
            "--exclude-module", "pandas",
            "--exclude-module", "scipy",
            "--exclude-module", "tensorflow",
            "--exclude-module", "torch"
        ]
        
        # Add icon if exists
        icon_file = self.root_dir / "assets" / "icon.ico"
        if icon_file.exists():
            cmd.extend(["--icon", str(icon_file)])
            print(f"🎨 Sử dụng icon: {icon_file}")
        
        # Add version info
        cmd.extend([
            "--version-file", str(self.create_version_file())
        ])
        
        try:
            print("⚡ Đang chạy PyInstaller...")
            subprocess.run(cmd, check=True, cwd=self.root_dir)
            
            # Check if build successful
            exe_file = self.dist_dir / f"{exe_name}.exe"
            if exe_file.exists():
                file_size = exe_file.stat().st_size / 1024 / 1024
                print(f"✅ Build thành công: {exe_file}")
                print(f"📊 Kích thước file: {file_size:.1f} MB")
                return exe_file
            else:
                print("❌ Build thất bại - không tìm thấy file executable")
                return None
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Build thất bại: {e}")
            return None
    
    def create_version_file(self):
        """Tạo file version info cho Windows executable"""
        version_content = f"""# UTF-8
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({self.version.replace('.', ',')},0),
    prodvers=({self.version.replace('.', ',')},0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'{self.config["author"]}'),
        StringStruct(u'FileDescription', u'{self.config["description"]}'),
        StringStruct(u'FileVersion', u'{self.version}'),
        StringStruct(u'InternalName', u'{self.app_name}'),
        StringStruct(u'LegalCopyright', u'© 2024 {self.config["author"]}'),
        StringStruct(u'OriginalFilename', u'{self.app_name}.exe'),
        StringStruct(u'ProductName', u'{self.config["app_name"]}'),
        StringStruct(u'ProductVersion', u'{self.version}')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)"""
        
        version_file = self.build_dir / "version_info.txt"
        with open(version_file, 'w', encoding='utf-8') as f:
            f.write(version_content)
        
        return version_file
    
    def create_release_package(self, exe_file):
        """Create release package with all necessary files"""
        release_name = f"TTS_Tool_Vietnamese_v{self.version}_Release"
        package_dir = self.release_dir / release_name
        
        # Clean and create package directory
        if package_dir.exists():
            shutil.rmtree(package_dir)
        package_dir.mkdir(parents=True)
        
        print(f"📦 Đang tạo gói phát hành: {package_dir}")
        
        # Copy executable
        shutil.copy2(exe_file, package_dir)
        
        # Copy documentation and config
        docs_to_copy = [
            ("docs/README.md", "README.md"),
            ("docs/INSTALL.md", "INSTALL.md") if (self.root_dir / "docs/INSTALL.md").exists() else None,
            ("requirements.txt", "requirements.txt"),
            ("config.json", "config.json"),
            ("LICENSE", "LICENSE") if (self.root_dir / "LICENSE").exists() else None
        ]
        
        for item in docs_to_copy:
            if item is None:
                continue
            src, dst = item
            src_path = self.root_dir / src
            if src_path.exists():
                shutil.copy2(src_path, package_dir / dst)
                print(f"✅ Đã copy: {src}")
        
        # Copy assets if exists
        assets_dir = self.root_dir / "assets"
        if assets_dir.exists() and any(assets_dir.iterdir()):
            shutil.copytree(assets_dir, package_dir / "assets")
            print(f"✅ Đã copy thư mục assets")
        
        # Create release notes
        self.create_release_notes(package_dir, exe_file)
        
        # Create ZIP file
        zip_file = self.release_dir / f"{release_name}.zip"
        with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
            for file_path in package_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(package_dir)
                    zf.write(file_path, arcname)
                    
        zip_size = zip_file.stat().st_size / 1024 / 1024
        print(f"📦 Gói phát hành đã tạo: {zip_file}")
        print(f"📊 Kích thước gói: {zip_size:.1f} MB")
        
        return zip_file
    
    def create_release_notes(self, package_dir, exe_file):
        """Tạo file ghi chú phát hành"""
        release_notes = f"""🎉 {self.config['app_name']} v{self.version}

📅 Ngày phát hành: {datetime.now().strftime('%d/%m/%Y')}
👨‍💻 Tác giả: {self.config['author']}

## 🚀 Cách cài đặt và sử dụng:

### Bước 1: Giải nén
- Giải nén file ZIP này vào thư mục bất kỳ
- Không cần cài đặt thêm gì khác

### Bước 2: Chạy ứng dụng
- Double-click file {exe_file.name}
- Lần đầu chạy có thể hơi lâu (khoảng 10-15 giây)
- Windows Defender có thể cảnh báo, chọn "More info" → "Run anyway"

### Bước 3: Sử dụng
1. Chọn giọng nói: HoaiMy (nữ) hoặc NamMinh (nam)
2. Nhập văn bản tiếng Việt vào ô text
3. Điều chỉnh tốc độ và cao độ nếu cần
4. Click "🎤 Chuyển thành giọng nói"
5. Click "▶️ Phát" để nghe hoặc "💾 Xuất file" để lưu

## ✨ Tính năng nổi bật:

🇻🇳 **Giọng tiếng Việt Neural chất lượng cao**
- HoaiMy (nữ): Giọng trẻ trung, phù hợp content giải trí
- NamMinh (nam): Giọng trang trọng, phù hợp tin tức, giáo dục

🚀 **Hiệu suất vượt trội**
- Không giới hạn ký tự - Tạo audio dài hàng trăm tiếng
- Tốc độ xử lý siêu nhanh - 1 tiếng audio chỉ cần 3 phút
- Không tốn phí API hàng tháng
- Chạy trên máy cấu hình thấp

⚡ **Tính năng nâng cao**
- Xử lý hàng loạt file văn bản/phụ đề
- Tự động tạo file phụ đề chuẩn timing với audio
- Điều chỉnh tốc độ (0.5x - 2.0x) và cao độ (-20Hz đến +20Hz)
- Xuất file MP3/WAV chất lượng cao

## 🎯 Ứng dụng thực tế:

📺 **Content Creators**: Voice-over cho video YouTube, TikTok
📚 **Giáo dục**: Đọc sách giáo khoa, tài liệu học tập  
📰 **Tin tức**: Tạo bản tin tự động
🎧 **Podcast**: Intro/Outro tự động
♿ **Trợ năng**: Hỗ trợ người khiếm thị

## 🔧 Yêu cầu hệ thống:

- **OS**: Windows 10/11, macOS 10.14+, Ubuntu 18.04+
- **RAM**: 4GB+ (khuyến nghị 8GB+)
- **Disk**: 500MB trống
- **Network**: Internet (để download giọng nói lần đầu)

## 🐛 Khắc phục sự cố:

**❌ Ứng dụng không khởi động được:**
- Tắt antivirus tạm thời
- Chạy với quyền Administrator
- Kiểm tra Windows Defender

**❌ Không có âm thanh:**
- Kiểm tra loa/headphone
- Khởi động lại ứng dụng
- Thử giọng khác

**❌ Lỗi "No internet connection":**
- Kiểm tra kết nối internet
- Edge TTS cần internet lần đầu để download giọng

## 📞 Liên hệ hỗ trợ:

👨‍💻 **Tác giả**: {self.config['author']}
📘 **Facebook**: {self.config['facebook']}
💬 **Telegram**: {self.config['telegram']}

## 💖 Ủng hộ tác giả:

Nếu bạn thấy ứng dụng hữu ích, hãy ủng hộ tác giả để duy trì và phát triển thêm tính năng!

🏦 **VPBank**: {self.config['support_info']['vpbank']}
₿ **Crypto (TRC20)**: {self.config['support_info']['crypto_trc20']}

## 📄 License:

{self.config['license']} License - Sử dụng miễn phí cho mục đích cá nhân

---

🙏 **Cảm ơn bạn đã sử dụng TTS Tool Vietnamese!**

⭐ Nếu thấy hữu ích, hãy chia sẻ cho bạn bè nhé! ⭐

**Made with ❤️ in Vietnam 🇻🇳**
"""
        
        with open(package_dir / "RELEASE_NOTES.txt", 'w', encoding='utf-8') as f:
            f.write(release_notes)
            
        print("✅ Đã tạo RELEASE_NOTES.txt")
    
    def create_installer_script(self):
        """Tạo script installer cho Windows (Inno Setup)"""
        iss_content = f"""[Setup]
AppName={self.config['app_name']}
AppVersion={self.version}
AppPublisher={self.config['author']}
AppPublisherURL={self.config['website']}
AppSupportURL={self.config['facebook']}
DefaultDirName={{autopf}}\\{self.config['app_name']}
DefaultGroupName={self.config['app_name']}
AllowNoIcons=yes
OutputDir=.\\dist
OutputBaseFilename=TTS_Tool_Vietnamese_Setup_v{self.version}
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "vietnamese"; MessagesFile: "compiler:Languages\\Vietnamese.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{{cm:CreateDesktopIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{{cm:CreateQuickLaunchIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked; OnlyBelowVersion: 6.1

[Files]
Source: ".\\dist\\TTS_Tool_Vietnamese_v{self.version}.exe"; DestDir: "{{app}}"; Flags: ignoreversion
Source: ".\\README.md"; DestDir: "{{app}}"; Flags: ignoreversion
Source: ".\\config.json"; DestDir: "{{app}}"; Flags: ignoreversion

[Icons]
Name: "{{group}}\\{self.config['app_name']}"; Filename: "{{app}}\\TTS_Tool_Vietnamese_v{self.version}.exe"
Name: "{{group}}\\Hướng dẫn sử dụng"; Filename: "{{app}}\\README.md"
Name: "{{group}}\\{{cm:UninstallProgram,{self.config['app_name']}}}"; Filename: "{{uninstallexe}}"
Name: "{{autodesktop}}\\{self.config['app_name']}"; Filename: "{{app}}\\TTS_Tool_Vietnamese_v{self.version}.exe"; Tasks: desktopicon

[Run]
Filename: "{{app}}\\TTS_Tool_Vietnamese_v{self.version}.exe"; Description: "{{cm:LaunchProgram,{self.config['app_name']}}}"; Flags: nowait postinstall skipifsilent

[Code]
function GetUninstallString(): String;
var
  sUnInstPath: String;
  sUnInstallString: String;
begin
  sUnInstPath := ExpandConstant('Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{self.config['app_name']}_is1');
  sUnInstallString := '';
  if not RegQueryStringValue(HKLM, sUnInstPath, 'UninstallString', sUnInstallString) then
    RegQueryStringValue(HKCU, sUnInstPath, 'UninstallString', sUnInstallString);
  Result := sUnInstallString;
end;

function IsUpgrade(): Boolean;
begin
  Result := (GetUninstallString() <> '');
end;
"""
        
        iss_file = self.root_dir / "installer.iss"
        with open(iss_file, 'w', encoding='utf-8') as f:
            f.write(iss_content)
            
        print(f"✅ Đã tạo installer script: {iss_file}")
        return iss_file
    
    def run_full_build(self):
        """Chạy toàn bộ quá trình build"""
        print("🚀 Bắt đầu quá trình build...")
        print(f"📱 App: {self.config['app_name']} v{self.version}")
        print(f"👨‍💻 Tác giả: {self.config['author']}")
        print("=" * 60)
        
        # 1. Setup directories
        self.setup_directories()
        
        # 2. Install dependencies
        if not self.install_dependencies():
            return False
            
        # 3. Build executable
        exe_file = self.build_executable()
        if not exe_file:
            return False
            
        # 4. Create release package
        zip_file = self.create_release_package(exe_file)
        
        # 5. Create installer script
        self.create_installer_script()
        
        print("=" * 60)
        print("🎉 BUILD HOÀN THÀNH!")
        print(f"📁 Executable: {exe_file}")
        print(f"📦 Release package: {zip_file}")
        print(f"💖 Đừng quên ủng hộ tác giả: VPBank - {self.config['support_info']['vpbank']}")
        print("=" * 60)
        
        return True

def main():
    """Main build function"""
    print("🔨 TTS Tool Vietnamese - Build Script")
    print("👨‍💻 Phát triển bởi: Nguyễn Vĩnh Bảo")
    print("📞 Liên hệ: fb.com/ngvinhbao14081 | t.me/nvb1408")
    print("💖 Ủng hộ: VPBank - 0567546604")
    print("=" * 60)
    
    builder = TTSToolBuilder()
    
    try:
        success = builder.run_full_build()
        if success:
            print("\n✅ Build thành công! Bạn có thể phân phối ứng dụng.")
            print("📋 Checklist sau khi build:")
            print("  [ ] Test ứng dụng trên máy sạch")
            print("  [ ] Kiểm tra tất cả tính năng")
            print("  [ ] Upload lên GitHub Releases")
            print("  [ ] Cập nhật documentation")
            print("  [ ] Thông báo cho user")
        else:
            print("\n❌ Build thất bại! Kiểm tra lại lỗi ở trên.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⏹️ Build bị hủy bởi người dùng")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Lỗi không mong muốn: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()