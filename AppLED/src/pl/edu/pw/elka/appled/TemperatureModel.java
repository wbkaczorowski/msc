package pl.edu.pw.elka.appled;

import android.graphics.Color;
import android.util.Log;

public class TemperatureModel {
	
	public static int[] getRGB(int temp) {
		double red = 0, green = 0, blue = 0;
		
		int t = temp / 100;
		
		// calculate red
		if (t <= 66) {
			red = 255;
		} else {
			red = t - 60;
			red = 326.698727446 * Math.pow(red, -0.1332047592);
			if (red < 0) {
				red = 0;
			} else if (red > 255) {
				red = 255;
			}
		}

		// calculate green
		if (t <= 66) {
			green = 99.4708025861 * Math.log(t) - 161.1195681661;
		} else {
			green = t - 60;
			green = 288.1221695283 * Math.pow(green, -0.0755148492);
		}
		if (green < 0) {
			green = 0;
		} else if (green > 255) {
			green = 255;
		}
		
		// calculate blue
		if (t >= 66) {
			blue = 255;
		} else {
			if (t <= 19) {
				blue = 0;
			} else {
				blue = t - 10;
				blue = 138.5177312231 * Math.log(blue) - 305.0447927307;
			}
			if (blue < 0) {
				blue = 0;
			} else if (blue > 255) {
				blue = 255;
			}
		}
//		Log.d("TEMP", "r:"+red + " g:" + green + " b:" + blue);
		return new int[]{(int) red, (int) green, (int) blue};
	}
	
	public static int getRGBToColor(int temp) {
		int[] colors = getRGB(temp);
		return Color.rgb(colors[0], colors[1], colors[2]);
	}

}
