package pl.edu.pw.elka.appled.fragments;

import pl.edu.pw.elka.appled.R;
import android.app.Fragment;
import android.graphics.Color;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.SeekBar;
import android.widget.SeekBar.OnSeekBarChangeListener;
import android.widget.TextView;

public class RGBFragment extends Fragment {

    public static final String TAG = "RGBFragment";

    private int chosenColor = Color.YELLOW; // default value
    private int red = Color.red(chosenColor);
    private int green = Color.green(chosenColor);
    private int blue = Color.blue(chosenColor);


    private TextView pickedColorCode;
    private PickedColorViewer pickedColorViewer;
    private SeekBar redSeekBar;
    private SeekBar greenSeekBar;
    private SeekBar blueSeekBar;

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View rootView = inflater.inflate(R.layout.rgb_fragment, container, false);
        pickedColorViewer = (PickedColorViewer) rootView.findViewById(R.id.picked_color_view);
        pickedColorCode = (TextView) rootView.findViewById(R.id.picked_color_code);
        redSeekBar = (SeekBar) rootView.findViewById(R.id.redSeekBar);
        greenSeekBar = (SeekBar) rootView.findViewById(R.id.greenSeekBar);
        blueSeekBar = (SeekBar) rootView.findViewById(R.id.blueSeekBar);

        redSeekBar.setProgress(red);
        greenSeekBar.setProgress(green);
        blueSeekBar.setProgress(blue);

        redSeekBar.setOnSeekBarChangeListener(new ColorOnSeekBarChangeListener());
        greenSeekBar.setOnSeekBarChangeListener(new ColorOnSeekBarChangeListener());
        blueSeekBar.setOnSeekBarChangeListener(new ColorOnSeekBarChangeListener());

        
        updateColor(chosenColor);

        return rootView;
    }

    public void updateColor(int color) {
        pickedColorCode.setText("#" + Integer.toHexString(color).substring(2));
        pickedColorViewer.updateColor(color);
        pickedColorViewer.invalidate();
    }

    private class ColorOnSeekBarChangeListener implements OnSeekBarChangeListener {

        @Override
        public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
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

        @Override
        public void onStartTrackingTouch(SeekBar seekBar) {
        }

        @Override
        public void onStopTrackingTouch(SeekBar seekBar) {
        }
    }

}
