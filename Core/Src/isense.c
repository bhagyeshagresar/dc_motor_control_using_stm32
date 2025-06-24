/*
 * isense.c
 *
 *  Created on: May 31, 2025
 *      Author: Bhagyesh Agresar
 */

#include "isense.h"
#include "stm32f4xx_hal.h"
#include <string.h>

volatile int16_t shunt_adc_cnts = 0;
volatile int16_t current = 0;

int read_adc_counts(I2C_HandleTypeDef* I2C_Handle){

	uint8_t shunt_adc_data[2];

	HAL_I2C_Mem_Read(I2C_Handle, INA219_ADDR, INA219_SHUNT_REG, I2C_MEMADD_SIZE_8BIT, shunt_adc_data, 2, 100);

	shunt_adc_cnts = (int16_t)(shunt_adc_data[0] << 8) | (shunt_adc_data[1]);

	return shunt_adc_cnts;

}


int read_current_amps(I2C_HandleTypeDef* I2C_Handle){
	uint8_t current_amps_data[2];

	HAL_I2C_Mem_Read(I2C_Handle, INA219_ADDR, INA219_CURRENT_REG, I2C_MEMADD_SIZE_8BIT, current_amps_data, 2, 100);

	current = (int16_t)((current_amps_data[0] << 8) | (current_amps_data[1]));

	return current;


}




void current_sensor_init(char * error_buffer, I2C_HandleTypeDef* I2C_Handle){
	HAL_StatusTypeDef ret;
	//char error_buff[100];
	uint8_t config_data[2];
	uint8_t calibration_data[2];
	uint16_t config_value = 0x39FF; //12bit and 128 samples
	uint16_t calibration_value = 0x1000; //Based on current_lsb of 0.1mA/bit, Datasheet Pg. 17, Eqn 4

	strcpy(error_buffer, "");

	//Do a test read
	char buffer[2];
	ret = HAL_I2C_Mem_Read(I2C_Handle, INA219_ADDR, INA219_CONFIG_REG, I2C_MEMADD_SIZE_8BIT, buffer, 2, 100);

	if(ret != HAL_OK){
		strcpy(error_buffer, "Test Read for I2C failed\n");
		return;
	}

	//Split the data into an array of two bytes. The INA219 chip requires MSB sent first
	config_data[0] = (config_value >> 8) & 0xFF; //MSB
	config_data[1] = (config_value) & 0xFF; //LSB

	//Write the default config value
	ret = HAL_I2C_Mem_Write(I2C_Handle, INA219_ADDR, INA219_CONFIG_REG, I2C_MEMADD_SIZE_8BIT, config_data, 2, 100);

	if(ret != HAL_OK){
		strcpy(error_buffer, "problem writing data to the configuration register\n");
		return;
	}

	calibration_data[0] = (calibration_value >> 8) & 0xFF; //MSB
	calibration_data[1] = (calibration_value) & 0xFF; //LSB

	//Write the calculated calibration value
	ret = HAL_I2C_Mem_Write(I2C_Handle, INA219_ADDR, INA219_CALIBRTN_REG, I2C_MEMADD_SIZE_8BIT, calibration_data, 2, 100);

	if(ret != HAL_OK){
		strcpy(error_buffer, "problem writing data to the calibration register\n");
		return;
	}

}

