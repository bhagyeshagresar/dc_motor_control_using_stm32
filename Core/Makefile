# Project Name:
PROJECT = led-toggle

# Driver Directory structure:
BASE_DIR = ..
DRIVER_DIR = $(BASE_DIR)/Drivers
HAL_DIR = $(DRIVER_DIR)/STM32F4xx_HAL_Driver
HAL_INC_DIR = $(HAL_DIR)/Inc
CMSIS_DIR = $(DRIVER_DIR)/CMSIS
BSP_DIR = $(DRIVER_DIR)/BSP

# Project Directory structure:
PROJ_DIR = $(BASE_DIR)/$(PROJECT)
SRC_DIR = $(PROJ_DIR)/src
INC_DIR = $(PROJ_DIR)/inc
BIN_DIR = $(PROJ_DIR)/bin
LINKER_DIR = $(PROJ_DIR)/linker
STRT_DIR = $(PROJ_DIR)/startup

# Static library of drivers to be used:
LIB = $(BIN_DIR)/libHAL_STATIC.a
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
SRCS =		$(CMSIS_DIR)/Device/ST/STM32F4xx/Source/Templates/gcc/startup_stm32f407xx.s
SRCS+=		$(CMSIS_DIR)/Device/ST/STM32F4xx/Source/Templates/system_stm32f4xx.c
SRCS+=		$(BSP_DIR)/STM32F4-Discovery/stm32f4_discovery.c

#Project source files:
SRCS+=		$(SRC_DIR)/main.c
SRCS+=		$(SRC_DIR)/stm32f4xx_it.c

# Object files:
OBJS=		${SRCS:.c=.o}
HAL_OBJS = ${HAL_SRCS:.c=.o} 

# Compiler flags.
CFLAGS=		-g -O2 -Wall
CFLAGS+=	-T$(LINKER_DIR)/stm32f407vg.ld
CFLAGS+=	-mcpu=cortex-m4
CFLAGS+=	-mlittle-endian -mthumb -mthumb-interwork
CFLAGS+=	-mfloat-abi=soft -mfpu=fpv4-sp-d16
CFLAGS+=	-ffreestanding
CFLAGS+=	--specs=nosys.specs

# Preprocessor flags.
CPPFLAGS+=	-DSTM32F407xx
CPPFLAGS+=	-I$(HAL_INC_DIR)
CPPFLAGS+=	-I$(BASE_DIR)/Drivers/BSP/STM32F4-Discovery
CPPFLAGS+=	-I$(BASE_DIR)/Drivers/CMSIS/Include
CPPFLAGS+=	-I$(BASE_DIR)/Drivers/CMSIS/Device/ST/STM32F4xx/Include
CPPFLAGS+=	-I$(BASE_DIR)/Drivers/STM32F4xx_HAL_Driver/Inc
CPPFLAGS+=	-I$(INC_DIR)
CPPFLAGS+=	-I../..

# Linker flags.
LDFLAGS+=	-L$(BIN_DIR)
LDFLAGS+=	-l${LIB_NAME}

# Clean files:
CLEANFILES+=	$(BIN_DIR)/${PROJECT}.elf $(BIN_DIR)/${PROJECT}.hex $(BIN_DIR)/${PROJECT}.bin $(SRC_DIR)/*.o

# Build HAL library and project:

all: HAL_LIB project

# HAL Library target:
HAL_LIB: $(LIB)

$(LIB): ${HAL_OBJS}
	${AR} -rcs $@ $^

# Object File target to compile hal source files:
$(HAL_DIR)/Src/%.o: $(HAL_DIR)/Src/%.c
	${CC} ${CFLAGS} ${CPPFLAGS} -c -o $@ $<

#Assembly Pattern Rule:
%.o: %.s
	${AS} -c -o $@ $<

# Project target:
project: ${BIN_DIR}/${PROJECT}.elf

$(BIN_DIR)/${PROJECT}.elf: ${SRCS}
	mkdir -p $(BIN_DIR)
	${CC} ${CFLAGS} ${CPPFLAGS} ${SRCS} ${LDFLAGS} -o $@
	${OBJCOPY} -O ihex   $(BIN_DIR)/${PROJECT}.elf $(BIN_DIR)/${PROJECT}.hex
	${OBJCOPY} -O binary $(BIN_DIR)/${PROJECT}.elf $(BIN_DIR)/${PROJECT}.bin
	${SIZE} $(BIN_DIR)/${PROJECT}.elf

# Program the STM32F4-Discovery board with st-flash(1) via USB.
flash: all
	st-flash --reset write $(BIN_DIR)/${PROJECT}.bin 0x08000000

hal-clean:
	rm -f ${HAL_OBJS} ${LIB}

clean:
	rm -f ${CLEANFILES}

cleanall: hal-clean clean

.PHONY: flash cleanlib clean cleanall
