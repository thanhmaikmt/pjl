package GM.jsyn;


import GM.javasound.*;

import javax.sound.sampled.AudioPermission;
import GM.music.*;
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
public class JsynHub extends Hub implements  SynthNode {

    JavaSoundSynth synth = null;
    SynthNode synths[] = null;
    TargetDataLineFeed feed;
    PeakAnalyst listener;

    public boolean javasoundMidi=true;
    public boolean jsyn=true;
    boolean inited=false;
    public VoicePatch defaultVoicePatch=null;

    public JsynHub() {

        assert(the==null);
        the=this;
        assert(inited==false);
        inited=true;
        int iflag=3;
       // System.out.println("B1");
        if (synths != null) {
            return;
        }

   //    if (javasoundMidi) iflag = 2;
   //    if (jsyn) iflag = iflag | 1;

        try {

            double sampleRate=44100;
            switch (iflag) {
            case 3: // Jsyn and JavaSound
                JsynConductor.slave = true;
                synths = new SynthNode[2];
                synths[0] = JsynSynth.the();
                synths[1] = synth = JavaSoundSynth.the();
                Conductor.init();
            //    Conductor.setTempo(60.0, new Time(0));
            //    JavaSoundConductor c = JavaSoundConductor.the(); // @TODO why ?
                sampleRate = JsynConductor.the().sampleRate();
                break;

            case 1: // Jsyn
               // JsynConductor.slave = false;
                synths = new SynthNode[1];
                synths[0] = JsynSynth.the();
                Conductor.init();
              //  Conductor.setTempo(60.0, new Time(0));
                break;

            case 2: // JavaSound
                synths = new SynthNode[1];
         //       System.out.println("B2");

                synths[0] = synth = JavaSoundSynth.the();
           //     System.out.println("B3");

                Conductor.init();
             //   System.out.println("B4");

         //       Conductor.setTempo(60.0, new Time(0));
                break;
            default:
                System.err.println(" Please use Palette.init with 1 2 or 3 ");
            }

            SecurityManager sm =System.getSecurityManager();

            boolean noRecord=false;
            if (sm != null) {
                System.out.println(" Security manager exists. Asking about record");
                Object context = sm.getSecurityContext();
                AudioPermission perm = new AudioPermission("record");
                try{
                    sm.checkPermission(perm, context);
                } catch (SecurityException ex) {
                    ex.printStackTrace();
                    noRecord=true;
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
                listener = new PeakAnalyst(feed);
                //   System.out.println("B4-3");
                t.start();
            }
        } catch (Exception e) {

            e.printStackTrace();

        }

    }

    public FramedFeed getFeed() {
        return feed;
    }

    public Voice createVoice(GMPatch pat) throws Exception
    {
        return null;
    }

    public Voice createDefaultVoice() throws Exception {
        return synth.createVoice(new GMPatch(0,0,0));
    }


    public Voice createVoice(VoicePatch pat) throws Exception {
        /*
        SimSynth syn = synths[pat.synth];
        Bank bank=syn.getBanks()[pat.bank];
        return bank.createVoice(new Patch(pat.bank,pat.prog));
        */
       return null;
    }

   /*
    public Synth[] getSynths() {
        return synths;
    }
*/

    public VoicePatch defaultVoicePatch() { return defaultVoicePatch;}

    public int size() { return synths.length; }
    public SynthNode nodeAt(int i) { return synths[i];}
    public String getName() { return "";}
    public int index() { return 0; }
    public SynthNode getParent() { return null; }


}
