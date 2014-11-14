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

/**
 * 
 * @author Wojciech Kaczorowski
 *
 */
public class DevicesFragment extends Fragment {

    private Button allDevicesButton;
    private Button noDevicesButton;
    
    private Communicator communicator;
    
    public DevicesFragment(Communicator communicator) {
        this.communicator = communicator;
    }
    
    
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View rootView = inflater.inflate(R.layout.devices_fragment, container, false);
        allDevicesButton = (Button) rootView.findViewById(R.id.all_devices_button);
        noDevicesButton = (Button) rootView.findViewById(R.id.no_devices_button);
        
        allDevicesButton.setOnClickListener(new OnClickListener() {
            
            @Override
            public void onClick(View v) {
                // TODO zaznaczanie wszystkiego na liście
            }
        });
        
        noDevicesButton.setOnClickListener(new OnClickListener() {
            
            @Override
            public void onClick(View v) {
                // TODO czyszczenie listy
            }
        });
        
        // TODO tez tak tymczasowo postawione
        communicator.connect();
        
        return rootView;
    }

    
    
    
    
    
}