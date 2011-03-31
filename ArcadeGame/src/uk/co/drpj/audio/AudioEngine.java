/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package uk.co.drpj.audio;

import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.logging.Level;
import java.util.logging.Logger;
import javazoom.jl.decoder.JavaLayerException;
import uk.co.drpj.audio.mp3.MP3AudioReader;
import uk.co.drpj.audio.mp3.MP3Clip;
import uk.org.toot.audio.core.AudioBuffer;
import uk.org.toot.audio.core.AudioProcess;
import uk.org.toot.audio.server.AudioClient;
import uk.org.toot.audio.server.AudioServer;

/**
 *
 * @author pjl
 */
public class AudioEngine {

    private AudioSystem audioSystem;
    MP3AudioReader audioReader;
    //private MP3Clip audioLoader;
    int block = 0;
    final ArrayList<ClipPlayer> players = new ArrayList<ClipPlayer>();

    public AudioEngine() {
        audioSystem = AudioSystem.instance();
    }

    public ClipPlayer playClip(ClipResource clip,boolean loop) {
        ClipPlayer player=null;
        synchronized (players) {
            players.add(player=clip.player());
        }
        player.setLooping(loop);
        return player;
    }

    public ClipResource loadClip(URL url) throws JavaLayerException, MalformedURLException, IOException {
        return new MP3Clip(url, audioSystem.getSampleRate(), audioSystem.getBufferSize());

    }

//    public void loadAudio() throws JavaLayerException, MalformedURLException, IOException {
//
//        //------------------------------------------------------------------
//        //  String source="/home/pjl/lect/audio/notes/samples/massive.mp3";
//        //String source = "http://people.bath.ac.uk/eespjl/courses/Audio/demo/massive.mp3";
//        //     String source="/home/pjl/lect/audio/notes/samples/kula.wav";
//
//
//        //URL url=new URL(source);
//
//        URL url = AudioEngine.class.getResource("/uk/co/drpj/chimera/images/Coinssilver.mp3");
//
//        // audioReader = new MP3AudioReader(url, 2.0f);
//        audioLoader = 
//
//    }
    public void configureAudio() {
        AudioServer server = audioSystem.getServer();

        final AudioProcess output = audioSystem.getOut();

        server.setClient(new AudioClient() {

            private AudioBuffer chunk;
            private int frameSize;

            public void work(int size) {

                if (chunk == null || size != frameSize) {
                    frameSize = size;
                    chunk = new AudioBuffer(null, 2, size, 48000.0f);
                    chunk.setRealTime(true);
                }

                chunk.makeSilence();
//
//                synchronized (readerMuex) {
//                    if (audioReader != null) {
//                        audioReader.processAudio(chunk);
//                    }
//                }

                synchronized (players) {
                    for (ClipPlayer clip : players) {
                        clip.processAudio(chunk);
                    }
                }
//                int n = audioLoader.buffer.size();
//                if (n == 0) {
//                    return;
//                }
//                AudioBuffer chunk = audioLoader.buffer.get(block % n);
//                block++;
//                //      System.out.println("chunk:"+chunk.getChannelCount()+" : "+ chunk.getSampleCount()+" >" +chunk.getSampleRate());

                output.processAudio(chunk);


            }

            public void setEnabled(boolean arg0) {
                //  throw new UnsupportedOperationException("Not supported yet.");
            }
        });
        try {
            audioSystem.start();
        } catch (Exception ex) {
            Logger.getLogger(AudioEngine.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
}
