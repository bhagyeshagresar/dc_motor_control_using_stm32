/*
 * utilties.c
 *
 *  Created on: May 18, 2025
 *      Author: bhagy
 */

#include "utilities.h"

volatile mode _mode;
int pwm = 0;

mode get_mode(){
	return _mode;
}

void set_mode(mode m){
	_mode = m;
}


