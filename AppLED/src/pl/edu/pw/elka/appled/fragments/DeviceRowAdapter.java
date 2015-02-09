package pl.edu.pw.elka.appled.fragments;

import java.util.LinkedHashMap;

import pl.edu.pw.elka.appled.R;
import pl.edu.pw.elka.appled.communication.Communicator;
import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.TextView;
import android.widget.ToggleButton;

public class DeviceRowAdapter extends BaseAdapter {

    private LinkedHashMap<String, String> data = new LinkedHashMap<String, String>();
    private String[] keys;
    private Context context;
    private Communicator communicator;

    public DeviceRowAdapter(Context context, Communicator communicator) {
        this.context = context;
        this.communicator = communicator;
    }

    @Override
    public int getCount() {
        return data.size();
    }

    @Override
    public Object getItem(int position) {
        return data.get(keys[position]);
    }

    @Override
    public long getItemId(int arg0) {
        return arg0;
    }
    
    public void setData(LinkedHashMap<String, String> data) {
        this.data = data;
        this.keys = data.keySet().toArray(new String[data.size()]);
    }
    

    @Override
    public View getView(int pos, View convertView, ViewGroup parent) {
        final String key = keys[pos];
        String value = (String) getItem(pos);

        LayoutInflater inflater = (LayoutInflater) context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        View rowView = inflater.inflate(R.layout.devices_row, parent, false);
        TextView deviceNameText = (TextView) rowView.findViewById(R.id.device_name_text);
        TextView deviceIPText = (TextView) rowView.findViewById(R.id.device_IP_text);
        deviceNameText.setText(value);
        deviceIPText.setText(key);
        final ToggleButton connectButton = (ToggleButton) rowView.findViewById(R.id.connect_button);
        connectButton.setOnClickListener(new OnClickListener() {
            
            @Override
            public void onClick(View v) {
                if (connectButton.isChecked()) {
                    communicator.connect(key);
                } else {
                    communicator.disconnect(key);
                }
            }
        });
       

        return rowView;
    }
}
