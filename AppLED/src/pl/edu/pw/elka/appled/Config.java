package pl.edu.pw.elka.appled;



/**
 * Class with some constans values.
 * @author Wojciech Kaczorowski
 *
 */
public class Config {
    
    /**
     * Port number for communication with controllers.
     */
    public static final int PORT = 9000;
    
    /**
     * Port number for discovering of controllers.
     */
    public static final int BROADCAST_PORT = 9001;
    
    /**
     * Ip address of controllers. TEMP
     * TODO usunuac
     */
//    public static final String RPI_IP = "192.168.1.14";

    /**
     * Time in ms for discovery of controllers.
     */
    public static long SCAN_TIME = 10000;
    
    


}
