/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package uk.co.drpj;

import uk.co.drpj.audio.FIRFilterDesign;
import uk.co.drpj.util.Graphs;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.GridLayout;
import javax.swing.AbstractAction;
import javax.swing.AbstractButton;
import javax.swing.JButton;

import uk.co.drpj.audio.AudioSystem;
import uk.co.drpj.audio.MeterPanel;

import uk.co.drpj.audio.source.MyFreqDampedSource;
import uk.co.drpj.audio.source.MyFreqDampedSource.Wave;
import uk.co.drpj.util.DoubleJSlider;
//import com.frinika.audio.gui.MeterPanel;
import com.frinika.audio.toot.AudioPeakMonitor;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.Box;
import javax.swing.BoxLayout;
import javax.swing.JCheckBox;
import javax.swing.JComboBox;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JSpinner;
import javax.swing.SpinnerNumberModel;
import javax.swing.Timer;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;
import uk.co.drpj.audio.AntiAliasedSource;
import uk.org.toot.audio.core.AudioBuffer;
import uk.org.toot.audio.core.AudioProcess;
import uk.org.toot.audio.server.AudioClient;
import uk.org.toot.audio.server.AudioServer;

/**
 *
 * @author pjl
 */
public class AliasPanel extends JPanel {

    private AudioBuffer chunk;
    private AudioPeakMonitor peakIn;
    private MeterPanel meterPanel;
    AudioSystem audioSystem;
    private final MyFreqDampedSource src;
    JLabel fresDisp;
    float targetSampleRate;
    private JLabel ampDisp;
    boolean antiAlias = false;
    AntiAliasedSource overSrc;
    private FIRDesignPanelAnti firPanel;
    int upBy=8;


    void rebuildFilters() {


    }


    public AliasPanel() throws Exception {

        setLayout(new BorderLayout());
        audioSystem = AudioSystem.instance();
        peakIn = new AudioPeakMonitor();
        src = new MyFreqDampedSource();
        AudioServer server = audioSystem.getServer();
        final AudioProcess output = audioSystem.getOut();
        targetSampleRate = server.getSampleRate();

        server.setClient(new AudioClient() {

            int frameSize = 0;

            public void work(int size) {
                if (chunk == null || size != frameSize) {
                    frameSize = size;
                    chunk = new AudioBuffer(null, 2, size, targetSampleRate);

                    chunk.setRealTime(true);
                }

                chunk.makeSilence();

                if (antiAlias) {
                    overSrc.processAudio(chunk);
                } else {
                    src.processAudio(chunk);
                }

                peakIn.processAudio(chunk);
                output.processAudio(chunk);
            }

            public void setEnabled(boolean arg0) {
                //  throw new UnsupportedOperationException("Not supported yet.");
            }
        });
        configure();
    }

    public void start() {
        try {
            audioSystem.start();
        } catch (Exception ex) {
            Logger.getLogger(AliasPanel.class.getName()).log(Level.SEVERE, null, ex);
        }



        Timer timer = new Timer(50, new ActionListener() {

            public void actionPerformed(ActionEvent ae) {
                updateMeters();
            }
        });
        timer.start();

        // setPreferredSize(new Dimension(500,80));
    }

    private void updateMeters() {
        double val = peakIn.getPeak();
        if (val > .99) {
            meterPanel.updateMeter(val, Color.RED);
        } else {
            meterPanel.updateMeter(val, Color.GREEN);
        }
        float freq = src.getFreq();

        fresDisp.setText(String.format("%9.3f [kHz]", freq / 1000.0));
        ampDisp.setText(String.format("    %5.3f ", src.getAmp()));

    }
    int nLevel = (int) Math.pow(2, 16);

