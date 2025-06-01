import serial
import serial.tools.list_ports
import customtkinter as ctk
from tkinter import PhotoImage

# --- Constants for Styling ---
APP_NAME = "NOVAFLUX PWM Modulator XE"
WINDOW_SIZE = "400x720"  # Taller, narrower — like a phone screen

# Softer, modern mobile palette
COLOR_BACKGROUND = "#f2f4f8"  # Light neutral off-white background
COLOR_FRAME_BG = "#ffffff"    # Pure white cards
COLOR_WIDGET_BG = "#e9eff5"   # Light blue-gray for inputs and sliders
COLOR_TEXT_PRIMARY = "#222222"  # Dark gray text (less harsh than black)
COLOR_TEXT_SECONDARY = "#666666"  # Medium gray for subtler text
COLOR_ACCENT_PRIMARY = "#007aff"  # iOS blue accent
COLOR_ACCENT_SECONDARY = "#34c759"  # iOS green accent
COLOR_ACCENT_TERTIARY = "#ff9500"  # iOS orange accent
COLOR_ERROR = "#ff3b30"       # iOS red
COLOR_WARNING = "#ffcc00"     # iOS yellow
COLOR_EMERGENCY = "#ff453a"   # iOS emergency red

# Fonts (Mobile friendly: San Francisco system font or fallback)
FONT_TITLE = ("San Francisco", 26, "bold")
FONT_HEADER = ("San Francisco", 18, "bold")
FONT_SUBHEADER = ("San Francisco", 14)
FONT_BODY = ("San Francisco", 13)
FONT_BUTTON = ("San Francisco", 15, "bold")
FONT_LABEL = ("San Francisco", 12)
FONT_SMALL = ("San Francisco", 11, "italic")

CORNER_RADIUS = 20
INPUT_FIELD_WIDTH = 120

# --- Serial Connection ---
ser = None
def setup_serial_connection():
    global ser
    print("Initializing Subspace Comms Array...")
    ports = serial.tools.list_ports.comports()
    if not ports:
        status_label.configure(text="❌ COMMS OFFLINE: No serial ports detected.", text_color=COLOR_ERROR)
        conn_info.configure(text="Link Status: DEACTIVATED", text_color=COLOR_ERROR)
        return False

    for port_info in ports:
        print(f"  Detected Port: {port_info.device} — {port_info.description}")

    stm_candidates = [p.device for p in ports if "STM" in p.description.upper() or "SERIAL" in p.description.upper()]
    generic_candidates = ['/dev/ttyUSB0', '/dev/ttyACM0'] + [f'COM{i}' for i in range(3, 10)]
    serial_device_candidates = list(dict.fromkeys(stm_candidates + [p.device for p in ports] + generic_candidates))

    for device in serial_device_candidates:
        try:
            ser = serial.Serial(device, 9600, timeout=1)
            print(f"Successfully established link with {device}")
            conn_info.configure(text=f"Link Active: {ser.port}", text_color=COLOR_ACCENT_SECONDARY)
            status_label.configure(text="SYSTEM ONLINE | Awaiting Directives", text_color=COLOR_ACCENT_SECONDARY)
            return True
        except serial.SerialException:
            print(f"Link attempt failed for {device}")
            continue
        except Exception as e:
            print(f"Unexpected subspace anomaly with {device}: {e}")
            continue

    status_label.configure(text="❌ COMMS OFFLINE: No compatible device found.", text_color=COLOR_ERROR)
    conn_info.configure(text="Link Status: FAILED", text_color=COLOR_ERROR)
    return False

# --- Core Logic Functions ---
def update_duty_from_slider(value):
    duty_val = int(value)
    duty_entry.delete(0, ctk.END)
    duty_entry.insert(0, str(duty_val))
    duty_progressbar.set(duty_val / 100)
    send_duty()

def update_duty_from_entry():
    if duty_entry.get().isdigit():
        val = int(duty_entry.get())
        val = max(0, min(100, val))
        duty_slider.set(val)
        duty_progressbar.set(val / 100)

def update_freq_from_slider(value):
    freq_val = int(value)
    freq_entry.delete(0, ctk.END)
    freq_entry.insert(0, str(freq_val))
    send_frequency()

def update_freq_from_entry():
    if freq_entry.get().isdigit():
        val = int(freq_entry.get())
        val = max(100, min(10000, val))
        freq_slider.set(val)

