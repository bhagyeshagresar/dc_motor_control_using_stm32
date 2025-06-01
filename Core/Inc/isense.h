/*
 * isense.h
 *
 *  Created on: May 10, 2025
 *      Author: bhagy
 */

#ifndef INC_ISENSE_H_
#define INC_ISENSE_H_

extern volatile int adc_cnts;
extern volatile int current_amp;

int read_adc_counts();
int read_current_amps();



#endif /* INC_ISENSE_H_ */
