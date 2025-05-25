import serial
import tkinter as tk
import serial.tools.list_ports

# Adjust COM port and baudrate to match your board
for port in serial.tools.list_ports.comports():
    print(f"{port.device} — {port.description}")

# Pick the first available port

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
def send_delay():
    delay = entry.get()
    print("Raw input:", delay)
    if delay.isdigit():
        val = int(delay)
        if 100 <= val <= 900:
            digit = str(val // 100)
            print(f"Sending over UART: '{digit}'")
            ser.write(digit.encode())

root = tk.Tk()
root.title("STM32 LED Delay Controller")

tk.Label(root, text="Enter Delay (100–900 ms):").pack(pady=10)
entry = tk.Entry(root)
entry.pack(padx=10)

tk.Button(root, text="Send", command=send_delay).pack(pady=10)

root.mainloop()
