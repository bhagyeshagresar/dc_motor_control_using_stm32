/*
 * encoder.c
 *
 *  Created on: May 19, 2025
 *      Author: bhagy
 */


#include "encoder.h"

volatile int motorPosition = 0;

int read_encoder_counts(){
	return motorPosition;
}


int read_encoder_degrees(){
	return (int)((360/PPR)*motorPosition);
}


void reset_encoder_position(){
	motorPosition = 0;
}
