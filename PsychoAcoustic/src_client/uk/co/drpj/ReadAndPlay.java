package uk.co.drpj;

import uk.co.drpj.audio.DitherProcess;
import uk.co.drpj.audio.AudioSystem;
import uk.co.drpj.audio.QuantizerProcess;
import uk.co.drpj.audio.URLWavReader;
import uk.co.drpj.util.DoubleJSlider;
import com.frinika.audio.io.AudioReader;
import com.frinika.audio.toot.AudioPeakMonitor;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.io.RandomAccessFile;
import java.net.URL;

import javax.swing.JCheckBox;
import javax.swing.JComboBox;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.Timer;
//import uk.ac.bath.audio.AudioPeakMonitor;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;
import uk.org.toot.audio.core.AudioBuffer;
import uk.org.toot.audio.core.AudioProcess;
import uk.org.toot.audio.server.AudioClient;
import uk.org.toot.audio.server.AudioServer;

/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
/**
 *
 * @author pjl
 */
public class ReadAndPlay {

//    private static JavaSoundAudioServer audioServer;
    private static AudioBuffer chunk;
    private static AudioBuffer chunk2;
    private static JFrame frame;
    private static AudioPeakMonitor peakIn;
    private static MeterPanel meterPanel;
    private static AudioProcess audioReader;
    private static QuantizerProcess quantizer;
    private static DitherProcess ditherer;
    private static boolean cancel;
    private static boolean quantizeOn;
    private static boolean ditherOn;

    public static void main(String args[]) throws Exception {

        AudioSystem audioSystem = AudioSystem.instance();


        peakIn = new AudioPeakMonitor();



        RandomAccessFile rafG;
        boolean url = true;




//        if (url) {
            URL u = ((new File("/home/pjl/lect/audio/notes/samples/massive.wav")).toURI()).toURL();
            audioReader = new URLWavReader(u);

//        } else {
//            File file = new File("/home/pjl/Sassy9.wav");
//            rafG = new RandomAccessFile(file, "r");
//            audioReader = new AudioReader(new VanillaRandomAccessFile(rafG), 44100);
//
//        }

        quantizer = new QuantizerProcess();
        ditherer = new DitherProcess();

        AudioServer server = audioSystem.getServer();
        chunk = server.createAudioBuffer("default");
        chunk.setRealTime(true);

        chunk2 = server.createAudioBuffer("default");
        chunk2.setRealTime(true);

        final AudioProcess output = audioSystem.getOut();

        server.setClient(new AudioClient() {

            public void work(int arg0) {
                chunk.makeSilence();

                if (audioReader != null) {
                    if ((audioReader instanceof AudioReader) && ((AudioReader) audioReader).eof()) {
                    } else {
                        audioReader.processAudio(chunk);
                    }
                }

                if (cancel) {
                    int n = chunk.getSampleCount();
                    for (int c = 0; c < chunk.getChannelCount(); c++) {
                        System.arraycopy(chunk.getChannel(c), 0, chunk2.getChannel(c), 0, n);
                    }
                }

                if (ditherOn) {
                    ditherer.processAudio(chunk);
                }

                if (quantizeOn) {
                    quantizer.processAudio(chunk);
                }

                peakIn.processAudio(chunk);

                if (cancel) {
                    int n = chunk.getSampleCount();
                    for (int c = 0; c < chunk.getChannelCount(); c++) {
                        float a[] = chunk.getChannel(c);
                        float b[] = chunk2.getChannel(c);
                        for (int i = 0; i < n; i++) {
                            a[i] = a[i] - b[i];
                        }
                    }
                }

                output.processAudio(chunk);


            }

            public void setEnabled(boolean arg0) {
                //  throw new UnsupportedOperationException("Not supported yet.");
            }
        });
        audioSystem.start();
        configure();


        Timer timer = new Timer(50, new ActionListener() {

            public void actionPerformed(ActionEvent ae) {

                updateMeters();
            }
        });
        timer.start();


    }

