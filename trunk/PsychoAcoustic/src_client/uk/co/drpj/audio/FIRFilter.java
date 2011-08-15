// Copyright (C) 2006 Steve Taylor.
// Distributed under the Toot Software License, Version 1.0. (See
// accompanying file LICENSE_1_0.txt or copy at
// http://www.toot.org.uk/LICENSE_1_0.txt)
package uk.co.drpj.audio;

import uk.org.toot.audio.core.AudioBuffer;
import uk.org.toot.audio.core.AudioProcess;

public class FIRFilter implements AudioProcess {

    private float[] a; // filter coefficients
    public float[] x; // filter delay stages

    public FIRFilter() {
    }

    public synchronized void setCoeffs(float a[]) {
        if (a != null) {
            this.a = new float[a.length];
            System.arraycopy(a, 0, this.a, 0, a.length);
            x = new float[a.length]; // !!! what if a.length changes
        } else {  
            x = this.a = null;
        }
    }

    public synchronized int processAudio(AudioBuffer buff) {

        // TODO more channels
        if (a == null) {
            return AUDIO_OK;
        }

        assert (buff.getChannelCount() == 1);

        float signal[] = buff.getChannel(0);
        int len = buff.getSampleCount();

        for (int i = 0; i < len; i++) {
            float y = 0.0f;
            int taps = a.length;
            x[0] = signal[i];
            for (int k = 0; k < taps; k++) {
                y += a[k] * x[k];
            }
            for (int k = taps - 1; k > 0; k--) {
                x[k] = x[k - 1];
            }
            signal[i] = y;
        }
        return AUDIO_OK;
    }

    public void open() throws Exception {
        throw new UnsupportedOperationException("Not supported yet.");
    }

    public void close() throws Exception {
        throw new UnsupportedOperationException("Not supported yet.");
    }
}
