from server import RPiServer
import ConfigParser


def main():
    config = ConfigParser.RawConfigParser()
    config.read('config.cfg')

    rpi_server = RPiServer(config.getint('communication', 'port'), config.get('meta', 'name'), config.getint('communication', 'broadcast_frequency'), config.getint('communication', 'broadcast_port'))
    rpi_server.run()


if __name__ == "__main__":
    main()