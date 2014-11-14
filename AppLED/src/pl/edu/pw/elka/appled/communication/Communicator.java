package pl.edu.pw.elka.appled.communication;

import java.util.LinkedList;

import pl.edu.pw.elka.appled.Config;
import android.os.AsyncTask;
import android.util.Log;
import de.tavendo.autobahn.WebSocketConnection;
import de.tavendo.autobahn.WebSocketException;
import de.tavendo.autobahn.WebSocketHandler;

public class Communicator {

    public static final String TAG = "Communicator";

    // TODO to żeby w threadpoola puścic jakiegoś
    private LinkedList<WebSocketConnection> connectedDevices = new LinkedList<>();

    public void connect() {
        new ConnectDataTask().execute("ws://" + Config.RPI_IP + ":" + Config.PORT);
    }

    public void sendData(String data) {
        new SendDataTask().execute(data);
    }

    public void disconnectAll() {
        new DisconnectAsyncTask().execute();
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

    private class DisconnectAsyncTask extends AsyncTask<Void, Void, Void> {

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
