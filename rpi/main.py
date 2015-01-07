from server import RPiServer
import ConfigParser


def main():
    config = ConfigParser.RawConfigParser()
    config.read('rpiserver.cfg')

    rpi_server = RPiServer(config.getint('communication', 'port'))
    rpi_server.run()


if __name__ == "__main__":
    main()