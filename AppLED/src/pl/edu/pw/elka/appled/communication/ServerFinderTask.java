package pl.edu.pw.elka.appled.communication;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.util.LinkedHashMap;
import java.util.Map;

import pl.edu.pw.elka.appled.Config;
import pl.edu.pw.elka.appled.fragments.DeviceRowAdapter;
import android.content.Context;
import android.net.wifi.WifiManager;
import android.net.wifi.WifiManager.MulticastLock;
import android.os.AsyncTask;
import android.util.Log;

public class ServerFinderTask extends AsyncTask<Void, Void, Map<String, String>> {

    public static final String TAG = "ServerFinder";

    private Context context;
    private DeviceRowAdapter adapter;

    public ServerFinderTask(Context context, DeviceRowAdapter adapter) {
        this.context = context;
        this.adapter = adapter;
    }


    @Override
    protected Map<String, String> doInBackground(Void... params) {
        DatagramSocket socket = null;
        MulticastLock multicastLock = getMulticastLock();
        Map<String, String> foundDevices = new LinkedHashMap<>();
        try {
            long startTime = System.currentTimeMillis();
            multicastLock.acquire();
            socket = new DatagramSocket(Config.BROADCAST_PORT);
            socket.setBroadcast(true);
            while ((System.currentTimeMillis() - startTime) <= Config.SCAN_TIME) {
                byte[] buf = new byte[256];
                DatagramPacket receivePacket = new DatagramPacket(buf, buf.length);
                socket.receive(receivePacket);
                foundDevices.put(receivePacket.getAddress().getHostAddress(), new String(buf, 0, receivePacket.getLength()));
                // Log.d(TAG, receivePacket.getAddress().getHostAddress() + " " + new String(buf, 0, receivePacket.getLength()));
            }
        } catch (IOException e) {
            Log.w(TAG, e.getMessage());
        } finally {
            if (socket != null && !socket.isClosed()) {
                socket.close();
            }
            multicastLock.release();
        }

        return foundDevices;
    }
    
    

    @Override
    protected void onProgressUpdate(Void... values) {
        super.onProgressUpdate(values);
    }


    @Override
    protected void onPostExecute(Map<String, String> result) {
        super.onPostExecute(result);
        adapter.setData((LinkedHashMap<String, String>) result);
        adapter.notifyDataSetChanged();
//        Log.d(TAG, result.toString());
    }

    public MulticastLock getMulticastLock() {
        WifiManager wifiManager = (WifiManager) context.getSystemService(Context.WIFI_SERVICE);
        MulticastLock multicastLock = wifiManager.createMulticastLock(TAG);
        return multicastLock;
    }

}
