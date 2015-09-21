package pl.edu.pw.elka.appled.fragments;

import pl.edu.pw.elka.appled.R;
import pl.edu.pw.elka.appled.communication.Communicator;
import android.app.Fragment;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ListView;

/**
 * 
 * @author Wojciech Kaczorowski
 *
 */
public class DevicesFragment extends Fragment {

    protected static final String TAG = "DevicesFragment";

    private Button searchButton;
//    private Button allDevicesButton;
//    private Button noDevicesButton;
    private ListView listView;
    private DeviceRowAdapter adapter;

    private Communicator communicator;

    public DevicesFragment(Communicator communicator) {
        this.communicator = communicator;
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View rootView = inflater.inflate(R.layout.devices_fragment, container, false);
        searchButton = (Button) rootView.findViewById(R.id.search_button);
        // allDevicesButton = (Button) rootView.findViewById(R.id.all_devices_button);
        // noDevicesButton = (Button) rootView.findViewById(R.id.no_devices_button);

        searchButton.setOnClickListener(new OnClickListener() {

            @Override
            public void onClick(View v) {
                communicator.getServerFinderTask(adapter).execute();
            }
        });
        
        
        // allDevicesButton.setOnClickListener(new OnClickListener() {
        //
        // @Override
        // public void onClick(View v) {
        // // TODO zaznaczanie wszystkiego na liście
        //
        // }
        // });
        //
        // noDevicesButton.setOnClickListener(new OnClickListener() {
        //
        // @Override
        // public void onClick(View v) {
        // // TODO czyszczenie listy
        // }
        // });

        listView = (ListView) rootView.findViewById(R.id.devices_list_view);
        adapter = new DeviceRowAdapter(getActivity().getApplicationContext(), communicator);
        listView.setAdapter(adapter);
        return rootView;
    }

}