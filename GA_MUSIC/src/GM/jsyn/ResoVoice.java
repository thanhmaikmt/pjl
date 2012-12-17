package GM.jsyn;

import GM.music.*;
import GM.jsyn.*;
import GM.io.*;
import com.softsynth.jsyn.*;
import com.softsynth.jsyn.circuits.*;

public class ResoVoice extends SynthNote {
    Filter_StateVariable flt;

    ResoVoice(SynthContext synthContext) {
        super(synthContext);
        add(flt = new Filter_StateVariable(synthContext));
        flt.resonance.set(0, .005);
        flt.amplitude.set(0, 1.0);
        addPort(output = flt.output);
        amplitude=flt.amplitude;
        frequency=flt.frequency;
    }


    public void noteOn(int tickOn,double freq,double amp) {
        flt.frequency.set(tickOn, freq);
        flt.input.set(tickOn, amp);
        flt.input.set(tickOn + 1, 0.0);
        start(tickOn);
    }

    public void noteOff(int time) {
        stop(time);
    }
}
