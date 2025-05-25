// //PA5. LED is connected to PA5
// //AHB1. PA5 is connected to AHB1
// //RCC->AHB1ENR. To enable clock of ports on AHB1
// //GPIOx_MODER
// //GPIOx_ODR

// #include "stm32f4xx.h"                  // Device header

// void delayMs (int delay)
// {
// 	int i;
// 	for(;delay>0;delay--)
// 		for(i=0;i<3195;i++);
// }

// int main(void)
// {
// 	RCC->AHB1ENR |= 1;   						 //Clock enabled for GPIOA  0000 0000 0000 0000 0000 0000 0000 0001. | is for friendly programming
	
// 	GPIOA->MODER |= 0x400;  				 // 0000 0000 0000 0000 0000 0100 0000 0000
	
// 	while(1)
// 	{
// 		GPIOA->ODR = 0x20;						 // 0000 0000 0000 0000 0000 0000 0010 0000
// 		delayMs(100);
// 		GPIOA->ODR = 0x00;
// 		delayMs(100);
// 	}
// }

#include "stm32f4xx.h"  // CMSIS device header

void delayMs(int delay)
{
    for (; delay > 0; delay--)
        for (volatile int i = 0; i < 3195; i++);
}

int main(void)
{
    // Enable GPIOA clock (bit 0 of AHB1ENR)
    RCC->AHB1ENR |= (1 << 0);  // or just RCC->AHB1ENR |= 1;

    // Configure PA5 as general purpose output
    GPIOA->MODER &= ~(0x3 << (5 * 2));  // clear mode bits for pin 5
    GPIOA->MODER |=  (0x1 << (5 * 2));  // set mode to 01 (output)

    // Optional: Set output type (push-pull), speed, and no pull-up/down
    GPIOA->OTYPER &= ~(1 << 5);        // push-pull
    GPIOA->OSPEEDR |= (0x3 << (5 * 2)); // high speed
    GPIOA->PUPDR &= ~(0x3 << (5 * 2)); // no pull-up/pull-down

    while (1)
    {
        GPIOA->ODR |= (1 << 5);  // LED ON (set PA5)
        delayMs(100);
        GPIOA->ODR &= ~(1 << 5); // LED OFF (clear PA5)
        delayMs(100);
    }
}
