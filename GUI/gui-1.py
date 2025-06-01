import serial
import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports
import time
import threading
from tkinter import font

# Adjust COM port and baudrate to match your board
print("Available serial ports:")
for port in serial.tools.list_ports.comports():
    print(f"{port.device} — {port.description}")

# Try common device names
serial_device_candidates = ['/dev/ttyUSB0', '/dev/ttyACM0', 'COM3', 'COM4', 'COM5', 'COM6']
 
ser = None
for device in serial_device_candidates:
    try:
        ser = serial.Serial(device, 9600, timeout=1)
        print(f"Connected to {device}")
        break
    except serial.SerialException:
        continue

if ser is None:
    print("No available serial device found.")

class FuturisticMotorController:
    def __init__(self, root):
        self.root = root
        self.setup_styles()
        self.create_gui()
        self.animate_scanner()
        
        # Status animation variables
        self.status_animation_id = None
        self.scanner_position = 0
        
    def setup_styles(self):
        # Color scheme - cyberpunk/sci-fi palette
        self.colors = {
            'bg_primary': '#0a0a0f',      # Deep space black
            'bg_secondary': '#1a1a2e',    # Dark blue-black
            'bg_panel': '#16213e',        # Panel background
            'accent_cyan': '#00ffff',     # Bright cyan
            'accent_blue': '#0066ff',     # Electric blue
            'accent_green': '#00ff88',    # Neon green
            'accent_orange': '#ff6600',   # Warning orange
            'accent_red': '#ff0044',      # Emergency red
            'text_primary': '#ffffff',    # Pure white
            'text_secondary': '#b3b3b3',  # Gray text
            'glow_blue': '#4da6ff',       # Blue glow
            'glow_green': '#66ff99',      # Green glow
        }
        
        # Configure root
        self.root.title("NEXUS MOTOR CONTROL SYSTEM v2.1")
        self.root.geometry("600x800")
        self.root.configure(bg=self.colors['bg_primary'])
        self.root.resizable(False, False)
        
        # Custom fonts
        self.fonts = {
            'title': ('Orbitron', 20, 'bold'),
            'subtitle': ('Orbitron', 12, 'bold'),
            'body': ('Consolas', 10),
            'button': ('Orbitron', 9, 'bold'),
            'status': ('Consolas', 11),
            'small': ('Consolas', 8)
        }
        
    def create_glowing_frame(self, parent, color, **kwargs):
        """Create a frame with glowing border effect"""
        outer_frame = tk.Frame(parent, bg=color, **kwargs)
        inner_frame = tk.Frame(outer_frame, bg=self.colors['bg_panel'])
        inner_frame.pack(padx=2, pady=2, fill='both', expand=True)
        return outer_frame, inner_frame
        
    def create_neon_button(self, parent, text, command, color, **kwargs):
        """Create a button with neon glow effect"""
        # Extract font from kwargs if provided, otherwise use default
        button_font = kwargs.pop('font', self.fonts['button'])
        
        button = tk.Button(parent, text=text, command=command,
                          bg=self.colors['bg_panel'], fg=color,
                          activebackground=color, activeforeground=self.colors['bg_primary'],
                          font=button_font, relief='flat',
                          borderwidth=2, highlightbackground=color,
                          **kwargs)
        
        # Hover effects
        def on_enter(e):
            button.config(bg=color, fg=self.colors['bg_primary'])
            
        def on_leave(e):
            button.config(bg=self.colors['bg_panel'], fg=color)
            
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
        return button
        
    def create_gui(self):
        # Main container
        main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header section
        self.create_header(main_container)
        
        # Scanner line
        self.create_scanner(main_container)
        
        # Control panels
        self.create_duty_panel(main_container)
        self.create_frequency_panel(main_container)
        self.create_emergency_panel(main_container)
        
        # Status and info
        self.create_status_panel(main_container)
        self.create_connection_info(main_container)
        
    def create_header(self, parent):
        header_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Main title with glow effect
        title_label = tk.Label(header_frame, text="NEXUS MOTOR CONTROL",
                              font=self.fonts['title'], fg=self.colors['accent_cyan'],
                              bg=self.colors['bg_primary'])
        title_label.pack()
        
        # Subtitle
        subtitle_label = tk.Label(header_frame, text="Advanced PWM Control System",
                                 font=self.fonts['subtitle'], fg=self.colors['text_secondary'],
                                 bg=self.colors['bg_primary'])
        subtitle_label.pack(pady=(5, 0))
        
        # Status indicators
        indicators_frame = tk.Frame(header_frame, bg=self.colors['bg_primary'])
        indicators_frame.pack(pady=(10, 0))
        
        # Power indicator
        self.power_indicator = tk.Label(indicators_frame, text="● PWR",
                                       font=self.fonts['small'], fg=self.colors['accent_green'],
                                       bg=self.colors['bg_primary'])
        self.power_indicator.pack(side='left', padx=10)
        
        # Connection indicator
        conn_color = self.colors['accent_green'] if ser else self.colors['accent_red']
        conn_text = "● CONN" if ser else "● DISC"
        self.conn_indicator = tk.Label(indicators_frame, text=conn_text,
                                      font=self.fonts['small'], fg=conn_color,
                                      bg=self.colors['bg_primary'])
        self.conn_indicator.pack(side='left', padx=10)
        
        # System status
        self.sys_indicator = tk.Label(indicators_frame, text="● SYS",
                                     font=self.fonts['small'], fg=self.colors['accent_blue'],
                                     bg=self.colors['bg_primary'])
        self.sys_indicator.pack(side='left', padx=10)
        
    def create_scanner(self, parent):
        # Animated scanner line
        self.scanner_frame = tk.Frame(parent, bg=self.colors['bg_primary'], height=3)
        self.scanner_frame.pack(fill='x', pady=(0, 20))
        
        self.scanner_canvas = tk.Canvas(self.scanner_frame, height=3, 
                                       bg=self.colors['bg_primary'], highlightthickness=0)
        self.scanner_canvas.pack(fill='x')
        
    def animate_scanner(self):
        """Animated scanning line effect"""
        if hasattr(self, 'scanner_canvas'):
            self.scanner_canvas.delete("scanner")
            width = self.scanner_canvas.winfo_width()
            if width > 1:
                x = (self.scanner_position % (width + 100)) - 50
                self.scanner_canvas.create_line(x, 1, x + 50, 1, 
                                              fill=self.colors['accent_cyan'], width=2, tags="scanner")
                self.scanner_position += 2
            
        self.root.after(50, self.animate_scanner)
        
    def create_duty_panel(self, parent):
        # Duty cycle control panel
        duty_outer, duty_frame = self.create_glowing_frame(parent, self.colors['accent_blue'])
        duty_outer.pack(fill='x', pady=10)
        
        # Panel header
        header = tk.Label(duty_frame, text="⚡ MOTOR VELOCITY CONTROL",
                         font=self.fonts['subtitle'], fg=self.colors['accent_blue'],
                         bg=self.colors['bg_panel'])
        header.pack(pady=(10, 5))
        
        # Input section
        input_frame = tk.Frame(duty_frame, bg=self.colors['bg_panel'])
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="DUTY CYCLE [%]", font=self.fonts['body'],
                fg=self.colors['text_primary'], bg=self.colors['bg_panel']).pack(anchor='w')
        
        self.duty_entry = tk.Entry(input_frame, font=self.fonts['body'], width=15,
                                  bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                                  insertbackground=self.colors['accent_cyan'], relief='flat',
                                  borderwidth=2, highlightcolor=self.colors['accent_cyan'])
        self.duty_entry.pack(pady=5, anchor='w')
        self.duty_entry.insert(0, "50")
        
        # Set button
        set_btn = self.create_neon_button(input_frame, "EXECUTE", self.send_duty,
                                         self.colors['accent_green'], width=12)
        set_btn.pack(pady=10)
        
        # Quick controls
        quick_frame = tk.Frame(duty_frame, bg=self.colors['bg_panel'])
        quick_frame.pack(pady=10)
        
        tk.Label(quick_frame, text="PRESET VALUES", font=self.fonts['small'],
                fg=self.colors['text_secondary'], bg=self.colors['bg_panel']).pack()
        
        buttons_frame = tk.Frame(quick_frame, bg=self.colors['bg_panel'])
        buttons_frame.pack(pady=5)
        
        duty_values = [0, 25, 50, 75, 100]
        for i, val in enumerate(duty_values):
            color = self.colors['accent_red'] if val == 0 else self.colors['accent_cyan']
            btn = self.create_neon_button(buttons_frame, f"{val}%", 
                                         lambda v=val: self.quick_duty(v),
                                         color, width=8)
            btn.pack(side='left', padx=2)
            
    def create_frequency_panel(self, parent):
        # Frequency control panel
        freq_outer, freq_frame = self.create_glowing_frame(parent, self.colors['accent_orange'])
        freq_outer.pack(fill='x', pady=10)
        
        # Panel header
        header = tk.Label(freq_frame, text="🌊 FREQUENCY MODULATION",
                         font=self.fonts['subtitle'], fg=self.colors['accent_orange'],
                         bg=self.colors['bg_panel'])
        header.pack(pady=(10, 5))
        
        # Input section
        input_frame = tk.Frame(freq_frame, bg=self.colors['bg_panel'])
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="FREQUENCY [Hz]", font=self.fonts['body'],
                fg=self.colors['text_primary'], bg=self.colors['bg_panel']).pack(anchor='w')
        
        self.freq_entry = tk.Entry(input_frame, font=self.fonts['body'], width=15,
                                  bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                                  insertbackground=self.colors['accent_cyan'], relief='flat',
                                  borderwidth=2, highlightcolor=self.colors['accent_cyan'])
        self.freq_entry.pack(pady=5, anchor='w')
        self.freq_entry.insert(0, "1000")
        
        # Set button
        set_btn = self.create_neon_button(input_frame, "EXECUTE", self.send_frequency,
                                         self.colors['accent_orange'], width=12)
        set_btn.pack(pady=10)
        
        # Quick controls
        quick_frame = tk.Frame(freq_frame, bg=self.colors['bg_panel'])
        quick_frame.pack(pady=10)
        
        tk.Label(quick_frame, text="PRESET VALUES", font=self.fonts['small'],
                fg=self.colors['text_secondary'], bg=self.colors['bg_panel']).pack()
        
        buttons_frame = tk.Frame(quick_frame, bg=self.colors['bg_panel'])
        buttons_frame.pack(pady=5)
        
        freq_values = [500, 1000, 2000, 5000]
        for val in freq_values:
            btn = self.create_neon_button(buttons_frame, f"{val}", 
                                         lambda v=val: self.quick_freq(v),
                                         self.colors['accent_cyan'], width=8)
            btn.pack(side='left', padx=2)
            
    def create_emergency_panel(self, parent):
        # Emergency control panel
        emergency_outer, emergency_frame = self.create_glowing_frame(parent, self.colors['accent_red'])
        emergency_outer.pack(fill='x', pady=20)
        
        # Emergency button with pulsing effect
        self.emergency_btn = self.create_neon_button(emergency_frame, "🛑 EMERGENCY SHUTDOWN", 
                                                    self.emergency_stop, self.colors['accent_red'], 
                                                    width=25, font=('Orbitron', 14, 'bold'))
        self.emergency_btn.pack(pady=20)
        
        # Warning text
        warning_label = tk.Label(emergency_frame, text="⚠ CRITICAL SYSTEM HALT ⚠",
                               font=self.fonts['small'], fg=self.colors['accent_red'],
                               bg=self.colors['bg_panel'])
        warning_label.pack()
        
    def create_status_panel(self, parent):
        # Status display panel
        status_outer, status_frame = self.create_glowing_frame(parent, self.colors['accent_green'])
        status_outer.pack(fill='x', pady=10)
        
        tk.Label(status_frame, text="SYSTEM STATUS", font=self.fonts['subtitle'],
                fg=self.colors['accent_green'], bg=self.colors['bg_panel']).pack(pady=(10, 5))
        
        self.status_label = tk.Label(status_frame, text="[ READY ] Awaiting command input...",
                                    font=self.fonts['status'], fg=self.colors['text_primary'],
                                    bg=self.colors['bg_panel'], wraplength=500)
        self.status_label.pack(pady=(0, 10))
        
    def create_connection_info(self, parent):
        # Connection information
        info_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        info_frame.pack(fill='x', pady=(20, 0))
        
        # Connection status
        conn_text = f"CONNECTED TO: {ser.port}" if ser else "STATUS: NO CONNECTION ESTABLISHED"
        conn_color = self.colors['accent_green'] if ser else self.colors['accent_red']
        
        self.conn_label = tk.Label(info_frame, text=conn_text, font=self.fonts['small'],
                                  fg=conn_color, bg=self.colors['bg_primary'])
        self.conn_label.pack()
        
        # System info
        sys_info = tk.Label(info_frame, text="NEXUS CONTROL SYSTEM | BUILD 2024.12 | STATUS: OPERATIONAL",
                           font=self.fonts['small'], fg=self.colors['text_secondary'],
                           bg=self.colors['bg_primary'])
        sys_info.pack(pady=(5, 0))
        
    def send_duty(self):
        duty_text = self.duty_entry.get()
        print("Raw duty input:", duty_text)
        if duty_text.isdigit():
            duty = int(duty_text)
            if 0 <= duty <= 100:
                if ser:
                    uart_cmd = f"D:{duty}\n"
                    print(f"Sending UART command: {uart_cmd.strip()}")
                    ser.write(uart_cmd.encode())
                    self.update_status(f"[ SUCCESS ] Motor velocity set to {duty}%", 'success')
                else:
                    self.update_status(f"[ ERROR ] No serial connection available", 'error')
            else:
                self.update_status("[ ERROR ] Duty cycle must be 0-100%", 'error')
        else:
            self.update_status("[ ERROR ] Invalid input - numbers only", 'error')

    def send_frequency(self):
        freq_text = self.freq_entry.get()
        print("Raw frequency input:", freq_text)
        if freq_text.isdigit():
            freq = int(freq_text)
            if 100 <= freq <= 10000:
                if ser:
                    uart_cmd = f"F:{freq}\n"
                    print(f"Sending UART command: {uart_cmd.strip()}")
                    ser.write(uart_cmd.encode())
                    self.update_status(f"[ SUCCESS ] PWM frequency set to {freq} Hz", 'success')
                else:
                    self.update_status(f"[ ERROR ] No serial connection available", 'error')
            else:
                self.update_status("[ ERROR ] Frequency must be 100-10000 Hz", 'error')
        else:
            self.update_status("[ ERROR ] Invalid input - numbers only", 'error')

    def quick_duty(self, value):
        """Quick set duty cycle buttons"""
        self.duty_entry.delete(0, tk.END)
        self.duty_entry.insert(0, str(value))
        self.send_duty()

    def quick_freq(self, value):
        """Quick set frequency buttons"""
        self.freq_entry.delete(0, tk.END)
        self.freq_entry.insert(0, str(value))
        self.send_frequency()

    def emergency_stop(self):
        """Emergency stop - set duty to 0%"""
        self.duty_entry.delete(0, tk.END)
        self.duty_entry.insert(0, "0")
        self.send_duty()
        self.update_status("[ EMERGENCY ] System shutdown initiated", 'emergency')

    def update_status(self, message, status_type='normal'):
        """Update status with color coding and animation"""
        colors = {
            'success': self.colors['accent_green'],
            'error': self.colors['accent_red'],
            'emergency': self.colors['accent_red'],
            'normal': self.colors['text_primary']
        }
        
        self.status_label.config(text=message, fg=colors.get(status_type, colors['normal']))
        
        # Flash effect for critical messages
        if status_type in ['error', 'emergency']:
            self.flash_status()
            
    def flash_status(self):
        """Flash status label for attention"""
        original_bg = self.status_label.cget('bg')
        self.status_label.config(bg=self.colors['accent_red'])
        self.root.after(200, lambda: self.status_label.config(bg=original_bg))

# Create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = FuturisticMotorController(root)
    
    try:
        root.mainloop()
    finally:
        # Close serial connection when GUI closes
        if ser:
            ser.close()