    private static void updateMeters() {
        double val = peakIn.getPeak();
        if (val > .99) {
            meterPanel.updateMeter(val, Color.RED);
        } else {
            meterPanel.updateMeter(val, Color.GREEN);
        }

    }
    static int nLevel = (int) Math.pow(2, 16);

    public static void configure() {



        frame = new JFrame();
        JPanel content = new JPanel();



        meterPanel = new MeterPanel();
        content.add(meterPanel);

        final JCheckBox canBut = new JCheckBox("Play Error");

        content.add(canBut);

        canBut.addActionListener(new ActionListener() {

            public void actionPerformed(ActionEvent e) {
                cancel = canBut.isSelected();
            }
        });

        final JCheckBox quant = new JCheckBox("Quantize (bits)");

        Integer bits[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16};

        final JComboBox combo = new JComboBox(bits);

        quant.addActionListener(new ActionListener() {

            public void actionPerformed(ActionEvent e) {
                quantizeOn=quant.isSelected();
            }
        });

        content.add(quant);
        content.add(combo);


        combo.setSelectedIndex(15);
        //  combo.setEnabled(false);

        combo.addActionListener(new ActionListener() {

            public void actionPerformed(ActionEvent e) {
                int n = (Integer) (combo.getSelectedItem());
                nLevel = (int) Math.pow(2, n);
                if (quantizer != null) {
                    quantizer.setNumberOfLevels(nLevel);
                    ditherer.setQuantizelevel(quantizer.getQuant());
                }
            }
        });




        //  dithering

        final JCheckBox dither = new JCheckBox("Dither");
        dither.addActionListener(new ActionListener() {

            public void actionPerformed(ActionEvent e) {
                ditherOn = dither.isSelected();
            }
        });


        final DoubleJSlider amt = new DoubleJSlider(0.0, 1.0, 0.0,100);
        final JLabel amtDisp=new JLabel("0.0000");
        amtDisp.setPreferredSize(new Dimension(80,20));
        amt.addChangeListener(new ChangeListener() {
            public void stateChanged(ChangeEvent e) {
                double val=amt.getDoubleValue();
                ditherer.setDither((float) val);
                amtDisp.setText(String.format("%6.4f",val));
            }
        });


        content.add(dither);
        content.add(amt);
        content.add(amtDisp);





        combo.setSelectedIndex(15);
        //  combo.setEnabled(false);

        combo.addActionListener(new ActionListener() {

            public void actionPerformed(ActionEvent e) {
                int n = (Integer) (combo.getSelectedItem());
                nLevel = (int) Math.pow(2, n);
                if (quantizer != null) {
                    quantizer.setNumberOfLevels(nLevel);
                }
            }
        });




        frame.setAlwaysOnTop(true);
        frame.setContentPane(content);
        frame.pack();
        frame.setVisible(true);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    }
}

class MeterPanel extends JPanel {

    double val = 0.0;
    Color color = null;
    int redcount = 0;

    @Override
    public Dimension getMaximumSize() {
        return new Dimension(10, 100);
    }

    @Override
    public Dimension getPreferredSize() {
        return new Dimension(10, 100);
    }

    void updateMeter(double val, Color col) {
        this.val = val;
        if (color == null || col == Color.RED) {
            color = col;
        }
        repaint();

    }

    @Override
    public void paintComponent(Graphics g) {

        int w = getWidth();
        int h = getHeight();

        if (val <= 0.0) {
            g.setColor(Color.DARK_GRAY);
            g.fillRect(0, 0, w, h);
        } else {
            int h2 = (int) ((1.0 - val) * h);
            g.setColor(Color.DARK_GRAY);
            g.fillRect(0, 0, w, h2);

            if ((redcount + 1) % 4 != 0) {
                g.setColor(color);
            } else {
                g.setColor(Color.WHITE);
            }
            g.fillRect(0, h2, w, h);
        }
        if (color == Color.RED) {
            redcount++;
            if (redcount > 20) {
                color = null;
                redcount = 0;
            }
        } else {
            color = null;
        }
        g.setColor(Color.BLACK);
        g.drawRect(0, 0, w - 1, h - 1);
    }
}
