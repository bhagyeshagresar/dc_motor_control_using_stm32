/*
 * isense.c
 *
 *  Created on: May 31, 2025
 *      Author: bhagy
 */

#include "isense.h"

volatile int adc_cnts = 0;
volatile int current_amp = 0;

int read_adc_counts(){
	return adc_cnts;
}


HAL_StatusTypeDef current_sensor_init(I2C_HandleTypeDef I2C_Handle){
	HAL_StatusTypeDef ret;
	uint8_t config_data[2];
	uint8_t calibration_data[2];
	uint16_t config_value = 0x399F; //Default power on reset value
	uint16_t calibration_value = 0x1000; //Based on current_lsb of 0.1mA/bit, Datasheet Pg. 17, Eqn 4

	//Split the data into an array of two bytes. The INA219 chip requires MSB sent first
	config_data[0] = (config_value >> 8) & 0xFF; //MSB
	config_data[1] = (config_value) & 0xFF; //LSB

	//Write the default config value
	ret = HAL_I2C_Mem_Write(&I2C_Handle, INA219_ADDR, INA219_CONFIG_REG, I2C_MEMADD_SIZE_8BIT, config_data, 2, 100);

	calibration_data[0] = (calibration_value >> 8) & 0xFF; //MSB
	calibration_data[1] = (calibration_value) & 0xFF; //LSB

	//Write the calculated calibration value
	ret = HAL_I2C_Mem_Write(&I2C_Handle, INA219_ADDR, INA219_CALIBRTN_REG, I2C_MEMADD_SIZE_8BIT, calibration_data, 2, 100);


	return ret;

}