def send_duty():
    if not ser or not ser.is_open:
        status_label.configure(text="⚠️ NO COMMS LINK: Connect Device", text_color=COLOR_WARNING)
        return

    duty_text = duty_entry.get()
    if duty_text.isdigit():
        duty = int(duty_text)
        if 0 <= duty <= 100:
            uart_cmd = f"D:{duty}\n"
            ser.write(uart_cmd.encode())
            status_label.configure(text=f"THRUST OUTPUT: {duty}%", text_color=COLOR_ACCENT_SECONDARY)
            duty_progressbar.set(duty / 100)
            if duty == 0:
                duty_progressbar.configure(progress_color=COLOR_WARNING)
            else:
                duty_progressbar.configure(progress_color=COLOR_ACCENT_PRIMARY)
        else:
            status_label.configure(text="DUTY RANGE ERROR: 0-100%", text_color=COLOR_ERROR)
    else:
        status_label.configure(text="INPUT INVALID: Numeric Duty Required", text_color=COLOR_ERROR)

def send_frequency():
    if not ser or not ser.is_open:
        status_label.configure(text="⚠️ NO COMMS LINK: Connect Device", text_color=COLOR_WARNING)
        return

    freq_text = freq_entry.get()
    if freq_text.isdigit():
        freq = int(freq_text)
        if 100 <= freq <= 10000:
            uart_cmd = f"F:{freq}\n"
            ser.write(uart_cmd.encode())
            status_label.configure(text=f"FREQUENCY CALIBRATED: {freq} Hz", text_color=COLOR_ACCENT_TERTIARY)
        else:
            status_label.configure(text="FREQ RANGE ERROR: 100-10000 Hz", text_color=COLOR_ERROR)
    else:
        status_label.configure(text="INPUT INVALID: Numeric Freq Required", text_color=COLOR_ERROR)

def quick_set_value(entry_widget, slider_widget, progress_bar_widget, value, send_function, is_duty=False):
    entry_widget.delete(0, ctk.END)
    entry_widget.insert(0, str(value))
    slider_widget.set(value)
    if is_duty and progress_bar_widget:
        progress_bar_widget.set(value / 100)
    send_function()

def emergency_stop():
    quick_set_value(duty_entry, duty_slider, duty_progressbar, 0, send_duty, is_duty=True)
    status_label.configure(text="🚨 EMERGENCY SHUTDOWN SEQUENCE INITIATED 🚨", text_color=COLOR_EMERGENCY, font=(FONT_BODY[0], 14, "bold"))
    duty_progressbar.configure(progress_color=COLOR_EMERGENCY)

# --- GUI Setup ---
ctk.set_appearance_mode("light")  # Light mode fits mobile better
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title(APP_NAME)
root.geometry(WINDOW_SIZE)
root.configure(fg_color=COLOR_BACKGROUND)
root.resizable(False, False)

# Title Label with subtle shadow effect
title_label = ctk.CTkLabel(root, text=APP_NAME, font=FONT_TITLE, text_color=COLOR_TEXT_PRIMARY)
title_label.pack(pady=(30, 20))

# Main Card Frame
main_content_frame = ctk.CTkFrame(root, fg_color=COLOR_FRAME_BG, corner_radius=CORNER_RADIUS, border_width=0)
main_content_frame.pack(pady=10, padx=20, fill="both", expand=True)

