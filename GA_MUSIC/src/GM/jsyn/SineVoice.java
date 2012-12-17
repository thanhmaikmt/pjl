package GM.jsyn;

import GM.music.*;
import GM.jsyn.*;
import GM.io.*;
import com.softsynth.jsyn.*;
import com.softsynth.jsyn.circuits.*;

public class SineVoice extends SynthNote {

    SineOscillator flt;
    boolean on = false;

    public SineVoice(SynthContext synthContext) {
        super(synthContext);
        add(flt = new SineOscillator(synthContext));
        flt.frequency.set(0, 200.0);
        flt.amplitude.set(0, 1.0);
        addPort(output = flt.output);
    }

    public void play(Effect effect, int tickOn) {
        if (on) {
            return;
        }
        try {
            if (effect == null) {
//                    stop(tickOn);
            } else {
                start(tickOn);
            }
        } catch (SynthException e) {
            System.err.println(e);
        }

    }


}


