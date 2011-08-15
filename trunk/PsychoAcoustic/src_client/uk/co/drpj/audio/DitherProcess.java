/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package uk.co.drpj.audio;

import java.util.Random;
import uk.org.toot.audio.core.AudioBuffer;
import uk.org.toot.audio.core.AudioProcess;

/**
 *
 * @author pjl
 */
public class DitherProcess implements AudioProcess {

    private float quant;
    private float amp;
    private Random rand=new Random();

    public void open() throws Exception {
        throw new UnsupportedOperationException("Not supported yet.");
    }

    public int processAudio(AudioBuffer buff) {
        int nChan = buff.getChannelCount();
        int nSamp = buff.getSampleCount();

        for (int chan = 0; chan < nChan; chan++) {
            float[] vals = buff.getChannel(chan);
            for (int i = 0; i < nSamp; i++) {
                vals[i] = (float) (vals[i] - quant * 0.5 + rand.nextDouble() * quant * amp * 2);
            }
        }


        return AudioProcess.AUDIO_OK;
    }

    public void close() throws Exception {
        throw new UnsupportedOperationException("Not supported yet.");
    }

    public void setQuantizelevel(float quant) {
        this.quant = quant;
    }

    public void setDither(float amp) {
        this.amp = amp;
    }
}
