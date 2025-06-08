# Project Name:
PROJECT = dc_motor_control_using_stm32

# Driver Directory structure:
DRIVER_DIR = Drivers
HAL_DIR = $(DRIVER_DIR)/STM32F4xx_HAL_Driver
HAL_INC_DIR = $(HAL_DIR)/Inc
CMSIS_DIR = $(DRIVER_DIR)/CMSIS
BSP_DIR = $(DRIVER_DIR)/BSP

# Project Directory structure:
SRC_DIR = src
INC_DIR = inc
BUILD_DIR = build
CONFIG_DIR = config

# Static library of drivers to be used:
LIB = $(BUILD_DIR)/libHAL_STATIC.a
LIB_NAME = HAL_STATIC

TOOLCHAIN=	arm-none-eabi
AR=		${TOOLCHAIN}-ar
AS=		${TOOLCHAIN}-as
CC=		${TOOLCHAIN}-gcc
LD=		${TOOLCHAIN}-ld
OBJCOPY=	${TOOLCHAIN}-objcopy
RANLIB=		${TOOLCHAIN}-ranlib
SIZE=		${TOOLCHAIN}-size

# Entire HAL source files folder:
HAL_SRCS = $(wildcard $(HAL_DIR)/Src/*.c)

# Driver source files:
SRCS =		$(CMSIS_DIR)/Device/ST/STM32F4xx/Source/Templates/gcc/startup_stm32f411xe.s
SRCS+=		$(CMSIS_DIR)/Device/ST/STM32F4xx/Source/Templates/system_stm32f4xx.c
SRCS+=		$(BSP_DIR)/stm32f4xx_nucleo.c

#Project source files:
SRCS+=		$(SRC_DIR)/main.c
SRCS+=		$(SRC_DIR)/stm32f4xx_it.c
SRCS+=		$(SRC_DIR)/stm32f4xx_hal_msp.c

# Object files:
OBJS=		${SRCS:.c=.o}
HAL_OBJS = ${HAL_SRCS:.c=.o} 

# Common compiler flags
CFLAGS_COMMON = -Wall
CFLAGS_COMMON += -T$(CONFIG_DIR)/stm32f411re.ld
CFLAGS_COMMON += -mcpu=cortex-m4
CFLAGS_COMMON += -mlittle-endian -mthumb -mthumb-interwork
CFLAGS_COMMON += -mfloat-abi=soft -mfpu=fpv4-sp-d16
CFLAGS_COMMON += -ffreestanding
CFLAGS_COMMON += --specs=nosys.specs

# Debug and release specific flags
DEBUG_FLAGS = -g -O0 -DDEBUG
RELEASE_FLAGS = -O2 -DNDEBUG

# Default to debug
CFLAGS = $(CFLAGS_COMMON) $(DEBUG_FLAGS)
CFLAGS_RELEASE = $(CFLAGS_COMMON) $(RELEASE_FLAGS)

# Preprocessor flags.
CPPFLAGS+=	-DSTM32F411xe
CPPFLAGS+=	-I $(HAL_INC_DIR)
CPPFLAGS+=	-I Drivers/BSP
CPPFLAGS+=	-I Drivers/CMSIS/Include
CPPFLAGS+=	-I Drivers/CMSIS/Device/ST/STM32F4xx/Include
CPPFLAGS+=	-I Drivers/STM32F4xx_HAL_Driver/Inc
CPPFLAGS+=	-I $(INC_DIR)
CPPFLAGS+=	-I../..

# Linker flags.
LDFLAGS+=	-L$(BUILD_DIR)
LDFLAGS+=	-l${LIB_NAME}

# Clean files:
CLEANFILES+=	$(BUILD_DIR)/${PROJECT}.elf $(BUILD_DIR)/${PROJECT}.hex $(BUILD_DIR)/${PROJECT}.bin $(SRC_DIR)/*.o

# HAL Library target:
$(LIB): ${HAL_OBJS}
	${AR} -rcs $@ $^
HAL_LIB: $(LIB)

# Object File target to compile hal source files:
$(HAL_DIR)/Src/%.o: $(HAL_DIR)/Src/%.c
	${CC} ${CFLAGS} ${CPPFLAGS} -c -o $@ $<

#Assembly Pattern Rule:
%.o: %.s
	${AS} -c -o $@ $<

# Function to build project with given flags
define build-project
	mkdir -p $(BUILD_DIR)
	${CC} $(1) ${CPPFLAGS} ${SRCS} ${LDFLAGS} -o $(BUILD_DIR)/${PROJECT}.elf
	${OBJCOPY} -O ihex   $(BUILD_DIR)/${PROJECT}.elf $(BUILD_DIR)/${PROJECT}.hex
	${OBJCOPY} -O binary $(BUILD_DIR)/${PROJECT}.elf $(BUILD_DIR)/${PROJECT}.bin
	${SIZE} $(BUILD_DIR)/${PROJECT}.elf
endef

# Project targets
project: ${SRCS}
	$(call build-project,${CFLAGS})

project-release: ${SRCS}
	$(call build-project,${CFLAGS_RELEASE})

# Program the STM32F4-Discovery board with st-flash(1) via USB.
flash: HAL_LIB project
	st-flash --reset write $(BUILD_DIR)/${PROJECT}.bin 0x08000000

flash-release: HAL_LIB project-release
	st-flash --reset write $(BUILD_DIR)/${PROJECT}.bin 0x08000000

hal-clean:
	rm -f ${HAL_OBJS} ${LIB}

clean:
	rm -f ${CLEANFILES}

cleanall: hal-clean clean

.PHONY: flash cleanlib clean cleanall
