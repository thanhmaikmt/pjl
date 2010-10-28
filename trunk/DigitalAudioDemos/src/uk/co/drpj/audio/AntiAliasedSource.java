/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package uk.co.drpj.audio;

import uk.org.toot.audio.core.AudioBuffer;
import uk.org.toot.audio.core.AudioProcess;

/**
 *
 * @author pjl
 */
public class AntiAliasedSource implements AudioProcess {

    FIRFilter filt;
    private final AudioProcess src;
    AudioBuffer chunk;
    private int N;
    private int overBuffSize;
    private final float sampRate;

    public AntiAliasedSource(float sampRate, int overFact, AudioProcess src,float coeffs[]) {

        this.sampRate = sampRate;
        this.src = src;
        setUp(overFact,coeffs);
    }
    final Object lock = new Object();

    void createFilter(int n,float coeffs[]) {
//        float alpha = 5;
//        int order = 50;
//        float bandwidth = 00;
//        FIRFilterDesign d = new FIRFilterDesign(alpha, sampRate * n, sampRate / 2.4f, FIRFilterDesign.LPF, order,
//                FIRFilterDesign.KAISER, bandwidth);
//        float coeffs[] = d.getCoefficients();
        FIRFilter filt1 = new FIRFilter();
        filt1.setCoeffs(coeffs);

        // there is a miniscule chance that concurrency problems might happen here.
        synchronized (lock) {
            filt = filt1;
            N = n;
        }
    }

    public void open() throws Exception {
        throw new UnsupportedOperationException("Not supported yet.");
    }

    public int processAudio(AudioBuffer ab) {

        int dstBuffSize = ab.getSampleCount();
        int NN;
        FIRFilter ff;
        // grab filter and NN
        synchronized (lock) {
            ff = filt;
            NN = N;
        }

        if (chunk == null || overBuffSize != dstBuffSize * NN) {
            overBuffSize = dstBuffSize * NN;
            chunk = new AudioBuffer("oversampled", 1, overBuffSize, ab.getSampleRate() * NN);
        }
        chunk.makeSilence();
        src.processAudio(chunk);
        ff.processAudio(chunk);

        float upa[] = chunk.getChannel(0);

        for (int chn = 0; chn < ab.getChannelCount(); chn++) {
            float a[] = ab.getChannel(chn);

            for (int i = 0; i < dstBuffSize; i++) {
                a[i] = upa[NN * i];
            }
        }
        return AUDIO_OK;
    }

    public void close() throws Exception {
        throw new UnsupportedOperationException("Not supported yet.");
    }

    public void setUp(int n,float coeffs[]) {
        createFilter(n,coeffs);
    }
}
