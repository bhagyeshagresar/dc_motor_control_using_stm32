import threading
import time
import serial
import serial.tools.list_ports
import customtkinter as ctk
from tkinter import PhotoImage # Keep for potential future icon use

# --- Constants for Styling ---
APP_NAME = "BG ROBOTICS PWM Modulator XE" # XE for Xtreme Edition ;)
WINDOW_SIZE = "550x850" # Slightly larger for more space

# Color Palette (Refined Sci-Fi Dark Theme)
COLOR_BACKGROUND = "#1a1a2e"  # Even darker, deeper space blue/purple
COLOR_FRAME_BG = "#24243e"    # Main content frame background
COLOR_WIDGET_BG = "#2d2d4f"   # Background for input elements, sliders
COLOR_TEXT = "#f0f0f0"        # Brighter Off-White for better contrast
COLOR_TEXT_SUBTLE = "#a0a0c0" # For less important text
COLOR_ACCENT_PRIMARY = "#00bfff" # Deep Sky Blue / Cyan (Keep)
COLOR_ACCENT_GLOW = "#00ffff" # Brighter Cyan for hover/focus
COLOR_ACCENT_SECONDARY = "#7f00ff" # Electric Purple for highlights
COLOR_SUCCESS = "#00e676"     # Vibrant Green
COLOR_ERROR = "#ff1744"       # Vibrant Red
COLOR_WARNING = "#ffc400"     # Amber/Yellow
COLOR_EMERGENCY = "#ff3d00"   # Bright Orange-Red

# Fonts (Ensure Exo 2 and Orbitron are installed for best effect)
try:
    ctk.CTkFont(family="Exo 2")
    ctk.CTkFont(family="Orbitron")
    FONT_TITLE = ("Orbitron", 24, "bold")
    FONT_HEADER = ("Exo 2", 18, "bold")
    FONT_SUBHEADER = ("Exo 2", 14)
    FONT_BODY = ("Exo 2", 12)
    FONT_BUTTON = ("Exo 2", 12, "bold")
    FONT_LABEL = ("Exo 2", 11)
    FONT_SMALL = ("Exo 2", 10, "italic")
except Exception:
    print("Sci-fi fonts (Exo 2, Orbitron) not found, using system defaults.")
    FONT_TITLE = ("Impact", 24, "bold")
    FONT_HEADER = ("Arial", 18, "bold")
    FONT_SUBHEADER = ("Arial", 14)
    FONT_BODY = ("Arial", 12)
    FONT_BUTTON = ("Arial", 12, "bold")
    FONT_LABEL = ("Arial", 11)
    FONT_SMALL = ("Arial", 10, "italic")

CORNER_RADIUS = 12
INPUT_FIELD_WIDTH = 100

# --- Serial Connection (No changes needed here) ---
ser = None
def setup_serial_connection():
    global ser
    print("Initializing Subspace Comms Array...") # Themed print
    ports = serial.tools.list_ports.comports()
    if not ports:
        status_label.configure(text="❌ COMMS OFFLINE: No serial ports detected.", text_color=COLOR_ERROR)
        conn_info.configure(text="Link Status: DEACTIVATED", text_color=COLOR_ERROR)
        return False

    for port_info in ports:
        print(f"  Detected Port: {port_info.device} — {port_info.description}")

    # Prioritize common STM32 descriptive names if available
    stm_candidates = [p.device for p in ports if "STM" in p.description.upper() or "SERIAL" in p.description.upper()]
    generic_candidates = ['/dev/ttyUSB0', '/dev/ttyACM0'] + [f'COM{i}' for i in range(3, 10)]
    
    # Combine and unique-ify, STM candidates first
    serial_device_candidates = list(dict.fromkeys(stm_candidates + [p.device for p in ports] + generic_candidates))

    for device in serial_device_candidates:
        try:
            ser = serial.Serial(device, 9600, timeout=1)
            print(f"Successfully established link with {device}")
            conn_info.configure(text=f"Link Active: {ser.port}", text_color=COLOR_SUCCESS)
            status_label.configure(text="SYSTEM ONLINE | Awaiting Directives", text_color=COLOR_SUCCESS)
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

