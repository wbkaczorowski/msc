from server import RPiServer
import ConfigParser


def main():
    config = ConfigParser.RawConfigParser()
    config.read('config.cfg')

    rpi_server = RPiServer(config.getint('communication', 'port'), config.get('meta', 'name'),
                           config.getint('communication', 'broadcast_frequency'),
                           config.getint('communication', 'broadcast_port'), config.get('sensor', 'sensor_port'),
                           config.getint('sensor', 'sensor_baudrate'),
                           config.get('database', 'db_file'))
    rpi_server.run()


if __name__ == "__main__":
    main()