#include "main.h"
#include <string.h>
#include <stdlib.h>  // for atoi()

#define TIMER_CLOCK_FREQ 84000000UL  // 84 MHz timer clock
TIM_HandleTypeDef TIM2_Handler;

volatile uint8_t frequency = 1000;
volatile uint8_t duty = 50;

volatile uint8_t duty_update_flag = 0;
volatile uint8_t freq_update_flag = 0;
volatile int new_duty_value = 0;
volatile int new_freq_value = 0;

volatile char uart_cmd_buffer[16];
volatile uint8_t uart_cmd_pos = 0;


int Set_PWM_Frequency(TIM_HandleTypeDef *htim, uint32_t freq)
{
    if (freq == 0) return -1;  // invalid frequency

    // Enable TIM2 clock
    if (htim->Instance == TIM2)
        __HAL_RCC_TIM2_CLK_ENABLE();

    uint32_t prescaler = 0;
    uint32_t period = 0;

    // Calculate prescaler and period for desired frequency:
    prescaler = (TIMER_CLOCK_FREQ / (freq * 65536)) + 1;
    if (prescaler > 0xFFFF) return -2; 

    period = (TIMER_CLOCK_FREQ / (freq * (prescaler + 1))) - 1;
    if (period > 0xFFFF) return -3;

    // Stop PWM before reconfiguring
    HAL_TIM_PWM_Stop(htim, TIM_CHANNEL_1);

    htim->Init.Prescaler = prescaler;
    htim->Init.Period = period;
    htim->Init.CounterMode = TIM_COUNTERMODE_UP;
    htim->Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;

    if (HAL_TIM_PWM_Init(htim) != HAL_OK)
        return -4;
        
    TIM_OC_InitTypeDef sConfigOC = {0};
    sConfigOC.OCMode = TIM_OCMODE_PWM1;
    sConfigOC.Pulse = (period + 1) / 2;  // Keep 50% or reuse old duty
    sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;
    sConfigOC.OCFastMode = TIM_OCFAST_DISABLE;

    if (HAL_TIM_PWM_ConfigChannel(htim, &sConfigOC, TIM_CHANNEL_1) != HAL_OK)
        return -5;
    
    // Restart PWM
    if (HAL_TIM_PWM_Start(htim, TIM_CHANNEL_1) != HAL_OK)
        return -6;

    __HAL_TIM_SET_COMPARE(htim, TIM_CHANNEL_1, (period + 1) / 2);

    return 0;
}

int Set_PWM_DutyCycle(TIM_HandleTypeDef *htim, uint8_t duty)
{
    if (duty > 100) return -1;

    uint32_t period = htim->Init.Period;
    uint32_t pulse = ((period + 1) * duty) / 100;

    __HAL_TIM_SET_COMPARE(htim, TIM_CHANNEL_1, pulse);

    return 0;
}

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
    USART2->BRR = (uint32_t)(HAL_RCC_GetPCLK1Freq() / 9600);  // works if PCLK1=42Mhz
    USART2->CR1 |= USART_CR1_RE | USART_CR1_RXNEIE; // Enable receiver + interrupt
    USART2->CR1 |= USART_CR1_UE; // Enable USART

    // Enable USART2 IRQ in NVIC
    NVIC_EnableIRQ(USART2_IRQn);
    NVIC_SetPriority(USART2_IRQn, 1);
}

void USART2_IRQHandler(void)
{
    HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);  // Onboard LED toggle on Nucleo
    if (USART2->SR & USART_SR_RXNE)
    {
        char ch = USART2->DR;

        // End of command
        if (ch == '\n' || uart_cmd_pos >= sizeof(uart_cmd_buffer) - 1) {
            uart_cmd_buffer[uart_cmd_pos] = '\0';  // Null terminate
            uart_cmd_pos = 0;

            // Check for D:xx pattern
            if (uart_cmd_buffer[0] == 'D' && uart_cmd_buffer[1] == ':') {
                int parsed_duty = atoi((char*)&uart_cmd_buffer[2]);
                if (parsed_duty >= 0 && parsed_duty <= 100) {
                    new_duty_value = parsed_duty;
                    duty_update_flag = 1;  // Set flag for main loop to handle
                }
            }
            // Check for F:xx pattern
            else if (uart_cmd_buffer[0] == 'F' && uart_cmd_buffer[1] == ':') {
                int parsed_freq = atoi((char*)&uart_cmd_buffer[2]);
                if (parsed_freq >= 100 && parsed_freq <= 10000) {
                    new_freq_value = parsed_freq;
                    freq_update_flag = 1;  // Set flag for main loop to handle
                }
            }
        } else {
            uart_cmd_buffer[uart_cmd_pos++] = ch;
        }
    }
}

// void USART2_IRQHandler(void)
// {
//     HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);  // Onboard LED toggle on Nucleo
//     if (USART2->SR & USART_SR_RXNE)
//     {
//         char ch = USART2->DR;

//         // End of command
//         if (ch == '\n' || uart_cmd_pos >= sizeof(uart_cmd_buffer) - 1) {
//             uart_cmd_buffer[uart_cmd_pos] = '\0';  // Null terminate
//             uart_cmd_pos = 0;

