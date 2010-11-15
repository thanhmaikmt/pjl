package uk.co.drpj;

import uk.co.drpj.*;
import uk.co.drpj.audio.URLWavReader;
import uk.co.drpj.audio.mp3.MP3AudioReader;
import java.awt.BorderLayout;

import java.io.File;
import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.JApplet;
import javazoom.jl.decoder.JavaLayerException;
import uk.co.drpj.audio.URLWavReader;




//@AppletServerClass
public class MDCTApplet extends JApplet {

    private static final long serialVersionUID = 1L;

  // AudioSystem audioSystem;
    private MDCTPanel panel;

    @Override
    public void init() {
        super.init();
        System.out.println(" INIT ");
    }

    @Override
    public void start() {
        System.out.println("START");
        if (panel != null) return;
        setLayout(new BorderLayout());
        try {
            panel = new MDCTPanel();
        } catch (Exception ex) {
            Logger.getLogger(MDCTApplet.class.getName()).log(Level.SEVERE, null, ex);
        }
        setContentPane(panel);

        panel.start();
      //  String source="/home/pjl/lect/audio/notes/samples/massive.mp3";
          String source="http://people.bath.ac.uk/eespjl/courses/Audio/demo/massive.mp3";
   //     String source="/home/pjl/lect/audio/notes/samples/kula.wav";

        if (source.toUpperCase().endsWith("MP3")) {
            setMP3(source);
        } else if (source.toUpperCase().endsWith("WAV")){
            setWAV(source);
        }
    }

    void setMP3(String url) {
        try {
            MP3AudioReader audioReader = new MP3AudioReader(url, 2.0f);
        panel.setAudioReader(audioReader);
 
            //    validate();
        } catch (JavaLayerException ex) {
            Logger.getLogger(MDCTApplet.class.getName()).log(Level.SEVERE, null, ex);
        } catch (MalformedURLException ex) {
            Logger.getLogger(MDCTApplet.class.getName()).log(Level.SEVERE, null, ex);
        } catch (IOException ex) {
            Logger.getLogger(MDCTApplet.class.getName()).log(Level.SEVERE, null, ex);
        }
    }



    void setWAV(String name) {
      try {
            URL u = ((new File(name)).toURI()).toURL();
            URLWavReader audioReader=new URLWavReader(u);
            panel.setAudioReader(audioReader);
        } catch (IOException ex) {
            Logger.getLogger(MDCTApplet.class.getName()).log(Level.SEVERE, null, ex);
        }

    }



    @Override
    public void stop() {
    System.out.println(" STOP ");
    if (panel == null) return;
        panel.dispose();
      //  audioSystem.stop();
        remove(panel);
        panel=null;
    }

    @Override
    public void destroy() {
        stop();
        super.destroy();
    }
}
