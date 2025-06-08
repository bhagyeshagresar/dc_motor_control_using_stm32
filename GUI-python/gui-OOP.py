import threading
import time
import serial
import serial.tools.list_ports
import customtkinter as ctk
from tkinter import PhotoImage  # Keep for potential future icon use


class BGRoboticsPWMModulatorXE(ctk.CTk):
    # --- Constants ---
    APP_NAME = "BG ROBOTICS PWM Modulator XE"  # XE for Xtreme Edition ;)
    WINDOW_SIZE = "550x850"

    # Colors
    COLOR_BACKGROUND = "#1a1a2e"
    COLOR_FRAME_BG = "#24243e"
    COLOR_WIDGET_BG = "#2d2d4f"
    COLOR_TEXT = "#f0f0f0"
    COLOR_TEXT_SUBTLE = "#a0a0c0"
    COLOR_ACCENT_PRIMARY = "#00bfff"
    COLOR_ACCENT_GLOW = "#00ffff"
    COLOR_ACCENT_SECONDARY = "#7f00ff"
    COLOR_SUCCESS = "#00e676"
    COLOR_ERROR = "#ff1744"
    COLOR_WARNING = "#ffc400"
    COLOR_EMERGENCY = "#ff3d00"

    CORNER_RADIUS = 12
    INPUT_FIELD_WIDTH = 100

    def __init__(self):
        super().__init__()

        # Serial port variable
        self.ser = None

        # Fonts setup
        self.setup_fonts()

        # Configure main window
        self.title(self.APP_NAME)
        self.geometry(self.WINDOW_SIZE)
        self.configure(fg_color=self.COLOR_BACKGROUND)
        self.resizable(False, False)

        # Initialize UI components
        self.create_widgets()

        # Initialize serial connection after a short delay
        self.after(500, self.setup_serial_connection)

        # Show startup animation
        self.show_startup_animation()

        # Protocol for window close
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_fonts(self):
        try:
            ctk.CTkFont(family="Exo 2")
            ctk.CTkFont(family="Orbitron")
            self.FONT_TITLE = ("Orbitron", 24, "bold")
            self.FONT_HEADER = ("Exo 2", 18, "bold")
            self.FONT_SUBHEADER = ("Exo 2", 14)
            self.FONT_BODY = ("Exo 2", 12)
            self.FONT_BUTTON = ("Exo 2", 12, "bold")
            self.FONT_LABEL = ("Exo 2", 11)
            self.FONT_SMALL = ("Exo 2", 10, "italic")
        except Exception:
            print("Sci-fi fonts not found, using system defaults.")
            self.FONT_TITLE = ("Impact", 24, "bold")
            self.FONT_HEADER = ("Arial", 18, "bold")
            self.FONT_SUBHEADER = ("Arial", 14)
            self.FONT_BODY = ("Arial", 12)
            self.FONT_BUTTON = ("Arial", 12, "bold")
            self.FONT_LABEL = ("Arial", 11)
            self.FONT_SMALL = ("Arial", 10, "italic")

    def create_widgets(self):
        # Title Label
        self.title_label = ctk.CTkLabel(self, text=self.APP_NAME, font=self.FONT_TITLE,
                                        text_color=self.COLOR_ACCENT_PRIMARY)
        self.title_label.pack(pady=(25, 15))

        # Main Frame
        self.main_content_frame = ctk.CTkFrame(self, fg_color=self.COLOR_FRAME_BG,
                                              corner_radius=self.CORNER_RADIUS)
        self.main_content_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Duty Control Section
        self.duty_entry, self.duty_slider, self.duty_progressbar = self.create_control_section(
            self.main_content_frame,
            title_text="THRUST MODULATION",
            unit_text="%",
            default_value=50,
            from_val=0,
            to_val=100,
            quick_values=[0, 25, 50, 75, 100],
            entry_update_cmd=self.update_duty_from_entry,
            slider_update_cmd=self.update_duty_from_slider,
            send_cmd=self.send_duty,
            is_duty_section=True,
        )

        # Visual separator
        ctk.CTkFrame(self.main_content_frame, height=2, fg_color=self.COLOR_WIDGET_BG,
                     corner_radius=0).pack(fill="x", padx=20, pady=15)

        # Frequency Control Section
        self.freq_entry, self.freq_slider, _ = self.create_control_section(
            self.main_content_frame,
            title_text="OSCILLATION FREQUENCY",
            unit_text="Hz",
            default_value=500,
            from_val=100,
            to_val=1000,
            quick_values=[100, 250, 500, 750, 1000],
            entry_update_cmd=self.update_freq_from_entry,
            slider_update_cmd=self.update_freq_from_slider,
            send_cmd=self.send_frequency,
            is_duty_section=False,
        )

        # Emergency Stop
        emergency_frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent")
        emergency_frame.pack(pady=(25, 15))
        ctk.CTkButton(emergency_frame, text="🛑 EMERGENCY SHUTDOWN 🛑", command=self.emergency_stop,
                      font=(self.FONT_BUTTON[0], 16, "bold"), fg_color=self.COLOR_EMERGENCY,
                      hover_color="#d40000", text_color="#FFFFFF", width=300, height=50,
                      corner_radius=self.CORNER_RADIUS, border_width=2, border_color=self.COLOR_WARNING).pack()

        # Status Display
        status_frame = ctk.CTkFrame(self.main_content_frame, fg_color=self.COLOR_WIDGET_BG,
                                    corner_radius=self.CORNER_RADIUS)
        status_frame.pack(pady=15, fill="x", padx=10)
        self.status_label = ctk.CTkLabel(status_frame, text="SYSTEM STANDBY | Initializing...",
                                         font=(self.FONT_BODY[0], 13, "normal"),
                                         text_color=self.COLOR_WARNING,
                                         height=40, wraplength=450)
        self.status_label.pack(pady=10, padx=10)

        # System Directives
        instr_frame = ctk.CTkFrame(self.main_content_frame, fg_color="transparent",
                                   border_color=self.COLOR_WIDGET_BG, border_width=1,
                                   corner_radius=self.CORNER_RADIUS)
        instr_frame.pack(pady=10, padx=10, fill="x")
        ctk.CTkLabel(instr_frame, text="SYSTEM DIRECTIVES", font=self.FONT_SUBHEADER,
                     text_color=self.COLOR_TEXT_SUBTLE).pack(pady=(10, 5))
        instructions_text = (
            "• Ensure BG ROBOTICS Modulator is securely linked to target device.\n"
            "• Calibrate Oscillation Frequency prior to Thrust Modulation.\n"
            "• Monitor telemetry for optimal performance parameters.\n"
            "• IMMEDIATE ACTION: Utilize Emergency Shutdown for critical system halts.\n"
            "• Power Core Stability: Verify source meets sustained operational demands."
        )
        ctk.CTkLabel(instr_frame, text=instructions_text, font=self.FONT_LABEL,
                     justify="left", text_color=self.COLOR_TEXT_SUBTLE,
                     wraplength=480).pack(anchor="w", padx=15, pady=(0, 15))

        # Footer / Connection Info
        footer_frame = ctk.CTkFrame(self, fg_color="transparent", height=30)
        footer_frame.pack(side="bottom", fill="x", pady=(5, 10), padx=20)

        self.conn_info = ctk.CTkLabel(footer_frame, text="Link Status: SCANNING...",
                                      font=self.FONT_SMALL, text_color=self.COLOR_WARNING)
        self.conn_info.pack(side="left")

        version_label = ctk.CTkLabel(footer_frame, text=f"{self.APP_NAME} v1.XE",
                                     font=self.FONT_SMALL, text_color=self.COLOR_TEXT_SUBTLE)
        version_label.pack(side="right")

        footer = ctk.CTkLabel(self, text="BG ROBOTICS™ | Firmware v1.0 | Developed by <ChatGPT>",
                              font=self.FONT_SMALL, text_color=self.COLOR_TEXT_SUBTLE)
        footer.pack(pady=(5, 10))

    def create_control_section(self, parent, title_text, unit_text, default_value,
                               from_val, to_val, quick_values,
                               entry_update_cmd, slider_update_cmd, send_cmd,
                               is_duty_section=False):
        section_frame = ctk.CTkFrame(parent, fg_color="transparent")
        section_frame.pack(pady=15, padx=10, fill="x")

        header_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(header_frame, text=title_text, font=self.FONT_HEADER,
                     text_color=self.COLOR_TEXT).pack(side="left")

        input_row_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        input_row_frame.pack(fill="x", pady=5)

        entry = ctk.CTkEntry(input_row_frame, width=self.INPUT_FIELD_WIDTH, font=self.FONT_BODY,
                             justify="center", fg_color=self.COLOR_WIDGET_BG,
                             border_color=self.COLOR_ACCENT_SECONDARY, text_color=self.COLOR_TEXT)
        entry.insert(0, str(default_value))
        entry.pack(side="left", padx=(0, 10))

        slider = ctk.CTkSlider(input_row_frame, from_=from_val, to=to_val,
                               button_color=self.COLOR_ACCENT_PRIMARY,
                               button_hover_color=self.COLOR_ACCENT_GLOW,
                               progress_color=self.COLOR_ACCENT_SECONDARY,
                               fg_color=self.COLOR_WIDGET_BG)
        slider.set(default_value)
        slider.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(input_row_frame, text=unit_text, font=self.FONT_LABEL,
                     text_color=self.COLOR_TEXT_SUBTLE).pack(side="left", padx=(10, 0))

        # Bind entry and slider updates
        entry.bind("<Return>", lambda e: entry_update_cmd())
        entry.bind("<FocusOut>", lambda e: entry_update_cmd())
        slider.configure(command=slider_update_cmd)

        # Progress bar for duty section only
        pb = None
        if is_duty_section:
            pb_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
            pb_frame.pack(fill="x", pady=(5, 0))
            pb = ctk.CTkProgressBar(pb_frame, width=500, corner_radius=self.CORNER_RADIUS,
                                   progress_color=self.COLOR_ACCENT_PRIMARY)
            pb.set(default_value / 100)
            pb.pack(fill="x")

        # Quick access buttons for fast setting
        quick_btn_frame = ctk.CTkFrame(section_frame, fg_color="transparent")
        quick_btn_frame.pack(pady=8)
        for val in quick_values:
            btn = ctk.CTkButton(quick_btn_frame, text=str(val), width=45,
                                fg_color=self.COLOR_ACCENT_SECONDARY,
                                hover_color=self.COLOR_ACCENT_GLOW,
                                command=lambda v=val: self.quick_set_value(v, entry, slider,
                                                                          send_cmd))
            btn.pack(side="left", padx=4)

        # Send button for manual sending
        send_btn = ctk.CTkButton(section_frame, text="▶ Send", width=100,
                                 fg_color=self.COLOR_ACCENT_PRIMARY,
                                 hover_color=self.COLOR_ACCENT_GLOW,
                                 command=lambda: send_cmd())
        send_btn.pack(pady=(10, 0))

        return entry, slider, pb

    def quick_set_value(self, val, entry, slider, send_func):
        entry.delete(0, "end")
        entry.insert(0, str(val))
        slider.set(val)
        send_func()

    # === DUTY MODULATION ===
    def update_duty_from_entry(self):
        try:
            val = float(self.duty_entry.get())
            if val < 0 or val > 100:
                raise ValueError("Duty out of range")
        except ValueError:
            self.set_status("Invalid Duty value. Must be 0-100%.", error=True)
            return
        self.duty_slider.set(val)
        if self.duty_progressbar:
            self.duty_progressbar.set(val / 100)
        self.send_duty()

    def update_duty_from_slider(self, val):
        val = float(val)
        self.duty_entry.delete(0, "end")
        self.duty_entry.insert(0, f"{val:.1f}")
        if self.duty_progressbar:
            self.duty_progressbar.set(val / 100)
        self.send_duty()

    def send_duty(self):
        val = self.duty_slider.get()
        self.send_serial_command(f"DUTY:{val:.1f}")

    # === FREQUENCY MODULATION ===
    def update_freq_from_entry(self):
        try:
            val = float(self.freq_entry.get())
            if val < 100 or val > 1000:
                raise ValueError("Frequency out of range")
        except ValueError:
            self.set_status("Invalid Frequency value. Must be 100-1000 Hz.", error=True)
            return
        self.freq_slider.set(val)
        self.send_frequency()

    def update_freq_from_slider(self, val):
        val = float(val)
        self.freq_entry.delete(0, "end")
        self.freq_entry.insert(0, f"{val:.1f}")
        self.send_frequency()

    def send_frequency(self):
        val = self.freq_slider.get()
        self.send_serial_command(f"FREQ:{val:.1f}")

    # === SERIAL COMMUNICATION ===
    def setup_serial_connection(self):
        ports = serial.tools.list_ports.comports()
        print("Initializing Subspace Comms Array...")
        for port in ports:
            print(f"  Detected Port: {port.device} — {port.description}")
        for port in ports:
            if "STM32" in port.description or "ACM" in port.device or "STLink" in port.description:
                try:
                    self.ser = serial.Serial(port.device, 115200, timeout=1)
                    print(f"Successfully established link with {port.device}")
                    self.set_status(f"Connected to {port.device}", success=True)
                    self.conn_info.configure(text=f"Link Status: Connected @ {port.device}", text_color=self.COLOR_SUCCESS)
                    return
                except (serial.SerialException, OSError) as e:
                    print(f"Failed to open {port.device}: {e}")
        self.set_status("No device found. Please connect BG ROBOTICS module.", error=True)
        self.conn_info.configure(text="Link Status: Not connected", text_color=self.COLOR_ERROR)

    def send_serial_command(self, command: str):
        if not self.ser or not self.ser.is_open:
            self.set_status("Serial port not connected.", error=True)
            return
        try:
            message = (command + "\n").encode('utf-8')
            self.ser.write(message)
            self.set_status(f"Sent: {command}", success=True)
        except serial.SerialException as e:
            self.set_status(f"Serial error: {str(e)}", error=True)

    # === EMERGENCY STOP ===
    def emergency_stop(self):
        self.set_status("EMERGENCY STOP ACTIVATED!", emergency=True)
        self.send_serial_command("STOP")

    # === STATUS DISPLAY ===
    def set_status(self, msg, success=False, error=False, warning=False, emergency=False):
        color = self.COLOR_TEXT
        if success:
            color = self.COLOR_SUCCESS
        elif error:
            color = self.COLOR_ERROR
        elif warning:
            color = self.COLOR_WARNING
        elif emergency:
            color = self.COLOR_EMERGENCY
        self.status_label.configure(text=msg, text_color=color)

    # === STARTUP ANIMATION ===
    def show_startup_animation(self):
        # Brief fading animation on the title label, cycling colors
        colors = [self.COLOR_ACCENT_PRIMARY, self.COLOR_ACCENT_SECONDARY,
                  self.COLOR_ACCENT_GLOW, self.COLOR_ACCENT_PRIMARY]
        def animate(i=0):
            self.title_label.configure(text_color=colors[i % len(colors)])
            if i < 15:
                self.after(150, animate, i + 1)
            else:
                self.title_label.configure(text_color=self.COLOR_ACCENT_PRIMARY)
        animate()

    def on_close(self):
        # Clean up serial port if open
        if self.ser and self.ser.is_open:
            self.ser.close()
        self.destroy()


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = BGRoboticsPWMModulatorXE()
    app.mainloop()
