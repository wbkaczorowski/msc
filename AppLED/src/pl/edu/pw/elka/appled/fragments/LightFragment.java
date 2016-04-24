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

public class LightFragment extends Fragment {

    public static final String TAG = "LightFragment";
    
    private Communicator communicator;

    private int lightValue;

    private TextView pickedLightValueCode;
    private PickedColorViewer pickedLightValueViewer;
    private SeekBar lightValueSeekBar;
    
    public LightFragment(Communicator communicator) {
        //TODO na taki jaki jest na rpi 
        lightValue = 50;
        this.communicator = communicator;
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View rootView = inflater.inflate(R.layout.light_fragment, container, false);
        pickedLightValueViewer = (PickedColorViewer) rootView.findViewById(R.id.picked_light_value_view);
        pickedLightValueCode = (TextView) rootView.findViewById(R.id.picked_light_value_code);
        lightValueSeekBar = (SeekBar) rootView.findViewById(R.id.light_value_seek_bar);

        lightValueSeekBar.setProgress(lightValue);
        lightValueSeekBar.setOnSeekBarChangeListener(new ColorOnSeekBarChangeListener());

        updateColorInApp(lightValue);
        return rootView;
    }

    public void updateColorInApp(int value) {
        pickedLightValueCode.setText(value + "%");
        int rgbValue = (int) (2.55f * value);
        pickedLightValueViewer.updateColor(Color.rgb(rgbValue, rgbValue, rgbValue));
        pickedLightValueViewer.invalidate();
    }
    
    public void updateColor(int value) {
        updateColorInApp(value);
        //TODO a może nie wysyłac wszystkich tylko co x ms?
        communicator.sendData(Data.light(value));
    }

    
    private class ColorOnSeekBarChangeListener implements OnSeekBarChangeListener {

        @Override
        public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
            lightValue = progress;
            updateColor(lightValue);
        }

        @Override
        public void onStartTrackingTouch(SeekBar seekBar) {
        }

        @Override
        public void onStopTrackingTouch(SeekBar seekBar) {
        }
    }

}
