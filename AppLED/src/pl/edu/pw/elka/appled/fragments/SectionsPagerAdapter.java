package pl.edu.pw.elka.appled.fragments;

import pl.edu.pw.elka.appled.R;
import pl.edu.pw.elka.appled.communication.Communicator;
import android.app.Fragment;
import android.app.FragmentManager;
import android.content.Context;
import android.support.v13.app.FragmentPagerAdapter;
import android.util.SparseArray;


public class SectionsPagerAdapter extends FragmentPagerAdapter {
    
       
    private SparseArray<String> fragmentNames;
    private final int fragmentsNumber = 2;

    private Communicator communicator;
    
    public SectionsPagerAdapter(FragmentManager fm, Context context, Communicator communicator) {
        super(fm);
        fragmentNames = new SparseArray<String>();
        fragmentNames.put(0, context.getString(R.string.colors_rbg_fragment));
        fragmentNames.put(1, context.getString(R.string.devices_section_title));
        
        this.communicator = communicator;
    }

    @Override
    public Fragment getItem(int position) {
        switch (position) {
        case 0:
            return new RGBFragment(communicator);
            
        case 1:
            return new DevicesFragment(communicator);
            
        default:
            return DefaultFragment.newInstance(position + 1);
        }
    }

    @Override
    public int getCount() {
        return fragmentsNumber;
    }

    @Override
    public CharSequence getPageTitle(int position) {
        return fragmentNames.get(position);
    }
}