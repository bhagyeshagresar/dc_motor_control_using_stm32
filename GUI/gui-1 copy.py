import serial
import serial.tools.list_ports
import customtkinter as ctk # Use customtkinter
from tkinter import PhotoImage # For potential icons

# --- Constants for Styling ---
APP_NAME = "NOVAFLUX PWM Modulator"
WINDOW_SIZE = "500x750"

# Color Palette (Sci-Fi Dark Theme)
COLOR_BACKGROUND = "#1e1e2f"  # Dark Space Blue/Purple
COLOR_FRAME = "#2b2b3b"      # Slightly Lighter Dark
COLOR_TEXT = "#e0e0e0"        # Light Grey/Off-White
COLOR_ACCENT_PRIMARY = "#00bfff" # Deep Sky Blue / Cyan
COLOR_ACCENT_SECONDARY = "#4a4a6a" # Muted Purple/Blue
COLOR_SUCCESS = "#28a745"     # Bright Green
COLOR_ERROR = "#dc3545"       # Bright Red
COLOR_WARNING = "#ffc107"     # Bright Yellow
COLOR_EMERGENCY = "#ff4500"   # OrangeRed

# Fonts
FONT_PRIMARY = ("Exo 2", 16, "bold") # Requires Exo 2 font installed, or fallback
FONT_SECONDARY = ("Exo 2", 12)
FONT_BUTTON = ("Exo 2", 11, "bold")
FONT_LABEL = ("Exo 2", 10)
FONT_SMALL = ("Exo 2", 9)
FONT_TITLE = ("Orbitron", 20, "bold") # Requires Orbitron font installed, or fallback

# Try to use sci-fi fonts, fallback to system defaults if not available
try:
    # Test if fonts are available, Tkinter will use a fallback if not
    ctk.CTkFont(family="Exo 2")
    ctk.CTkFont(family="Orbitron")
except Exception:
    print("Sci-fi fonts (Exo 2, Orbitron) not found, using system defaults.")
    FONT_PRIMARY = ("Arial", 16, "bold")
    FONT_SECONDARY = ("Arial", 12)
    FONT_BUTTON = ("Arial", 11, "bold")
    FONT_LABEL = ("Arial", 10)
    FONT_SMALL = ("Arial", 9)
    FONT_TITLE = ("Impact", 20, "bold")


# --- Serial Connection ---
ser = None

def setup_serial_connection():
    global ser
    print("Scanning for available serial ports...")
    ports = serial.tools.list_ports.comports()
    if not ports:
        print("No serial ports found.")
        status_label.configure(text="❌ No serial ports detected.", text_color=COLOR_ERROR)
        return False

    for port in ports:
        print(f"  {port.device} — {port.description}")

    serial_device_candidates = ['/dev/ttyUSB0', '/dev/ttyACM0', 'COM3', 'COM4', 'COM5', 'COM6']
    # Add detected ports to the front of the candidates list for higher priority
    detected_devices = [port.device for port in ports]
    serial_device_candidates = detected_devices + [c for c in serial_device_candidates if c not in detected_devices]

    for device in serial_device_candidates:
        try:
            ser = serial.Serial(device, 9600, timeout=1)
            print(f"Successfully connected to {device}")
            conn_info.configure(text=f"Connected: {ser.port}", text_color=COLOR_SUCCESS)
            status_label.configure(text="SYSTEM ONLINE", text_color=COLOR_SUCCESS)
            return True
        except serial.SerialException:
            print(f"Failed to connect to {device}")
            continue
        except Exception as e:
            print(f"An unexpected error occurred with {device}: {e}")
            continue


    print("No compatible serial device found.")
    status_label.configure(text="❌ Connection Failed: No device found.", text_color=COLOR_ERROR)
    conn_info.configure(text="Disconnected", text_color=COLOR_ERROR)
    return False

# --- Core Logic Functions ---
def send_duty():
    if not ser or not ser.is_open:
        status_label.configure(text="⚠️ SERIAL PORT NOT CONNECTED", text_color=COLOR_WARNING)
        return

    duty_text = duty_entry.get()
    print("Raw duty input:", duty_text)
    if duty_text.isdigit():
        duty = int(duty_text)
        if 0 <= duty <= 100:
            uart_cmd = f"D:{duty}\n"
            print(f"Sending UART command: {uart_cmd.strip()}")
            ser.write(uart_cmd.encode())
            status_label.configure(text=f"MODULATION: {duty}% DUTY CYCLE", text_color=COLOR_SUCCESS)
        else:
            status_label.configure(text="INVALID DUTY: 0-100% RANGE", text_color=COLOR_ERROR)
    else:
        status_label.configure(text="INPUT ERROR: NUMERIC DUTY ONLY", text_color=COLOR_ERROR)

