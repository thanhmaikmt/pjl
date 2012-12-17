package GM.jsyn;

import GM.music.*;

import java.util.*;
import GM.io.*;

import com.softsynth.jsyn.*;
import javax.sound.midi.*;

/**
 * Just a  list of players.
 *
 * @author Dr PJ
 * @version dec/2004
 */
public class JsynSynth implements SynthNode {
    protected GMMixer mixer;
    private JsynConductor conductor;
    Vector<Voice> voices;
    JsynBank bank;


/*
    public IdString[] getBankNames() {
        IdString ret[] = new IdString[1];
        ret[0]=new IdString(0,"Default");
        return ret;
    }

    public Bank[] getBanks() {
        Bank b[]={bank};
        return b;
    }
*/

    private JsynSynth() throws Exception {
        super();
        conductor = JsynConductor.the();
        bank=new JsynBank();
        if (JsynConductor.slave)
            mixer = new JsynMixer(conductor.getContext());
        else
            mixer = new JsynMixerToLineOut(conductor.getContext());

        /** @todo dynamic allocation of voice to the mixer */
        mixer.rebuild(voices);
    }

    static JsynSynth the=null;

    static public JsynSynth the() throws Exception {
        if (the == null) the= new JsynSynth();
        return the;
    }

    public String getName() {
        return "Jsyn";
    }

    public Conductor getConductor() throws Exception {
        return JsynConductor.the();
    }


    public Voice createVoice(VoicePatch pat) throws Exception {
        return bank.createVoice(pat);
    }

    class JsynBank implements  SynthNode {

     //   Vector voices;
        SynthContext c=conductor.getContext();
        JsynBank() {

            //@TODO   this is crap. Look into VoiceAllocation and redo the Mixer

            voices=new Vector<Voice>();

            int ii=0;
            try {
                addVoice(new JsynVoice(new Sample(c, "CowBell"),"Cow",ii++));
                addVoice(new JsynVoice(new Sample(c, "RIM"),"Rim",ii++));
                addVoice(new JsynVoice(new Sample(c, "RIDE"),"Ride",ii++));
                addVoice(new JsynVoice(new Sample(c,  "HIHAT"),"HiHat",ii++));
                addVoice(new JsynVoice(new Sample(c,  "BASS"),"BDrum",ii++));
                Voice v;
                addVoice(new JsynVoice(new DBuff(c), "PString1",ii++));
                addVoice(new JsynVoice(new DBuff(c), "PString2",ii++));
                addVoice(new JsynVoice(new ResoVoice(c), "Vibes1",ii++));
                addVoice(new JsynVoice(new ResoVoice(c), "Vibes2",ii++));
                addVoice(new JsynVoice(new FeedbackFM(),"FM",ii++));
            } catch (Exception e) {
                e.printStackTrace();
            }
        }

        public IdString getIdString() {
            return new IdString(0,"BANK");
        }
        private void addVoice(Voice v) {
            voices.add(v);
        }

        public Voice createVoice(VoicePatch pat) throws Exception {
            return (Voice)voices.elementAt(pat.getProg());
        }

        public IdString[] getVoiceNames() {
            IdString ret[]= new IdString[voices.size()];
            for (int i=0;i<voices.size();i++)
                ret[i]=new IdString(i,((Voice)(voices.elementAt(i))).getName());
            return ret;
        }

        public int size() { return voices.size(); }
        public SynthNode nodeAt(int i) { return null;} //voices.elementAt(i); }
        public String getName() { return "BANK"; }
        public int index() { return 0; }
        public SynthNode getParent() { return JsynSynth.this;}


    }

   // public Voice createVoice(VoicePatch pat){ return bank.createVoice(pat);}


    public int size() { return 1; }
    public SynthNode nodeAt(int i) { return bank; }
   public SynthNode getParent() { return null; }
   public int index() { return 0;}
}
