#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TTS Tool Vietnamese - Main Application
Công cụ chuyển văn bản thành giọng nói tiếng Việt
Tác giả: Nguyễn Vĩnh Bảo
Liên hệ: fb.com/ngvinhbao14081 | t.me/nvb1408
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import asyncio
import os
import sys
from pathlib import Path
import json
import time
from datetime import datetime
import webbrowser

# Import thư viện TTS
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

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

# Import thư viện âm thanh
try:
    import pygame
    pygame.mixer.init()
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

class TTSApp:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        self.load_settings()
        self.current_audio_file = None
        
        # Voices dictionary - VERIFIED Vietnamese only
        self.edge_voices = {
            "👩 HoaiMy (Nữ) - Giọng Việt Neural": "vi-VN-HoaiMyNeural",
            "👨 NamMinh (Nam) - Giọng Việt Neural": "vi-VN-NamMinhNeural"
        }
        
        self.google_voices = {
            "🇻🇳 Tiếng Việt (Google TTS)": "vi"
        }
        
    def setup_ui(self):
        self.root.title("🎤 TTS Tool Vietnamese - Chuyển văn bản thành giọng nói")
        self.root.geometry("950x750")
        self.root.configure(bg='#2b2b2b')
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Segoe UI', 16, 'bold'), background='#2b2b2b', foreground='#ffffff')
        style.configure('Heading.TLabel', font=('Segoe UI', 10, 'bold'), background='#2b2b2b', foreground='#4CAF50')
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2b2b2b')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title với thông tin liên hệ
        title_label = ttk.Label(main_frame, text="🎤 TTS Tool Vietnamese - Chuyển văn bản thành giọng nói", style='Title.TLabel')
        title_label.pack(pady=(0, 5))
        
        # Subtitle với thông tin tác giả
        subtitle_label = tk.Label(main_frame, text="Phát triển bởi Nguyễn Vĩnh Bảo | fb.com/ngvinhbao14081 | t.me/nvb1408", 
                                bg='#2b2b2b', fg='#888888', font=('Segoe UI', 9))
        subtitle_label.pack(pady=(0, 15))
        
        # Menu bar
        self.create_menu_bar()
        
        # Engine selection frame - Ẩn Engine
        engine_frame = tk.LabelFrame(main_frame, text="🎛️ Cài đặt giọng nói", bg='#3c3c3c', fg='#ffffff', font=('Segoe UI', 10, 'bold'))
        engine_frame.pack(fill='x', pady=(0, 15))
        
        # Ẩn Engine selection - tự động chọn Edge TTS
        self.engine_var = tk.StringVar(value="Edge TTS")
        
        # Voice selection - chỉ hiển thị Voice
        tk.Label(engine_frame, text="🎭 Giọng nói:", bg='#3c3c3c', fg='#ffffff', font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, sticky='w', padx=10, pady=10)
        self.voice_var = tk.StringVar()
        self.voice_combo = ttk.Combobox(engine_frame, textvariable=self.voice_var, width=35, state='readonly')
        self.voice_combo.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        
        # Speed and pitch controls
        controls_frame = tk.Frame(engine_frame, bg='#3c3c3c')
        controls_frame.grid(row=1, column=0, columnspan=2, sticky='ew', padx=10, pady=(0, 10))
        
        tk.Label(controls_frame, text="Tốc độ:", bg='#3c3c3c', fg='#ffffff').grid(row=0, column=0, sticky='w')
        self.speed_var = tk.DoubleVar(value=1.0)
        speed_scale = tk.Scale(controls_frame, from_=0.5, to=2.0, resolution=0.1, orient='horizontal', 
                              variable=self.speed_var, bg='#3c3c3c', fg='#ffffff', highlightbackground='#3c3c3c')
        speed_scale.grid(row=0, column=1, sticky='ew', padx=(5, 20))
        
        tk.Label(controls_frame, text="Cao độ:", bg='#3c3c3c', fg='#ffffff').grid(row=0, column=2, sticky='w')
        self.pitch_var = tk.DoubleVar(value=0.0)
        pitch_scale = tk.Scale(controls_frame, from_=-20.0, to=20.0, resolution=1.0, orient='horizontal',
                              variable=self.pitch_var, bg='#3c3c3c', fg='#ffffff', highlightbackground='#3c3c3c')
        pitch_scale.grid(row=0, column=3, sticky='ew', padx=(5, 0))
        
        controls_frame.columnconfigure(1, weight=1)
        controls_frame.columnconfigure(3, weight=1)
        
        # Cấu hình grid column weights
        engine_frame.columnconfigure(1, weight=1)
        
        # Text input frame
        text_frame = tk.LabelFrame(main_frame, text="📝 Nhập văn bản tiếng Việt", bg='#3c3c3c', fg='#ffffff', font=('Segoe UI', 10, 'bold'))
        text_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        # Text area with scrollbar
        text_container = tk.Frame(text_frame, bg='#3c3c3c')
        text_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.text_area = scrolledtext.ScrolledText(text_container, wrap=tk.WORD, height=10, 
                                                  font=('Consolas', 11), bg='#1e1e1e', fg='#ffffff',
                                                  insertbackground='#ffffff', selectbackground='#4CAF50')
        self.text_area.pack(fill='both', expand=True)
        
        # Placeholder text tiếng Việt
        placeholder_text = """Nhập văn bản tiếng Việt cần chuyển thành giọng nói...

Ví dụ:
- Xin chào, tôi là công cụ TTS Tool Vietnamese!
- Hôm nay trời đẹp quá, chúng ta đi dạo nhé!
- Công nghệ Text-to-Speech ngày càng phát triển.
- Việt Nam là một đất nước xinh đẹp với nhiều danh lam thắng cảnh.
- Ứng dụng này được phát triển bởi Nguyễn Vĩnh Bảo.

🚀 Tính năng nâng cao:
• Không giới hạn ký tự - Tạo audio dài hàng trăm tiếng
• Tốc độ xử lý siêu nhanh - 1 tiếng audio chỉ cần 3 phút  
• Không tốn phí API hàng tháng
• Xử lý hàng loạt file văn bản"""
        
        self.text_area.insert(1.0, placeholder_text)
        
        # Character count
        char_frame = tk.Frame(text_frame, bg='#3c3c3c')
        char_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        self.char_count_label = tk.Label(char_frame, text="Characters: 0", bg='#3c3c3c', fg='#888888')
        self.char_count_label.pack(side='right')
        
        self.text_area.bind('<KeyRelease>', self.update_char_count)
        
        # File operations frame
        file_frame = tk.Frame(text_frame, bg='#3c3c3c')
        file_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        load_btn = tk.Button(file_frame, text="📁 Load Text File", command=self.load_text_file,
                           bg='#4CAF50', fg='white', font=('Segoe UI', 9, 'bold'), relief='flat')
        load_btn.pack(side='left', padx=(0, 10))
        
        save_btn = tk.Button(file_frame, text="💾 Save Text", command=self.save_text_file,
                           bg='#2196F3', fg='white', font=('Segoe UI', 9, 'bold'), relief='flat')
        save_btn.pack(side='left')
        
        clear_btn = tk.Button(file_frame, text="🗑️ Clear", command=self.clear_text,
                            bg='#f44336', fg='white', font=('Segoe UI', 9, 'bold'), relief='flat')
        clear_btn.pack(side='right')
        
        # Control buttons frame
        control_frame = tk.LabelFrame(main_frame, text="🎵 Điều khiển", bg='#3c3c3c', fg='#ffffff', font=('Segoe UI', 10, 'bold'))
        control_frame.pack(fill='x', pady=(0, 15))
        
        button_container = tk.Frame(control_frame, bg='#3c3c3c')
        button_container.pack(pady=15)
        
        # Convert button
        self.convert_btn = tk.Button(button_container, text="🎤 Chuyển thành giọng nói", command=self.start_conversion,
                                   bg='#FF9800', fg='white', font=('Segoe UI', 12, 'bold'),
                                   relief='flat', padx=20, pady=10)
        self.convert_btn.pack(side='left', padx=(0, 15))
        
        # Play button
        self.play_btn = tk.Button(button_container, text="▶️ Phát", command=self.play_audio,
                                bg='#4CAF50', fg='white', font=('Segoe UI', 10, 'bold'),
                                relief='flat', padx=15, pady=8, state='disabled')
        self.play_btn.pack(side='left', padx=(0, 10))
        
        # Stop button  
        self.stop_btn = tk.Button(button_container, text="⏹️ Dừng", command=self.stop_audio,
                                bg='#f44336', fg='white', font=('Segoe UI', 10, 'bold'),
                                relief='flat', padx=15, pady=8, state='disabled')
        self.stop_btn.pack(side='left', padx=(0, 10))
        
        # Export button
        self.export_btn = tk.Button(button_container, text="💾 Xuất file", command=self.export_audio,
                                  bg='#9C27B0', fg='white', font=('Segoe UI', 10, 'bold'),
                                  relief='flat', padx=15, pady=8, state='disabled')
        self.export_btn.pack(side='left')
        
        # Progress frame với thông tin ủng hộ
        progress_frame = tk.Frame(main_frame, bg='#2b2b2b')
        progress_frame.pack(fill='x', pady=(0, 10))
        
        self.progress = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress.pack(fill='x', pady=5)
        
        self.status_label = tk.Label(progress_frame, text="Sẵn sàng", bg='#2b2b2b', fg='#4CAF50', font=('Segoe UI', 9))
        self.status_label.pack()
        
        # Thông tin ủng hộ (hiển thị khi đang xử lý)
        self.support_frame = tk.Frame(progress_frame, bg='#2b2b2b')
        self.support_label = tk.Label(self.support_frame, 
                                    text="💖 Ủng hộ tác giả: VPBank - 0567546604 | Crypto: TULbGQbBGLL4VNrUYob7eWJUDup2ixkUT4", 
                                    bg='#2b2b2b', fg='#FFE66D', font=('Segoe UI', 8))
        self.support_label.pack()
        
        # Features info
        features_frame = tk.LabelFrame(main_frame, text="✨ Tính năng nâng cao", bg='#3c3c3c', fg='#ffffff', font=('Segoe UI', 10, 'bold'))
        features_frame.pack(fill='x', pady=(0, 10))
        
        features_text = """🚀 Không giới hạn ký tự • ⚡ Tốc độ xử lý siêu nhanh • 📁 Xử lý hàng loạt file
💰 Không tốn phí API • 🎯 Tự động tạo phụ đề • 💻 Chạy trên máy cấu hình thấp
📞 Liên hệ: fb.com/ngvinhbao14081 • Telegram: t.me/nvb1408"""
        
        features_label = tk.Label(features_frame, text=features_text, bg='#3c3c3c', fg='#4CAF50', 
                                font=('Segoe UI', 9), wraplength=900, justify='center')
        features_label.pack(pady=10)
        
        # Initialize voices
        self.on_engine_change()
        
    def create_menu_bar(self):
        """Tạo menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="📁 Mở file text...", command=self.load_text_file)
        file_menu.add_command(label="💾 Lưu file text...", command=self.save_text_file)
        file_menu.add_separator()
        file_menu.add_command(label="🚪 Thoát", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Trợ giúp", menu=help_menu)
        help_menu.add_command(label="📞 Liên hệ Facebook", command=lambda: webbrowser.open("https://fb.com/ngvinhbao14081"))
        help_menu.add_command(label="💬 Liên hệ Telegram", command=lambda: webbrowser.open("https://t.me/nvb1408"))
        help_menu.add_separator()
        help_menu.add_command(label="💖 Ủng hộ tác giả", command=self.show_support_info)
        help_menu.add_command(label="ℹ️ Về ứng dụng", command=self.show_about)
        
    def show_support_info(self):
        """Hiển thị thông tin ủng hộ"""
        support_msg = """💖 Ủng hộ tác giả

