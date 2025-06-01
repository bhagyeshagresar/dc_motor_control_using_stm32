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




