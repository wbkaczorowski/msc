#include <Timer.h>
#include <stdio.h>
//#include <string.h>
#include "SensorMote.h"
//#include "printf.h"

module SensorMoteC {

	uses {

		// general
		interface Boot;
		interface Timer<TMilli>;
		interface Leds;

		// read light value
		interface Read<uint16_t> as LightRead;

		// radio communication
		interface Packet;
		interface AMPacket;
		interface AMSend;
		interface SplitControl as AMControl;
		interface Receive;
	}
}

implementation {

	uint16_t lightValue;
	bool radioBusy = FALSE;
	message_t pkt;
	error_t sendError;

	event void Boot.booted() {
		call AMControl.start();
	}

	event void Timer.fired() {
		if(call LightRead.read() != SUCCESS) {
			call Leds.led0Toggle();
		}
	}

	event void LightRead.readDone(error_t result, uint16_t val) {
		if(result == SUCCESS) {
			lightValue = 2.5 * (val / 4096.0) * 6250.0;
			printf("%d:%d\r\n", TOS_NODE_ID, lightValue);

			// creating the packet 
			if(radioBusy == FALSE) {
				SensorMoteMsg_t * msg = call Packet.getPayload(&pkt, sizeof(SensorMoteMsg_t));
				msg->lightValue = lightValue;
				msg->nodeId = TOS_NODE_ID;

				// sending packet
				sendError = call AMSend.send(AM_BROADCAST_ADDR, &pkt, sizeof(SensorMoteMsg_t));
				if(sendError == SUCCESS) {
					//call Leds.led2Toggle();
					radioBusy = TRUE;
				} else {
					printf("Error sending msg, code: %d", sendError);
					call Leds.led0Toggle();					
				}
				sendError = 0;
			}
		}
		else {
			printf("Error reading light sensor.\r\n");
			call Leds.led0Toggle();
		}
		printfflush();
	}

	event void AMSend.sendDone(message_t * msg, error_t error) {
		if(msg == &pkt) {
			radioBusy = FALSE;
		}
	}

	event void AMControl.startDone(error_t err) {
		if(err == SUCCESS) {
			call Timer.startPeriodic(TIMER_PERIOD_MILLI);
		}
		else {
			call AMControl.start();
		}
	}

	event void AMControl.stopDone(error_t error){
		
	}

	event message_t * Receive.receive(message_t *msg, void *payload, uint8_t len){
		if(len == sizeof(SensorMoteMsg_t)) { 
			SensorMoteMsg_t* incomingPacket = (SensorMoteMsg_t *) payload;
			printf("%d:%d\r\n", incomingPacket->nodeId, incomingPacket->lightValue);
			printfflush();
			call Leds.led1Toggle();
		}
		return msg;
	}
}
