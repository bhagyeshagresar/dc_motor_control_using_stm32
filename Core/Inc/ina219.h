/*
 * isense.h
 *
 *  Created on: May 10, 2025
 *      Author: bhagy
 */

#ifndef INC_INA219_H_
#define INC_INA219_H_

#include "stm32f4xx_hal.h"


#define INA219_ADDR 			0x40 << 1
#define INA219_CONFIG_REG		0x00
#define INA219_SHUNT_REG		0x01
#define INA219_BUS				0x02
#define INA219_CURRENT_REG 		0x04
#define INA219_PWR_REG			0x03
#define INA219_CALIBRTN_REG 	0x05

#define CURRENT_LSB 0.0001f


extern volatile int adc_cnts;
extern volatile int current_amp;

void current_sensor_init(char* error_buffer, I2C_HandleTypeDef* I2C_Handle);
int read_adc_counts(I2C_HandleTypeDef* I2C_Handle);
int read_current_amps(I2C_HandleTypeDef* I2C_Handle);



#endif /* INC_INA219_H_ */
