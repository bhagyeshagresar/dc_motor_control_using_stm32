# Brushed DC Motor Control using STM32

## 🧰 Hardware

1. **STM32F401RE** microcontroller (MCU)  
2. **Brushed DC Motor** with encoder  
3. **INA219** current sensor  
4. **DRV8835** H-Bridge motor driver  
5. **Battery Pack**  
6. **Resistors and Capacitors**

---

## 🧑‍💻 Software Overview

### 1. Client Application / GUI

Supports the following features:

- `a:` Read current sensor (ADC counts)  
- `b:` Read current sensor (mA)  
- `c:` Read encoder (counts)  
- `d:` Read encoder (degrees)  
- `e:` Reset encoder  
- `f:` Set PWM (range: -100 to 100)  
- `g:` Set current gains  
- `h:` Get current gains  
- `i:` Set position gains  
- `j:` Get position gains  
- `k:` Test current control  
- `l:` Go to angle (degrees)  
- `m:` Load step trajectory  
- `n:` Load cubic trajectory  
- `o:` Execute trajectory  
- `p:` Unpower the motor  
- `q:` Quit client  
- `r:` Get current mode

---

### 2. STM32 Firmware

- **Current Control Loop**: High-frequency loop running at **5 kHz**  
- **Position Control Loop**: Lower-frequency loop running at **200 Hz**