Nếu bạn thấy ứng dụng hữu ích, hãy ủng hộ tác giả để duy trì và phát triển thêm tính năng!

🏦 VPBank: 0567546604
₿ Crypto (TRC20): TULbGQbBGLL4VNrUYob7eWJUDup2ixkUT4

📞 Liên hệ:
• Facebook: fb.com/ngvinhbao14081  
• Telegram: t.me/nvb1408

Cảm ơn bạn! 🙏"""
        
        messagebox.showinfo("Ủng hộ tác giả", support_msg)
        
    def show_about(self):
        """Hiển thị thông tin về ứng dụng"""
        about_msg = """🎤 TTS Tool Vietnamese v1.0.0

Công cụ chuyển văn bản thành giọng nói tiếng Việt chất lượng cao
sử dụng công nghệ Neural TTS của Microsoft

✨ Tính năng nổi bật:
• Giọng Việt Neural: HoaiMy (nữ) và NamMinh (nam)
• Không giới hạn ký tự
• Tốc độ xử lý siêu nhanh 
• Không tốn phí API
• Xuất file MP3/WAV chất lượng cao

👨‍💻 Tác giả: Nguyễn Vĩnh Bảo
📞 Liên hệ: fb.com/ngvinhbao14081 | t.me/nvb1408

