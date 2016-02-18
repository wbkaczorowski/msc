package pl.edu.pw.elka.appled.fragments;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicLong;

import org.achartengine.GraphicalView;

import android.app.Fragment;
import android.graphics.Color;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import pl.edu.pw.elka.appled.R;
import pl.edu.pw.elka.appled.communication.Communicator;

/**
 * 
 * @author Wojciech Kaczorowski
 *
 */
public class SensorsFragment extends Fragment {

	protected static final String TAG = "SensorsFragment";

	private Communicator communicator;


	private GraphicalView graphView;
	private LineGraph lineGraph;
	
	private AtomicInteger dataCounter = new AtomicInteger(0);

	public SensorsFragment(Communicator communicator) {
		this.communicator = communicator;
		lineGraph = new LineGraph();

	}

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
		graphView = lineGraph.getView(getActivity().getApplicationContext());
//		addData();
		return graphView;
	}

	public void addData(String key, String data) {
		lineGraph.addNewPoints(key, new Point(dataCounter.getAndIncrement(), Integer.parseInt(data)));
	}
	
	private void addData() {
		new Thread(new Runnable() {

			@Override
			public void run() {
				for (int i = 0; i < 40; i++) {
					final int x = i;

					getActivity().runOnUiThread(new Runnable() {

						@Override
						public void run() {
							lineGraph.addNewPoints("4", Point.randomPoint(x));
							graphView.repaint();
						}
					});

					try {
						Thread.sleep(600);
					} catch (InterruptedException e) {
						// manage error ...
					}
				}
			}
		}).start();
	}

}