//#define NEW_PRINTF_SEMANTICS
#include "printf.h"

configuration SensorMoteAppC {

}

implementation {

	// general components
	components SensorMoteC as App;
	components MainC, LedsC;
	components new TimerMilliC();
	
	// for writing into serial port
	  components SerialPrintfC;
//	components PrintfC;
//	components SerialStartC;


	App.Boot->MainC;
	App.Leds->LedsC;
	App.Timer->TimerMilliC;

	// light measuring
	components new HamamatsuS1087ParC() as LightSensor;

	App.LightRead->LightSensor;

	// radio communication
	components ActiveMessageC;
	components new AMSenderC(AM_SENSOR_MOTE);
	components new AMReceiverC(AM_SENSOR_MOTE);

	App.Packet->AMSenderC;
	App.AMPacket->AMSenderC;
	App.AMSend->AMSenderC;
	App.AMControl->ActiveMessageC;
	App.Receive->AMReceiverC;
}
