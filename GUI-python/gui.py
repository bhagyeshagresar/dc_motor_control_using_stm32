import serial
import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports

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
    exit(1)

def send_duty():
    duty_text = duty_entry.get()
    print("Raw duty input:", duty_text)
    if duty_text.isdigit():
        duty = int(duty_text)
        if 0 <= duty <= 100:
            uart_cmd = f"D:{duty}\n"
            print(f"Sending UART command: {uart_cmd.strip()}")
            ser.write(uart_cmd.encode())
            status_label.config(text=f"✓ Duty cycle set to {duty}%", fg="green")
        else:
            status_label.config(text="❌ Enter duty cycle 0-100%", fg="red")
    else:
        status_label.config(text="❌ Invalid input! Numbers only.", fg="red")

def send_frequency():
    freq_text = freq_entry.get()
    print("Raw frequency input:", freq_text)
    if freq_text.isdigit():
        freq = int(freq_text)
        if 100 <= freq <= 10000:
            uart_cmd = f"F:{freq}\n"
            print(f"Sending UART command: {uart_cmd.strip()}")
            ser.write(uart_cmd.encode())
            status_label.config(text=f"✓ PWM frequency set to {freq} Hz", fg="blue")
        else:
            status_label.config(text="❌ Enter frequency 100-10000 Hz", fg="red")
    else:
        status_label.config(text="❌ Invalid input! Numbers only.", fg="red")

def quick_duty(value):
    """Quick set duty cycle buttons"""
    duty_entry.delete(0, tk.END)
    duty_entry.insert(0, str(value))
    send_duty()

def quick_freq(value):
    """Quick set frequency buttons"""
    freq_entry.delete(0, tk.END)
    freq_entry.insert(0, str(value))
    send_frequency()

def emergency_stop():
    """Emergency stop - set duty to 0%"""
    duty_entry.delete(0, tk.END)
    duty_entry.insert(0, "0")
    send_duty()

# GUI layout
root = tk.Tk()
root.title("STM32 Motor PWM Controller")
root.geometry("450x550")
root.configure(bg='#f0f0f0')

# Title
title_label = tk.Label(root, text="STM32 Motor PWM Controller", 
                      font=("Arial", 16, "bold"), bg='#f0f0f0')
title_label.pack(pady=10)

# === DUTY CYCLE CONTROL ===
duty_frame = tk.LabelFrame(root, text="🎛️ Motor Speed (Duty Cycle)", 
                          font=("Arial", 12, "bold"), padx=15, pady=10, bg='#f0f0f0')
duty_frame.pack(pady=10, padx=15, fill="x")

tk.Label(duty_frame, text="Duty Cycle (%):", font=("Arial", 10), bg='#f0f0f0').pack(anchor="w")
duty_entry = tk.Entry(duty_frame, width=20, font=("Arial", 11))
duty_entry.pack(anchor="w", pady=5)
duty_entry.insert(0, "50")  # Default value

tk.Button(duty_frame, text="Set Duty Cycle", command=send_duty, 
          bg="lightgreen", font=("Arial", 10, "bold"), width=15).pack(pady=8)

# Quick duty cycle buttons
quick_duty_frame = tk.Frame(duty_frame, bg='#f0f0f0')
quick_duty_frame.pack(pady=5)
tk.Label(quick_duty_frame, text="Quick Set:", font=("Arial", 9), bg='#f0f0f0').pack(side="left")

duty_values = [0, 25, 50, 75, 100]
for val in duty_values:
    color = "lightcoral" if val == 0 else "lightblue"
    tk.Button(quick_duty_frame, text=f"{val}%", width=6, bg=color,
             command=lambda v=val: quick_duty(v), font=("Arial", 8)).pack(side="left", padx=2)

# === FREQUENCY CONTROL ===
freq_frame = tk.LabelFrame(root, text="⚡ PWM Frequency", 
                          font=("Arial", 12, "bold"), padx=15, pady=10, bg='#f0f0f0')
freq_frame.pack(pady=10, padx=15, fill="x")

tk.Label(freq_frame, text="Frequency (Hz):", font=("Arial", 10), bg='#f0f0f0').pack(anchor="w")
freq_entry = tk.Entry(freq_frame, width=20, font=("Arial", 11))
freq_entry.pack(anchor="w", pady=5)
freq_entry.insert(0, "1000")  # Default frequency

tk.Button(freq_frame, text="Set Frequency", command=send_frequency, 
          bg="lightblue", font=("Arial", 10, "bold"), width=15).pack(pady=8)

# Quick frequency buttons
quick_freq_frame = tk.Frame(freq_frame, bg='#f0f0f0')
quick_freq_frame.pack(pady=5)
tk.Label(quick_freq_frame, text="Quick Set:", font=("Arial", 9), bg='#f0f0f0').pack(side="left")

freq_values = [500, 1000, 2000, 5000]
for val in freq_values:
    tk.Button(quick_freq_frame, text=f"{val}", width=6, bg="lightyellow",
             command=lambda v=val: quick_freq(v), font=("Arial", 8)).pack(side="left", padx=2)

# === EMERGENCY STOP ===
emergency_frame = tk.Frame(root, bg='#f0f0f0')
emergency_frame.pack(pady=15)

tk.Button(emergency_frame, text="🛑 EMERGENCY STOP", command=emergency_stop, 
          bg="red", fg="white", font=("Arial", 12, "bold"), width=20).pack()

# === STATUS DISPLAY ===
status_label = tk.Label(root, text="Ready to send commands", 
                       fg="black", font=("Arial", 11), bg='#f0f0f0')
status_label.pack(pady=10)

# === INSTRUCTIONS ===
instructions_frame = tk.LabelFrame(root, text="📋 Instructions", 
                                  font=("Arial", 10, "bold"), padx=10, pady=5, bg='#f0f0f0')
instructions_frame.pack(pady=10, padx=15, fill="x")

instructions_text = """• Set PWM frequency first (1000-5000 Hz recommended for motors)
• Adjust duty cycle to control motor speed (0-100%)
• Use Emergency Stop to immediately stop the motor
• Ensure motor is connected through motor driver (L298N, etc.)
• Check that power supply can handle motor current requirements"""

instructions_label = tk.Label(instructions_frame, text=instructions_text, 
                             font=("Arial", 9), justify="left", bg='#f0f0f0')
instructions_label.pack(anchor="w")

# === CONNECTION INFO ===
conn_info = tk.Label(root, text=f"Connected to: {ser.port if ser else 'No connection'}", 
                    font=("Arial", 8), fg="gray", bg='#f0f0f0')
conn_info.pack(side="bottom", pady=5)

root.mainloop()

# Close serial connection when GUI closes
if ser:
    ser.close()