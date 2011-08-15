/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package uk.co.drpj;

import uk.co.drpj.audio.AudioSystem;
import uk.co.drpj.audio.MeterPanel;

import uk.co.drpj.audio.source.EnvelopeProcess;

import uk.co.drpj.audio.source.TickReference;
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
import javax.swing.JComboBox;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.Timer;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;


import uk.co.drpj.audio.FIRFilter;
import uk.co.drpj.audio.FIRFilterDesign;
import uk.co.drpj.audio.source.MySource;
import uk.co.drpj.audio.source.MySource.Wave;
import uk.org.toot.audio.core.AudioBuffer;
import uk.org.toot.audio.core.AudioProcess;
import uk.org.toot.audio.server.AudioClient;
import uk.org.toot.audio.server.AudioServer;

/**
 *
 * @author pjl
 */
public class MaskPanel extends JPanel {

    private AudioBuffer maskChunk;
    private AudioBuffer signalChunk;
    private AudioBuffer outChunk;
    private AudioPeakMonitor peakIn;
    private MeterPanel meterPanel;
    AudioSystem audioSystem;
    private final MySource maskSrc;
    private final MySource signalSrc;
    private final EnvelopeProcess maskEnv;
    private final EnvelopeProcess signalEnv;
    private TickReference ref;
    private long currentTick;
    JLabel maskFreqDisp;
    private long nWait;
    private int nRel;
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
    private boolean beep;
    private boolean mask;
    private final FIRFilter filt; 
    private final float Fs;

