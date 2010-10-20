/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package uk.co.drpj;

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
import javax.swing.JComboBox;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.Timer;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;
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
    float sampleRate;
    private JLabel ampDisp;

    public AliasPanel() throws Exception {

        setLayout(new BorderLayout());



        audioSystem = AudioSystem.instance();


        peakIn = new AudioPeakMonitor();


        src = new MyFreqDampedSource();


        AudioServer server = audioSystem.getServer();

        final AudioProcess output = audioSystem.getOut();
        sampleRate=server.getSampleRate();

        server.setClient(new AudioClient() {

            int frameSize = 0;

            public void work(int size) {

                if (chunk == null || size != frameSize) {
                    frameSize = size;
                    chunk = new AudioBuffer(null, 2, size, sampleRate);

                    chunk.setRealTime(true);
                }
                chunk.makeSilence();
                src.processAudio(chunk);
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
        ampDisp.setText( String.format("    %5.3f ", src.getAmp()));

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

        MyFreqDampedSource.Wave wavs[] = {MyFreqDampedSource.Wave.SAW, MyFreqDampedSource.Wave.SIN, MyFreqDampedSource.Wave.SQUARE,MyFreqDampedSource.Wave.NOISE};


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

        JLabel rateLabel=new JLabel(" Sample rate (Fs) is " + sampleRate/1000.0+ " kHz");


        JPanel freqPanel = new JPanel(new FlowLayout(FlowLayout.LEFT));


        //  frequency

        freqPanel = new JPanel(new FlowLayout(FlowLayout.LEFT));
        final DoubleJSlider freqSlide = new DoubleJSlider(0.0, 1.5*sampleRate, 0.0, 1.0);
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


        JPanel center=new JPanel();

        center.setLayout(new BoxLayout(center,BoxLayout.Y_AXIS));
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

        center.add(ampPanel);
      
        center.add(Box.createVerticalGlue());
        center.add(rateLabel);


        content.add(center, BorderLayout.CENTER);
        add(content);
        

    }

    void dispose() {
        audioSystem.stop();
    }
}
