package GM.javasound;

import GM.music.*;
import javax.sound.midi.*;
import java.io.*;
import java.util.*;
import GM.tweak.*;

abstract public class JavaSoundVoice extends Voice {
    Patch patch;
    protected int channel = -1;
    protected int vol = 127; // used to adjust pec sounds
    GMPatch gmPatch;



    public JavaSoundVoice(long id,String name) {
        super(name);
        gmPatch = new GMPatch(id);
        patch = new Patch(gmPatch.bank,gmPatch.prog);
    }

    public long getId() { return gmPatch.getId(); }
    /*
    public JavaSoundVoice(StreamTokenizer st) {
        super(st);

      //  String sbname = null;
        try {

            st.nextToken();
            int b = (int) st.nval;
            st.nextToken();
            int p = (int) st.nval;
            patch = new Patch(b, p);

           // JavaSoundHub.the().getSynth()
 //           sb = JavaSoundSynth.the().getSoundbank(sbname);
 //           String sbn = sb.getName();
   //         if (!sbname.equals(sbn)) {
    //            System.err.println(" Voice soundbank was = \"" + sbname +
    //                               "\" actual is \"" + sbn + "\"");
    //        }

        } catch (Exception ex) {
            ex.printStackTrace();
        }

    }



    public JavaSoundVoice(String name, Patch p, String bankName,String synthName) {
        super(name,p.getProgram(),bankName,synthName);
        this.patch = p;
   //     this.sb = sb;

    }
    */

    public void tweakCtrl(int ctrl,int val) {
        if (channel < 0 ) return;
        if (ctrl == 7) {
            vol = val;
            if (channel != 9) {
                JavaSoundConductor.the().setController(channel, ctrl, val);
            }
        } else {
            JavaSoundConductor.the().setController(channel, ctrl, val);
        }
    }

/*
    public String getData() {

        StringBuffer buf = new StringBuffer(super.getData() +
                                            " " + patch.getBank() +
                                            " " + patch.getProgram());
        return buf.toString();
    }
*/

    public Conductor getConductor() {
        return JavaSoundConductor.the();
    }

    public SynthNode getParent() { return null; }

}
