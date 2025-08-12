/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2025 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include <string.h>
#include <stdio.h>
/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "encoder.h"
#include "utilities.h"
#include "current.h"
#include "ina219.h"
#include "main.h"
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */
#define MSG_SIZE 100
#define EINTMAX 1000
/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
I2C_HandleTypeDef hi2c1;

TIM_HandleTypeDef htim2;
TIM_HandleTypeDef htim3;
TIM_HandleTypeDef htim4;

UART_HandleTypeDef huart2;

/* USER CODE BEGIN PV */
volatile uint8_t pwm_rx_bytes[4];
uint8_t rx_bytes[100];
volatile int result;
char tx_bytes[100];
char itest_message[100];
volatile int encoder_cnts = 0;
volatile int encoder_cnts_deg = 0;
volatile int current_adc_cnts = 0;
volatile int current_mA = 0;
volatile float required_current[100];
volatile float actual_current[100];
uint8_t buff_size = 0;
/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_USART2_UART_Init(void);
static void MX_TIM3_Init(void);
static void MX_I2C1_Init(void);
static void MX_TIM4_Init(void);
static void MX_TIM2_Init(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{

  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */
  HAL_StatusTypeDef ret;
  char status_buff[MSG_SIZE];
  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_USART2_UART_Init();
  MX_TIM3_Init();
  MX_I2C1_Init();
  MX_TIM4_Init();
  MX_TIM2_Init();
  /* USER CODE BEGIN 2 */
  HAL_TIM_Base_Start_IT(&htim2);
  HAL_TIM_Base_Start_IT(&htim4);
  current_sensor_init(status_buff, &hi2c1);
  set_mode(IDLE); //Set mode to IDLE initially
  //test
  //char buffer[2];
  //ret = HAL_I2C_Mem_Read(&hi2c1, INA219_ADDR, INA219_CONFIG_REG, I2C_MEMADD_SIZE_8BIT, buffer, 2, 100);


  if (strcmp(status_buff, "") == 0) {
      strcpy(status_buff, "Successfully configured the current sensor\n");
  }

  //strcpy(status_buff, "Test!!!\n");
  buff_size = strlen(status_buff);
  ret = HAL_UART_Transmit(&huart2, status_buff, buff_size, HAL_MAX_DELAY);

  if(ret != HAL_OK){
  	 //this need to be handled using an LED or something
  }

  HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_3);
  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {

	ret = HAL_UART_Receive(&huart2, rx_bytes, 2, HAL_MAX_DELAY);

	if(ret == HAL_OK){
		 strcpy(status_buff, "received 2 bytes of data\r\n");
	  }
	else{
		strcpy(status_buff, "problem with receiving data\r\n");
	  }

	  switch(rx_bytes[0]){


		 case 'a':
			 //send encoder counts
			 encoder_cnts = read_encoder_counts();
			 sprintf(tx_bytes, "ENC:%d\n", encoder_cnts);
			 buff_size = strlen(tx_bytes);
			 ret = HAL_UART_Transmit(&huart2, (uint8_t*)tx_bytes, buff_size, HAL_MAX_DELAY);

			 if(ret == HAL_OK){
			 	strcpy(status_buff, "sent bytes of data\r\n");
			 	}
			else{
				strcpy(status_buff, "problem with sending data\r\n");
			  }
			 break;

		 case 'b':
			 //send encoder counts in degrees
			 encoder_cnts_deg = read_encoder_degrees();
			 sprintf(tx_bytes, "ENC_DEG:%d\n", encoder_cnts_deg);
			 buff_size = strlen(tx_bytes);
			 ret = HAL_UART_Transmit(&huart2, (uint8_t*)tx_bytes, buff_size, HAL_MAX_DELAY);

			 if(ret == HAL_OK){
				strcpy(status_buff, "sent bytes of data\r\n");
				}
			else{
				strcpy(status_buff, "problem with sending data\r\n");
			  }
			 break;

		 case 'c':
			 //reset encoder
			 reset_encoder_position();
			 sprintf(tx_bytes, "RESET_ENC_CNTS:%d\n", encoder_cnts);
			 buff_size = strlen(tx_bytes);
			 ret = HAL_UART_Transmit(&huart2, (uint8_t*)tx_bytes, buff_size, HAL_MAX_DELAY);

			 if(ret == HAL_OK){
				strcpy(status_buff, "sent bytes of data\r\n");
				}
			else{
				strcpy(status_buff, "problem with sending data\r\n");
			  }
			 break;

		 case 'd':
			 //send adc counts
			 current_adc_cnts = read_adc_counts(&hi2c1);
			 sprintf(tx_bytes, "ADC_CNTS:%d\n", current_adc_cnts);
			 buff_size = strlen(tx_bytes);
			 ret = HAL_UART_Transmit(&huart2, (uint8_t*)tx_bytes, buff_size, HAL_MAX_DELAY);

			 if(ret == HAL_OK){
				strcpy(status_buff, "sent bytes of data\r\n");
				}
			else{
				strcpy(status_buff, "problem with sending data\r\n");
			  }
			 break;

		 case 'e':
			 //read current in amps
			 current_mA = read_current_amps(&hi2c1);
			 sprintf(tx_bytes, "CURR_mA:%d\n", current_mA);
			 buff_size = strlen(tx_bytes);
			 ret = HAL_UART_Transmit(&huart2, (uint8_t*)tx_bytes, buff_size, HAL_MAX_DELAY);

			 if(ret == HAL_OK){
				strcpy(status_buff, "sent bytes of data\r\n");
				}
			else{
				strcpy(status_buff, "problem with sending data\r\n");
			  }
			 break;

		 case 'f':

			 //send response to the GUI
			 sprintf(tx_bytes, "PWM_REQ:\n");
			 buff_size = strlen(tx_bytes);
			 ret = HAL_UART_Transmit(&huart2, (uint8_t*)tx_bytes, buff_size, HAL_MAX_DELAY);

			 //read the duty cycle from the GUI
			 ret = HAL_UART_Receive(&huart2, pwm_rx_bytes, 4, HAL_MAX_DELAY);

			 //pwm mode
			 set_mode(PWM);

			 if(ret == HAL_OK){
				strcpy(status_buff, "sent bytes of data\r\n");
			}
			else{
				strcpy(status_buff, "problem with sending data\r\n");
			  }
			 break;

		 case 'p':
			 //stop the motor
			 set_mode(IDLE);
			 break;

		 case 'k':
			 //set the mode to current test
			 set_mode(ITEST);
			 while(get_mode() == ITEST){
				 ;
			 }

			 //ITEST mode is done, let's print
			sprintf(tx_bytes, "ITEST_DATA_START:\n");
			buff_size = strlen(tx_bytes);
			ret = HAL_UART_Transmit(&huart2, (uint8_t*)tx_bytes, buff_size, HAL_MAX_DELAY);

			for(int i = 0;i < 100; i++){
				sprintf(itest_message, "%f %f\r\n", required_current[i], actual_current[i]);
				HAL_UART_Transmit(&huart2, (uint8_t*)itest_message, strlen(itest_message), HAL_MAX_DELAY);
			}
			sprintf(tx_bytes, "ITEST_DATA_COMPLETE:\n");
			buff_size = strlen(tx_bytes);
		    ret = HAL_UART_Transmit(&huart2, (uint8_t*)tx_bytes, buff_size, HAL_MAX_DELAY);



		    break;

		 case 'g':
			//set the current gains by reading kp and ki over serial and update the current control kp and ki

			//Send response to the GUI
			sprintf(tx_bytes, "CURR_Kp_Ki:\n");
			buff_size = strlen(tx_bytes);
			HAL_UART_Transmit(&huart2, (uint8_t*)tx_bytes, buff_size, HAL_MAX_DELAY);

		    //read the Kp and Ki from GUI
			ret = HAL_UART_Receive(&huart2, rx_bytes, 8, HAL_MAX_DELAY);

			 if (ret == HAL_OK)
			{
				// Data was received successfully.
				// Update the global kp_current and ki_current variables.
				// The memcpy function is correct for this.
				memcpy(&kp_current, &rx_bytes[0], 4);
				memcpy(&ki_current, &rx_bytes[4], 4);

				// Optional: Send a confirmation message back to the GUI
				sprintf(status_buff, "Gains updated to Kp:%.2f, Ki:%.2f\r\n", kp_current, ki_current);
				HAL_UART_Transmit(&huart2, (uint8_t*)status_buff, strlen(status_buff), HAL_MAX_DELAY);
			}
			else
			{
				// There was a problem reading the data
				sprintf(status_buff, "Problem with reading data\r\n");
				HAL_UART_Transmit(&huart2, (uint8_t*)status_buff, strlen(status_buff), HAL_MAX_DELAY);
			}

		   break;

		 case 'h':
			 //get current gains
			 //TODO: also add a button for get current gains in GUI

		   break;


	  }
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Configure the main internal regulator output voltage
  */
  __HAL_RCC_PWR_CLK_ENABLE();
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE2);

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSI;
  RCC_OscInitStruct.PLL.PLLM = 16;
  RCC_OscInitStruct.PLL.PLLN = 336;
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV4;
  RCC_OscInitStruct.PLL.PLLQ = 7;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_2) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief I2C1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_I2C1_Init(void)
{

  /* USER CODE BEGIN I2C1_Init 0 */

  /* USER CODE END I2C1_Init 0 */

  /* USER CODE BEGIN I2C1_Init 1 */

  /* USER CODE END I2C1_Init 1 */
  hi2c1.Instance = I2C1;
  hi2c1.Init.ClockSpeed = 100000;
  hi2c1.Init.DutyCycle = I2C_DUTYCYCLE_2;
  hi2c1.Init.OwnAddress1 = 0;
  hi2c1.Init.AddressingMode = I2C_ADDRESSINGMODE_7BIT;
  hi2c1.Init.DualAddressMode = I2C_DUALADDRESS_DISABLE;
  hi2c1.Init.OwnAddress2 = 0;
  hi2c1.Init.GeneralCallMode = I2C_GENERALCALL_DISABLE;
  hi2c1.Init.NoStretchMode = I2C_NOSTRETCH_DISABLE;
  if (HAL_I2C_Init(&hi2c1) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN I2C1_Init 2 */

  /* USER CODE END I2C1_Init 2 */

}

/**
  * @brief TIM2 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM2_Init(void)
{

  /* USER CODE BEGIN TIM2_Init 0 */

  /* USER CODE END TIM2_Init 0 */

  TIM_ClockConfigTypeDef sClockSourceConfig = {0};
  TIM_MasterConfigTypeDef sMasterConfig = {0};

  /* USER CODE BEGIN TIM2_Init 1 */

  /* USER CODE END TIM2_Init 1 */
  htim2.Instance = TIM2;
  htim2.Init.Prescaler = 84-1;
  htim2.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim2.Init.Period = 200-1;
  htim2.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim2.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
  if (HAL_TIM_Base_Init(&htim2) != HAL_OK)
  {
    Error_Handler();
  }
  sClockSourceConfig.ClockSource = TIM_CLOCKSOURCE_INTERNAL;
  if (HAL_TIM_ConfigClockSource(&htim2, &sClockSourceConfig) != HAL_OK)
  {
    Error_Handler();
  }
  sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;
  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
  if (HAL_TIMEx_MasterConfigSynchronization(&htim2, &sMasterConfig) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN TIM2_Init 2 */

  /* USER CODE END TIM2_Init 2 */

}

/**
  * @brief TIM3 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM3_Init(void)
{

  /* USER CODE BEGIN TIM3_Init 0 */

  /* USER CODE END TIM3_Init 0 */

  TIM_MasterConfigTypeDef sMasterConfig = {0};
  TIM_OC_InitTypeDef sConfigOC = {0};

  /* USER CODE BEGIN TIM3_Init 1 */

  /* USER CODE END TIM3_Init 1 */
  htim3.Instance = TIM3;
  htim3.Init.Prescaler = 84-1;
  htim3.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim3.Init.Period = 100-1;
  htim3.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim3.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
  if (HAL_TIM_PWM_Init(&htim3) != HAL_OK)
  {
    Error_Handler();
  }
  sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;
  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
  if (HAL_TIMEx_MasterConfigSynchronization(&htim3, &sMasterConfig) != HAL_OK)
  {
    Error_Handler();
  }
  sConfigOC.OCMode = TIM_OCMODE_PWM1;
  sConfigOC.Pulse = 0;
  sConfigOC.OCPolarity = TIM_OCPOLARITY_HIGH;
  sConfigOC.OCFastMode = TIM_OCFAST_DISABLE;
  if (HAL_TIM_PWM_ConfigChannel(&htim3, &sConfigOC, TIM_CHANNEL_3) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN TIM3_Init 2 */

  /* USER CODE END TIM3_Init 2 */
  HAL_TIM_MspPostInit(&htim3);

}

/**
  * @brief TIM4 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM4_Init(void)
{

  /* USER CODE BEGIN TIM4_Init 0 */

  /* USER CODE END TIM4_Init 0 */

  TIM_ClockConfigTypeDef sClockSourceConfig = {0};
  TIM_MasterConfigTypeDef sMasterConfig = {0};

  /* USER CODE BEGIN TIM4_Init 1 */

  /* USER CODE END TIM4_Init 1 */
  htim4.Instance = TIM4;
  htim4.Init.Prescaler = 8400-1;
  htim4.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim4.Init.Period = 100-1;
  htim4.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim4.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
  if (HAL_TIM_Base_Init(&htim4) != HAL_OK)
  {
    Error_Handler();
  }
  sClockSourceConfig.ClockSource = TIM_CLOCKSOURCE_INTERNAL;
  if (HAL_TIM_ConfigClockSource(&htim4, &sClockSourceConfig) != HAL_OK)
  {
    Error_Handler();
  }
  sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;
  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
  if (HAL_TIMEx_MasterConfigSynchronization(&htim4, &sMasterConfig) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN TIM4_Init 2 */

  /* USER CODE END TIM4_Init 2 */

}

/**
  * @brief USART2 Initialization Function
  * @param None
  * @retval None
  */
static void MX_USART2_UART_Init(void)
{

  /* USER CODE BEGIN USART2_Init 0 */

  /* USER CODE END USART2_Init 0 */

  /* USER CODE BEGIN USART2_Init 1 */

  /* USER CODE END USART2_Init 1 */
  huart2.Instance = USART2;
  huart2.Init.BaudRate = 115200;
  huart2.Init.WordLength = UART_WORDLENGTH_8B;
  huart2.Init.StopBits = UART_STOPBITS_1;
  huart2.Init.Parity = UART_PARITY_NONE;
  huart2.Init.Mode = UART_MODE_TX_RX;
  huart2.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart2.Init.OverSampling = UART_OVERSAMPLING_16;
  if (HAL_UART_Init(&huart2) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN USART2_Init 2 */

  /* USER CODE END USART2_Init 2 */

}

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */
static void MX_GPIO_Init(void)
{
  GPIO_InitTypeDef GPIO_InitStruct = {0};
  /* USER CODE BEGIN MX_GPIO_Init_1 */
  /* USER CODE END MX_GPIO_Init_1 */

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOC_CLK_ENABLE();
  __HAL_RCC_GPIOH_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOA, LD2_Pin|GPIO_PIN_8, GPIO_PIN_RESET);

  /*Configure GPIO pin : B1_Pin */
  GPIO_InitStruct.Pin = B1_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_IT_FALLING;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(B1_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pins : LD2_Pin PA8 */
  GPIO_InitStruct.Pin = LD2_Pin|GPIO_PIN_8;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

  /*Configure GPIO pin : PC7 */
  GPIO_InitStruct.Pin = GPIO_PIN_7;
  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);

  /*Configure GPIO pin : PA9 */
  GPIO_InitStruct.Pin = GPIO_PIN_9;
  GPIO_InitStruct.Mode = GPIO_MODE_IT_RISING_FALLING;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

  /* EXTI interrupt init*/
  HAL_NVIC_SetPriority(EXTI9_5_IRQn, 0, 0);
  HAL_NVIC_EnableIRQ(EXTI9_5_IRQn);

  /* USER CODE BEGIN MX_GPIO_Init_2 */
  /* USER CODE END MX_GPIO_Init_2 */
}

/* USER CODE BEGIN 4 */
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)
{
  if(GPIO_Pin == GPIO_PIN_9){
	  GPIO_PinState state1 = HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_9);
	  GPIO_PinState state2 = HAL_GPIO_ReadPin(GPIOC, GPIO_PIN_7);
	  if(state1 != state2){
		  motorPosition++;
	  }
	  else{
		  motorPosition--;
	  }

  }
}



