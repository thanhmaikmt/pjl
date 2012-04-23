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
    float chunk[];
    float lastInChunk[];
    float outChunk[];
    private float[] outBufNext;
    private float[] quant;
    private float[] base;

    //  QuantizerVariables controls;
    public void open() throws Exception {
        throw new UnsupportedOperationException("Not supported yet.");
    }

    public int processAudio(AudioBuffer buff) {

        // if (true) return AUDIO_OK;


        int nSamp = buff.getSampleCount();

        if (nSamp * 2 != this.N) {
            this.N = nSamp * 2;
            chunk = new float[this.N];
            lastInChunk = new float[this.N];
            outBufNext = new float[this.N];
            quant = new float[N];
            base = new float[N];

        }


        float inChunk[] = buff.getChannel(0);


        System.arraycopy(lastInChunk, 0, chunk, 0, nSamp);
        System.arraycopy(inChunk, 0, chunk, nSamp, nSamp);
        System.arraycopy(inChunk, 0, lastInChunk, 0, nSamp);

        MDCT.Transform(chunk, N, N / 2);

        for (int i = 0; i < N; i++) {
            chunk[i] = base[i] + Math.round((chunk[i] - base[i]) / quant[i]) * quant[i];
        }

        MDCT.ITransform(chunk, N, N / 2);



        float out[] = inChunk;

        for (int j = 0; j < nSamp; j++) {
            out[j] = (outBufNext[j] + chunk[j]) * 0.5f;
        }

        // Save the second half for the next call
        System.arraycopy(chunk, nSamp, outBufNext, 0, nSamp);

        return AUDIO_OK;
    }

    public void close() throws Exception {
        throw new UnsupportedOperationException("Not supported yet.");
    }
    int nnnn=-1;
    public void setBandQuantization(int nLevel, int band) {

        quant[band] =2.0f* (2.0f) / (nLevel);
        base[band] = -1.0f + quant[band] / 2.0f;
        if (nnnn != nLevel) {
            System.out.println(nLevel);
            nnnn=nLevel;
        }


//            float tmp=base;
//            for (int i=0;i<nLevel;i++) {
//                System.out.println(tmp);
//                tmp +=quant;
//            }


    }

    public int getBandCount() {
        return N;
    }
//    public float getQuant() {
//        return quant;
//    }
}
