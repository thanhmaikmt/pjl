/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package uk.co.drpj.audio.source;

import java.util.Vector;
import uk.org.toot.audio.core.AudioBuffer;
import uk.org.toot.audio.core.AudioProcess;

/**
 *
 * @author pjl
 */
public class AudioProcessChain implements AudioProcess {
    private final Vector<AudioProcess> chain;


    public AudioProcessChain(AudioProcess src) {
        chain=new Vector<AudioProcess>();
        chain.add(src);

    }

    public void open() throws Exception {
        throw new UnsupportedOperationException("Not supported yet.");
    }

    public int processAudio(AudioBuffer arg0) {
        for (AudioProcess p:chain) {
            p.processAudio(arg0);
        }
        return AUDIO_OK;

    }

    public void close() throws Exception {
        throw new UnsupportedOperationException("Not supported yet.");
    }

 
}
