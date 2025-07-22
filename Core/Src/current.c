/*
 * current.c
 *
 *  Created on: Jul 21, 2025
 *      Author: bhagy
 */

#include "current.h"


volatile float kp_current = 0.05;
volatile float ki_current = 0.01;



void set_current_gains(float kp, float ki){
		kp_current = kp;
		ki_current = ki;

}


float get_current_kp(){
	return kp_current;
}

float get_current_ki(){
	return ki_current;
}
