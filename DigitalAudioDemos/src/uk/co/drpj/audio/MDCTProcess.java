/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package uk.co.drpj.audio;

import mediaframe.mpeg4.audio.AAC.MDCT;
import uk.org.toot.audio.core.AudioBuffer;
import uk.org.toot.audio.core.AudioProcess;

/**
 *
 * @author pjl
 */
public class MDCTProcess implements AudioProcess {

    int N;     // size of MDCT  (twice buffer size)
    float out[];
    CycliclyBufferedAudio buffer;
    float chunk[];
    float lastChunk[];
    float outChunk[];


    
    //  QuantizerVariables controls;
    public void open() throws Exception {
        throw new UnsupportedOperationException("Not supported yet.");
    }

    public int processAudio(AudioBuffer buff) {


        int nSamp = buff.getSampleCount();

        if (nSamp * 2 != this.N) {
            this.N = nSamp * 2;
            chunk = new float[this.N];
            lastChunk=new float[this.N];
        }

        float b[]=buff.getChannel(0);

        System.arraycopy(lastChunk, 0, chunk, 0, nSamp);
        System.arraycopy(b, 0, chunk, nSamp, nSamp);

        MDCT.Transform(chunk, N, N/2);
        MDCT.ITransform(chunk, N, N/2);



        for (int j = 0; j < N; j++) {
            out[i1 + j] += chunk[j] * 0.5;
        }


        return AUDIO_OK;
    }

    public void close() throws Exception {
        throw new UnsupportedOperationException("Not supported yet.");
    }

    public void setNumberOfLevels(int n) {
        quant = (2.0f) / (n);
        base = -1.0f + quant / 2.0f;

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
