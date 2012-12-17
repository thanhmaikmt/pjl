package GM.javasound;

import GM.music.*;
//import javax.sound.sampled.AudioSystem.*;
import javax.sound.sampled.*;

import java.util.*;

/**
 * Write a description of class Mixer here.
 *
 * @author DR pJ
 * @version 1
 */
public class JavaSoundMixer extends GMMixer {
    /**
     * Constructor for objects of class Mixer
     */

//    protected Vector voices;
    boolean isDirty;
    Mixer mixer;
    Mixer.Info info;
    public JavaSoundMixer() {
        super();
      //  System.out.println(" HELLO FROM JavaSoundMixer ");
        Mixer.Info mixerInfo[] = AudioSystem.getMixerInfo();
        for (int j = 0; j < mixerInfo.length; j++) {
     //       System.out.println(" -------------  " + mixerInfo[j]);

            mixer = AudioSystem.getMixer(mixerInfo[j]);
       //     System.out.println(mixer);
            Line sourceLine[] = mixer.getSourceLines();
            for (int i = 0; i < sourceLine.length; i++) {
                Line line = sourceLine[i];
         //       System.out.println("S " + line);
            }
            Line[] targetLine = mixer.getTargetLines();
            for (int i = 0; i < targetLine.length; i++) {
                Line line = targetLine[i];
           //     System.out.println("T " + line);
            }
            //       voices = new Vector();
        }
    }

    public void update(Observable o, Object arg) {
        if (o instanceof Voice) {
//            updateVoiceState();
        }
    }

    public void rebuild(Vector voices) {}

    public void kill() {}

    /*
        public void updateVoiceState() {
            boolean isSoloist = false;
            Iterator iter = voices.iterator();
            while (iter.hasNext()) {
                Voice v = ((Voice) iter.next());
                if (v.isSolo()) {
                    isSoloist = true;
                    break;
                }
            }

            iter = voices.iterator();

            while (iter.hasNext()) {
                Voice v = ((Voice) iter.next());
                if (v.isMute() || (isSoloist && (!v.isSolo()))) {
                    System.out.println(v.getName() + " muting ");
                    v.setSilent(true);
                } else {
                    System.out.println(v.getName() + " unmuting ");
                    v.setSilent(false);
                }
            }
        }

        public void setDirty() { isDirty=true; }
     */
    // public Mixer createMixer() { return new Mixer();}

}
