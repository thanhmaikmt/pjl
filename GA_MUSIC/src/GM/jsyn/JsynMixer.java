package GM.jsyn;

import GM.music.*;
import java.util.*;
import com.softsynth.jsyn.*;
import com.softsynth.jsyn.util.*;
import GM.javasound.*;

/**
 * Write a description of class Mixer here.
 *
 * @author DR pJ
 * @version 1
 */
public class JsynMixer extends GMMixer {
    /**
     * Constructor for objects of class Mixer
     */

    SynthMixer mixer;
    SampleWriter_16F2 writer;
    SynthContext context;
  //  SynthSample sample;
    public int numFrames=256;
    SampleQueueInputStream inStream;

    public JsynMixer(SynthContext context) {
        super();
        writer = new SampleWriter_16F2(context);
//        sample = new SynthSample(numFrames,2);
//        writer.samplePort.queueLoop(sample);
        this.context = context;
        inStream=new SampleQueueInputStream(writer.samplePort,numFrames,2);
    }

    public int read(short d[],int off,int n) {
        if (inStream.getOverflowed()) {
            System.err.println(" OVERFLOW ");
        }
        if (n > numFrames) n = numFrames;
        n = inStream.read(d,off,n);
        return n;
    }

    public int getMaxFramesPerRead() {
        return numFrames;
    }

    public int getFrameSizeInBytes() {
        return 4;
    }

    public int getNChannel() {
        return 2;
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
//        out = new LineOut(context);
        writer.input.connect(0, mixer.getOutput(0), 0);
        writer.input.connect(1, mixer.getOutput(1), 0);
        for (int i = 0; i < n; i++) {
            JsynVoice v = (JsynVoice) (voices.elementAt(i));
            v.addObserver(this);

            //@TODO parts ?
   //         if (v.note.outputL != null) {
   //             mixer.connectInput(i * 2, v.note.outputL, 0);
   //         } else
            if (v.note.output != null) {
                mixer.connectInput(i * 2, v.note.output, 0);
            }

            if (v.note.output != null) {
                mixer.connectInput(i * 2 + 1, v.note.output, 0);
            }
            mixer.setGain(i * 2, 0, 1.0);
            mixer.setGain(i * 2 + 1, 1, 1.0);
        }
        writer.start();
        mixer.start();
        inStream.start(0);
        try {
             Thread t=new PlaySoundStream(this);
             t.start();
         }catch(Exception e) {
             e.printStackTrace();
        }
   //     isDirty=false;
    }

    public void kill() {
        if (mixer != null) {
            mixer.stop();
            inStream.stop(0);
            writer.stop();
        }
        voices = null;
    }

}
