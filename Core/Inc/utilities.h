/*
 * utilities.h
 *
 *  Created on: May 10, 2025
 *      Author: bhagy
 */

#ifndef INC_UTILITIES_H_
#define INC_UTILITIES_H_


enum mode
{ IDLE,
  PWM,
  ITEST,
  HOLD,
  TRACK
};



void set_mode(enum mode);
enum mode get_mode();







#endif /* INC_UTILITIES_H_ */
