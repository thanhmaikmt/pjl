/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package uk.co.drpj.audio.source;

import java.util.logging.Level;
import java.util.logging.Logger;
import uk.org.toot.audio.core.AudioBuffer;
import uk.org.toot.audio.core.AudioProcess;

/**
 *
 * @author pjl
 */
public class EnvelopeProcess implements AudioProcess {

    long tickOn;
    long tickOff;
    long riseTicks;
    float ramp[];
    TickReference ref;
    private long ticksDur;

    public EnvelopeProcess(TickReference ref) {
        this.ref = ref;
    }

    public void open() throws Exception {
        throw new UnsupportedOperationException("Not supported yet.");
    }

    public void setNRise(int n) {
        riseTicks = n;
        ramp = new float[n];
        for (int i = 0; i < n; i++) {
            ramp[i] = (float)(0.5* (1.0 - Math.cos((i + 1) * Math.PI / (n + 1))));
   //         System.out.println(ramp[i]);
        }
    }

    public void setTicksOn(long ticksDur) {
        this.ticksDur = ticksDur;
    }

    public void setFireAt(long tickOn) {
        this.tickOn = tickOn;
        this.tickOff = tickOn + ticksDur-riseTicks;

      //  System.out.printf(" fire at, now, dur, rise \n"+ tickOn + "  " + "  " + ref.getCurrentTick()+ "  " + ticksDur + " " + riseTicks);
        if (2*riseTicks > ticksDur ) {
            try {
                throw new Exception(" 2*riseTicks > ticksDur ");
            } catch (Exception ex) {
                Logger.getLogger(EnvelopeProcess.class.getName()).log(Level.SEVERE, null, ex);
            }
        }

    }

    public int processAudio(AudioBuffer arg0) {
        if (ramp == null) {
            return AUDIO_OK;
        }
        int n = arg0.getSampleCount();
        long tick = ref.getCurrentTick();
        for (int c = 0; c < arg0.getChannelCount(); c++) {
            float b[] = arg0.getChannel(c);

            for (int i = 0; i < n; i++) {

                long tR = tick - tickOn + i;
                if (tR <= 0) {
                    b[i] = 0.0f;
                } else if (tR < riseTicks) {
                    b[i] *= ramp[(int) tR];
                } else {
                    long tF = tick - tickOff + i;
                    if (tF <= 0)  {
                    } else if (tF <= riseTicks) {
                        b[i] *= ramp[(int) (riseTicks - tF)];
                  //      System.out.println((int) (riseTicks - tF));
                    } else {
                        b[i]=0.0f;
                    }

                }
            }
        }
        return AUDIO_OK;
    }

    public void close() throws Exception {
        throw new UnsupportedOperationException("Not supported yet.");
    }
}
