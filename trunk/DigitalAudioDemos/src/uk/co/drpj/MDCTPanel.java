/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package uk.co.drpj;

import uk.co.drpj.audio.AudioSystem;
//import uk.co.drpj.audio.DitherProcess;
import uk.co.drpj.audio.MeterPanel;
import uk.co.drpj.audio.MDCTProcess;
import uk.co.drpj.util.DoubleJSlider;
//import com.frinika.audio.gui.MeterPanel;
import com.frinika.audio.io.AudioReader;
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
import javax.swing.Timer;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;
//import uk.co.drpj.audio.CycliclyBufferedAudio;
import uk.co.drpj.audio.CycliclyBufferedAudio1;
import uk.org.toot.audio.core.AudioBuffer;
import uk.org.toot.audio.core.AudioProcess;
import uk.org.toot.audio.server.AudioClient;
import uk.org.toot.audio.server.AudioServer;

/**
 *
 * @author pjl
 */
public class MDCTPanel extends JPanel {

    //    private static JavaSoundAudioServer audioServer;
    private AudioBuffer chunk;
   // private AudioBuffer chunk2;
    // private  JFrame frame;
    private AudioPeakMonitor peakIn;
    private MeterPanel meterPanel;
    private AudioProcess audioReader;
    private MDCTProcess mdctizer;
//    private DitherProcess ditherer;
    private boolean cancel;
    private boolean quantizeOn = true;
    private boolean ditherOn = true;
    AudioSystem audioSystem;
    private JLabel qlab;
    final Object readerMuex = new Object();
    private Timer timer;

    public MDCTPanel() throws Exception {

        setLayout(new BorderLayout());


        audioSystem = AudioSystem.instance();
        //    audioSystem.getServer().

        peakIn = new AudioPeakMonitor();


        mdctizer = new MDCTProcess();
        //    ditherer = new DitherProcess();

        AudioServer server = audioSystem.getServer();

        final AudioProcess output = audioSystem.getOut();
        final float sampleRate = 44100.0f;
        final AudioBuffer readChunk = new AudioBuffer(null, 2, 128, sampleRate);
        final AudioBuffer mdctChunk = new AudioBuffer(null, 2, 128, sampleRate);

        server.setClient(new AudioClient() {

            int frameSize = 0;
            CycliclyBufferedAudio1 inbuff = new CycliclyBufferedAudio1(10000, sampleRate);
            CycliclyBufferedAudio1 outbuff = new CycliclyBufferedAudio1(10000, sampleRate);

            public void work(int size) {

                if (chunk == null || size != frameSize) {
                    frameSize = size;
                    chunk = new AudioBuffer(null, 2, size, 44100.0f);
                    // chunk2 = new AudioBuffer(null, 2, size, 44100.0f);
                    chunk.setRealTime(true);
                }

                chunk.makeSilence();


                // Fill input buffer
              //  System.out.println(" FILLING INPUT ");
                while (inbuff.freeSpace() > size) {
                    synchronized (readerMuex) {
                        if (audioReader != null) {
                            if ((audioReader instanceof AudioReader) && ((AudioReader) audioReader).eof()) {
                            } else {
                                readChunk.makeSilence();
                                audioReader.processAudio(readChunk);
                                inbuff.in.processAudio(readChunk);
                            }
                        }
                    }
                }


           //     System.out.println(" FILLING OUTPUT ");

                while(outbuff.avail() < chunk.getSampleCount()) {
                    inbuff.out.processAudio(mdctChunk);  // grab chunk
                    mdctizer.processAudio(mdctChunk);
                    outbuff.in.processAudio(mdctChunk);
                }

                outbuff.out.processAudio(chunk);

//                if (cancel) {
//                    int n = chunk.getSampleCount();
//                    for (int c = 0; c < chunk.getChannelCount(); c++) {
//                        System.arraycopy(chunk.getChannel(c), 0, chunk2.getChannel(c), 0, n);
//                    }
//                }

           //     System.out.println(" PLAYING OUTPUT ");

                peakIn.processAudio(chunk);

//                if (cancel) {
//                    int n = chunk.getSampleCount();
//                    for (int c = 0; c < chunk.getChannelCount(); c++) {
//                        float a[] = chunk.getChannel(c);
//                        float b[] = chunk2.getChannel(c);
//                        for (int i = 0; i < n; i++) {
//                            a[i] = a[i] - b[i];
//                        }
//                    }
//                }

                output.processAudio(chunk);


            }

            public void setEnabled(boolean arg0) {
                //  throw new UnsupportedOperationException("Not supported yet.");
            }
        });
        configureGUI();
    }

