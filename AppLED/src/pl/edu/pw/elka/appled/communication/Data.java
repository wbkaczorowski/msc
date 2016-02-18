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
	
	public static JSONObject temperature(int tempValue) {
		JSONObject json = new JSONObject();
		try {
			json.put("temperature", tempValue);
//			Log.d(TAG, "temperature: " + tempValue);
		} catch (JSONException e) {
			Log.w(TAG, e);
		}
		return json;
	}
	
	public static boolean isLightJson(String data) {
		try {
			JSONObject json = new JSONObject(data);
			return json.optJSONObject("light") != null;
		} catch (Exception e) {
			Log.w(TAG, e);
			return false;
		}
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

	public static JSONObject parseLightJson(String payload) {
		try {
			JSONObject jsonObject = new JSONObject(payload);
			return jsonObject.getJSONObject("light");
		} catch (JSONException e) {
			Log.w(TAG, e);
		}
		return null;
	}
}
