package pl.edu.pw.elka.appled.communication;

import org.json.JSONException;
import org.json.JSONObject;

import android.graphics.Color;
import android.util.Log;

public class Data {

	public static final String TAG = "Data";

	public static JSONObject color(String colorValue) {
		JSONObject json = new JSONObject();
		try {
			json.put("color", colorValue);
		} catch (JSONException e) {
			Log.w(TAG, e);
		}
		return json;
	}

	public static JSONObject light(int lightValue) {
		JSONObject json = new JSONObject();
		try {
			json.put("light", Math.round(lightValue * 2.55f));
		} catch (JSONException e) {
			Log.w(TAG, e);
		}
		return json;
	}

	public static int colorFromJson(String data) {
		try {
			JSONObject json = new JSONObject(data);
			return Color.parseColor("#" + json.getString("color"));
		} catch (JSONException e) {
			Log.w(TAG, e);
		}
		return 0;

	}
}
