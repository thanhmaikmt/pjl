package GM.jsyn;

import GM.music.*;
import java.util.*;
import com.softsynth.jsyn.*;

/**
 * Write a description of class Mixer here.
 *
 * @author DR pJ
 * @version 1
 */
public class JsynMixerToLineOut extends GMMixer {
    /**
     * Constructor for objects of class Mixer
     */

    SynthMixer mixer;
    LineOut  out;
    SynthContext context;

    public JsynMixerToLineOut(SynthContext context) {
        super();
        out = new LineOut(context);
        this.context = context;
    }


    public void rebuild(Vector voices) {
        //      Vector voices=band.getVoices();
        //      SynthContext context=band.getConductor().getContext();
        super.voices = voices;
        int n = voices.size();
        assert (n > 0);
        if (mixer != null) {
            mixer.stop();
        }

        mixer = new SynthMixer(n * 2, 2);
        out = new LineOut(context);
        out.input.connect(0, mixer.getOutput(0), 0);
        out.input.connect(1, mixer.getOutput(1), 0);
        for (int i = 0; i < n; i++) {
            JsynVoice v = (JsynVoice) (voices.elementAt(i));
            v.addObserver(this);
            //@TODO parts
//            if (v.note.outputL != null) {
//                mixer.connectInput(i * 2, v.note.outputL, 0);
//            } else
            if (v.note.output != null) {
                mixer.connectInput(i * 2, v.note.output, 0);
            }

            if (v.note.output != null) {
                mixer.connectInput(i * 2 + 1, v.note.output, 0);
            }
            mixer.setGain(i * 2, 0, 1.0);
            mixer.setGain(i * 2 + 1, 1, 1.0);
        }
        out.start();
        mixer.start();
   //     isDirty=false;
    }

    public void kill() {
        if (mixer != null) {
            mixer.stop();
        }
        if (out != null) {
            out.stop();
        }
        voices = null;
    }

}
