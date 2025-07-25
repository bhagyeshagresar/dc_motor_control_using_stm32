/*
 * utilities.h
 *
 *  Created on: May 10, 2025
 *      Author: bhagy
 */

#ifndef INC_UTILITIES_H_
#define INC_UTILITIES_H_


typedef enum mode_set
{ IDLE,
  PWM,
  ITEST,
  HOLD,
  TRACK
}mode;


void set_mode(enum mode_set);
mode get_mode();
void set_pwm(int);
int get_pwm();

#endif /* INC_UTILITIES_H_ */
