package pl.edu.pw.elka.appled.fragments;

import pl.edu.pw.elka.appled.R;
import pl.edu.pw.elka.appled.TemperatureModel;
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

public class TemperatureFragment extends Fragment {

    public static final String TAG = "TemperatureFragment";
    
    private Communicator communicator;

    private int temperatureValue;

    private TextView pickedTemperatureValueCode;
    private PickedColorViewer pickedTemperatureValueViewer;
    private SeekBar temperatureValueSeekBar;
    
    public TemperatureFragment(Communicator communicator) {
        //TODO na taki jaki jest na rpi 
        temperatureValue = 4500;
        this.communicator = communicator;
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View rootView = inflater.inflate(R.layout.temperature_fragment, container, false);
        pickedTemperatureValueViewer = (PickedColorViewer) rootView.findViewById(R.id.picked_temperature_value_view);
        pickedTemperatureValueCode = (TextView) rootView.findViewById(R.id.picked_temperature_value_code);
        temperatureValueSeekBar = (SeekBar) rootView.findViewById(R.id.temperature_value_seek_bar);

        temperatureValueSeekBar.setProgress(temperatureValue);
        temperatureValueSeekBar.setOnSeekBarChangeListener(new ColorOnSeekBarChangeListener());

        updateColorInApp(TemperatureModel.getRGBToColor(temperatureValue), temperatureValue);
        return rootView;
    }

    private void updateColorInApp(int valueRGB, int tempValue) {
    	pickedTemperatureValueCode.setText(tempValue + " K");
        pickedTemperatureValueViewer.updateColor(valueRGB);
        pickedTemperatureValueViewer.invalidate();
    }
    
    public void updateColor(int value) {
    	int colorValue = TemperatureModel.getRGBToColor(value);
        updateColorInApp(colorValue, value);
        //TODO wysyłanie tutaj?
        //TODO a może nie wysyłac wszystkich tylko co x ms?
        communicator.sendData(Data.temperature(value));
    }

    
    private class ColorOnSeekBarChangeListener implements OnSeekBarChangeListener {

        @Override
        public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
            temperatureValue = progress + 1000;
            updateColor(temperatureValue);
        }

        @Override
        public void onStartTrackingTouch(SeekBar seekBar) {
        }

        @Override
        public void onStopTrackingTouch(SeekBar seekBar) {
        }
    }

}
