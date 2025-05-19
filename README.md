# Brushed DC Motor Control using STM32

# Hardware 

1 - STM32F401RE MCU
2 - Brushed DC Motor with encoder
3 - INA219 Current Sensor
4 - DRV8835 H Bridge
5 - Battery Pack
6 - Resistors and Capacitors


# Software Overview

1 - Client Application /GUI that supports the following features:
    a: Read current sensor (ADC counts)
    b: Read current sensor (mA)
    c: Read encoder (counts)
    d: Read encoder (deg)
    e: Reset encoder
    f: Set PWM (-100 to 100)
    g: Set current gains
    h: Get current gains
    i: Set position gains
    j: Get position gains
    k: Test current control
    l: Go to angle (deg)
    m: Load step trajectory
    n: Load cubic trajectory
    o: Execute trajectory
    p: Unpower the motor
    q: Quit client
    r: Get mode


2 - STM32 firmware for motor driver:
    The firmware will include a low frequency position control loop(200 Hz) and a high freqeuency current control loop (5 KHz). 