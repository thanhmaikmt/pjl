/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package uk.co.drpj;

import uk.co.drpj.audio.FIRFilterDesign;
import uk.co.drpj.util.DoubleJSlider;
import uk.co.drpj.util.Graphs;
import java.awt.BorderLayout;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.AbstractAction;
import javax.swing.AbstractButton;
import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JComboBox;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;

/**
 *
 * @author pjl
 */
public class FIRDesignPanel extends JPanel {

    float bandwidth = 500.0f;
    float sampleRate = 44100.0f;
    float frequency = 10000;
    float alpha = 10.0f;
    int order = 100;
    JLabel freqDisp;
    JLabel attenDisp;
    JLabel orderDisp;
    JLabel bwDisp;
    JPanel graphPanel;
    //  boolean useOrder = false;
    private JButton redraw;
    private AbstractButton autoOrder;
    private DoubleJSlider aphaSlide;
    private DoubleJSlider orderSlide;
    private DoubleJSlider transSlide;
    private final Thread graphThread;

    enum WinType {

        KAISER(FIRFilterDesign.KAISER, "Kaiser"),
        RECT(FIRFilterDesign.RECT, "Rect");

        WinType(int i, String name) {
            this.id = i;
            ;
            this.name = name;
        }

        public String toString() {
            return name;
        }
        final int id;
        private final String name;
    }
    WinType winType = WinType.KAISER;

    enum FiltType {

        LPF(FIRFilterDesign.LPF, "Low pass"),
        BPF(FIRFilterDesign.BPF, "Band pass"),
        HPF(FIRFilterDesign.HPF, "High pass");

        FiltType(int i, String name) {
            this.id = i;
            ;
            this.name = name;
        }

        public String toString() {
            return name;
        }
        final int id;
        private final String name;
    }
//    WinType winType=WinType.RECT;
    FiltType filtType = FiltType.LPF;

    FIRDesignPanel() {
        super();
        setLayout(new BorderLayout());
        JPanel panel = createControls();
        add(panel, BorderLayout.SOUTH);

        graphPanel = new JPanel();
        graphPanel.setLayout(new GridLayout(3, 2));

        //      createGraphs();
        //       autoOrder.setSelected(true);
        update();
        graphThread = new Thread(new Runnable() {

            public synchronized void run() {
                createGraphs();

                while (true) {
                    try {
                        wait();
                    } catch (InterruptedException ex) {
                        //              Logger.getLogger(FIRDesignPanel.class.getName()).log(Level.SEVERE, null, ex);
                    }
                    while (Thread.interrupted()) {
                    } // clear pending interupts
                    createGraphs();
                }
            }
        });
        graphThread.start();
    }
    final Object muex = new Object();

    void createGraphs() {

        JPanel oldPanel = graphPanel;

        graphPanel = new JPanel();
        graphPanel.setLayout(new GridLayout(3, 2));





        FIRFilterDesign filt = new FIRFilterDesign(alpha, sampleRate, frequency, filtType.id, order, winType.id, bandwidth);

        float coeffs[] = filt.getCoefficients();

        order = filt.getOrder();

        graphPanel.add(Graphs.timePanel(filt.getRawCoefficients(), sampleRate, "Time [s]", "h(t)", "Ideal Impulse response"));
        switch (filtType) {
            case LPF:
                graphPanel.add(Graphs.xyPanel(new float[]{0, frequency, frequency, sampleRate / 2}, new float[]{1, 1, 0, 0}, "Frequency [Hz]", "Attenuation", "Ideal Attenuation"));
                break;
            case HPF:
                graphPanel.add(Graphs.xyPanel(new float[]{0, frequency, frequency, sampleRate / 2}, new float[]{0, 0, 1, 1}, "Frequency [Hz]", "Attenuation", "Ideal Attenuation"));
                break;
            case BPF:
                graphPanel.add(Graphs.xyPanel(new float[]{0, frequency-bandwidth/2, frequency-bandwidth/2,frequency+bandwidth/2, frequency+bandwidth/2, sampleRate / 2}, new float[]{0, 0, 1, 1,0,0}, "Frequency [Hz]", "Attenuation", "Ideal Attenuation"));
                break;


        }
        graphPanel.add(Graphs.timePanel(filt.getWin(), sampleRate, "Time [s]", "w(t)", "Window"));
        graphPanel.add(Graphs.fftDBPanel(filt.getWin(), sampleRate, "Frequency [Hz]", "Attenuation [dB]", "Fourrier Transform of window"));
        graphPanel.add(Graphs.timePanel(coeffs, sampleRate, "Time [s]", "h(t)", "Windowed Impulse response"));
        graphPanel.add(Graphs.fftDBPanel(coeffs, sampleRate, "Frequency [Hz]", "Attenuation [dB]", "Final Filter Attenuation"));
        //         redraw.setEnabled(false);

        if (oldPanel != null) {
            remove(oldPanel);
            oldPanel.removeAll();
        }
        add(graphPanel, BorderLayout.CENTER);

        validate();
        //   updateLabels();

        //    repaint();
    }

