/*
 * encoder.h
 *
 *  Created on: May 10, 2025
 *      Author: Bhagyesh Agresar
 */

#ifndef INC_ENCODER_H_
#define INC_ENCODER_H_

#include <stdint.h>

#define ENCODER_A GPIO_PIN_9 //
#define ENCODER_B GPIO_PIN_7
#define ENCODER_VEL_SAMPLE_FREQ 1000
#define PPR 684

extern volatile int motorPosition;
extern volatile int oldMotorPosition;
extern volatile int64_t motorVelocity;


int read_encoder_counts();
int read_encoder_degrees();
void reset_encoder_position();



#endif /* INC_ENCODER_H_ */
