# Brushed DC Motor Control using STM32

This blog covers the latest updates for this project: [text](https://bhagyeshagresar.blogspot.com/2025/06/building-dc-motor-control-system-with.html)

## Hardware

1. **STM32F401RE** microcontroller (MCU)  
2. **Brushed DC Motor** with encoder  
3. **INA219** current sensor  
4. **DRV8835** H-Bridge motor driver  
5. **Battery Pack**  
6. **Resistors and Capacitors**

---

## Software Overview

### 1. Client Application / GUI
![alt text](Csharp_form_snapshot.png)


---

### 2. STM32 Firmware

- **Current Control Loop**: High-frequency loop running at **5 kHz**  
- **Position Control Loop**: Lower-frequency loop running at **200 Hz**



### Step 1: Testing the encoder
1. Powered the encoder on the DC motor using 3.3V from the STM32 and connected the channels A and B of the encoder to the nscope to test quadrature signals

2. Implemented a simple GPIO interrupt on every rising and falling edge of channel A and then increment the encoder position using simple quadrature decoding logic


![alt text](Ccw_encoder2.jpg)


### Step 2: Basic PWM Generation using Timer
 1. Configured Timer3 to generate a user defined duty cycle. The prescaler of the timer is set to 1MHz and the ARR register(max rollover counter) is set to 100.

 2. Tpwm = ARR/Prescaler = 100/1MHZ = 100 microseconds. The frequency of the PWM is 10 kHZ.

 Nscope Output with 30% duty cycle:
 
![alt text](pwm_30_percent_duty_cycle.png)


