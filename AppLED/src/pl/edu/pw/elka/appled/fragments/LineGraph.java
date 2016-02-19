package pl.edu.pw.elka.appled.fragments;

import java.util.HashMap;
import java.util.Map;

import org.achartengine.ChartFactory;
import org.achartengine.GraphicalView;
import org.achartengine.model.TimeSeries;
import org.achartengine.model.XYMultipleSeriesDataset;
import org.achartengine.model.XYSeries;
import org.achartengine.renderer.XYMultipleSeriesRenderer;
import org.achartengine.renderer.XYSeriesRenderer;

import android.content.Context;
import android.graphics.Color;
import android.graphics.Paint.Align;
import android.graphics.Typeface;

public class LineGraph {
	private Map<String, Integer> moteColors;
	private Map<String, XYSeries> dataSeries;
	private Map<String, XYSeriesRenderer> seriesRenderers;

	private XYMultipleSeriesDataset dataset;
	private XYMultipleSeriesRenderer mr;
	private GraphicalView view;

	public LineGraph() {
		dataset = new XYMultipleSeriesDataset();
		mr = new XYMultipleSeriesRenderer();
		moteColors = new HashMap<>();
		dataSeries = new HashMap<>();
		seriesRenderers = new HashMap<>();

		moteColors.put("4", Color.RED);
		moteColors.put("6", Color.GREEN);
		moteColors.put("7", Color.BLUE);

		for (String key : moteColors.keySet()) {
			XYSeries s = new XYSeries(key);
			dataSeries.put(key, s);
			dataset.addSeries(s);
			XYSeriesRenderer renderer = new XYSeriesRenderer();
			renderer.setColor(moteColors.get(key));
			renderer.setLineWidth(2);
			// renderer.setDisplayChartValues(true);
			seriesRenderers.put(key, renderer);
			mr.addSeriesRenderer(renderer);
		}

		mr.setMargins(new int[] { 20, 100, 100, 20 });
		mr.setShowGrid(true);
		mr.setGridColor(Color.GRAY);
		mr.setLegendTextSize(50);
		mr.setLegendHeight(100);
		mr.setLabelsTextSize(30);
		
		mr.setLabelsColor(Color.DKGRAY);
		mr.setXLabels(12);
		mr.setXRoundedLabels(false);
		
		mr.setYLabels(12);
		mr.setYTitle("light intensity [lx]");
		mr.setYLabelsAlign(Align.RIGHT);
		mr.setYLabelsPadding(10);
		mr.setYLabelsColor(0, Color.DKGRAY);


		mr.setTextTypeface(Typeface.SANS_SERIF);
		mr.setAxisTitleTextSize(40);
		
		mr.setBackgroundColor(Color.WHITE);
		mr.setApplyBackgroundColor(true);
		mr.setMarginsColor(Color.parseColor("#fff3f3f3"));
		mr.setAntialiasing(true);
		
		mr.setZoomButtonsVisible(false);

	}

	public GraphicalView getView(Context context) {
		view = ChartFactory.getLineChartView(context, dataset, mr);
		return view;
	}

	public void addNewPoints(String seriesKey, Point p) {
		XYSeries xySeries = dataSeries.get(seriesKey);
		if (xySeries == null) {
			xySeries = new XYSeries(seriesKey);
			dataSeries.put(seriesKey, xySeries);
		}
		xySeries.add(p.x, p.y);

		// data.add(p.x, p.y);
	}

}