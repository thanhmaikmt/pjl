/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package uk.co.drpj.audio.mp3;

import java.util.ArrayList;
import java.util.List;
import uk.co.drpj.audio.ClipPlayer;
import uk.co.drpj.audio.ClipResource;
import uk.org.toot.audio.core.AudioBuffer;

/**
 *
 * @author pjl
 */
public class AudioBufferListClip implements ClipResource {

    final private List<AudioBuffer> buffer = new ArrayList<AudioBuffer>();
    int nch;

    public ClipPlayer player() {


        return new ClipPlayer() {

            boolean loop=false;

            int block = 0;
            float c[][] = new float[2][];
            float i[][] = new float[2][];
            AudioBuffer chunk;
            int nIn;
            int ptrIn;
            private boolean eof=false;

            public void open() throws Exception {
                throw new UnsupportedOperationException("Not supported yet.");
            }

            void nextChunk() {

                if (!loop && block >= buffer.size()) {
                    eof=true;
                    return;
                }
                chunk = buffer.get(block % buffer.size());
                nch=chunk.getChannelCount();
                nIn = chunk.getSampleCount();
                ptrIn = 0;
                i[0] = chunk.getChannel(0);
                i[1] = chunk.getChannel(nch-1);
                block++;
            }

            public int processAudio(AudioBuffer buff) {
                if (eof) return AUDIO_DISCONNECT;
                if (chunk == null) {
                    nextChunk();
                }

                int n = buff.getSampleCount();
                c[0] = buff.getChannel(0);
                c[1] = buff.getChannel(1);

                for (int ptrOut = 0; ptrOut < n; ptrOut++) {

                     c[0][ptrOut] += i[0][ptrIn];
                     c[1][ptrOut] += i[1][ptrIn];

                    ptrIn++;
                    if (ptrIn >= nIn) {
                        nextChunk();
                    }
                }

                return AUDIO_OK;
            }

            public void close() throws Exception {
                throw new UnsupportedOperationException("Not supported yet.");
            }

            public void setLooping(boolean yes) {
                loop=yes;
            }
        };

    }

    public void addBuffer(AudioBuffer buff) {
        buffer.add(buff);
    }
}