def create_control_section(parent, title_text, unit_text, default_value, from_val, to_val, quick_values,
                           entry_update_cmd, slider_update_cmd, send_cmd, is_duty_section=False):
    section_frame = ctk.CTkFrame(parent, fg_color=COLOR_FRAME_BG, corner_radius=CORNER_RADIUS, border_width=1)
    section_frame.pack(pady=15, padx=10, fill="x")

    ctk.CTkLabel(section_frame, text=title_text, font=FONT_HEADER, text_color=COLOR_TEXT_PRIMARY).pack(anchor="w", padx=15, pady=(15,10))

    input_row_frame = ctk.CTkFrame(section_frame, fg_color=COLOR_FRAME_BG)
    input_row_frame.pack(fill="x", padx=15)

    entry = ctk.CTkEntry(input_row_frame, width=INPUT_FIELD_WIDTH, font=FONT_BODY, justify="center",
                         fg_color=COLOR_WIDGET_BG, border_color=COLOR_ACCENT_PRIMARY, text_color=COLOR_TEXT_PRIMARY,
                         corner_radius=CORNER_RADIUS//2, border_width=0)
    entry.insert(0, str(default_value))
    entry.pack(side="left", padx=(0, 10), pady=10)

    slider = ctk.CTkSlider(input_row_frame, from_=from_val, to=to_val,
                           button_color=COLOR_ACCENT_PRIMARY, button_hover_color=COLOR_ACCENT_SECONDARY,
                           progress_color=COLOR_ACCENT_PRIMARY, fg_color=COLOR_WIDGET_BG,
                           corner_radius=CORNER_RADIUS//2)
    slider.set(default_value)
    slider.pack(side="left", fill="x", expand=True, pady=10)
    
    ctk.CTkLabel(input_row_frame, text=unit_text, font=FONT_LABEL, text_color=COLOR_TEXT_SECONDARY).pack(side="left", padx=(10,0))

    # Link entry and slider
    entry.bind("<Return>", lambda event: entry_update_cmd())
    entry.bind("<FocusOut>", lambda event: entry_update_cmd())
    slider.configure(command=slider_update_cmd)

    pb = None
    if is_duty_section:
        pb_frame = ctk.CTkFrame(section_frame, fg_color=COLOR_FRAME_BG)
        pb_frame.pack(fill="x", padx=15, pady=(0,15))
        pb = ctk.CTkProgressBar(pb_frame, orientation="horizontal", height=14, corner_radius=CORNER_RADIUS,
                                fg_color=COLOR_WIDGET_BG, progress_color=COLOR_ACCENT_PRIMARY)
        pb.set(default_value / 100)
        pb.pack(fill="x", expand=True)

    quick_btn_frame = ctk.CTkFrame(section_frame, fg_color=COLOR_FRAME_BG)
    quick_btn_frame.pack(pady=(0,15), padx=15, fill="x")

    ctk.CTkLabel(quick_btn_frame, text="⚡ Quick Presets:", font=FONT_LABEL, text_color=COLOR_TEXT_SECONDARY).pack(side="left", padx=(0,10))

    for val in quick_values:
        is_zero_duty = is_duty_section and val == 0
        btn_color = COLOR_EMERGENCY if is_zero_duty else COLOR_WIDGET_BG
        hover_c = "#d94a4a" if is_zero_duty else COLOR_ACCENT_SECONDARY
        txt_color = "#fff" if is_zero_duty else COLOR_TEXT_PRIMARY

        pb_arg = pb if is_duty_section else None

        ctk.CTkButton(quick_btn_frame, text=f"{val}", width=60, height=36,
                      font=FONT_BUTTON, fg_color=btn_color, hover_color=hover_c, text_color=txt_color,
                      corner_radius=CORNER_RADIUS//2,
                      command=lambda v=val, e=entry, s=slider, p=pb_arg, sf=send_cmd, id=is_duty_section: \
                              quick_set_value(e, s, p, v, sf, id)
                     ).pack(side="left", padx=6)
    return entry, slider, pb

# === Frequency Control Section ===
freq_entry, freq_slider, _ = create_control_section(
    main_content_frame, "PWM Frequency", "Hz", 1500, 100, 10000,
    [1000, 1500, 2000, 4000, 6000, 9000, 10000],
    update_freq_from_entry, update_freq_from_slider, send_frequency, is_duty_section=False
)

# === Duty Cycle Control Section ===
duty_entry, duty_slider, duty_progressbar = create_control_section(
    main_content_frame, "Duty Cycle", "%", 0, 0, 100,
    [0, 10, 20, 25, 50, 75, 100],
    update_duty_from_entry, update_duty_from_slider, send_duty, is_duty_section=True
)

# === Emergency Stop Section ===
emergency_frame = ctk.CTkFrame(root, fg_color=COLOR_FRAME_BG, corner_radius=CORNER_RADIUS)
emergency_frame.pack(pady=15, padx=20, fill="x")

emergency_button = ctk.CTkButton(
    emergency_frame,
    text="🛑 EMERGENCY SHUTDOWN",
    font=FONT_BUTTON,
    fg_color=COLOR_EMERGENCY,
    hover_color="#ff6b68",
    text_color="#fff",
    height=60,
    corner_radius=CORNER_RADIUS,
    border_width=2,
    border_color=COLOR_ERROR,
    command=emergency_stop
)
emergency_button.pack(fill="x")

# --- Status Labels ---
status_label = ctk.CTkLabel(root, text="Initializing...", font=FONT_BODY, text_color=COLOR_TEXT_SECONDARY)
status_label.pack(pady=(15, 5))

conn_info = ctk.CTkLabel(root, text="Link Status: Unknown", font=FONT_SMALL, text_color=COLOR_TEXT_SECONDARY)
conn_info.pack()

# --- Pulsate Emergency Button Effect ---
def pulse_emergency():
    current_color = emergency_button.cget("fg_color")
    new_color = "#ff6b68" if current_color == COLOR_EMERGENCY else COLOR_EMERGENCY
    emergency_button.configure(fg_color=new_color)
    root.after(1200, pulse_emergency)

root.after(1000, pulse_emergency)

# --- Initialize Serial ---
setup_serial_connection()

root.mainloop()
