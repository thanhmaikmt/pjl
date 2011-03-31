/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package uk.co.drpj.audio;

import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;
import uk.org.toot.audio.server.AudioServer;
import uk.org.toot.audio.server.IOAudioProcess;
import uk.org.toot.audio.server.JavaSoundAudioServer;

/**
 *
 * @author pjl
 */
public class AudioSystem {

    AudioServer server;
    IOAudioProcess out;
    boolean inited=false;
    private float sampleRate;
    private int bufferSize;

    public IOAudioProcess getOut() {
        return out;
    }
    static private AudioSystem instance;
//    MyAudioClient client;
//
//    public MyAudioClient getClient() {
//        return client;
//    }

    private AudioSystem() {
        init();
    }
    static public AudioSystem instance() {
        if (instance == null) {
            instance = new AudioSystem();
        }
        return instance;
    }

    public float getSampleRate() {
        return sampleRate;
    }
    public int getBufferSize() {
        return bufferSize;
    }
    public void init() {
        if (inited) return;
        try {
            sampleRate=48000.0f;
            bufferSize=512;

            server = new MyJavaSoundAudioServer(sampleRate,bufferSize);
           
            //new AudioFormat(44100.0f, 16, 2,
            //		true, false), 50, 5);
            List<String> list = server.getAvailableOutputNames();
            Object[] a = new Object[list.size()];
            a = list.toArray(a);
            //Object selectedValue = JOptionPane.showInputDialog(null,
            //		"Select audio output", "output",
            //		JOptionPane.INFORMATION_MESSAGE, null, a, a[0]);
            Object selectedValue = a[0];
            System.out.println(" Opening "+a[0]);
            
            out = server.openAudioOutput((String) selectedValue, "output");
        
        } catch (Exception ex) {
            Logger.getLogger(AudioSystem.class.getName()).log(Level.SEVERE, null, ex);
        }
        server.start();
        inited=true;
    }

    public void stop() {
        if (server == null) {
            return;
        }

        server.closeAudioOutput(out);
        server.stop();
        server = null;
        out = null;
        inited=false;
        instance=null;
    }

    public void start() throws Exception {
        init();
//        server.start();
//            server.openAudioOutput(out,"output");
    }

    public AudioServer getServer() {
       return server;
    }

   class MyJavaSoundAudioServer extends JavaSoundAudioServer {

        private MyJavaSoundAudioServer(float rate,int buffSize) {
            setSampleRate(rate);
            resizeBuffers(buffSize);
        }

       
   }
}