def send_frequency():
    if not ser or not ser.is_open:
        status_label.configure(text="⚠️ SERIAL PORT NOT CONNECTED", text_color=COLOR_WARNING)
        return

    freq_text = freq_entry.get()
    print("Raw frequency input:", freq_text)
    if freq_text.isdigit():
        freq = int(freq_text)
        if 100 <= freq <= 10000: # Adjusted range for practicality
            uart_cmd = f"F:{freq}\n"
            print(f"Sending UART command: {uart_cmd.strip()}")
            ser.write(uart_cmd.encode())
            status_label.configure(text=f"FREQUENCY SET: {freq} Hz", text_color=COLOR_ACCENT_PRIMARY)
        else:
            status_label.configure(text="INVALID FREQ: 100-10000 Hz", text_color=COLOR_ERROR)
    else:
        status_label.configure(text="INPUT ERROR: NUMERIC FREQ ONLY", text_color=COLOR_ERROR)

def quick_duty(value):
    duty_entry.delete(0, ctk.END)
    duty_entry.insert(0, str(value))
    send_duty()

def quick_freq(value):
    freq_entry.delete(0, ctk.END)
    freq_entry.insert(0, str(value))
    send_frequency()

def emergency_stop():
    duty_entry.delete(0, ctk.END)
    duty_entry.insert(0, "0")
    send_duty()
    status_label.configure(text="EMERGENCY STOP ENGAGED - DUTY 0%", text_color=COLOR_EMERGENCY, font=(FONT_SECONDARY[0], 14, "bold"))

# --- GUI Setup ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue") # or "green", "dark-blue"

root = ctk.CTk()
root.title(APP_NAME)
root.geometry(WINDOW_SIZE)
root.configure(fg_color=COLOR_BACKGROUND)

# --- Title ---
title_label = ctk.CTkLabel(root, text=APP_NAME, font=FONT_TITLE, text_color=COLOR_ACCENT_PRIMARY)
title_label.pack(pady=(20, 10))

# --- Main Content Frame ---
main_frame = ctk.CTkFrame(root, fg_color="transparent")
main_frame.pack(pady=10, padx=20, fill="both", expand=True)

# === DUTY CYCLE CONTROL ===
duty_frame = ctk.CTkFrame(main_frame, fg_color=COLOR_FRAME, corner_radius=10)
duty_frame.pack(pady=10, padx=10, fill="x")

ctk.CTkLabel(duty_frame, text="THRUST MODULATION (Duty Cycle %)", font=FONT_PRIMARY, text_color=COLOR_TEXT).pack(pady=(10,5))
duty_entry = ctk.CTkEntry(duty_frame, width=150, font=FONT_SECONDARY,
                          placeholder_text="0-100", fg_color=COLOR_ACCENT_SECONDARY,
                          border_color=COLOR_ACCENT_PRIMARY, text_color=COLOR_TEXT)
duty_entry.pack(pady=5)
duty_entry.insert(0, "50")

ctk.CTkButton(duty_frame, text="SET DUTY CYCLE", command=send_duty,
              font=FONT_BUTTON, fg_color=COLOR_ACCENT_PRIMARY, hover_color=COLOR_SUCCESS,
              text_color="#000000", corner_radius=8).pack(pady=8)

# Quick duty cycle buttons
quick_duty_frame = ctk.CTkFrame(duty_frame, fg_color="transparent")
quick_duty_frame.pack(pady=5)
ctk.CTkLabel(quick_duty_frame, text="Presets:", font=FONT_LABEL, text_color=COLOR_TEXT).pack(side="left", padx=(0,5))
duty_values = [0, 25, 50, 75, 100]
for val in duty_values:
    btn_color = COLOR_EMERGENCY if val == 0 else COLOR_ACCENT_SECONDARY
    hover_c = "#c82333" if val == 0 else COLOR_ACCENT_PRIMARY
    ctk.CTkButton(quick_duty_frame, text=f"{val}%", width=50,
                  fg_color=btn_color, hover_color=hover_c, text_color=COLOR_TEXT,
                  command=lambda v=val: quick_duty(v), font=FONT_SMALL, corner_radius=6).pack(side="left", padx=3)

# === FREQUENCY CONTROL ===
freq_frame = ctk.CTkFrame(main_frame, fg_color=COLOR_FRAME, corner_radius=10)
freq_frame.pack(pady=10, padx=10, fill="x")

