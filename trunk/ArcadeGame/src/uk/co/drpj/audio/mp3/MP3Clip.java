/*
 * 11/19/04		1.0 moved to LGPL.
 * 
 * 06/04/01		Streaming support added. javalayer@javazoom.net
 * 
 * 29/01/00		Initial version. mdm@techie.com
 *-----------------------------------------------------------------------
 *   This program is free software; you can redistribute it and/or modify
 *   it under the terms of the GNU Library General Public License as published
 *   by the Free Software Foundation; either version 2 of the License, or
 *   (at your option) any later version.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU Library General Public License for more details.
 *
 *   You should have received a copy of the GNU Library General Public
 *   License along with this program; if not, write to the Free Software
 *   Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
 *----------------------------------------------------------------------
 */
package uk.co.drpj.audio.mp3;

import java.io.BufferedInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.logging.Level;
import java.util.logging.Logger;
import javazoom.jl.decoder.Decoder;
import javazoom.jl.decoder.JavaLayerException;
import javazoom.jl.player.AudioDevice;
import javazoom.jl.player.Player;
import uk.org.toot.audio.core.AudioBuffer;

//import javazoom.jl.decoder.JavaLayerException;
/**
 * The <code>jlp</code> class implements a simple command-line
 * player for MPEG audio files.
 *
 * @author Mat McGowan (mdm@techie.com)
 */
public class MP3Clip extends AudioBufferListClip {

    public void open() throws Exception {
        throw new UnsupportedOperationException("Not supported yet.");
    }

    // float Fs = 48000;
    public MP3Clip(URL url, final float sampleRate, final int chunkSize) throws JavaLayerException, MalformedURLException, IOException {
        // System.out.println("playing " + fFilename + "...");

        InputStream fin = url.openStream();
        BufferedInputStream in = new BufferedInputStream(fin);
        AudioDevice dev = new AudioDevice() {

            Decoder dec;
            AudioBuffer buff;
            int inChunkSize = chunkSize;
            int inPtr = 0;
            int nChannel;
            float Fs;
            long pos = 0;

            public void open(Decoder arg0) throws JavaLayerException {
//                float Fs = arg0.getOutputFrequency();
//                int nChannel = arg0.getOutputChannels();
//                System.out.println(" Fs=" + Fs + "  chan=" + nChannel);
                this.dec = arg0;
            }

            public boolean isOpen() {
                throw new UnsupportedOperationException("Not supported yet.");
            }

            public void write(short[] arg0, int arg1, int arg2) throws JavaLayerException {
                if (buff == null) {
                    Fs = dec.getOutputFrequency();
                    nChannel = dec.getOutputChannels();
                    System.out.println(" Fs=" + Fs + "  chan=" + nChannel + " inChunkSize" + inChunkSize);
                    if (Fs != sampleRate) {
                        System.out.println(" Sample rate mismatch mp3 rate =" + Fs + " should be " + sampleRate);

                    }
                    buff = new AudioBuffer("input", nChannel, inChunkSize, sampleRate);
                    buff.setRealTime(true);
                }

                for (int i = arg1; i < arg2; i += nChannel) {
                    for (int c = 0; c < nChannel; c++) {
                        buff.getChannel(c)[inPtr] = ((float) arg0[i + c]) / Short.MAX_VALUE;
                    }
                    inPtr++;
                    if (inPtr == inChunkSize) {
//                        System.out.print("+");
                        addBuffer(buff);
                        inPtr = 0;
                        buff = new AudioBuffer("input", nChannel, inChunkSize, Fs);
                        buff.setRealTime(true);
                        //           System.out.println(" Added chunk "+inChunkSize);
                    }
                }
                pos += arg2 - arg1;
            }

            public void close() {
                //    throw new UnsupportedOperationException("Not supported yet.");
            }

            public void flush() {
                //   throw new UnsupportedOperationException("Not supported yet.");
            }

            public int getPosition() {
                return (int) pos;
                // throw new UnsupportedOperationException("Not supported yet.");
            }
            //FactoryRegistry.systemRegistry().createAudioDevice();
        };

        final Player player = new Player(in, dev);

//        Thread t = new Thread(new Runnable() {
//
//            public void run() {
        try {
            player.play();
        } catch (JavaLayerException ex) {
            Logger.getLogger(MP3Clip.class.getName()).log(Level.SEVERE, null, ex);
        }
//            }
//        });
//        t.start();
//
//        // Give the buffer a seconf to fill
//        try {
//            Thread.sleep((long) (1000));
//        } catch (InterruptedException ex) {
//            // Logger.getLogger(MP3AudioReader.class.getName()).log(Level.SEVERE, null, ex);
//        }

    }
}
