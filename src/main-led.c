#include "main.h"

volatile int user_delay = 100;

void UART2_Init(void)
{
    // Enable GPIOA and USART2 clocks
    RCC->AHB1ENR |= RCC_AHB1ENR_GPIOAEN;
    RCC->APB1ENR |= RCC_APB1ENR_USART2EN;

    // Set PA2 as alternate function for USART2_TX, PA3 for RX
    GPIOA->MODER &= ~(0xF << 2*2);          // Clear mode for PA2, PA3
    GPIOA->MODER |=  (0xA << 2*2);          // Alternate function mode

    GPIOA->AFR[0] &= ~((0xF << 8) | (0xF << 12)); // Clear bits first
    GPIOA->AFR[0] |= (7 << 8) | (7 << 12);  // AF7 for USART2 on PA2 and PA3

    // Configure USART2: 9600 baud, 8N1
    USART2->BRR = 0x0683; // For 16MHz and 9600 baud (see RM)
    USART2->CR1 |= USART_CR1_RE | USART_CR1_RXNEIE; // Enable receiver + interrupt
    USART2->CR1 |= USART_CR1_UE; // Enable USART

    // Enable USART2 IRQ in NVIC
    NVIC_EnableIRQ(USART2_IRQn);
    NVIC_SetPriority(USART2_IRQn, 1);
}

void USART2_IRQHandler(void)
{
    if (USART2->SR & USART_SR_RXNE)
    {
        char ch = USART2->DR; // Read received byte

        // Expecting digits '1' to '9' -> 100ms to 900ms
        if (ch >= '1' && ch <= '9') {
            user_delay = (ch - '0') * 100;
        }
    }
}


int main(void)
{
    // Init UART
    UART2_Init();

    // Enable GPIOA clock (PA5 is connected to AHB1)
    RCC->AHB1ENR |= RCC_AHB1ENR_GPIOAEN;

    // Configure PA5 as output
    GPIOA->MODER &= ~(0x3 << (5 * 2)); // LED is connected to PA5
    GPIOA->MODER |=  (0x1 << (5 * 2));

    while (1)
    {
        GPIOA->ODR |= (1 << 5);  // LED ON
        delayMs(user_delay);
        GPIOA->ODR &= ~(1 << 5); // LED OFF
        delayMs(user_delay);
    }
}
/*---------------------------------------------------------------------------------*/
