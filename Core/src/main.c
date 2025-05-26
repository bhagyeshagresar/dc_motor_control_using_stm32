#include "main.h"
#include <string.h>

TIM_HandleTypeDef TIM2_Handler;
#define TIMER_CLOCK_FREQ 84000000UL  // 84 MHz timer clock

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
}

void TIMER2_Init(void)
{
    TIM_OC_InitTypeDef TIM2_PWM_Init = {0};

    __HAL_RCC_TIM2_CLK_ENABLE();

    TIM2_Handler.Instance = TIM2;
    TIM2_Handler.Init.Prescaler = 84 - 1;       // 1 MHz
    TIM2_Handler.Init.Period = 1000 - 1;        // 1 kHz PWM
    TIM2_Handler.Init.CounterMode = TIM_COUNTERMODE_UP;
    TIM2_Handler.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;

    if (HAL_TIM_PWM_Init(&TIM2_Handler) != HAL_OK)
        Error_Handler();

    TIM2_PWM_Init.OCMode = TIM_OCMODE_PWM1;
    TIM2_PWM_Init.OCPolarity = TIM_OCPOLARITY_HIGH;
    TIM2_PWM_Init.Pulse = 500;  // 50% duty

    if (HAL_TIM_PWM_ConfigChannel(&TIM2_Handler, &TIM2_PWM_Init, TIM_CHANNEL_1) != HAL_OK)
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

int Set_PWM_Frequency(TIM_HandleTypeDef *htim, uint32_t freq)
{
    if (freq == 0) return -1;  // invalid frequency

    // Enable TIM2 clock
    if (htim->Instance == TIM2)
        __HAL_RCC_TIM2_CLK_ENABLE();

    uint32_t prescaler = 0;
    uint32_t period = 0;

    prescaler = (TIMER_CLOCK_FREQ / (freq * 65536)) + 1;
    if (prescaler > 0xFFFF) return -2; 

    period = (TIMER_CLOCK_FREQ / (freq * (prescaler + 1))) - 1;
    if (period > 0xFFFF) return -3;

    htim->Init.Prescaler = prescaler;
    htim->Init.Period = period;
    htim->Init.CounterMode = TIM_COUNTERMODE_UP;
    htim->Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;

    if (HAL_TIM_PWM_Init(htim) != HAL_OK)
        return -4;

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


int main(void)
{
    HAL_Init();
    SystemClock_Config();
    GIOP_LED_Init();

    TIM2_Handler.Instance = TIM2;
    TIM2_Handler.Init.CounterMode = TIM_COUNTERMODE_UP;
    TIM2_Handler.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;

    // frequency
    if (Set_PWM_Frequency(&TIM2_Handler, 5) != 0)
        Error_Handler();

    // PWM channel
    TIM_OC_InitTypeDef sConfigOC = {0};
    sConfigOC.OCMode = TIM_OCMODE_PWM1;
    sConfigOC.Pulse = (TIM2_Handler.Init.Period + 1) / 2;  // 50% duty cycle
    sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;
    sConfigOC.OCFastMode = TIM_OCFAST_DISABLE;

    if (HAL_TIM_PWM_ConfigChannel(&TIM2_Handler, &sConfigOC, TIM_CHANNEL_1) != HAL_OK)
        Error_Handler();

    if (HAL_TIM_PWM_Start(&TIM2_Handler, TIM_CHANNEL_1) != HAL_OK)
        Error_Handler();

    Set_PWM_DutyCycle(&TIM2_Handler, 75);  // 75% duty cycle

    while (1)
    {
        // PWM runs automatically
    }
}


void Error_Handler(void)
{
    while(1);
}