def show_startup_animation():
    splash = ctk.CTk()
    splash.title("Initializing...")
    splash.geometry("500x300")
    splash.configure(fg_color=COLOR_BACKGROUND)
    splash.resizable(False, False)

    splash_label = ctk.CTkLabel(splash, text="BG ROBOTICS Systems Booting", font=FONT_TITLE, text_color=COLOR_ACCENT_PRIMARY)
    splash_label.pack(expand=True)

    # Hide main window
    root.withdraw()

    # Animation state
    dots = ["", ".", "..", "..."]
    i = 0

    def update_label():
        nonlocal i
        splash_label.configure(text=f"BG ROBOTICS Systems Booting{dots[i % 4]}")
        i += 1
        if i < 3:  # runs ~3 seconds (10 * 300ms)
            splash.after(300, update_label)
        else:
            splash.destroy()
            root.deiconify()

    splash.after(100, update_label)
    splash.mainloop()


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
        val = max(0, min(100, val)) # Clamp value
        duty_slider.set(val)
        duty_progressbar.set(val / 100)
        # send_duty() # Slider's command will call this
    # else: let send_duty handle non-digit error

def update_freq_from_slider(value):
    freq_val = int(value)
    freq_entry.delete(0, ctk.END)
    freq_entry.insert(0, str(freq_val))
    send_frequency()

def update_freq_from_entry():
    if freq_entry.get().isdigit():
        val = int(freq_entry.get())
        val = max(100, min(1000, val)) # Clamp value
        freq_slider.set(val)
        # send_frequency() # Slider's command will call this
    # else: let send_frequency handle non-digit error

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
            status_label.configure(text=f"THRUST OUTPUT: {duty}%", text_color=COLOR_SUCCESS)
            duty_progressbar.set(duty / 100) # Ensure progress bar is in sync
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
        if 100 <= freq <= 1000:
            uart_cmd = f"F:{freq}\n"
            ser.write(uart_cmd.encode())
            status_label.configure(text=f"FREQUENCY CALIBRATED: {freq} Hz", text_color=COLOR_TEXT)
        else:
            status_label.configure(text="FREQ RANGE ERROR: 100-1000 Hz", text_color=COLOR_ERROR)
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
ctk.set_appearance_mode("dark")
# ctk.set_default_color_theme("blue") # Can try "dark-blue" or a custom theme file later

root = ctk.CTk()
root.title(APP_NAME)
root.geometry(WINDOW_SIZE)
root.configure(fg_color=COLOR_BACKGROUND)
root.resizable(False, False) # For a more appliance-like feel

# --- Title ---
title_label = ctk.CTkLabel(root, text=APP_NAME, font=FONT_TITLE, text_color=COLOR_ACCENT_PRIMARY)
title_label.pack(pady=(25, 15))

# --- Main Content Frame ---
main_content_frame = ctk.CTkFrame(root, fg_color=COLOR_FRAME_BG, corner_radius=CORNER_RADIUS)
main_content_frame.pack(pady=10, padx=20, fill="both", expand=True)