© 2024 - Made with ❤️ in Vietnam 🇻🇳"""
        
        messagebox.showinfo("Về TTS Tool Vietnamese", about_msg)
        
    def on_engine_change(self, event=None):
        """Update voice list - chỉ hiển thị giọng Việt đã verify"""
        # Luôn dùng Edge TTS với giọng Việt CHÍNH THỨC
        if EDGE_TTS_AVAILABLE:
            # Đảm bảo chắc chắn là giọng Việt từ Microsoft
            verified_vietnamese_voices = {
                "👩 HoaiMy (Nữ) - Giọng Việt Neural": "vi-VN-HoaiMyNeural",
                "👨 NamMinh (Nam) - Giọng Việt Neural": "vi-VN-NamMinhNeural"
            }
            voices = list(verified_vietnamese_voices.keys())
            self.voice_combo['values'] = voices
            if voices:
                self.voice_var.set(voices[0])  # Mặc định chọn HoaiMy
            # Cập nhật dictionary để sử dụng
            self.edge_voices = verified_vietnamese_voices
        elif GTTS_AVAILABLE:
            self.voice_combo['values'] = ["🇻🇳 Tiếng Việt (Google TTS)"]
            self.voice_var.set("🇻🇳 Tiếng Việt (Google TTS)")
        elif PYTTSX3_AVAILABLE:
            self.voice_combo['values'] = ["🇻🇳 Tiếng Việt (Hệ thống)"]
            self.voice_var.set("🇻🇳 Tiếng Việt (Hệ thống)")
        else:
            self.voice_combo['values'] = ["❌ Không có engine TTS"]
            self.voice_var.set("❌ Không có engine TTS")
            
    def update_char_count(self, event=None):
        """Update character count"""
        text = self.text_area.get(1.0, tk.END)
        char_count = len(text.strip())
        self.char_count_label.config(text=f"Số ký tự: {char_count}")
        
    def load_text_file(self):
        """Load text from file"""
        file_path = filedialog.askopenfilename(
            title="Chọn file văn bản",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(1.0, content)
                    self.update_char_count()
                    self.status_label.config(text=f"Đã tải: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể tải file: {str(e)}")
                
    def save_text_file(self):
        """Save text to file"""
        file_path = filedialog.asksaveasfilename(
            title="Lưu file văn bản",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    content = self.text_area.get(1.0, tk.END)
                    file.write(content.strip())
                    self.status_label.config(text=f"Đã lưu: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu file: {str(e)}")
                
    def clear_text(self):
        """Clear text area"""
        if messagebox.askyesno("Xác nhận", "Xóa toàn bộ văn bản?"):
            self.text_area.delete(1.0, tk.END)
            self.update_char_count()
            
    def start_conversion(self):
        """Start TTS conversion in a separate thread"""
        text = self.text_area.get(1.0, tk.END).strip()
        
        if not text:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập văn bản cần chuyển đổi!")
            return
            
        # Disable convert button and start progress
        self.convert_btn.config(state='disabled')
        self.progress.config(mode='determinate')
        self.progress['value'] = 0
        self.support_frame.pack(pady=(5, 0))  # Hiển thị thông tin ủng hộ
        self.status_label.config(text="0% - Đang xử lý... chờ xíu, đừng đóng ứng dụng nhé (-_-)")
        
        # Start conversion in separate thread
        thread = threading.Thread(target=self.convert_text, args=(text,))
        thread.daemon = True
        thread.start()
        
        # Start progress animation
        self.update_progress()
        
    def update_progress(self):
        """Update progress bar during conversion"""
        if self.progress['value'] < 90:
            self.progress['value'] += 2
            progress_text = [
                "Đang khởi tạo engine...",
                "Đang phân tích văn bản...", 
                "Đang kết nối server...",
                "Đang tạo giọng nói...",
                "Đang xử lý audio...",
                "Sắp hoàn thành..."
            ]
            text_idx = min(int(self.progress['value'] // 15), len(progress_text) - 1)
            self.status_label.config(text=f"{int(self.progress['value'])}% - {progress_text[text_idx]}")
            
            # Schedule next update
            self.root.after(100, self.update_progress)
            
    def convert_text(self, text):
        """Convert text to speech - tự động chọn engine tốt nhất"""
        try:
            # Create output directory
            output_dir = Path("output")
            output_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Ưu tiên Edge TTS cho chất lượng tốt nhất
            if EDGE_TTS_AVAILABLE:
                voice = self.edge_voices[self.voice_var.get()]
                output_file = output_dir / f"tts_vietnamese_{timestamp}.mp3"
                
                # Run async function
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self.edge_tts_convert(text, voice, str(output_file)))
                loop.close()
                
            elif GTTS_AVAILABLE:
                output_file = output_dir / f"tts_vietnamese_{timestamp}.mp3"
                tts = gTTS(text=text, lang='vi', slow=False)
                tts.save(str(output_file))
                
            elif PYTTSX3_AVAILABLE:
                output_file = output_dir / f"tts_vietnamese_{timestamp}.wav"
                engine = pyttsx3.init()
                engine.setProperty('rate', int(self.speed_var.get() * 200))
                engine.save_to_file(text, str(output_file))
                engine.runAndWait()
                
            else:
                raise Exception("Không có TTS engine nào khả dụng!")
            
            # Update UI in main thread
            self.root.after(0, self.conversion_complete, str(output_file))
            
        except Exception as e:
            self.root.after(0, self.conversion_error, str(e))
            
    async def edge_tts_convert(self, text, voice, output_file):
        """Edge TTS conversion with custom settings - Fixed"""
        try:
            # Fix rate calculation
            speed_value = self.speed_var.get()
            if speed_value == 1.0:
                rate = "+0%"  # Mặc định
            else:
                rate_percent = int((speed_value - 1) * 100)
                if rate_percent > 0:
                    rate = f"+{rate_percent}%"
                else:
                    rate = f"{rate_percent}%"
            
            # Fix pitch calculation  
            pitch_value = self.pitch_var.get()
            if pitch_value == 0.0:
                pitch = "+0Hz"  # Mặc định
            else:
                if pitch_value > 0:
                    pitch = f"+{int(pitch_value)}Hz"
                else:
                    pitch = f"{int(pitch_value)}Hz"
            
            print(f"🎵 Voice: {voice}")
            print(f"⚡ Rate: {rate}")  
            print(f"🎶 Pitch: {pitch}")
            
            # Tạo communicate object
            communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
            await communicate.save(output_file)
            
            print(f"✅ Saved: {output_file}")
            
        except Exception as e:
            print(f"❌ Edge TTS Error: {e}")
            # Fallback: Sử dụng giọng mặc định không có rate/pitch
            try:
                communicate = edge_tts.Communicate(text, voice)
                await communicate.save(output_file)
                print(f"✅ Saved with default settings: {output_file}")
            except Exception as e2:
                print(f"❌ Fallback failed: {e2}")
                raise e2
        
    def conversion_complete(self, output_file):
        """Handle successful conversion"""
        self.current_audio_file = output_file
        self.convert_btn.config(state='normal')
        self.play_btn.config(state='normal')
        self.stop_btn.config(state='normal')
        self.export_btn.config(state='normal')
        self.progress['value'] = 100
        self.support_frame.pack_forget()  # Ẩn thông tin ủng hộ
        
        file_size = os.path.getsize(output_file) / 1024  # KB
        self.status_label.config(text=f"✅ Hoàn thành! File: {os.path.basename(output_file)} ({file_size:.1f} KB)")
        
    def conversion_error(self, error_msg):
        """Handle conversion error"""
        self.convert_btn.config(state='normal')
        self.progress['value'] = 0
        self.support_frame.pack_forget()  # Ẩn thông tin ủng hộ
        self.status_label.config(text="❌ Chuyển đổi thất bại!")
        messagebox.showerror("Lỗi chuyển đổi", f"Không thể chuyển văn bản thành giọng nói:\n\n{error_msg}")
        
    def play_audio(self):
        """Play generated audio"""
        if not self.current_audio_file or not os.path.exists(self.current_audio_file):
            messagebox.showwarning("Cảnh báo", "Không có file audio để phát!")
            return
            
        try:
            if PYGAME_AVAILABLE:
                pygame.mixer.music.load(self.current_audio_file)
                pygame.mixer.music.play()
                self.status_label.config(text="🔊 Đang phát audio...")
            else:
                # Fallback to system default player
                if sys.platform.startswith('win'):
                    os.startfile(self.current_audio_file)
                elif sys.platform.startswith('darwin'):
                    os.system(f'open "{self.current_audio_file}"')
                else:
                    os.system(f'xdg-open "{self.current_audio_file}"')
                    
        except Exception as e:
            messagebox.showerror("Lỗi phát âm", f"Không thể phát audio: {str(e)}")
            
    def stop_audio(self):
        """Stop audio playback"""
        try:
            if PYGAME_AVAILABLE:
                pygame.mixer.music.stop()
                self.status_label.config(text="⏹️ Đã dừng phát")
        except Exception as e:
            print(f"Stop audio error: {e}")
            
    def export_audio(self):
        """Export audio file to chosen location"""
        if not self.current_audio_file or not os.path.exists(self.current_audio_file):
            messagebox.showwarning("Cảnh báo", "Không có file audio để xuất!")
            return
            
        file_extension = Path(self.current_audio_file).suffix
        file_path = filedialog.asksaveasfilename(
            title="Xuất file Audio",
            defaultextension=file_extension,
            filetypes=[
                ("MP3 files", "*.mp3"),
                ("WAV files", "*.wav"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                import shutil
                shutil.copy2(self.current_audio_file, file_path)
                self.status_label.config(text=f"📁 Đã xuất: {os.path.basename(file_path)}")
                messagebox.showinfo("Thành công", f"Đã xuất audio thành công:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Lỗi xuất file", f"Không thể xuất file: {str(e)}")
                
    def load_settings(self):
        """Load application settings"""
        settings_file = Path("settings.json")
        if settings_file.exists():
            try:
                with open(settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    self.speed_var.set(settings.get('speed', 1.0))
                    self.pitch_var.set(settings.get('pitch', 0.0))
            except:
                pass
                
    def save_settings(self):
        """Save application settings"""
        settings = {
            'speed': self.speed_var.get(),
            'pitch': self.pitch_var.get(),
            'engine': self.engine_var.get(),
            'voice': self.voice_var.get()
        }
        
        try:
            with open("settings.json", 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
        except:
            pass
            
    def on_closing(self):
        """Handle application closing"""
        self.save_settings()
        if PYGAME_AVAILABLE:
            pygame.mixer.quit()
        self.root.destroy()

def check_dependencies():
    """Check and install required dependencies"""
    missing_deps = []
    
    if not EDGE_TTS_AVAILABLE:
        missing_deps.append("edge-tts")
    if not GTTS_AVAILABLE:
        missing_deps.append("gTTS")
    if not PYTTSX3_AVAILABLE:
        missing_deps.append("pyttsx3")
    if not PYGAME_AVAILABLE:
        missing_deps.append("pygame")
        
    if missing_deps:
        print("⚠️  Thiếu dependencies!")
        print("Để cài đặt các package còn thiếu, chạy:")
        print(f"pip install {' '.join(missing_deps)}")
        print("\nBạn vẫn có thể sử dụng app với các engine hiện có.")
        
    return len(missing_deps) == 0

def main():
    """Main application entry point"""
    print("🎤 TTS Tool Vietnamese - Chuyển văn bản thành giọng nói")
    print("=" * 60)
    print("👨‍💻 Phát triển bởi: Nguyễn Vĩnh Bảo")
    print("📞 Liên hệ: fb.com/ngvinhbao14081 | t.me/nvb1408")
    print("💖 Ủng hộ: VPBank - 0567546604")
    print("=" * 60)
    
    # Check dependencies
    check_dependencies()
    
    # Create and run application
    root = tk.Tk()
    app = TTSApp(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    print("✅ Ứng dụng khởi động thành công!")
    print("📁 File audio sẽ được lưu trong thư mục 'output'")
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()