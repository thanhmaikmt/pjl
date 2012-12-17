package GM.javasound;

import GM.music.*;

import javax.sound.midi.*;
import java.util.*;
import java.io.File;
import GM.gui.TopFrame;

/**
 * Just a  list of players.
 *
 * @author Dr PJ
 * @version dec/2004
 */
public class JavaSoundSynth implements SynthNode {

    public VoicePatch defaultVoicePatch = null;

    XSynth mySynths[];
    Synthesizer synth;
    Soundbank soundbanks[];


    static private JavaSoundSynth the = null;
    boolean[] freeChannel = new boolean[16];

    private JavaSoundSynth() throws Exception {

        Soundbank sb1;
        try {
            synth = MidiSystem.getSynthesizer();
            System.out.println(synth + " " + MidiHub.defaultMidiOut);
            printInfo(synth);
            synth.open();
        } catch (Exception ex) {
            TopFrame.displayException(ex);
            synth=null;
        }

        Vector<Soundbank> sbvector = new Vector<Soundbank>();
        if (false) {
            try {
              sb1 = MidiSystem.getSoundbank(new File(
                       "/home/pjl/SB/soundbank-deluxe.gm"));
               sbvector.add(sb1);
               System.out.println(sb1.getDescription() + " " + sb1.getName() + " " + sb1.getVendor() + " " + sb1.getVersion());
               sb1 = MidiSystem.getSoundbank(new File(
                        "/home/pjl/SB/soundbank.gm"));
               System.out.println(sb1.getDescription() + " " + sb1.getName() + " " + sb1.getVendor() + " " + sb1.getVersion());
               sbvector.add(sb1);

           } catch (Exception ex) {
               ex.printStackTrace();
               sb1 = synth.getDefaultSoundbank();
               System.out.println(sb1.getName());
           }
        } else {
            sbvector.add(synth.getDefaultSoundbank());
        }

       // sb1 = synth.getDefaultSoundbank();
       // System.out.println(sb1.getDescription() + " " + sb1.getName() + " " + sb1.getVendor() + " " + sb1.getVersion());

        if (sbvector.size() == 0) {
            throw new Exception(" No soundbanks found");
        }

        //  chan = synth.getChannels();

        for (int i = 0; i < 16; i++) {
            freeChannel[i] = true;
        }
        freeChannel[9] = false;

        soundbanks = new Soundbank[sbvector.size()];
        mySynths = new XSynth[sbvector.size()];
        for (int i = 0; i < mySynths.length; i++) {
            soundbanks[i] = sbvector.elementAt(i);
            mySynths[i] = new XSynth(sbvector.elementAt(i), i);
            System.out.println(soundbanks[i]+ " " + soundbanks[i].getName());
        }
    }

    public void releaseChannel(int chan) {
        freeChannel[chan] = true;
    }

    public int allocateChannel() throws Exception {
        int chan = -1;
        for (int i = 0; i < 16; i++) {
            if (freeChannel[i]) {
                freeChannel[i] = false;
                return i;
            }
        }

        throw new Exception(" Sorry all 16 channels in use ");
    }

    public VoicePatch defaultVoicePatch() {
         return defaultVoicePatch;
     }


    public String getName() {
        return "JavaSound";
    }

    public static JavaSoundSynth the() throws Exception {
        if (the == null) {
            the = new JavaSoundSynth();
        }
        JavaSoundConductor.the();
        return the;

    }

    public Conductor getConductor() throws Exception {
        return JavaSoundConductor.the();
    }

    public void printInfo(Synthesizer s) {
        System.out.println(s);
        System.out.println();
        System.out.println(" MAX POLY =" + s.getMaxPolyphony());
        MidiChannel[] chans = s.getChannels();
        System.out.println(" MAX CHANNELS =" + chans.length);
    }

    public Soundbank getSoundbank(String str) {
        for (int i = 0; i < soundbanks.length; i++) {
            if (soundbanks[i].getName().equals(str)) {
                return soundbanks[i];
            }
        }
        return soundbanks[0];
    }

    public Voice createVoice(VoicePatch patch) {
        return mySynths[patch.idAt(2)].banks[patch.getBank()].createVoice(patch);
    }

    public Voice createVoice(GMPatch patch) {
          return mySynths[patch.synth].banks[patch.bank].createVoice(patch.prog);
      }


    public int size() {
        return mySynths.length;
    }