    void update() {
        if (graphThread != null) {
            graphThread.interrupt();
        }

        freqDisp.setText(String.format("%6.1f", frequency));
        orderDisp.setText(String.format("%5d", order));
//        if (!autoOrder.isSelected()) {
//            bwDisp.setText("");
//            attenDisp.setText("");
//        } else {
        attenDisp.setText(String.format("%4.1f", alpha));
        bwDisp.setText(String.format("%6.1f", bandwidth));
//        }

        //       redraw.setEnabled(true);


    }

    JPanel createControls() {

        int row = 0;

        JPanel panel = new JPanel();
        panel.setLayout(new GridBagLayout());
        GridBagConstraints c = new GridBagConstraints();



        //      c.gridy = row++;
        c.gridx = 0;
        c.anchor = GridBagConstraints.EAST;
        c.fill = GridBagConstraints.HORIZONTAL;
        c.gridwidth = GridBagConstraints.REMAINDER;

//        final JComboBox combo = new JComboBox(new WinType[]{WinType.RECT, WinType.KAISER});
//
//        combo.addActionListener(new ActionListener() {
//
//            public void actionPerformed(ActionEvent e) {
//                winType = (WinType) (combo.getSelectedItem());
//                update();
//            }
//        });
//        c.gridwidth = GridBagConstraints.REMAINDER;
//        panel.add(combo, c);


//            public void actionPerformed(ActionEvent e) {
//                winType=(WinType)(combo.getSelectedItem());
//            }
//        });
//       // c.gridwidth = GridBagConstraints.REMAINDER;
//        panel.add(combo,c);


        final JComboBox comboF = new JComboBox(new FiltType[]{FiltType.LPF, FiltType.BPF, FiltType.HPF});

        comboF.addActionListener(new ActionListener() {

            public void actionPerformed(ActionEvent e) {
                filtType = (FiltType) (comboF.getSelectedItem());
                transSlide.setEnabled(filtType == FiltType.BPF);
                update();
            }
        });
        //    c.gridwidth = GridBagConstraints.REMAINDER;
        panel.add(comboF, c);


        // ------------------------
        c.gridwidth = 1;
        c.gridy = row++;

//        autoOrder = new JCheckBox("Auto length");
//        autoOrder.addActionListener(new ActionListener() {
//
//            public void actionPerformed(ActionEvent e) {
//                if (!autoOrder.isSelected()) {
//                    orderSlide.setEnabled(true);
//                    transSlide.setEnabled(false);
//                    attenSlide.setEnabled(false);
//                } else {
//                    orderSlide.setEnabled(false);
//                    attenSlide.setEnabled(true);
//                    transSlide.setEnabled(true);
//                }
//            }
//        });
//
//
//
//        panel.add(autoOrder, c);

//        redraw = new JButton(new AbstractAction("Redraw") {
//
//            public void actionPerformed(ActionEvent e) {
//                createGraphs();
//            }
//        });
//
//
//        c.gridwidth = GridBagConstraints.REMAINDER;
//        c.gridx += 1;
//        panel.add(redraw, c);




        c.gridy = row++;
        c.gridx = 0;
        c.gridwidth = 1;



        //  frequency


        final DoubleJSlider freqSlide = new DoubleJSlider(0.0, sampleRate / 2, frequency, 100);
        //freqSlide.setPreferredSize(new Dimension(1000, 20));
        freqDisp = new JLabel((String) null, JLabel.RIGHT);
//        freqDisp.setPreferredSize(new Dimension(80, 20));


        freqSlide.addChangeListener(new ChangeListener() {

            public void stateChanged(ChangeEvent e) {
                frequency = (float) freqSlide.getDoubleValue();
                update();

            }
        });


        panel.add(new JLabel("Frequency", JLabel.RIGHT), c);
        c.gridx = GridBagConstraints.RELATIVE;

        panel.add(freqSlide, c);
        panel.add(freqDisp, c);




        //  trans frequency

        c.gridy = row++;
        c.gridx = 0;

        transSlide = new DoubleJSlider(10.0, sampleRate / 4.0, bandwidth, 10);
        ///  transSlide.setPreferredSize(new Dimension(1000, 20));
        bwDisp = new JLabel((String) null, JLabel.RIGHT);
        //      bwDisp.setPreferredSize(new Dimension(80, 20));


        transSlide.addChangeListener(new ChangeListener() {

            public void stateChanged(ChangeEvent e) {
                bandwidth = (float) transSlide.getDoubleValue();
                update();

            }
        });
        transSlide.setEnabled(false);

        panel.add(new JLabel("Bandwidth [Hz]", JLabel.RIGHT), c);
        c.gridx = GridBagConstraints.RELATIVE;

        panel.add(transSlide, c);
        panel.add(bwDisp, c);


        // ---- attenuation

        c.gridy = row++;
        c.gridx = 0;

        aphaSlide = new DoubleJSlider(0.0, 25.0, alpha, 0.5);
        // attenSlide.setPreferredSize(new Dimension(1000, 20));
        attenDisp = new JLabel((String) null, JLabel.RIGHT);
        //   attenDisp.setPreferredSize(new Dimension(80, 20));




        aphaSlide.addChangeListener(new ChangeListener() {

            public void stateChanged(ChangeEvent e) {
                alpha = (float) aphaSlide.getDoubleValue();
                update();

            }
        });


        panel.add(new JLabel(" (Kaiser) alpha", JLabel.RIGHT), c);
        c.gridx = GridBagConstraints.RELATIVE;

        panel.add(aphaSlide, c);
        panel.add(attenDisp, c);


        // ---- order

        c.gridy = row++;
        c.gridx = 0;
        order = 32;

        orderSlide = new DoubleJSlider(10.0, 200, order, 10);
        // orderSlide.setPreferredSize(new Dimension(1000, 20));
        orderDisp = new JLabel((String) null, JLabel.RIGHT);
        //     orderDisp.setPreferredSize(new Dimension(80, 20));
        //     orderSlide.setEnabled(false);



        orderSlide.addChangeListener(new ChangeListener() {

            public void stateChanged(ChangeEvent e) {
                order = (int) Math.round(orderSlide.getDoubleValue());
                update();
            }
        });


        panel.add(new JLabel("filter length", JLabel.RIGHT), c);
        c.gridx = GridBagConstraints.RELATIVE;

        panel.add(orderSlide, c);
        panel.add(orderDisp, c);


        return panel;
    }

    class AbstractActionImpl extends AbstractAction {

        public AbstractActionImpl(String name) {
            super(name);
        }

        public void actionPerformed(ActionEvent e) {
            createGraphs();
        }
    }
}
