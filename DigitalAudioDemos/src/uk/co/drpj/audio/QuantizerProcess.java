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
public class QuantizerProcess implements AudioProcess {

    float quant;
    float base;
  //  QuantizerVariables controls;
    
    public void open() throws Exception {
        throw new UnsupportedOperationException("Not supported yet.");
    }

    public int processAudio(AudioBuffer buff) {
        int nChan = buff.getChannelCount();
        int nSamp = buff.getSampleCount();

        for (int chan = 0; chan < nChan; chan++) {
            float[] vals = buff.getChannel(chan);
            for (int i = 0; i < nSamp; i++) {
                vals[i] = base + Math.round((vals[i]-base) / quant) * quant;
            }
        }

        return AUDIO_OK;
    }

    public void close() throws Exception {
        throw new UnsupportedOperationException("Not supported yet.");
    }

    public void setNumberOfLevels(int n) {
            quant=(2.0f)/(n);
            base=-1.0f+quant/2.0f;

//            float tmp=base;
//            for (int i=0;i<n;i++) {
//                System.out.println(tmp);
//                tmp +=quant;
//            }
    }

    public float getQuant() {
        return quant;
    }

}