    public void start() {
        try {
            audioSystem.start();
        } catch (Exception ex) {
            Logger.getLogger(MDCTPanel.class.getName()).log(Level.SEVERE, null, ex);
        }



        timer = new Timer(50, new ActionListener() {

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

    }
    int nLevel = (int) Math.pow(2, 16);

    public void setAudioReader(AudioProcess reader) {
        synchronized (readerMuex) {
            audioReader = reader;
        }
    }

    public void configureGUI() {


        //    frame = new JFrame();
        JPanel content = new JPanel();
        content.setLayout(new BorderLayout());

        meterPanel = new MeterPanel();
        meterPanel.setMinimumSize(new Dimension(50, 20));
        meterPanel.setPreferredSize(new Dimension(50, 20));
        content.add(meterPanel, BorderLayout.WEST);


        JPanel side = new JPanel();
        side.setLayout(new BoxLayout(side, BoxLayout.Y_AXIS));
        content.add(side, BorderLayout.CENTER);

        JPanel tt = new JPanel(new FlowLayout(FlowLayout.LEFT));

        final JCheckBox canBut = new JCheckBox("Just play error");
        tt.add(canBut);
        tt.add(Box.createHorizontalGlue());
        side.add(tt);
        canBut.addActionListener(new ActionListener() {

            public void actionPerformed(ActionEvent e) {
                cancel = canBut.isSelected();
            }
        });



        final JCheckBox quant = new JCheckBox("Quantize");

        Integer bits[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16};

        final JComboBox combo = new JComboBox(bits);

        quant.addActionListener(new ActionListener() {

            public void actionPerformed(ActionEvent e) {
                quantizeOn = quant.isSelected();
            }
        });

        tt = new JPanel(new FlowLayout(FlowLayout.LEFT));

        tt.add(quant);
        tt.add(combo);
        //   tt.add(qlab = new JLabel(String.format("(q=%7.2g)", mdctizer.getQuant())));
        //tt.add(Box.createHorizontalGlue());

        side.add(tt);

        combo.setSelectedIndex(15);
        //  combo.setEnabled(false);
        combo.addActionListener(new ActionListener() {

            public void actionPerformed(ActionEvent e) {
                int n = (Integer) (combo.getSelectedItem());
                nLevel = (int) Math.pow(2, n);
                if (mdctizer != null) {
                    for (int i = 0; i < mdctizer.getBandCount(); i++) {
                        mdctizer.setNumberOfLevels(nLevel, i);
                    }
                    //        ditherer.setQuantizelevel(mdctizer.getQuant());
                    //         qlab.setText(String.format("(q=%7.1g)", mdctizer.getQuant()));
                }
            }
        });




        //  dithering

        tt = new JPanel(new FlowLayout(FlowLayout.LEFT));
        final DoubleJSlider amt = new DoubleJSlider(0.0, 1.0, 0.0, .1);
        final JLabel amtDisp = new JLabel("disabled");
        amtDisp.setPreferredSize(new Dimension(80, 20));

        final JCheckBox dither = new JCheckBox("Dither");
        dither.addActionListener(new ActionListener() {

            public void actionPerformed(ActionEvent e) {
                ditherOn = dither.isSelected();
                double val = amt.getDoubleValue();
                //      ditherer.setDither((float) val);
                if (ditherOn) {
                    amtDisp.setText(String.format("%6.3f*q", val));
                } else {
                    amtDisp.setText(String.format("disabled", val));
                }
            }
        });



        amt.addChangeListener(new ChangeListener() {

            public void stateChanged(ChangeEvent e) {
                double val = amt.getDoubleValue();
                //     ditherer.setDither((float) val);
                if (ditherOn) {
                    amtDisp.setText(String.format("%6.3f*q", val));
                } else {
                    amtDisp.setText(String.format("disabled", val));
                }
            }
        });


        tt.add(dither);
        tt.add(amt);
        tt.add(amtDisp);
        side.add(tt);

        combo.setSelectedIndex(15);
        //  combo.setEnabled(false);

        combo.addActionListener(new ActionListener() {

            public void actionPerformed(ActionEvent e) {
                int n = (Integer) (combo.getSelectedItem());
                nLevel = (int) Math.pow(2, n);
                if (mdctizer != null) {
                    for (int i = 0; i < mdctizer.getBandCount(); i++) {
                        mdctizer.setNumberOfLevels(nLevel, i);
                    }
                }
            }
        });
        add(content, BorderLayout.CENTER);
        dither.setSelected(true);
        quant.setSelected(true);
    }

    void dispose() {
        audioSystem.stop();
        timer.stop();
        timer = null;
    }
}
