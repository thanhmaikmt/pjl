package GM.jsyn;

import GM.music.*;
import GM.jsyn.*;
import com.softsynth.jsyn.*;
import com.softsynth.jsyn.circuits.*;
import GM.io.*;

public class DBuff extends SynthNote {


    InterpolatingDelayUnit iDelay;
    InterpolatingDelayUnit iDelay2;
    MultiplyAddUnit multAdd;
    WhiteNoise wtNoise;
    public SynthInput feedBack;
    EnvelopePlayer envPlay;
    SynthEnvelope envelope;
    MultiplyUnit mult;
    ParabolicEnvelope prblEnv;
    AddUnit add;
    MultiplyUnit mult2;
    double unitDelay;

    public DBuff(SynthContext synthContext) {
        super(synthContext);
        add(iDelay = new InterpolatingDelayUnit(synthContext, 1.0));
        frequency = new SynthDistributor(this, "frequency");
        add(iDelay2 = new InterpolatingDelayUnit(synthContext, 1.0));
        add(multAdd = new MultiplyAddUnit(synthContext));
        add(wtNoise = new WhiteNoise(synthContext));

        add(envPlay = new EnvelopePlayer(synthContext));
        double[] envelopeData = {
                                0.0, 0.0,
                                0.004, 0.9,
                                0.005, 0.00000005,
        };

        envelope = new SynthEnvelope(synthContext, envelopeData);
        envelopeData = null;
        envelope.setSustainLoop( -1, -1);
        envelope.setReleaseLoop( -1, -1);

        add(mult = new MultiplyUnit(synthContext));
        add(prblEnv = new ParabolicEnvelope(synthContext));
        add(add = new AddUnit(synthContext));
        add(mult2 = new MultiplyUnit(synthContext));

        addPort(amplitude = envPlay.amplitude, "amplitude");
        frequency.connect(mult2.inputB);
        iDelay.output.connect(iDelay2.input);
        iDelay2.output.connect(multAdd.inputA);
        multAdd.output.connect(iDelay.input);
        wtNoise.output.connect(multAdd.inputC);

        addPort(feedBack = multAdd.inputB, "feedBack");
        feedBack.setup( -1.0, 0.98, 1.0);
        addPort(output = iDelay2.output, "output");
        envPlay.rate.set(0, 1.0);
        envPlay.output.connect(wtNoise.amplitude);
        envPlay.output.connect(add.inputA);

        double T = 1.0 / synthContext.getFrameRate();

        unitDelay = 4 * T;
        prblEnv.amplitude.set(0, 1.0);
        add.inputB.set(0, -0.3);
        add.output.connect(prblEnv.triggerInput);
        mult2.inputA.set(0, 55.0);
        mult2.output.connect(prblEnv.frequency);
    }





    public void noteOff(int time) {
        envPlay.envelopePort.queueOff(time, envelope);
        stop(time);
    }

    public void noteOn(int time,double freq,double amp) {

        double dTime = 0.5 / freq - unitDelay;

        iDelay.delay.set(time, dTime);
        iDelay2.delay.set(time, dTime);
        envPlay.amplitude.set(time, amp);
        envPlay.envelopePort.queue(time, envelope);

        start(time);

    }



}
