package GM.jsyn;

import java.awt.*;
import java.applet.Applet;
import com.softsynth.jsyn.*;
import GM.Brad.*;
import GM.music.*;
import GM.jsyn.*;
import GM.io.*;

public class Bass extends SynthNote {



 //   class JNote {
        Strum bass1, bass2;
        MultiplyUnit ampoutL, ampoutR;

        EnvelopePlayer benvplayer1, benvplayer2;
        SynthEnvelope benv;
        double[] evpdata = {
                           0.01, 0.7,
                           .5, 1.8,
                           1.0, 1.4,
                           2.0, 0.0
        };

        Filter_LowPass bfilt1, bfilt2;
        double amp;
        double pan;


 //   }



/*
  public Bass(GeneReader r) throws Exception {
     super(null);
   }
*/
   /* public Bass(String name) throws SynthException {
 //       super((Conductor)null);
        assert (false);
        setName(name);
        jsynStuff();
    }
*/
    void jsynStuff() {
        this.amp = 1.0;
        this.pan = 0.5;
        bass1 = new Strum();
        bass2 = new Strum();
        //  noteOut = new LineOut();
        benv = new SynthEnvelope(evpdata);
        benvplayer1 = new EnvelopePlayer();
        benvplayer2 = new EnvelopePlayer();

        bfilt1 = new Filter_LowPass();
        bfilt2 = new Filter_LowPass();

        bass1.output.connect(benvplayer1.amplitude);
        bass2.output.connect(benvplayer2.amplitude);

        benvplayer1.output.connect(bfilt1.input);
        benvplayer2.output.connect(bfilt2.input);
        bfilt1.amplitude.set(2.0);
        bfilt2.amplitude.set(2.0);
        bfilt1.frequency.set(2000.0);
        bfilt2.frequency.set(2000.0);
        bfilt1.Q.set(0.3);
        bfilt2.Q.set(0.3);

        ampoutL = new MultiplyUnit();
        ampoutR = new MultiplyUnit();
        bfilt1.output.connect(ampoutL.inputA);
        bfilt2.output.connect(ampoutR.inputA);
        //  ampoutL.inputB.set(amp);
        //  ampoutR.inputB.set(ampval);

   //     outputL = ampoutL.output; //.connect(0, noteOut.input, 0);
        output = ampoutR.output; //.connect(0, noteOut.input, 1);
    }

    public void play(Effect effect, int tickOn) {
        try {
            if (effect == null) {
                bass1.stop(tickOn);
                bass2.stop(tickOn);
                benvplayer1.stop(tickOn);
                benvplayer2.stop(tickOn);
                bfilt1.stop(tickOn);
                bfilt2.stop(tickOn);
                ampoutL.stop(tickOn);
                ampoutR.stop(tickOn);
                //  noteOut.stop(tickOn);
            } else {

                Note note = (Note) effect;
                double pch = note.getFrequency();
                double ampval = this.amp * note.getVelocity();
                bass1.start(tickOn);
                bass2.start(tickOn);
                benvplayer1.start(tickOn);
                benvplayer2.start(tickOn);
                bfilt1.start(tickOn);
                bfilt2.start(tickOn);
                ampoutL.inputB.set(tickOn, ampval * (pan));
                ampoutR.inputB.set(tickOn, ampval * (1.0 - pan));

                ampoutL.start(tickOn);
                ampoutR.start(tickOn);
//      noteOut.start(tickOn);

                benvplayer1.envelopePort.clear(tickOn);
                benvplayer1.envelopePort.queue(tickOn, benv);
                benvplayer2.envelopePort.clear(tickOn);
                benvplayer2.envelopePort.queue(tickOn, benv);
                bass2.go(tickOn, pch + (0.005 * pch), 30.0, 50.1, 20000.0, 10);
                bass1.go(tickOn, pch + ( -0.005 * pch), 30.0, 50.1, 20000.0, 10);
            }
        } catch (SynthException e) {
            System.err.println(e);
        }

    }

    public boolean isMelodic() { return true; }
//     public void setAmp(double aaa)
//     {
//  ampoutL.inputB.set(aaa);
//  ampoutR.inputB.set(aaa);
//     }

}
