/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package uk.co.drpj;

import uk.co.drpj.audio.AudioSystem;
import uk.co.drpj.audio.MeterPanel;


import uk.co.drpj.util.DoubleJSlider;
//import com.frinika.audio.gui.MeterPanel;
import com.frinika.audio.toot.AudioPeakMonitor;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Random;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JComboBox;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.Timer;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;


import uk.co.drpj.audio.CycliclyBufferedAudio;
import uk.co.drpj.audio.gui.ScopePanel;
import uk.co.drpj.audio.source.MySource.Wave;
import uk.org.toot.audio.core.AudioBuffer;
import uk.org.toot.audio.core.AudioProcess;
import uk.org.toot.audio.server.AudioClient;
import uk.org.toot.audio.server.AudioServer;

/**
 *
 * @author pjl
 */
public class MaskPanel1 extends JPanel {

    private ScopePanel scopePanel;
    private CycliclyBufferedAudio cyclicBuffer;
    private MaskProcess maskProcess;
    private AudioBuffer outChunk;
    private AudioPeakMonitor peakIn;
    private MeterPanel meterPanel;
    AudioSystem audioSystem;
    JLabel maskFreqDisp;
    private JLabel sigFreqDisp;
    private DoubleJSlider sigFreqSlide;
    private DoubleJSlider srcAmpSlide;
    private DoubleJSlider maskAmpSlide;
    private DoubleJSlider maskFreqSlide;
    private JComboBox noiseCombo;
    private JLabel maskAmpDisp;
    private JLabel srcAmpDisp;
    private DoubleJSlider maskBWSlide;
    private JLabel maskBWDisp;
    //private final float Fs;
    private boolean beep;
    private float Fs;
    private JCheckBox scopeOn;

    public MaskPanel1() throws Exception {

   //     setBackground(null);
        setLayout(new BorderLayout());


        audioSystem = AudioSystem.instance();

        peakIn = new AudioPeakMonitor();


        AudioServer server = audioSystem.getServer();
        outChunk = server.createAudioBuffer("OUT");
        outChunk.setRealTime(true);

        Fs = server.getSampleRate();

        System.out.println(" Fs = " + Fs);

        final AudioProcess output = audioSystem.getOut();

        maskProcess = new MaskProcess();

        //final AudioProcess src=new MySource();

        cyclicBuffer = new CycliclyBufferedAudio(100000, Fs);

        server.setClient(new AudioClient() {

            public void work(int size) {

                if (outChunk == null || outChunk.getSampleCount() != size) {
                    outChunk = new AudioBuffer(null, 2, size, Fs);
                    outChunk.setRealTime(true);
                }

                outChunk.makeSilence();
                maskProcess.processAudio(outChunk);
                peakIn.processAudio(outChunk);
                output.processAudio(outChunk);
                cyclicBuffer.processAudio(outChunk);
            }

            public void setEnabled(boolean arg0) {
                //  throw new UnsupportedOperationException("Not supported yet.");
            }
        });

        configureGUI();
        update();

    }

