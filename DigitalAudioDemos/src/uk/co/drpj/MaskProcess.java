package uk.co.drpj;

import uk.co.drpj.audio.AudioSystem;
import uk.co.drpj.audio.source.EnvelopeProcess;
import uk.co.drpj.audio.source.TickReference;

import java.util.Random;


import uk.co.drpj.audio.FIRFilter;
import uk.co.drpj.audio.FIRFilterDesign;
import uk.co.drpj.audio.source.MySource;
import uk.co.drpj.audio.source.MySource.Wave;
import uk.org.toot.audio.core.AudioBuffer;
import uk.org.toot.audio.core.AudioProcess;
import uk.org.toot.audio.server.AudioServer;

/**
 *
 * @author pjl
 */
public class MaskProcess implements AudioProcess {

    private AudioBuffer maskChunk;
    private AudioBuffer signalChunk;
    private final MySource maskSrc;
    private final MySource signalSrc;
    private final EnvelopeProcess maskEnv;
    private final EnvelopeProcess signalEnv;
    private TickReference ref;
    private long currentTick;
    private long nWait;
    private int nRel;
    private boolean beep;
    private boolean mask;
    private final FIRFilter filt;
    private final float Fs;
    MySource src=new MySource();

    public MaskProcess() {

        AudioServer server = AudioSystem.instance().getServer();

        Fs = server.getSampleRate();

        System.out.println(" Fs = " + Fs);


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


    }
    int frameSize;
    float a[];
    float b[];
    float c[][] = new float[2][];

    public int processAudio(AudioBuffer buff) {


        int size = buff.getSampleCount();


        if (maskChunk == null || size != frameSize) {
            frameSize = size;
            maskChunk = new AudioBuffer(null, 1, size, Fs);
            maskChunk.setRealTime(true);
            signalChunk = new AudioBuffer(null, 1, size, Fs);
            signalChunk.setRealTime(true);
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

        a = maskChunk.getChannel(0);
        b = signalChunk.getChannel(0);

        for (int ch = 0; ch < buff.getChannelCount(); ch++) {
            c[ch] = buff.getChannel(ch);
        }

     //    src.processAudio(maskChunk);
         
        for (int ch = 0; ch < buff.getChannelCount(); ch++) {
            for (int i = 0; i < size; i++) {
                c[ch][i] = b[i] + a[i];
            }
        }

       
        currentTick += size;

        return AUDIO_OK;
    }

    public void doBoth() {
        beep = true;
        mask = true;

        long tickOn = ref.getCurrentTick() + nWait;
        maskEnv.setFireAt(tickOn);
        signalEnv.setFireAt(tickOn + nRel);
    }

    public void doBeep() {
        beep = true;
        mask = false;
        long tickOn = ref.getCurrentTick() + nWait;
        maskEnv.setFireAt(tickOn);
        signalEnv.setFireAt(tickOn + nRel);

    }

    public void doMask() {
        beep = false;
        mask = true;
        long tickOn = ref.getCurrentTick() + nWait;
        maskEnv.setFireAt(tickOn);
        signalEnv.setFireAt(tickOn + nRel);
    }
    Random rand = new Random();

    public boolean doRandom() {
        beep = rand.nextFloat() > 0.5;
        mask = true;
        long tickOn = ref.getCurrentTick() + nWait;
        maskEnv.setFireAt(tickOn);
        signalEnv.setFireAt(tickOn + nRel);
        return beep;
    }

    void update(float sigFreq, float sigAmp, Wave maskType, float maskFreq, float maskBW, float maskAmp) {

        signalSrc.setFreq(sigFreq);
        signalSrc.setAmp(sigAmp);
        maskSrc.setWave(maskType);

        if (maskType != Wave.NOISE) {
            maskSrc.setFreq(maskFreq);
            filt.setCoeffs(null);
        } else {

            int order = 256;
            float alpha = 10.0f;

            FIRFilterDesign filtDesign = new FIRFilterDesign(alpha, Fs, maskFreq, FIRFilterDesign.BPF, order,
                    FIRFilterDesign.KAISER, maskBW);

            float coeffs[] = filtDesign.getCoefficients();

            filt.setCoeffs(coeffs);
        }

        maskSrc.setAmp(maskAmp);

    }

    public void open() throws Exception {
        throw new UnsupportedOperationException("Not supported yet.");
    }

    public void close() throws Exception {
        throw new UnsupportedOperationException("Not supported yet.");
    }
}