    public SynthNode nodeAt(int i) {
        return mySynths[i];
    }

    public SynthNode getParent() {
        return null;
    }

    public int index() {
        return 0;
    }

    public String toString() { return "Javasound Synth"; }


    class XSynth implements SynthNode {

        JavaSoundBank[] banks;
        Soundbank sb;
        Instrument inst[];
        int index;

        public String toString() {
            return sb.getName();
        }

        XSynth(Soundbank sb, int index) {
            this.sb = sb;
            this.index = index;
            inst = sb.getInstruments();
            int maxB = 0;
            for (int i = 0; i < inst.length; i++) {
                int bank = inst[i].getPatch().getBank();
                maxB = Math.max(bank, maxB);
            }

            maxB = maxB + 1;

            System.out.println("MaxBANK="+maxB);

            JavaSoundBank[] bankT = new JavaSoundBank[maxB];

            for (int i = 0; i < inst.length; i++) {
                int bank = inst[i].getPatch().getBank();
                if (bankT[bank] == null) {
                    bankT[bank] = new JavaSoundBank(bank);
                }
            }

            int n = 0;
            for (int i = 0; i < maxB; i++) {
                if (bankT[i] == null) {
                    int j = i + 1;
                    while (bankT[j] == null && j < maxB) {
                        j++;
                    }
                    if (j < maxB) {
                        bankT[i] = bankT[j];
                        bankT[j] = null;
                    }
                } else {
                    n = i+1;
                }
            }
            banks = new JavaSoundBank[n];
            for (int i = 0; i < n; i++) {
                banks[i] = bankT[i];
            }
        }

        public int size() {
            return banks.length;
        }

        public SynthNode nodeAt(int i) {
            return banks[i];
        }

        public String getName() {
            return toString();
        }

        public Voice createVoice(VoicePatch patch) {
            return banks[patch.getBank()].createVoice(patch);
        }

        public int index() {
            return index;
        }

        public SynthNode getParent() {
            return JavaSoundSynth.this;
        }

        class JavaSoundBank implements SynthNode {


            VoicePatch[] names;

            int id;

            public String toString() {
                return "Bank:" + id;
            }

            JavaSoundBank( int id) {
                this.id = id;
                setVoiceNames();
            }

            public void setVoiceNames() {
                //  ArrayList<IdString> an = new ArrayList<IdString>();

              //  System.out.println(" CREATING NAMES FOR " + getName());
                int count = 0;

                for (int i = 0; i < inst.length; i++) {
                    if (inst[i].getPatch().getBank() == id) {
                        count++;
                    }
                }
                names = new VoicePatch[count];
                count = 0;

                for (int i = 0; i < inst.length; i++) {
                    if (inst[i].getPatch().getBank() == id) {
                        VoicePatch pat = new VoicePatch(this,
                                inst[i].getName(),
                                inst[i].getPatch().getProgram());

                    //    System.out.println(pat.toDebug());

    //                    if (JavaSoundHub.the().defaultVoicePatch == null) {
    //                        JavaSoundHub.the().defaultVoicePatch = pat;
    //                    }

                        names[count++] = pat;
                    }
                }

            }

            /*
                        public IdString[] getVoiceNames() {
                            return names;
                        }
             */

            public Voice createVoice(VoicePatch pat) {
                return createVoice(pat.getProg());
            }

            public Voice createVoice(int  prog) {


                Patch p = new Patch(id, prog);

            //    System.out.println(" LoadingVoice " + " " + p.getProgram() + " " +
            //                       p.getBank());

                Instrument inst = sb.getInstrument(p);


                synth.loadInstrument(inst);
                //    synth.loadInstruments(sb,new Patch[]{p});
                //  String name=getVoiceNames()[pat.getProgram()].toString();


                Voice v;
                GMPatch gp=new GMPatch(0,p.getBank(),p.getProgram());
                if (p.getBank() != 1) {
                    v = new JavaSoundMelodicVoice(gp.getId(), inst.getName());
              //      v.allocate(true);
                } else {
                    v = new JavaSoundPercusiveVoice(gp.getId(),inst.getName());
                }
                return v;
            }

            public int size() {
                return names.length;
            }

            public SynthNode nodeAt(int i) {
                return names[i];
            }

            public String getName() {
                return toString();
            }

            public SynthNode getParent() {
                return XSynth.this;
            }

            public int index() {
                return id;
            }
        }

    }


}
