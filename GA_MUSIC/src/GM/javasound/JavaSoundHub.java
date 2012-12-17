package GM.javasound;


import javax.sound.sampled.AudioPermission;
import GM.music.*;

import GM.audio.FFTAnalyst;
import GM.audio.FramedFeed;


/**
 * <p>Title: </p>
 *
 * <p>Description: </p>
 *
 * <p>Copyright: Copyright (c) 2005</p>
 *
 * <p>Company: </p>
 *
 * @author not attributable
 * @version 1.0
 */
public class JavaSoundHub extends Hub {


    JavaSoundSynth synth = null;

    TargetDataLineFeed feed;
    PeakAnalyst peakAnalyst;
    FFTAnalyst fftAnalyst;
    boolean inited = false;




    static public JavaSoundHub the() {
         return (JavaSoundHub)the;
    }

    public JavaSoundHub() {

        System.out.println("---------------------------------------------");
        assert (the == null);
        the = this;
        assert (inited == false);

        inited = true;
        int iflag = 0;
        // System.out.println("B1");
        if (synth != null) {
            return;
        }

        try {

            double sampleRate = 44100;
            synth = JavaSoundSynth.the();

            Conductor.init();

            SecurityManager sm = System.getSecurityManager();

            boolean noRecord = false;
            if (sm != null) {
                System.out.println(
                        " Security manager exists. Asking about record");
                Object context = sm.getSecurityContext();
                AudioPermission perm = new AudioPermission("record");
                try {
                    sm.checkPermission(perm, context);
                } catch (SecurityException ex) {
                    ex.printStackTrace();
                    noRecord = true;
                }
            } else {
                System.out.println(" No Security manager.");
            }

            if (!noRecord) {
                feed = new TargetDataLineFeed(sampleRate);
                //   System.out.println("B4-1");
                Thread t = new Thread(feed);
                t.setPriority(Thread.MAX_PRIORITY);

                //   System.out.println("B4-2");
                peakAnalyst = new PeakAnalyst(feed);
                fftAnalyst = new FFTAnalyst(feed);                //   System.out.println("B4-3");
                t.start();
            }
        } catch (Exception e) {

            e.printStackTrace();

        }


    }



    public FramedFeed getFeed() {
        return feed;
    }

    public Voice createVoice(VoicePatch pat) throws Exception {
        return synth.createVoice(pat);
    }



    public Voice createVoice(GMPatch pat) throws Exception {
        return synth.createVoice(pat);
    }

    public Voice createDefaultVoice() throws Exception {
           return synth.createVoice(new GMPatch(0,0,0));
       }



    public String getName() {
        return "Javasound";
    }

    public int size() {
        return 1;
    }

    public SynthNode nodeAt(int i) {
        return synth;
    }

    public int index() {
        return 0;
    }

    public SynthNode getParent() {
        return null;
    }



}