//             // Check for D:xx pattern
//             if (uart_cmd_buffer[0] == 'D' && uart_cmd_buffer[1] == ':') {
//                 int new_duty = atoi((char*)&uart_cmd_buffer[2]);
//                 if (new_duty >= 0 && new_duty <= 100) {
//                     duty = new_duty;  // UPDATE THE GLOBAL VARIABLE!
//                     Set_PWM_DutyCycle(&TIM2_Handler, duty);
//                 }
//             }
//             // Optional: Add frequency control
//             else if (uart_cmd_buffer[0] == 'F' && uart_cmd_buffer[1] == ':') {
//                 int new_freq = atoi((char*)&uart_cmd_buffer[2]);
//                 if (new_freq >= 100 && new_freq <= 10000) {
//                     frequency = new_freq;  // UPDATE THE GLOBAL VARIABLE!
//                     Set_PWM_Frequency(&TIM2_Handler, frequency);
//                     // Reapply duty cycle after frequency change
//                     Set_PWM_DutyCycle(&TIM2_Handler, duty);
//                 }
//             }
//         } else {
//             uart_cmd_buffer[uart_cmd_pos++] = ch;
//         }
//     }
// }

void GIOP_LED_Init(void)
{
    // Configure PA0 as TIM2_CH1 (AF1)
    GPIO_InitTypeDef GPIO_PWM;

    __HAL_RCC_GPIOA_CLK_ENABLE();

    GPIO_PWM.Pin = GPIO_PIN_0;
    GPIO_PWM.Mode = GPIO_MODE_AF_PP;
    GPIO_PWM.Pull = GPIO_NOPULL;
    GPIO_PWM.Speed = GPIO_SPEED_FREQ_LOW;
    GPIO_PWM.Alternate = GPIO_AF1_TIM2;  // TIM2_CH1 on PA0

    HAL_GPIO_Init(GPIOA, &GPIO_PWM);

    // Also initialize the onboard LED (PA5) for debugging
    GPIO_InitTypeDef GPIO_LED;
    GPIO_LED.Pin = GPIO_PIN_5;
    GPIO_LED.Mode = GPIO_MODE_OUTPUT_PP;
    GPIO_LED.Pull = GPIO_NOPULL;
    GPIO_LED.Speed = GPIO_SPEED_FREQ_LOW;
    HAL_GPIO_Init(GPIOA, &GPIO_LED);
}


void TIMER2_Init(void)
{
    // Enable TIM2 clock
    __HAL_RCC_TIM2_CLK_ENABLE();

    // Basic timer setup - frequency will be set later
    TIM2_Handler.Instance = TIM2;
    TIM2_Handler.Init.Prescaler = 84 - 1;       // 1 MHz timer clock
    TIM2_Handler.Init.Period = 1000 - 1;        // Default period (will be updated)
    TIM2_Handler.Init.CounterMode = TIM_COUNTERMODE_UP;
    TIM2_Handler.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;

    if (HAL_TIM_PWM_Init(&TIM2_Handler) != HAL_OK)
        Error_Handler();

    // Configure PWM channel
    TIM_OC_InitTypeDef TIM2_PWM_Init = {0};
    TIM2_PWM_Init.OCMode = TIM_OCMODE_PWM1;
    TIM2_PWM_Init.OCPolarity = TIM_OCPOLARITY_HIGH;
    TIM2_PWM_Init.OCFastMode = TIM_OCFAST_DISABLE;
    TIM2_PWM_Init.Pulse = 500;  // 50% duty (will be updated)

    if (HAL_TIM_PWM_ConfigChannel(&TIM2_Handler, &TIM2_PWM_Init, TIM_CHANNEL_1) != HAL_OK)
        Error_Handler();

    // Start PWM
    if (HAL_TIM_PWM_Start(&TIM2_Handler, TIM_CHANNEL_1) != HAL_OK)
        Error_Handler();
}

void SystemClock_Config(void)
{
    RCC_OscInitTypeDef RCC_OscInitStruct = {0};
    RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

    /** Use HSI (internal 16 MHz) and set PLL to 84 MHz SYSCLK */
    RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
    RCC_OscInitStruct.HSIState = RCC_HSI_ON;
    RCC_OscInitStruct.HSICalibrationValue = 16;
    RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
    RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSI;
    RCC_OscInitStruct.PLL.PLLM = 16;
    RCC_OscInitStruct.PLL.PLLN = 336;
    RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV4;  // 84 MHz
    RCC_OscInitStruct.PLL.PLLQ = 7;

    if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
        Error_Handler();

    RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK | RCC_CLOCKTYPE_SYSCLK
                                 | RCC_CLOCKTYPE_PCLK1 | RCC_CLOCKTYPE_PCLK2;
    RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
    RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
    RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
    RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

    if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_2) != HAL_OK)
        Error_Handler();
}

int main(void)
{
    HAL_Init();
    SystemClock_Config();
    GIOP_LED_Init();
    UART2_Init();
    TIMER2_Init();    

// Set desired frequency and duty cycle
    if (Set_PWM_Frequency(&TIM2_Handler, frequency) != 0)
        Error_Handler();
    
    Set_PWM_DutyCycle(&TIM2_Handler, duty);

    // Main loop
    while (1)
    {
        // Handle duty cycle updates
        if (duty_update_flag) {
            duty_update_flag = 0;
            duty = new_duty_value;
            Set_PWM_DutyCycle(&TIM2_Handler, duty);
        }
        
        // Handle frequency updates
        if (freq_update_flag) {
            freq_update_flag = 0;
            frequency = new_freq_value;
            Set_PWM_Frequency(&TIM2_Handler, frequency);
            // Reapply duty cycle after frequency change
            Set_PWM_DutyCycle(&TIM2_Handler, duty);
        }

        __WFI(); // Wait for interrupt - low power
    }
}


void Error_Handler(void)
{
       // Flash LED rapidly to indicate error
    while(1) {
        HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
        HAL_Delay(100);
    }
}
