/*
 * encoder.h
 *
 *  Created on: May 10, 2025
 *      Author: Bhagyesh Agresar
 */

#ifndef INC_ENCODER_H_
#define INC_ENCODER_H_

#define ENCODER_A GPIO_PIN_9 //
#define ENCODER_B GPIO_PIN_7

volatile long motorPosition = 0;

int read_encoder_counts();
int read_encoder_degrees();
void reset_encoder_position(long);



#endif /* INC_ENCODER_H_ */
