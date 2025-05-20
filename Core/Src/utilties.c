/*
 * utilties.c
 *
 *  Created on: May 18, 2025
 *      Author: bhagy
 */

#include "utilities.h"

enum mode_set mode;
int pwm = 0;

enum mode_set get_mode(){
	return mode;
}

void set_mode(enum mode_set m){
	mode = m;
}


void set_pwm(int a){
	pwm = a;
}

int get_pwm(){
	return pwm;
}
