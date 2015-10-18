#ifndef SENSOR_MOTE_H
#define SENSOR_MOTE_H

typedef nx_struct SensorMoteMsg {
	nx_uint16_t nodeId;
	nx_uint16_t lightValue;

} SensorMoteMsg_t;


enum {
  AM_SENSORMOTEMSG = 141,
  TIMER_PERIOD_MILLI = 8,
  ARVG_SIZE = 50
};

#endif /* SENSOR_MOTE_H */
