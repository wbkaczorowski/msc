COMPONENT=SensorMoteAppC
CFLAGS += -I$(TINYOS_OS_DIR)/lib/printf
#CFLAGS += -DNEW_PRINTF_SEMANTICS
#TOSMAKE_PRE_EXE_DEPS += SensorMoteMsg.py SensorMoteMsg.class
#TOSMAKE_CLEAN_EXTRA += SensorMoteMsg.py SensorMoteMsg.class

#SensorMoteMsg.py:
#	mig python -target=$(PLATFORM) $(CFLAGS) -python-classname=SensorMoteMsg SensorMote.h SensorMoteMsg -o $@
	
#SensorMoteMsg.class: SensorMoteMsg.java
#	javac *.java
	
#SensorMoteMsg.java:
#	mig java -target=$(PLATFORM) $(CFLAGS) -java-classname=SensorMoteMsg SensorMote.h SensorMoteMsg -o $@


TINYOS_ROOT_DIR?=../..
include $(TINYOS_ROOT_DIR)/Makefile.include