# Helper function to create sections
def create_control_section(parent, title_text, unit_text, default_value, from_val, to_val, quick_values,
                           entry_update_cmd, slider_update_cmd, send_cmd, is_duty_section=False):
    section_frame = ctk.CTkFrame(parent, fg_color="transparent")
    section_frame.pack(pady=15, padx=10, fill="x")

    header_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
    header_frame.pack(fill="x", pady=(0, 10))
    ctk.CTkLabel(header_frame, text=title_text, font=FONT_HEADER, text_color=COLOR_TEXT).pack(side="left")

    # Input Row (Entry and Slider)
    input_row_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
    input_row_frame.pack(fill="x", pady=5)

    entry = ctk.CTkEntry(input_row_frame, width=INPUT_FIELD_WIDTH, font=FONT_BODY, justify="center",
                         fg_color=COLOR_WIDGET_BG, border_color=COLOR_ACCENT_SECONDARY, text_color=COLOR_TEXT)
    entry.insert(0, str(default_value))
    entry.pack(side="left", padx=(0, 10))

    slider = ctk.CTkSlider(input_row_frame, from_=from_val, to=to_val,
                           button_color=COLOR_ACCENT_PRIMARY, button_hover_color=COLOR_ACCENT_GLOW,
                           progress_color=COLOR_ACCENT_SECONDARY, fg_color=COLOR_WIDGET_BG)
    slider.set(default_value)
    slider.pack(side="left", fill="x", expand=True)
    
    ctk.CTkLabel(input_row_frame, text=unit_text, font=FONT_LABEL, text_color=COLOR_TEXT_SUBTLE).pack(side="left", padx=(10,0))


    # Link entry and slider
    entry.bind("<Return>", lambda event: entry_update_cmd()) # Update slider on Enter
    entry.bind("<FocusOut>", lambda event: entry_update_cmd()) # Update slider when focus leaves
    slider.configure(command=slider_update_cmd)

    # Progress bar for duty cycle
    pb = None
    if is_duty_section:
        pb_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        pb_frame.pack(fill="x", pady=(5,0))
        pb = ctk.CTkProgressBar(pb_frame, orientation="horizontal", height=12, corner_radius=6,
                                fg_color=COLOR_WIDGET_BG, progress_color=COLOR_ACCENT_PRIMARY)
        pb.set(default_value / 100)
        pb.pack(fill="x", expand=True, pady=(5,5))


    # Quick Set Buttons
    quick_btn_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
    quick_btn_frame.pack(pady=(10,0))
    ctk.CTkLabel(quick_btn_frame, text="⚡ Quick Presets:", font=FONT_LABEL, text_color=COLOR_TEXT_SUBTLE).pack(side="left", padx=(0,10))
    for val in quick_values:
        is_zero_duty = is_duty_section and val == 0
        btn_color = COLOR_EMERGENCY if is_zero_duty else COLOR_WIDGET_BG
        hover_c = "#c82333" if is_zero_duty else COLOR_ACCENT_GLOW
        txt_color = COLOR_TEXT if not is_zero_duty else "#FFFFFF"
        
        # Determine if this is the '0' button for duty to pass the progress bar
        pb_arg = pb if is_duty_section else None
        
        ctk.CTkButton(quick_btn_frame, text=f"{val}", width=55, height=30,
                      font=FONT_BUTTON, fg_color=btn_color, hover_color=hover_c, text_color=txt_color,
                      corner_radius=CORNER_RADIUS-4, border_width=1 if is_zero_duty else 0, border_color=COLOR_WARNING,
                      command=lambda v=val, e=entry, s=slider, p=pb_arg, sf=send_cmd, id=is_duty_section: \
                              quick_set_value(e, s, p, v, sf, id)
                     ).pack(side="left", padx=4)
    return entry, slider, pb


# === DUTY CYCLE CONTROL ===
duty_entry, duty_slider, duty_progressbar = create_control_section(
    main_content_frame, "THRUST MODULATION", "%", 50, 0, 100, [0, 25, 50, 75, 100],
    update_duty_from_entry, update_duty_from_slider, send_duty, is_duty_section=True
)

# Visual Separator
ctk.CTkFrame(main_content_frame, height=2, fg_color=COLOR_WIDGET_BG, corner_radius=0).pack(fill="x", padx=20, pady=15)

# === FREQUENCY CONTROL ===
# freq_entry, freq_slider, _ = create_control_section(
#     main_content_frame, "OSCILLATION FREQUENCY", "Hz", 1000, 100, 10000, [500, 1000, 2000, 5000, 10000],
#     update_freq_from_entry, update_freq_from_slider, send_frequency
# )

