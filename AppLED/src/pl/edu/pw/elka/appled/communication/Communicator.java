package pl.edu.pw.elka.appled.communication;

import java.util.LinkedList;

import org.json.JSONObject;

import pl.edu.pw.elka.appled.Config;
import pl.edu.pw.elka.appled.fragments.DeviceRowAdapter;
import pl.edu.pw.elka.appled.fragments.RGBFragment;
import pl.edu.pw.elka.appled.fragments.SensorsFragment;
import android.content.Context;
import android.graphics.Color;
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

	private LinkedList<WebSocketConnection> connectedDevices = new LinkedList<>();

	private RGBFragment rgbFragment;
	private SensorsFragment sensorsFragment;

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

	public void sendData(JSONObject data) {
		if (connectedDevices.isEmpty()) {
			if (System.currentTimeMillis() - lastToastTime >= 2000) {
				lastToastTime = System.currentTimeMillis();
				Toast.makeText(context, "No connected devices!", Toast.LENGTH_SHORT).show();
			}
		} else {
			new SendDataTask().execute(data.toString());
		}
	}

	public void disconnectAll() {
		new DisconnectAllAsyncTask().execute();
	}

	public ServerFinderTask getServerFinderTask(DeviceRowAdapter adapter) {
		return new ServerFinderTask(this.context, adapter);
	}

	private class SendDataTask extends AsyncTask<String, Void, Void> {

		@Override
		protected Void doInBackground(String... params) {
			String data = params[0];

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
						if (Data.isLightJson(payload)) {
							JSONObject json = Data.parseLightJson(payload);
							sensorsFragment.addData(json.optString("key"), json.optString("value"));
						} else {
							if (rgbFragment != null) {
								int color = Data.colorFromJson(payload);
								rgbFragment.setChosenColor(color);
								rgbFragment.updateColorInApp(color);
							}
						}
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

			for (WebSocketConnection wsc : connectedDevices) {
				if (wsc.isConnected()) {
					wsc.disconnect();
				}
			}
			connectedDevices.removeAll(connectedDevices);

			return null;
		}

	}

	public void setRgbFragment(RGBFragment rgbFragment) {
		this.rgbFragment = rgbFragment;
	}

	public void setSensorsFragment(SensorsFragment sensorsFragment) {
		this.sensorsFragment = sensorsFragment;
	}

}
