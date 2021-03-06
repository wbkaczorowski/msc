package pl.edu.pw.elka.appled.fragments;

import pl.edu.pw.elka.appled.R;
import pl.edu.pw.elka.appled.communication.Communicator;
import pl.edu.pw.elka.appled.communication.Data;
import android.app.Fragment;
import android.graphics.Color;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.SeekBar;
import android.widget.SeekBar.OnSeekBarChangeListener;
import android.widget.TextView;

public class RGBFragment extends Fragment {

	public static final String TAG = "RGBFragment";

	private Communicator communicator;

	private int chosenColor;
	private int red;
	private int green;
	private int blue;

	private TextView pickedColorCode;
	private PickedColorViewer pickedColorViewer;
	private SeekBar redSeekBar;
	private SeekBar greenSeekBar;
	private SeekBar blueSeekBar;

	public RGBFragment(Communicator communicator) {
		// TODO na taki jaki jest na rpi
		chosenColor = Color.GRAY; // default value
		red = Color.red(chosenColor);
		green = Color.green(chosenColor);
		blue = Color.blue(chosenColor);
		this.communicator = communicator;
	}

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
		View rootView = inflater.inflate(R.layout.rgb_fragment, container, false);
		pickedColorViewer = (PickedColorViewer) rootView.findViewById(R.id.picked_color_view);
		pickedColorCode = (TextView) rootView.findViewById(R.id.picked_color_code);
		redSeekBar = (SeekBar) rootView.findViewById(R.id.red_seek_bar);
		greenSeekBar = (SeekBar) rootView.findViewById(R.id.green_seek_bar);
		blueSeekBar = (SeekBar) rootView.findViewById(R.id.blue_seek_bar);

		redSeekBar.setProgress(red);
		greenSeekBar.setProgress(green);
		blueSeekBar.setProgress(blue);

		redSeekBar.setOnSeekBarChangeListener(new ColorOnSeekBarChangeListener());
		greenSeekBar.setOnSeekBarChangeListener(new ColorOnSeekBarChangeListener());
		blueSeekBar.setOnSeekBarChangeListener(new ColorOnSeekBarChangeListener());

		updateColorInApp(chosenColor);
		return rootView;
	}

	public void updateColorInApp(int color) {
		pickedColorCode.setText("#" + Integer.toHexString(color).substring(2));
		pickedColorViewer.updateColor(color);
		pickedColorViewer.invalidate();
	}

	public void updateColor(int color) {
		updateColorInApp(color);
		// TODO a może nie wysyłac wszystkich tylko co x ms?
		communicator.sendData(Data.color(Integer.toHexString(color).substring(2)));
	}

	private class ColorOnSeekBarChangeListener implements OnSeekBarChangeListener {

		@Override
		public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
			if (fromUser) {
				if (seekBar.equals(redSeekBar)) {
					red = progress;
				} else if (seekBar.equals(greenSeekBar)) {
					green = progress;
				} else if (seekBar.equals(blueSeekBar)) {
					blue = progress;
				}
				chosenColor = Color.rgb(red, green, blue);
				updateColor(chosenColor);
			}
		}

		@Override
		public void onStartTrackingTouch(SeekBar seekBar) {
		}

		@Override
		public void onStopTrackingTouch(SeekBar seekBar) {
		}
	}

	/**
	 * @return the chosenColor
	 */
	public int getChosenColor() {
		return chosenColor;
	}

	/**
	 * @param chosenColor
	 *            the chosenColor to set
	 */
	public void setChosenColor(int chosenColor) {
		this.chosenColor = chosenColor;
	}

}