freq_entry, freq_slider, _ = create_control_section(
    main_content_frame, "OSCILLATION FREQUENCY", "Hz", 500, 100, 1000, [100, 250, 500, 750, 1000],
    update_freq_from_entry, update_freq_from_slider, send_frequency
)


# === EMERGENCY STOP ===
emergency_frame = ctk.CTkFrame(main_content_frame, fg_color="transparent")
emergency_frame.pack(pady=(25,15))
ctk.CTkButton(emergency_frame, text="🛑 EMERGENCY SHUTDOWN 🛑", command=emergency_stop,
              font=(FONT_BUTTON[0], 16, "bold"), fg_color=COLOR_EMERGENCY, hover_color="#d40000",
              text_color="#FFFFFF", width=300, height=50, corner_radius=CORNER_RADIUS,
              border_width=2, border_color=COLOR_WARNING).pack()

# === STATUS DISPLAY ===
status_frame = ctk.CTkFrame(main_content_frame, fg_color=COLOR_WIDGET_BG, corner_radius=CORNER_RADIUS)
status_frame.pack(pady=15, fill="x", padx=10)
status_label = ctk.CTkLabel(status_frame, text="SYSTEM STANDBY | Initializing...",
                            font=(FONT_BODY[0], 13, "normal"), text_color=COLOR_WARNING,
                            height=40, wraplength=450)
status_label.pack(pady=10, padx=10)


# === SYSTEM DIRECTIVES (Instructions) ===
instr_frame = ctk.CTkFrame(main_content_frame, fg_color="transparent", border_color=COLOR_WIDGET_BG, border_width=1, corner_radius=CORNER_RADIUS)
instr_frame.pack(pady=10, padx=10, fill="x")
ctk.CTkLabel(instr_frame, text="SYSTEM DIRECTIVES", font=FONT_SUBHEADER, text_color=COLOR_TEXT_SUBTLE).pack(pady=(10,5))
instructions_text = """• Ensure BG ROBOTICS Modulator is securely linked to target device.
• Calibrate Oscillation Frequency prior to Thrust Modulation.
• Monitor telemetry for optimal performance parameters.
• IMMEDIATE ACTION: Utilize Emergency Shutdown for critical system halts.
• Power Core Stability: Verify source meets sustained operational demands."""
instructions_label = ctk.CTkLabel(instr_frame, text=instructions_text,
                                 font=FONT_LABEL, justify="left", text_color=COLOR_TEXT_SUBTLE,
                                 wraplength=480)
instructions_label.pack(anchor="w", padx=15, pady=(0,15))
# instructions_label.pack(pady=(0, 10), padx=10)

# --- Footer / Connection Info ---
footer_frame = ctk.CTkFrame(root, fg_color="transparent", height=30)
footer_frame.pack(side="bottom", fill="x", pady=(5,10), padx=20)

conn_info = ctk.CTkLabel(footer_frame, text="Link Status: SCANNING...",
                         font=FONT_SMALL, text_color=COLOR_WARNING)
conn_info.pack(side="left")

version_label = ctk.CTkLabel(footer_frame, text=f"{APP_NAME} v1.XE",
                             font=FONT_SMALL, text_color=COLOR_TEXT_SUBTLE)
version_label.pack(side="right")

footer = ctk.CTkLabel(root, text="BG ROBOTICS™ | Firmware v1.0 | Developed by <ChatGPT>", 
                      font=FONT_SMALL, text_color=COLOR_TEXT_SUBTLE)
footer.pack(pady=(5, 10))


# --- Initialize Serial and Start GUI ---
root.after(500, setup_serial_connection) # Delay slightly to allow GUI to draw first
show_startup_animation()
root.mainloop()

# --- Cleanup ---
if ser and ser.is_open:
    print("Deactivating Subspace Comms. Link terminated.")
    ser.close()