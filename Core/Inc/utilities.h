/*
 * utilities.h
 *
 *  Created on: May 10, 2025
 *      Author: bhagy
 */

#ifndef INC_UTILITIES_H_
#define INC_UTILITIES_H_


typedef enum mode_set
{ IDLE,   //Put the H-bridge in brake mode
  PWM,    //In this mode, set the user defined duty cycle (-100 <= pwm <= 100)
  ITEST  //Perform the PI Current Control test using reference current
}mode;


void set_mode(mode m);
mode get_mode();

#endif /* INC_UTILITIES_H_ */