void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim)
{

	//this is for calculating motor speed
    if (htim->Instance == TIM4)
    {
    	motorVelocity = ((motorPosition - oldMotorPosition)*ENCODER_VEL_SAMPLE_FREQ);
    	oldMotorPosition = motorPosition;
    }

    //TODO: Handle state machine in here for pwm mode, ITEST mode, etc.
    //TODO: add arrays for plotting reference vs controlled current
    if (htim->Instance == TIM2)
   {
    	static int counter = 0;
    	static float desired_current = 100.0;
    	static float eint = 0;
    	static float e = 0;
    	static float eprev = 0;

    	switch(get_mode()){

    	   case PWM:
    		   //Set the new duty cycle
    		   //Read data coming from the serial - rx_bytes = MSB-> 0x04 0x03 0x02 0x01 <- LSB assume this is the order for now
			   result = (pwm_rx_bytes[3] << 24) | (pwm_rx_bytes[2] << 16) | (pwm_rx_bytes[1] << 8) | (pwm_rx_bytes[0]);


			   if(result > 0){

				   if(result > 100){
					   result = 100;
				   }
				   // Sets PA8 high
				   GPIOA->BSRR = (1 << 8);
				   htim3.Instance->CCR3 = result;
			   }
			   else{

				   if(result < -100){
					   result = -100;
				   }

				   // Sets PA8 to low
				   GPIOA->BSRR = (1 << (8 + 16));
				   htim3.Instance->CCR3 = -result;
			   }

    		   break;

			case ITEST:

				//increment the counter everytime the ISR is fired
				counter++;
				if (counter == 25)
				{
					desired_current = -100.0;
				}

				if(counter == 50)
				{
					desired_current = 100.0;
				}

				if(counter == 75)
				{
					desired_current = -100.0;
				}

				if(counter == 100){
					counter = 0;
					desired_current = 100.0;
					eint = 0;
					set_mode(IDLE);
				}

				int measured_current = read_current_amps(&hi2c1); //read the actual current
				e = desired_current - (float)measured_current; //compute the error
				eint = eint + e; //add the error

				//make sure there is no integrator windup
				if(eint > EINTMAX){
					eint = EINTMAX;
				}

				if (eint < -EINTMAX)
				{
					eint = -EINTMAX;
				}

				//calculate the controlled output
				float u = (kp_current*e) + (ki_current*eint);

				//cap the duty cycle between -100 and 100
				if(u > 100){
					u = 100;
				}
				else if(u < -100){
					u = -100;
				}

				if (u >= 0) {
				    GPIOA->BSRR = (1 << 8); // DIR = HIGH
				    htim3.Instance->CCR3 = (uint32_t)u;
				} else {
				    GPIOA->BSRR = (1 << (8 + 16)); // DIR = LOW
				    htim3.Instance->CCR3 = (uint32_t)-u;
				}

				required_current[counter] = desired_current;
				actual_current[counter] = measured_current;

				break;

			case IDLE:
				htim3.Instance->CCR3 = 0; //zero out the duty cycle

				break;

			}

   }

}


/*
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
    if (huart->Instance == USART2)
    {
    	result = (pwm_rx_bytes[3] << 24) | (pwm_rx_bytes[2] << 16) | (pwm_rx_bytes[1] << 8) | (pwm_rx_bytes[0]);
    	htim3.Instance->CCR3 = result;
    }
    //This callback is triggered everytime 4 bytes are received so it is necessary to call the below function to start receiving bytes again
    HAL_UART_Receive_IT(&huart2, pwm_rx_bytes, 4);  // Start interrupt-based reception

}
*/
/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
