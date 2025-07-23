#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TTS Tool Vietnamese - Setup Script
Python package setup for TTS Tool Vietnamese
Tác giả: Nguyễn Vĩnh Bảo
Liên hệ: fb.com/ngvinhbao14081 | t.me/nvb1408
"""

from setuptools import setup, find_packages
import json
import os
from pathlib import Path

# Read config file
def load_config():
    config_path = Path(__file__).parent / 'config.json'
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        # Default config if file doesn't exist
        return {
            "app_name": "TTS Tool Vietnamese",
            "version": "1.0.0",
            "author": "Nguyễn Vĩnh Bảo",
            "author_email": "contact@example.com",
            "description": "Công cụ chuyển văn bản thành giọng nói tiếng Việt chất lượng cao",
            "website": "https://github.com/ngvinhbao/tts-tool-vietnamese",
            "license": "MIT"
        }

# Read README file
def read_readme():
    readme_path = Path(__file__).parent / 'docs' / 'README.md'
    if readme_path.exists():
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "TTS Tool Vietnamese - Công cụ chuyển văn bản thành giọng nói tiếng Việt"

# Read requirements
def read_requirements():
    req_path = Path(__file__).parent / 'requirements.txt'
    requirements = []
    if req_path.exists():
        with open(req_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Remove version constraints for basic setup
                    package = line.split('>=')[0].split('==')[0].split('~=')[0]
                    requirements.append(package)
    return requirements

# Load configuration
config = load_config()

# Package information
PACKAGE_NAME = "tts-tool-vietnamese"
VERSION = config['version']
AUTHOR = config['author']
AUTHOR_EMAIL = config.get('author_email', 'contact@example.com')
DESCRIPTION = config['description']
LONG_DESCRIPTION = read_readme()
URL = config.get('website', 'https://github.com/ngvinhbao/tts-tool-vietnamese')
LICENSE = config.get('license', 'MIT')

# Requirements
INSTALL_REQUIRES = [
    'edge-tts>=6.1.0',
    'gTTS>=2.3.0',
    'pyttsx3>=2.90',
    'pygame>=2.1.0',
    'pillow>=9.0.0',
    'requests>=2.28.0',
]

EXTRAS_REQUIRE = {
    'dev': [
        'pytest>=7.0',
        'black>=22.0',
        'flake8>=4.0',
        'mypy>=0.950',
        'isort>=5.10',
    ],
    'build': [
        'pyinstaller>=5.0',
        'setuptools>=65.0',
        'wheel>=0.37',
    ],
    'audio': [
        'librosa>=0.9.0',
        'soundfile>=0.10.0',
        'pydub>=0.25.0',
    ],
    'gui': [
        'customtkinter>=5.0.0',
        'pillow>=9.0.0',
    ]
}

# All extras
EXTRAS_REQUIRE['all'] = [
    package for extra in EXTRAS_REQUIRE.values()
    for package in extra
]

setup(
    # Basic package information
    name=PACKAGE_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url=URL,
    
    # Project URLs
    project_urls={
        "Bug Reports": f"{URL}/issues",
        "Source": f"{URL}",
        "Documentation": f"{URL}/wiki",
        "Facebook": "https://fb.com/ngvinhbao14081",
        "Telegram": "https://t.me/nvb1408",
        "Funding": "https://github.com/sponsors/ngvinhbao",  # Nếu có GitHub Sponsors
    },
    
    # Package discovery
    packages=find_packages(exclude=['tests*', 'docs*', 'scripts*']),
    
    # Include additional files
    package_data={
        'tts_tool_vietnamese': [
            '*.json',
            '*.txt',
            '*.md',
            'assets/*',
            'config/*',
        ],
    },
    include_package_data=True,
    
    # Classifiers
    classifiers=[
        # Development Status
        "Development Status :: 4 - Beta",
        
        # Intended Audience
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Other Audience",
        
        # Topic
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Desktop Environment",
        "Topic :: Utilities",
        
        # License
        "License :: OSI Approved :: MIT License",
        
        # Programming Language
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
        
        # Operating System
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        
        # Natural Language
        "Natural Language :: Vietnamese",
        "Natural Language :: English",
        
        # Environment
        "Environment :: Win32 (MS Windows)",
        "Environment :: MacOS X",
        "Environment :: X11 Applications :: Tkinter",
        "Environment :: Console",
    ],
    
    # Keywords
    keywords=[
        "tts", "text-to-speech", "vietnamese", "voice", "synthesis", 
        "speech", "audio", "ai", "neural", "edge-tts", "gtts",
        "hoimy", "namminh", "microsoft", "vietnam", "desktop",
        "gui", "tkinter", "mp3", "wav", "free", "open-source"
    ],
    
    # Python version requirement
    python_requires='>=3.8',
    
    # Dependencies
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    
    # Entry points
    entry_points={
        'console_scripts': [
            'tts-tool=src.tts_app:main',
            'tts-vietnamese=src.tts_app:main',
            'tts-tool-gui=src.tts_app:main',
        ],
        'gui_scripts': [
            'tts-tool-desktop=src.tts_app:main',
        ]
    },
    
    # Data files
    data_files=[
        ('config', ['config.json']),
        ('docs', ['docs/README.md', 'docs/INSTALL.md']),
        ('', ['LICENSE', 'requirements.txt']),
    ],
    
    # Zip safe
    zip_safe=False,
    
    # Additional metadata
    platforms=['Windows', 'macOS', 'Linux'],
    license=LICENSE,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    
    # Options for different commands
    options={
        'bdist_wheel': {
            'universal': False,  # Not universal because of binary dependencies
        },
        'build_py': {
            'compile': True,
            'optimize': 1,
        },
    },
    
    # Command classes (if needed)
    # cmdclass={
    #     'build_exe': BuildExeCommand,
    #     'clean': CleanCommand,
    # },
)

# Post-install message
def post_install():
    print("""
🎉 TTS Tool Vietnamese đã được cài đặt thành công!

🚀 Cách sử dụng:
   
   # Chạy ứng dụng GUI
   tts-tool
   
   # Hoặc
   python -m src.tts_app

📚 Tài liệu:
   https://github.com/ngvinhbao/tts-tool-vietnamese

🐛 Báo lỗi:
   https://github.com/ngvinhbao/tts-tool-vietnamese/issues

👨‍💻 Tác giả: Nguyễn Vĩnh Bảo
📞 Liên hệ: fb.com/ngvinhbao14081 | t.me/nvb1408
💖 Ủng hộ: VPBank - 0567546604

✨ Tính năng nổi bật:
   🇻🇳 Giọng tiếng Việt Neural chất lượng cao
   🚀 Không giới hạn ký tự
   ⚡ Tốc độ xử lý siêu nhanh
   💰 Không tốn phí API
   📁 Xử lý hàng loạt file

🙏 Cảm ơn bạn đã sử dụng TTS Tool Vietnamese!
""")

if __name__ == "__main__":
    # Run setup
    setup()
    
    # Post-install message
    import sys
    if 'install' in sys.argv:
        post_install()