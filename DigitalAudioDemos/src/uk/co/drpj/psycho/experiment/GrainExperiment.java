 /* 
 * Created on Mar 6, 2007
 *
 * Copyright (c) 2006 P.J.Leonard
 * 
 * http://www.frinika.com
 *  
 * This file is part of Frinika.
 * 
 * Frinika is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or 
 * (at your option) any later version.

 * Frinika is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.

 * You should have received a copy of the GNU General Public License
 * along with Frinika; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */
package uk.co.drpj.psycho.experiment;

import java.awt.BorderLayout;
import java.util.Date;
import java.util.Observable;
import java.util.Observer;
import java.util.Vector;

import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.SpringLayout;

import edu.cornell.lassp.houle.RngPack.Ranlux;

import rasmus.interpreter.sampled.util.FFT;

import uk.ac.bath.gui.SpinTweaker;
import uk.ac.bath.util.Tweakable;
import uk.ac.bath.util.TweakableDouble;
import uk.org.toot.audio.core.AudioBuffer;

/**
 *
 * Make random grains.
 *
 * @author pjl
 */
public class GrainExperiment extends ThreeChoiceExperiment {

    // LowFreqQProcess ping;
    final double fs;
    JPanel panel = new JPanel();
    Vector<Tweakable> tweaks = new Vector<Tweakable>();
    final TweakableDouble dur = new TweakableDouble(tweaks, 1, 1000, 100, 1,
            " length [mS]");
    // final TweakableDouble period = new TweakableDouble(tweaks,0 , 200, 50, 1,
    // " period [mS]");
    // final TweakableDouble pulselen = new TweakableDouble(tweaks,0, 200, 10,
    // 1, " pulse length [mS]");
    // final TweakableDouble amp = new TweakableDouble(tweaks,0.0, 1.0, 1.0, .1,
    // "Amp");
    // private double tolHigh=0.2;
    double tolNow = 0.1;

    // private double tolLow=0.0;
    // private double damp = 0.2;
    public GrainExperiment(final MyAudioClient client) {
        super(client);

        // JFrame frame = new JFrame();
        // frame.setLocationRelativeTo(null);
        // frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        //
        // SpringLayout layout=new SpringLayout();

        JPanel tw = makeTweakPanel(tweaks);
        audioProcess = new GrainProcess(client);

        dur.addObserver(new Observer() {

            public void update(Observable arg0, Object arg1) {
                ((GrainProcess) audioProcess).setDuration(dur.doubleValue());
            }
        });

        ((GrainProcess) audioProcess).setDuration(dur.doubleValue());

        ((GrainProcess) audioProcess).makePulse();

        JPanel cntrlPanel = new JPanel();

        cntrlPanel.setLayout(new BorderLayout());
        cntrlPanel.add(tw, BorderLayout.NORTH);
        this.fs = client.getSampleRate();

        client.addInput(audioProcess);

        panel.add(threeChoicePanel(), BorderLayout.SOUTH);
        panel.add(cntrlPanel);
        // frame.setContentPane(panel);
        // frame.pack();
        // frame.setVisible(true);
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }

    private JPanel makeTweakPanel(Vector<Tweakable> tweaks) {
        JPanel panel2 = new JPanel(new SpringLayout());
        int n = tweaks.size();

        for (Tweakable t : tweaks) {
            SpinTweaker spin = new SpinTweaker(t);
            JLabel label = new JLabel(t.getLabel());
            panel2.add(label);
            panel2.add(spin);
        }
        SpringUtilities.makeCompactGrid(panel2, 2, n, 2, 2, 2, 2);
        return panel2;
    }

    protected void setResults() {
        results.setText(String.format(" Acrruracy estimate %4.3f%%  ",
                tolNow * 100));
    }

    protected void fire(boolean key) {
        // double periodMs=period.doubleValue();
        // int nPulse= (int) (dur.doubleValue()/periodMs);
        ((GrainProcess) audioProcess).fire();
    }

    /**
     * decrease tolerance if we guess correctly.
     *
     */
    @Override
    protected void correctResultAction(int guess) {
        //
    }

    protected void incorrectResultAction(int guess, int real) {
    }

    protected void passAction(int real) {
    }

    public JPanel getGUIPanel() {
        return panel;
    }

    class GrainProcess extends FiniteAudioProcess {

        // private double amp;
        private MyAudioClient sync;
        private boolean isDone = true;
        private int pulseSize;
        private float[] pulse;
        private int pulseSamplePtr;
        private FFT fft;
        private double[] coeff;
        Ranlux r = new Ranlux(4, new Date());
        private float maxP;

        GrainProcess(MyAudioClient sync) {
            this.sync = sync;

        }

        public int processAudio(AudioBuffer buffer) {
            if (isDone) {
                return AUDIO_OK;
            }
            buffer.makeSilence();
            int n = buffer.getSampleCount();

            float buffL[] = buffer.getChannel(0);
            float buffR[] = buffer.getChannel(1);

            for (int i = 0; i < n; i++, pulseSamplePtr++) {
                if (pulseSamplePtr == pulseSize) {

                    isDone = true;
                    wakeUpSleepers();
                    return AUDIO_OK;
                }
                if (pulseSamplePtr < pulseSize) {
                    buffL[i] = buffR[i] = pulse[pulseSamplePtr];
                }
            }
            return AUDIO_OK;

        }

        public void fire() {
            System.out.println("fire");
            makePulse();
            this.isDone = false;
            this.pulseSamplePtr = 0;
        }

        public void setDuration(double pulseWidth) {
            pulseSize = (int) sync.milliToSamples(pulseWidth);
            fft = new FFT(pulseSize);
            coeff = new double[pulseSize * 2];
        }

        public void makePulse() {

            for (int i = 1; i < pulseSize / 2; i++) {
                if (i < pulseSize / 4) {
                    coeff[2 * i] = 0.5 - r.raw();
                    coeff[2 * i + 1] = 0.5 - r.raw();
                } else {
                    coeff[2 * i] = 0;
                    coeff[2 * i + 1] = 0;
                }
                coeff[2 * pulseSize - 2 * i] = coeff[2 * i];
                coeff[2 * pulseSize - 2 * i + 1] = -coeff[2 * i + 1];

            }

            coeff[0] = 0;
            coeff[1] = 0;

            //coeff[3] = 1;

            fft.calc(coeff, 1);

            // System.out.println(" Size = " + pulseSize);
            pulse = new float[pulseSize];

            //	double offSet=coeff[0];

            for (int i = 0; i < pulseSize; i++) {
                // double z = i / (double) (pulseSize - 1);
                // double w = Math.sin(Math.PI * z);
                pulse[i] = (float) (coeff[2 * i]); // -offSet);
                if (Math.abs(pulse[i]) > maxP) {
                    maxP = Math.abs(pulse[i]);
                }
                //		System.out.println(coeff[2*i] + " " + coeff[2*i+1]);
            }

            System.out.println(maxP);

            for (int i = 0; i < pulseSize; i++) {
                pulse[i] = (pulse[i] / 400.0f);
            }


        }

        public boolean isDone() {
            return isDone;
        }
    }
}