    public MaskPanel() throws Exception {

        setLayout(new BorderLayout());


        audioSystem = AudioSystem.instance();


        peakIn = new AudioPeakMonitor();


        AudioServer server = audioSystem.getServer();

        Fs = server.getSampleRate();

        System.out.println(" Fs = " + Fs);

        final AudioProcess output = audioSystem.getOut();

        ref = new TickReference() {

            public long getCurrentTick() {
                return currentTick;
            }
        };

        nWait = (long) (Fs / 4.0);

        maskSrc = new MySource();
        maskSrc.setWave(MySource.Wave.NOISE);
        maskEnv = new EnvelopeProcess(ref);
        filt = new FIRFilter();

        signalSrc = new MySource();
        signalSrc.setWave(MySource.Wave.SIN);
        signalEnv = new EnvelopeProcess(ref);


        float tSigWidth = 100e-3f;
        float tRise = tSigWidth / 3;
        float tMaskOn = 5 * tSigWidth;
        float tRel = tMaskOn * 0.4f;


        int nWidth = (int) (Fs * tSigWidth);
        int nRise = (int) (Fs * tRise);
        int nMask = (int) (Fs * tMaskOn);
        nRel = (int) (Fs * tRel);

        maskEnv.setNRise(nRise);
        maskEnv.setTicksOn(nMask);

        signalEnv.setNRise(nRise);
        signalEnv.setTicksOn(nWidth);

        server.setClient(new AudioClient() {

            int frameSize = 0;
            float a[];
            float b[];
            float c[][] = new float[2][];

            public void work(int size) {

                if (maskChunk == null || size != frameSize) {
                    frameSize = size;
                    maskChunk = new AudioBuffer(null, 1, size, 44100.0f);
                    maskChunk.setRealTime(true);
                    signalChunk = new AudioBuffer(null, 1, size, 44100.0f);
                    signalChunk.setRealTime(true);
                    outChunk = new AudioBuffer(null, 2, size, 44100.0f);
                    outChunk.setRealTime(true);

                    a = maskChunk.getChannel(0);
                    b = signalChunk.getChannel(0);

                    c[0] = outChunk.getChannel(0);
                    c[1] = outChunk.getChannel(1);
                }


                maskChunk.makeSilence();
                signalChunk.makeSilence();

                if (mask) {
                    maskSrc.processAudio(maskChunk);
                    filt.processAudio(maskChunk);
                    maskEnv.processAudio(maskChunk);
                }

                if (beep) {
                    signalSrc.processAudio(signalChunk);
                    signalEnv.processAudio(signalChunk);
                }

                for (int i = 0; i < size; i++) {
                    c[0][i] = c[1][i] = b[i] + a[i];
                }

                peakIn.processAudio(outChunk);
                output.processAudio(outChunk);
                currentTick += size;
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
            Logger.getLogger(MaskPanel.class.getName()).log(Level.SEVERE, null, ex);
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
        if (val > .99999) {
            meterPanel.updateMeter(val, Color.RED);
        } else {
            meterPanel.updateMeter(val, Color.GREEN);
        }
        //    float freq = maskSrc.getFreq();
        //     maskFreqDisp.setText(String.format("%9.3f kHz", freq / 1000));
    }
    int nLevel = (int) Math.pow(2, 16);

    public void configureGUI() {

        //    frame = new JFrame();


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

        JPanel content = new JPanel();
        content.setLayout(new BorderLayout());

        meterPanel = new MeterPanel();
        meterPanel.setMinimumSize(new Dimension(50, 20));
        meterPanel.setPreferredSize(new Dimension(50, 20));
        content.add(meterPanel, BorderLayout.WEST);


        JPanel side = new JPanel();

        GridBagConstraints c = new GridBagConstraints();
        side.setLayout(new GridBagLayout());
        content.add(side, BorderLayout.CENTER);

        Wave wavs[] = {Wave.SIN, Wave.NOISE};

        noiseCombo = new JComboBox(wavs);

        noiseCombo.setSelectedIndex(1);
        noiseCombo.addActionListener(updater);

        c.gridy = 0;
        c.gridx = 0;
        c.gridwidth = GridBagConstraints.REMAINDER;
        c.fill=GridBagConstraints.HORIZONTAL;
        
        side.add(noiseCombo, c);

        //  Mask frequency

        maskFreqSlide = new DoubleJSlider(0.0, 10000.0, 1000.0, 100);
        maskFreqDisp = new JLabel();
        maskFreqDisp.setPreferredSize(new Dimension(80, 20));
        maskFreqSlide.addChangeListener(cupdater);
        c.gridy++;
        c.gridwidth = 1;
        c.gridx = 0;
        side.add(new JLabel("Mask Freq"), c);
        c.gridx++;
        side.add(maskFreqSlide, c);
        c.gridx++;
        side.add(maskFreqDisp, c);



        maskBWSlide = new DoubleJSlider(10, 10000.0, 500.0, 100);
        maskBWDisp = new JLabel();
        maskBWDisp.setPreferredSize(new Dimension(80, 20));
        maskBWSlide.addChangeListener(cupdater);
        c.gridy++;
        c.gridwidth = 1;
        c.gridx = 0;
        side.add(new JLabel("Mask BW"), c);
        c.gridx++;
        side.add(maskBWSlide, c);
        c.gridx++;
        side.add(maskBWDisp, c);


        //  Mask AMP -----------------------------------------------------


        maskAmpSlide = new DoubleJSlider(-90.0, .0, -10, 100);
        maskAmpDisp = new JLabel();
        maskAmpDisp.setPreferredSize(new Dimension(80, 20));
        maskAmpSlide.addChangeListener(cupdater);

        c.gridy++;
        c.gridwidth = 1;
        c.gridx = 0;

        side.add(new JLabel("Mask Amp"), c);
        c.gridx++;

        side.add(maskAmpSlide, c);
        c.gridx++;
        side.add(maskAmpDisp, c);





        // Src

        srcAmpSlide = new DoubleJSlider(-90.0, .0, -20, 100);
        srcAmpDisp = new JLabel();
        srcAmpDisp.setPreferredSize(new Dimension(80, 20));


        srcAmpSlide.addChangeListener(cupdater);


        c.gridy++;
        c.gridwidth = 1;
        c.gridx = 0;

        side.add(new JLabel("Src Amp"), c);
        c.gridx++;

        side.add(srcAmpSlide, c);
        c.gridx++;

        side.add(srcAmpDisp, c);



        sigFreqSlide = new DoubleJSlider(0.0, 10000.0, 1000.0, 100);
        sigFreqDisp = new JLabel();
        sigFreqDisp.setPreferredSize(new Dimension(80, 20));



        sigFreqSlide.addChangeListener(cupdater);

        c.gridy++;
        c.gridwidth = 1;
        c.gridx = 0;

        side.add(new JLabel("Signal Freq"), c);
        c.gridx++;

        side.add(sigFreqSlide, c);
        c.gridx++;

        side.add(sigFreqDisp, c);


        //---- DO IT BUTTON
        JButton doit = new JButton("BOTH ");

        doit.addActionListener(new ActionListener() {

            public void actionPerformed(ActionEvent e) {
                beep = true;
                mask = true;

                long tickOn = ref.getCurrentTick() + nWait;
                maskEnv.setFireAt(tickOn);
                signalEnv.setFireAt(tickOn + nRel);
            }
        });

        c.gridy++;
        c.gridwidth = GridBagConstraints.REMAINDER;
        c.gridx = 0;

        side.add(doit, c);

        //---- DO IT BEEP BUTTON
        JButton doitBeep = new JButton("BEEP");

        doitBeep.addActionListener(new ActionListener() {

            public void actionPerformed(ActionEvent e) {
                beep = true;
                mask = false;
                long tickOn = ref.getCurrentTick() + nWait;
                maskEnv.setFireAt(tickOn);
                signalEnv.setFireAt(tickOn + nRel);
            }
        });


        c.gridy++;
        c.gridwidth = GridBagConstraints.REMAINDER;
        c.gridx = 0;

        side.add(doitBeep, c);

             //---- DO IT BEEP BUTTON
        JButton doitMASK = new JButton("MASK");

        doitMASK.addActionListener(new ActionListener() {

            public void actionPerformed(ActionEvent e) {
                beep = false;
                mask = true;
                long tickOn = ref.getCurrentTick() + nWait;
                maskEnv.setFireAt(tickOn);
                signalEnv.setFireAt(tickOn + nRel);
            }
        });


        c.gridy++;
        c.gridwidth = GridBagConstraints.REMAINDER;
        c.gridx = 0;

        side.add(doitMASK, c);



             //---- DO IT BEEP BUTTON
        JButton doitRand = new JButton("?");

        final JLabel showLab=new JLabel("   ");
        final Random rand=new Random();
        
        doitRand.addActionListener(new ActionListener() {

            public void actionPerformed(ActionEvent e) {
                beep = rand.nextFloat() > 0.5;
                mask = true;
                long tickOn = ref.getCurrentTick() + nWait;
                maskEnv.setFireAt(tickOn);
                signalEnv.setFireAt(tickOn + nRel);
                showLab.setText(" ? ");
            }
        });

        c.gridx=0;
        c.gridy++;
        c.gridwidth=1;

        side.add(doitRand, c);


        JButton doitShow= new JButton("SHOW");

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
        side.add(doitShow, c);

        c.gridx++;
        side.add(showLab, c);


        add(content, BorderLayout.CENTER);


    }

    void update() {

        double valDisp;
        double val = sigFreqSlide.getDoubleValue();
        signalSrc.setFreq(val);


        val = valFromLog10(valDisp = srcAmpSlide.getDoubleValue());
        signalSrc.setAmp(val);
        srcAmpDisp.setText(String.format("%4.0f dB", valDisp));

        val = sigFreqSlide.getDoubleValue();
        signalSrc.setFreq(val);
        sigFreqDisp.setText(String.format("%6.0f Hz", val));


        Wave o = (Wave) noiseCombo.getSelectedItem();
        maskSrc.setWave(o);

        if (o != Wave.NOISE) {
            val = maskFreqSlide.getDoubleValue();
            maskSrc.setFreq(val);
            maskFreqDisp.setText(String.format("%6.0f Hz", val));
            filt.setCoeffs(null);
        } else {

            float valF = (float) maskFreqSlide.getDoubleValue();
            maskFreqDisp.setText(String.format("%6.0f Hz", valF));


            float valBW= (float) maskBWSlide.getDoubleValue();
          //  float valBW=valF/valQ;
            //maskSrc.setBW(val);
            maskBWDisp.setText(String.format("%6.0f Hz", valBW));

            int order=256;
            float alpha=10.0f;

            FIRFilterDesign filtDesign = new FIRFilterDesign(alpha, Fs, valF, FIRFilterDesign.BPF, order,
                    FIRFilterDesign.KAISER, valBW);

            float coeffs[] = filtDesign.getCoefficients();

            filt.setCoeffs(coeffs);
        }

        val = valFromLog10(valDisp = maskAmpSlide.getDoubleValue());
        maskSrc.setAmp(val);
        maskAmpDisp.setText(String.format("%4.0f dB", valDisp));


    }

    void dispose() {
        audioSystem.stop();
    }

    double valFromLog10(double val) {
        return Math.pow(10.0, val / 20.0);
    }
}
