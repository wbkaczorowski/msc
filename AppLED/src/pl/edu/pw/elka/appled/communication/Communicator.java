package pl.edu.pw.elka.appled.communication;

import java.util.LinkedList;

import pl.edu.pw.elka.appled.Config;
import pl.edu.pw.elka.appled.fragments.DeviceRowAdapter;
import android.content.Context;
import android.os.AsyncTask;
import android.util.Log;
import android.widget.Toast;
import de.tavendo.autobahn.WebSocketConnection;
import de.tavendo.autobahn.WebSocketException;
import de.tavendo.autobahn.WebSocketHandler;

public class Communicator {

    private Context context;

    private long lastToastTime;

    public static final String TAG = "Communicator";

    // TODO to żeby w threadpoola puścic jakiegoś
    private LinkedList<WebSocketConnection> connectedDevices = new LinkedList<>();

    public Communicator(Context context) {
        this.context = context;
        this.lastToastTime = System.currentTimeMillis();
    }

    public void connect(String key) {
        new ConnectDataTask().execute("ws://" + key + ":" + Config.PORT);
    }

    public void disconnect(String key) {
        new DisconnectSingleAsyncTask().execute(key);
    }

    public void sendData(String data) {
        if (connectedDevices.isEmpty()) {
            if (System.currentTimeMillis() - lastToastTime >= 2000) {
                lastToastTime = System.currentTimeMillis();
                Toast.makeText(context, "No connected devices!", Toast.LENGTH_SHORT).show();
            }
        } else {
            new SendDataTask().execute(data);
        }
    }

    public void disconnectAll() {
        new DisconnectAllAsyncTask().execute();
    }


    public ServerFinderTask getServerFinderTask(DeviceRowAdapter adapter) {
        return new ServerFinderTask(this.context, adapter);
    }

    // TODO pozmieniać asynki to wszystko (threadpool jakiś?)
    private class SendDataTask extends AsyncTask<String, Void, Void> {

        @Override
        protected Void doInBackground(String... params) {
            String data = params[0];

            // TODO to żeby w threadpoola puścic jakiegoś
            if (connectedDevices.size() < 1) {
                // toast tutaj
            } else {
                for (WebSocketConnection wsc : connectedDevices) {
                    if (wsc.isConnected()) {
                        wsc.sendTextMessage(data);
                    }
                }
            }

            return null;
        }

    }

    private class ConnectDataTask extends AsyncTask<String, Void, Void> {

        @Override
        protected Void doInBackground(String... params) {
            String data = params[0];

            connectedDevices.add(startSingleConnction(data));

            return null;
        }

        public WebSocketConnection startSingleConnction(final String wsUri) {
            WebSocketConnection connection = new WebSocketConnection();

            try {
                connection.connect(wsUri, new WebSocketHandler() {

                    @Override
                    public void onOpen() {
                        Log.d(TAG, "Connected: " + wsUri);
                    }

                    @Override
                    public void onTextMessage(String payload) {
                        Log.d(TAG, "Recieved message: " + payload);
                        // TODO ustawianie tego?
                    }

                    @Override
                    public void onClose(int code, String reason) {
                        Log.d(TAG, "Connection lost.");
                    }
                });
            } catch (WebSocketException e) {
                Log.d(TAG, e.toString());
            }
            return connection;
        }

        public void startMultipleConnections() {
            // TODO przygotować na wiele
        }

    }

    private class DisconnectSingleAsyncTask extends AsyncTask<String, Void, Void> {

        @Override
        protected Void doInBackground(String... params) {

            // TODO zeby na jedym wylaczalo
            for (WebSocketConnection wsc : connectedDevices) {
                if (wsc.isConnected()) {
                    wsc.disconnect();
                }
            }
            connectedDevices.removeAll(connectedDevices);

            return null;
        }

    }

    private class DisconnectAllAsyncTask extends AsyncTask<Void, Void, Void> {

        @Override
        protected Void doInBackground(Void... params) {

            // TODO to żeby w threadpoola puścic jakiegoś
            for (WebSocketConnection wsc : connectedDevices) {
                if (wsc.isConnected()) {
                    wsc.disconnect();
                }
            }
            connectedDevices.removeAll(connectedDevices);

            return null;
        }

    }



}
