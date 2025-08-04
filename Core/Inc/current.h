/*
 * currentcontrol.h
 *
 *  Created on: May 10, 2025
 *      Author: bhagy
 */

#ifndef INC_CURRENT_H_
#define INC_CURRENT_H_


extern volatile float kp_current;
extern volatile float ki_current;


void set_current_gains(float kp, float ki);
float get_current_kp();
float get_current_ki();



#endif /* INC_CURRENT_H_ */
