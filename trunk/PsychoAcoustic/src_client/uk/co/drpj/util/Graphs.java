/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package uk.co.drpj.util;

import java.awt.Color;
import javax.swing.JPanel;
import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.axis.NumberAxis;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.chart.plot.XYPlot;
import org.jfree.data.xy.XYSeries;
import org.jfree.data.xy.XYSeriesCollection;
import rasmus.interpreter.sampled.util.FFT;

/**
 *
 * @author pjl
 */
public class Graphs {

    public static JPanel fftDBPanel(float a[], float sampleRate, String xTit, String yTit, String tit) {

        int len = 1024 * 16;

        double buff[] = new double[2 * len];

        for (int i = 0; i < a.length; i++) {
            buff[i] = a[i];
        }

        FFT fft = new FFT(len);
        fft.calcReal(buff, -1);

        int nBin = len / 2;

        final XYSeries s1 = new XYSeries(tit);

        for (int i = 0; i < nBin; i++) {
            double real = buff[2 * i];
            double imag = buff[2 * i + 1];
            double val = Math.sqrt(real * real + imag * imag);
            val = 20.0 * Math.log10(val);
            double freq = i * sampleRate / (2.0 * nBin);
            s1.add(freq, val);
        }


        final XYSeriesCollection dataset = new XYSeriesCollection();
        dataset.addSeries(s1);

        final JFreeChart chart = ChartFactory.createXYLineChart(
                tit, // chart title
                "Category", // domain axis label
                "Value", // range axis label
                dataset, // data
                PlotOrientation.VERTICAL,
                false, // include legend
                true,
                false);

        final XYPlot plot = chart.getXYPlot();
        final NumberAxis domainAxis = new NumberAxis(xTit);
        final NumberAxis rangeAxis = new NumberAxis(yTit); //new LogarithmicAxis("Log(y)");
        plot.setDomainAxis(domainAxis);
        plot.setRangeAxis(rangeAxis);
        chart.setBackgroundPaint(Color.white);
        plot.setOutlinePaint(Color.black);
        final ChartPanel chartPanel = new ChartPanel(chart);
        chartPanel.setPreferredSize(new java.awt.Dimension(500, 270));

        return chartPanel;

    }

    public static JPanel timePanel(float a[], float sampleRate, String xTit, String yTit, String tit) {

        final XYSeries s1 = new XYSeries(tit);
        double dt = 1.0 / sampleRate;

        for (int i = 0; i < a.length; i++) {

            double t = i * dt;
            s1.add(t, a[i]);
        }


        final XYSeriesCollection dataset = new XYSeriesCollection();
        dataset.addSeries(s1);

        final JFreeChart chart = ChartFactory.createXYLineChart(
                tit, // chart title
                "Category", // domain axis label
                "Value", // range axis label
                dataset, // data
                PlotOrientation.VERTICAL,
                false, // include legend
                true,
                false);

        final XYPlot plot = chart.getXYPlot();
        final NumberAxis domainAxis = new NumberAxis(xTit);
        final NumberAxis rangeAxis = new NumberAxis(yTit);
        plot.setDomainAxis(domainAxis);
        plot.setRangeAxis(rangeAxis);
        chart.setBackgroundPaint(Color.white);
        plot.setOutlinePaint(Color.black);
        final ChartPanel chartPanel = new ChartPanel(chart);
        chartPanel.setPreferredSize(new java.awt.Dimension(500, 270));

        return chartPanel;

    }

      public static JPanel xyPanel(float x[], float y[], String xTit, String yTit, String tit) {

        final XYSeries s1 = new XYSeries(tit);

        for (int i = 0; i < x.length; i++) {

            s1.add(x[i], y[i]);
        }


        final XYSeriesCollection dataset = new XYSeriesCollection();
        dataset.addSeries(s1);

        final JFreeChart chart = ChartFactory.createXYLineChart(
                tit, // chart title
                "Category", // domain axis label
                "Value", // range axis label
                dataset, // data
                PlotOrientation.VERTICAL,
                false, // include legend
                true,
                false);

        final XYPlot plot = chart.getXYPlot();
        final NumberAxis domainAxis = new NumberAxis(xTit);
        final NumberAxis rangeAxis = new NumberAxis(yTit);
        plot.setDomainAxis(domainAxis);
        plot.setRangeAxis(rangeAxis);
        chart.setBackgroundPaint(Color.white);
        plot.setOutlinePaint(Color.black);
        final ChartPanel chartPanel = new ChartPanel(chart);
        chartPanel.setPreferredSize(new java.awt.Dimension(500, 270));

        return chartPanel;

    }
}
