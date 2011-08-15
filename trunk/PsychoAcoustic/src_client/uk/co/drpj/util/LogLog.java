/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package uk.co.drpj.util;

/**
 *
 * @author pjl
 */

import java.awt.Color;
 
import javax.swing.JFrame;
import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.axis.LogarithmicAxis;
import org.jfree.chart.axis.NumberAxis;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.chart.plot.XYPlot;
import org.jfree.data.xy.XYSeries;
import org.jfree.data.xy.XYSeriesCollection;


/**
 * A demo showing the use of log axes.
 *
 */
public class LogLog extends JFrame {

    /**
     * Creates a new demo.
     *
     * @param title  the frame title.
     */
    public LogLog(final String title) {

        super(title);

        //Object[][][] data = new Object[3][50][2];
        final XYSeries s1 = new XYSeries("Series 1");
        final XYSeries s2 = new XYSeries("Series 2");
        final XYSeries s3 = new XYSeries("Series 3");

//        for (int i = 1; i <= 50; i++) {
//            s1.add(i, 1000 * Math.pow(i, -2));
//            s2.add(i, 1000 * Math.pow(i, -3));
//            s3.add(i, 1000 * Math.pow(i, -4));
//        }

        for (int i = 1; i <= 50; i++) {
            s1.add(i, 10 * Math.exp(i / 5.0));
            s2.add(i, 20 * Math.exp(i / 5.0));
            s3.add(i, 30 * Math.exp(i / 5.0));
        }

        final XYSeriesCollection dataset = new XYSeriesCollection();
        dataset.addSeries(s1);
        dataset.addSeries(s2);
        dataset.addSeries(s3);

        final JFreeChart chart = ChartFactory.createXYLineChart(
            "Log Axis Demo",          // chart title
            "Category",               // domain axis label
            "Value",                  // range axis label
            dataset,                  // data
            PlotOrientation.VERTICAL,
            true,                     // include legend
            true,
            false
        );

        final XYPlot plot = chart.getXYPlot();
        final NumberAxis domainAxis = new NumberAxis("x");
        final NumberAxis rangeAxis = new LogarithmicAxis("Log(y)");
        plot.setDomainAxis(domainAxis);
        plot.setRangeAxis(rangeAxis);
        chart.setBackgroundPaint(Color.white);
        plot.setOutlinePaint(Color.black);
        final ChartPanel chartPanel = new ChartPanel(chart);
        chartPanel.setPreferredSize(new java.awt.Dimension(500, 270));
        setContentPane(chartPanel);

    }

    // ****************************************************************************
    // * JFREECHART DEVELOPER GUIDE                                               *
    // * The JFreeChart Developer Guide, written by David Gilbert, is available   *
    // * to purchase from Object Refinery Limited:                                *
    // *                                                                          *
    // * http://www.object-refinery.com/jfreechart/guide.html                     *
    // *                                                                          *
    // * Sales are used to provide funding for the JFreeChart project - please    *
    // * support us so that we can continue developing free software.             *
    // ****************************************************************************

    /**
     * Starting point for the demonstration application.
     *
     * @param args  ignored.
     */
    public static void main(String[] args) {

        final  LogLog demo = new LogLog("XY Log Axes Demo");
        demo.pack();
       // RefineryUtilities.centerFrameOnScreen(demo);
        demo.setVisible(true);

    }

}