    public void start() {
        try {
            audioSystem.start();
        } catch (Exception ex) {
            Logger.getLogger(MaskPanel1.class.getName()).log(Level.SEVERE, null, ex);
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
        if (meterPanel != null) {
            double val = peakIn.getPeak();
            if (val > .99999) {
                meterPanel.updateMeter(val, Color.RED);
            } else {
                meterPanel.updateMeter(val, Color.GREEN);
            }
        }
        scopePanel.repaint();
        //    float freq = maskSrc.getFreq();
        //     maskFreqDisp.setText(String.format("%9.3f kHz", freq / 1000));
    }
    int nLevel = (int) Math.pow(2, 16);

    public void configureGUI() {

        //    frame = new JFrame();




        //   JPanel content = new JPanel();

        GridBagConstraints c1 = new GridBagConstraints();

        setLayout(new GridBagLayout());

        c1.gridx = 0;
        c1.gridy = 0;
        c1.weightx = 0.0;
        c1.weighty = 0.0;

        scopeOn = new JCheckBox("Show scope");

        scopeOn.addActionListener(new ActionListener() {

            public void actionPerformed(ActionEvent e) {
                scopePanel.setOn(scopeOn.isSelected());

            }
        });
        scopeOn.setSelected(true);
        add(scopeOn, c1);

        //        c1.weightx = 0.0;
//        c1.weighty = 1.0;
//        c1.fill=GridBagConstraints.VERTICAL;
//
//        meterPanel = new MeterPanel();
//        meterPanel.setMinimumSize(new Dimension(50, 20));
//        meterPanel.setPreferredSize(new Dimension(50, 20));
//        add(meterPanel, c1);
//
        c1.gridx = 1;
        c1.gridy = 0;
        c1.gridwidth = GridBagConstraints.REMAINDER;
        c1.weightx = 1.0;
        c1.weighty = 1.0;
        c1.fill = GridBagConstraints.BOTH;
        scopePanel = new ScopePanel(cyclicBuffer, (int) Fs);

        add(scopePanel, c1);

        c1.weightx = 0.0;
        c1.weighty = 0.0;


        c1.gridy = 1;
        c1.gridx = 0;
        c1.gridwidth = GridBagConstraints.REMAINDER;
        JPanel cntrlPanel = createControlPanel();
        add(cntrlPanel, c1);
    }

    JPanel createControlPanel() {

        ActionListener updater = new ActionListener() {

            public void actionPerformed(ActionEvent e) {
                update();
            }
        };

        ChangeListener cupdater = new ChangeListener() {

            public void stateChanged(ChangeEvent e) {
                update();
            }
        };
        JPanel cntrlPanel = new JPanel();

        GridBagConstraints c = new GridBagConstraints();
        cntrlPanel.setLayout(new GridBagLayout());

        Wave wavs[] = {Wave.SIN, Wave.NOISE};

        noiseCombo = new JComboBox(wavs);

        noiseCombo.setSelectedIndex(1);
        noiseCombo.addActionListener(updater);

        c.gridy = 0;
        c.gridx = 0;
        c.gridwidth = GridBagConstraints.REMAINDER;
        c.fill = GridBagConstraints.HORIZONTAL;

        cntrlPanel.add(noiseCombo, c);

        //  Mask frequency

        maskFreqSlide = new DoubleJSlider(0.0, 10000.0, 3000.0, 100);
        maskFreqDisp = new JLabel();
        maskFreqDisp.setPreferredSize(new Dimension(80, 20));
        maskFreqSlide.addChangeListener(cupdater);
        c.gridy++;
        c.gridwidth = 1;
        c.gridx = 0;
        cntrlPanel.add(new JLabel("Mask Freq"), c);
        c.gridx++;
        cntrlPanel.add(maskFreqSlide, c);
        c.gridx++;
        cntrlPanel.add(maskFreqDisp, c);



        maskBWSlide = new DoubleJSlider(10, 10000.0, 500.0, 10);
        maskBWDisp = new JLabel();
        maskBWDisp.setPreferredSize(new Dimension(80, 20));
        maskBWSlide.addChangeListener(cupdater);
        c.gridy++;
        c.gridwidth = 1;
        c.gridx = 0;
        cntrlPanel.add(new JLabel("Mask BW"), c);
        c.gridx++;
        cntrlPanel.add(maskBWSlide, c);
        c.gridx++;
        cntrlPanel.add(maskBWDisp, c);


        //  Mask AMP -----------------------------------------------------


        maskAmpSlide = new DoubleJSlider(-90.0, .0, -10, 1);
        maskAmpDisp = new JLabel();
        maskAmpDisp.setPreferredSize(new Dimension(80, 20));
        maskAmpSlide.addChangeListener(cupdater);

        c.gridy++;
        c.gridwidth = 1;
        c.gridx = 0;

        cntrlPanel.add(new JLabel("Mask Amp"), c);
        c.gridx++;

        cntrlPanel.add(maskAmpSlide, c);
        c.gridx++;
        cntrlPanel.add(maskAmpDisp, c);



        // Src

        srcAmpSlide = new DoubleJSlider(-90.0, .0, -20, 1);
        srcAmpDisp = new JLabel();
        srcAmpDisp.setPreferredSize(new Dimension(80, 20));


        srcAmpSlide.addChangeListener(cupdater);


        c.gridy++;
        c.gridwidth = 1;
        c.gridx = 0;

        cntrlPanel.add(new JLabel("Src Amp"), c);
        c.gridx++;

        cntrlPanel.add(srcAmpSlide, c);
        c.gridx++;

        cntrlPanel.add(srcAmpDisp, c);



        sigFreqSlide = new DoubleJSlider(0.0, 10000.0, 3000.0, 100);
        sigFreqDisp = new JLabel();
        sigFreqDisp.setPreferredSize(new Dimension(80, 20));



        sigFreqSlide.addChangeListener(cupdater);

        c.gridy++;
        c.gridwidth = 1;
        c.gridx = 0;

        cntrlPanel.add(new JLabel("Signal Freq"), c);
        c.gridx++;

        cntrlPanel.add(sigFreqSlide, c);
        c.gridx++;

        cntrlPanel.add(sigFreqDisp, c);


        //---- DO IT BUTTON
        JButton doit = new JButton("BOTH ");

        doit.addActionListener(new ActionListener() {

            public void actionPerformed(ActionEvent e) {

                maskProcess.doBoth();
            }
        });

        c.gridy++;
        c.gridwidth = GridBagConstraints.REMAINDER;
        c.gridx = 0;

        cntrlPanel.add(doit, c);

        //---- DO IT BEEP BUTTON
        JButton doitBeep = new JButton("BEEP");

        doitBeep.addActionListener(new ActionListener() {

            public void actionPerformed(ActionEvent e) {
                maskProcess.doBeep();
            }
        });


        c.gridy++;
        c.gridwidth = GridBagConstraints.REMAINDER;
        c.gridx = 0;

        cntrlPanel.add(doitBeep, c);

        //---- DO IT BEEP BUTTON
        JButton doitMASK = new JButton("MASK");

        doitMASK.addActionListener(new ActionListener() {

            public void actionPerformed(ActionEvent e) {
                maskProcess.doMask();
            }
        });


        c.gridy++;
        c.gridwidth = GridBagConstraints.REMAINDER;
        c.gridx = 0;

        cntrlPanel.add(doitMASK, c);



        //---- DO IT BEEP BUTTON
        JButton doitRand = new JButton("?");

        final JLabel showLab = new JLabel("   ");
        final Random rand = new Random();

        doitRand.addActionListener(new ActionListener() {

            public void actionPerformed(ActionEvent e) {
                beep = maskProcess.doRandom();

                showLab.setText(" ? ");
            }
        });

        c.gridx = 0;
        c.gridy++;
        c.gridwidth = 1;

        cntrlPanel.add(doitRand, c);


        JButton doitShow = new JButton("SHOW");

        doitShow.addActionListener(new ActionListener() {

            public void actionPerformed(ActionEvent e) {
                if (beep) {
                    showLab.setText("yes");
                } else {
                    showLab.setText("no ");
                }
            }
        });

        c.gridx++;
        cntrlPanel.add(doitShow, c);

        c.gridx++;
        cntrlPanel.add(showLab, c);


        return cntrlPanel;


    }

    void update() {

        float sigFreq = (float) sigFreqSlide.getDoubleValue();
        float sigAmpDB = (float) srcAmpSlide.getDoubleValue();
        float sigAmp = (float) valFromLog10(sigAmpDB);

        srcAmpDisp.setText(String.format("%4.0f dB", sigAmpDB));
        sigFreqDisp.setText(String.format("%6.0f Hz", sigFreq));


        Wave maskType = (Wave) noiseCombo.getSelectedItem();
        float maskFreq = (float) maskFreqSlide.getDoubleValue();

        maskFreqDisp.setText(String.format("%6.0f Hz", maskFreq));
        float valF = (float) maskFreqSlide.getDoubleValue();
        maskFreqDisp.setText(String.format("%6.0f Hz", valF));


        float maskBW = (float) maskBWSlide.getDoubleValue();

        maskBWDisp.setText(String.format("%6.0f Hz", maskBW));

        float maskAmpDB = (float) maskAmpSlide.getDoubleValue();
        float maskAmp = valFromLog10(maskAmpDB);

        maskAmpDisp.setText(String.format("%4.0f dB", maskAmpDB));

        maskProcess.update(sigFreq, sigAmp, maskType, maskFreq, maskBW, maskAmp);

    }

    void dispose() {

        audioSystem.stop();

    }

    float valFromLog10(double val) {
        return (float) Math.pow(10.0, val / 20.0);
    }
}