ctk.CTkLabel(freq_frame, text="PWM FREQUENCY (Hz)", font=FONT_PRIMARY, text_color=COLOR_TEXT).pack(pady=(10,5))
freq_entry = ctk.CTkEntry(freq_frame, width=150, font=FONT_SECONDARY,
                          placeholder_text="100-10000", fg_color=COLOR_ACCENT_SECONDARY,
                          border_color=COLOR_ACCENT_PRIMARY, text_color=COLOR_TEXT)
freq_entry.pack(pady=5)
freq_entry.insert(0, "1000")

ctk.CTkButton(freq_frame, text="SET FREQUENCY", command=send_frequency,
              font=FONT_BUTTON, fg_color=COLOR_ACCENT_PRIMARY, hover_color=COLOR_SUCCESS,
              text_color="#000000", corner_radius=8).pack(pady=8)

# Quick frequency buttons
quick_freq_frame = ctk.CTkFrame(freq_frame, fg_color="transparent")
quick_freq_frame.pack(pady=5)
ctk.CTkLabel(quick_freq_frame, text="Presets:", font=FONT_LABEL, text_color=COLOR_TEXT).pack(side="left", padx=(0,5))
freq_values = [500, 1000, 2000, 5000]
for val in freq_values:
    ctk.CTkButton(quick_freq_frame, text=f"{val}", width=50,
                  fg_color=COLOR_ACCENT_SECONDARY, hover_color=COLOR_ACCENT_PRIMARY, text_color=COLOR_TEXT,
                  command=lambda v=val: quick_freq(v), font=FONT_SMALL, corner_radius=6).pack(side="left", padx=3)

# === EMERGENCY STOP ===
emergency_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
emergency_frame.pack(pady=15)

# Consider adding an icon if you have one (e.g., using PhotoImage)
# stop_icon = PhotoImage(file="path_to_stop_icon.png") # Example
ctk.CTkButton(emergency_frame, text="🛑 EMERGENCY STOP 🛑", command=emergency_stop,
              font=(FONT_BUTTON[0], 14, "bold"), fg_color=COLOR_EMERGENCY, hover_color="#c82333", # Darker red
              text_color="#FFFFFF", width=250, height=40, corner_radius=10,
              border_width=2, border_color=COLOR_WARNING).pack()

# === STATUS DISPLAY ===
status_label = ctk.CTkLabel(main_frame, text="SYSTEM STANDBY",
                            font=(FONT_SECONDARY[0], 13, "italic"), text_color=COLOR_WARNING,
                            fg_color=COLOR_FRAME, corner_radius=8, height=30)
status_label.pack(pady=10, fill="x", padx=10)

# === INSTRUCTIONS (Collapsible or simplified) ===
# For a cleaner look, instructions could be in a tooltip, a separate "Help" button/window,
# or a very compact form. Here's a compact version.
instructions_frame = ctk.CTkFrame(main_frame, fg_color=COLOR_FRAME, corner_radius=10)
instructions_frame.pack(pady=10, padx=10, fill="x")
ctk.CTkLabel(instructions_frame, text="SYSTEM PROTOCOLS", font=FONT_PRIMARY, text_color=COLOR_TEXT).pack(pady=(10,0))
instructions_text = """• Establish Frequency (1-5kHz rec. for motors)
• Modulate Duty Cycle (0-100%) for output
• Utilize EMERGENCY STOP for immediate shutdown
• Ensure L298N or similar driver is mediating motor connection
• Verify power source meets current demands"""
instructions_label = ctk.CTkLabel(instructions_frame, text=instructions_text,
                                 font=FONT_SMALL, justify="left", text_color=COLOR_TEXT,
                                 wraplength=400) # Adjust wraplength as needed
instructions_label.pack(anchor="w", padx=15, pady=(5,10))


# --- Footer / Connection Info ---
footer_frame = ctk.CTkFrame(root, fg_color="transparent", height=30)
footer_frame.pack(side="bottom", fill="x", pady=(0,10), padx=20)

conn_info = ctk.CTkLabel(footer_frame, text="Attempting connection...",
                         font=FONT_SMALL, text_color=COLOR_WARNING)
conn_info.pack(side="left")

version_label = ctk.CTkLabel(footer_frame, text="v1.0 SciFi Edition",
                             font=FONT_SMALL, text_color=COLOR_ACCENT_SECONDARY)
version_label.pack(side="right")


# --- Initialize Serial and Start GUI ---
if not setup_serial_connection():
    # Optionally, you could disable controls if connection fails
    # Or show a prominent "Reconnect" button
    print("Continuing in offline mode. Controls will not send commands.")
    # Example: disable_controls()

root.mainloop()

# --- Cleanup ---
if ser and ser.is_open:
    print("Closing serial port.")
    ser.close()