    public void configure() {

        //    frame = new JFrame();
        JPanel content = new JPanel();
        content.setLayout(new BorderLayout());

        meterPanel = new MeterPanel();
        meterPanel.setMinimumSize(new Dimension(50, 20));
        meterPanel.setPreferredSize(new Dimension(50, 20));
        content.add(meterPanel, BorderLayout.WEST);


        JPanel north = new JPanel();
        north.setLayout(new BoxLayout(north, BoxLayout.Y_AXIS));
        content.add(north, BorderLayout.NORTH);

        MyFreqDampedSource.Wave wavs[] = {MyFreqDampedSource.Wave.SAW, MyFreqDampedSource.Wave.SIN, MyFreqDampedSource.Wave.SQUARE, MyFreqDampedSource.Wave.NOISE};


        final JComboBox wavCombo = new JComboBox(wavs);

        wavCombo.setSelectedIndex(1);
        //  combo.setEnabled(false);
        wavCombo.addActionListener(new ActionListener() {

            public void actionPerformed(ActionEvent e) {
                MyFreqDampedSource.Wave o = (Wave) wavCombo.getSelectedItem();
                src.setWave(o);
            }
        });

        north.add(wavCombo);
        // wavCombo.setSize(new Dimension(1000,20));
        // north.add(Box.createVerticalGlue());

        JLabel rateLabel = new JLabel(" Sample rate (Fs) is " + targetSampleRate / 1000.0 + " kHz");


        JPanel freqPanel = new JPanel(new FlowLayout(FlowLayout.LEFT));


        //  frequency

        freqPanel = new JPanel(new FlowLayout(FlowLayout.LEFT));
        final DoubleJSlider freqSlide = new DoubleJSlider(0.0, 1.5 * targetSampleRate, 0.0, 1.0);
        freqSlide.setPreferredSize(new Dimension(600, 20));
        fresDisp = new JLabel();
        fresDisp.setPreferredSize(new Dimension(100, 20));




        freqSlide.addChangeListener(new ChangeListener() {

            public void stateChanged(ChangeEvent e) {
                double val = freqSlide.getDoubleValue();
                src.setFreq(val);


            }
        });


        freqPanel.add(new JLabel("Frequency"));
        freqPanel.add(freqSlide);
        freqPanel.add(fresDisp);


        JPanel center = new JPanel();

        center.setLayout(new BoxLayout(center, BoxLayout.Y_AXIS));
        center.add(freqPanel);

        //  frequency

        JPanel ampPanel = new JPanel();
        ampPanel.setLayout(new FlowLayout(FlowLayout.LEFT));
        final DoubleJSlider ampSlide = new DoubleJSlider(0.0, 1.5, 0., .10);
        ampDisp = new JLabel();
        ampDisp.setPreferredSize(new Dimension(100, 20));
        ampSlide.setPreferredSize(new Dimension(600, 20));

        ampSlide.addChangeListener(new ChangeListener() {

            public void stateChanged(ChangeEvent e) {
                double val = ampSlide.getDoubleValue();
                src.setAmp(val);
                ampDisp.setText(String.format("     %5.3f", val));
            }
        });


        ampPanel.add(new JLabel("Amplitude"));
        ampPanel.add(ampSlide);
        ampPanel.add(ampDisp);

        final JCheckBox antiBut = new JCheckBox("Antialias Filter");
        antiBut.addActionListener(new ActionListener() {

            public void actionPerformed(ActionEvent e) {
                antiAlias = antiBut.isSelected();
            }
        });


        center.add(ampPanel);
        center.add(antiBut);


        final SpinnerNumberModel model =
                new SpinnerNumberModel(8, 1, 32, 1);
        JSpinner spin = new JSpinner(model);
// 	model =   (SpinnerNumberModel)spin.getModel();
// 	model.setValue(t.getNumber());
// 	model.setMinimum((Comparable)t.getMinimum());
// 	model.setMaximum((Comparable)t.getMaximum());

        spin.addChangeListener(new ChangeListener() {

            public void stateChanged(ChangeEvent e) {
                int n = model.getNumber().intValue();
                overSrc.setUp(n,firPanel.getCoeffs());
            }
        });

        center.add(spin);

        firPanel = new FIRDesignPanelAnti();
        overSrc = new AntiAliasedSource(targetSampleRate, upBy, src,firPanel.getCoeffs());
        center.add(firPanel);

        center.add(Box.createVerticalGlue());
        center.add(rateLabel);


        content.add(center, BorderLayout.CENTER);
        add(content);


    }

    void dispose() {
        audioSystem.stop();
    }

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
    /**
     *
     * @author pjl
     */
    public class FIRDesignPanelAnti extends JPanel {

        float bandwidth = 500.0f;
        //float sampleRate = 44100.0f;
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

        
        WinType winType = WinType.KAISER;

//    WinType winType=WinType.RECT;
        FiltType filtType = FiltType.LPF;

        FIRDesignPanelAnti() {
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
        float coeffs[];
        
        void createGraphs() {

            JPanel oldPanel = graphPanel;

            graphPanel = new JPanel();
            graphPanel.setLayout(new GridLayout(3, 2));

            float srcSampleRate=upBy*targetSampleRate;
            FIRFilterDesign filt = new FIRFilterDesign(alpha, srcSampleRate, frequency, filtType.id, order, winType.id, bandwidth);

            coeffs = filt.getCoefficients();
            overSrc.setUp(upBy, coeffs);
            order = filt.getOrder();

            graphPanel.add(Graphs.timePanel(filt.getRawCoefficients(), srcSampleRate, "Time [s]", "h(t)", "Ideal Impulse response"));
            switch (filtType) {
                case LPF:
                    graphPanel.add(Graphs.xyPanel(new float[]{0, frequency, frequency, srcSampleRate / 2}, new float[]{1, 1, 0, 0}, "Frequency [Hz]", "Attenuation", "Ideal Attenuation"));
                    break;
                case HPF:
                    graphPanel.add(Graphs.xyPanel(new float[]{0, frequency, frequency, srcSampleRate / 2}, new float[]{0, 0, 1, 1}, "Frequency [Hz]", "Attenuation", "Ideal Attenuation"));
                    break;
                case BPF:
                    graphPanel.add(Graphs.xyPanel(new float[]{0, frequency - bandwidth / 2, frequency - bandwidth / 2, frequency + bandwidth / 2, frequency + bandwidth / 2, srcSampleRate / 2}, new float[]{0, 0, 1, 1, 0, 0}, "Frequency [Hz]", "Attenuation", "Ideal Attenuation"));
                    break;


            }
            graphPanel.add(Graphs.timePanel(filt.getWin(), srcSampleRate, "Time [s]", "w(t)", "Window"));
            graphPanel.add(Graphs.fftDBPanel(filt.getWin(), srcSampleRate, "Frequency [Hz]", "Attenuation [dB]", "Fourrier Transform of window"));
            graphPanel.add(Graphs.timePanel(coeffs, srcSampleRate, "Time [s]", "h(t)", "Windowed Impulse response"));
            graphPanel.add(Graphs.fftDBPanel(coeffs, srcSampleRate, "Frequency [Hz]", "Attenuation [dB]", "Final Filter Attenuation"));
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

            c.gridy = row++;
            c.gridx = 0;
            c.gridwidth = 1;

            //  frequency


            final DoubleJSlider freqSlide = new DoubleJSlider(0.0, targetSampleRate / 2, frequency, 100);
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

            transSlide = new DoubleJSlider(10.0, targetSampleRate / 4.0, bandwidth, 10);
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

        private float[] getCoeffs() {
                return coeffs;
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
}
