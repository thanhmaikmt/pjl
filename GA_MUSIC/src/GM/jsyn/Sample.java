package GM.jsyn;

import GM.*;
import GM.music.*;
import java.io.*;
import java.net.*;


import com.softsynth.jsyn.*;


class Sample extends SynthNote {


    static public String paramBase;

    URL url;
    String sampName;

    SynthSample sample;
    SynthSample sampleZero;
    SampleReader_16V1 samplePlayer;
    SynthEnvelope envelope;
    EnvelopePlayer envPlayer;


    final int NUM_FRAMES = 64;
    double rampUpTime = 0.0; // so we can hear pops
    double rampDownTime = 0.2;

    Sample(SynthContext c, URL url) throws Exception {
        super(c);
        DataInputStream in = null;
        URLConnection connection = url.openConnection();
        in = new DataInputStream(connection.getInputStream());

        switch (SynthSample.getFileType(url.getFile())) {
        case SynthSample.AIFF:
            sample = new SynthSampleAIFF(getSynthContext());
            break;
        case SynthSample.WAV:
            sample = new SynthSampleWAV(getSynthContext());
            break;
        default:

            //      SynthAlert.showError(this, "Unrecognized sample file suffix.");
            break;
        }

        if (sample != null) {
            sample.load(in);
        }

        /* Create a unit generator to play the sample. */
        add(samplePlayer = new SampleReader_16V1(getSynthContext()));
        short zeros[] = {0, 0, 0, 0};
        sampleZero = new SynthSample(getSynthContext(), zeros.length, 1);
        sampleZero.write(zeros);

        add(envPlayer = new EnvelopePlayer(getSynthContext()));
        double data[] = {
                        rampUpTime, 1.0,
                        rampDownTime, 0.0
        };
        envelope = new SynthEnvelope(getSynthContext(), data);

        /* Create a unit generator to output the sound from the player. */

        /* Connect sample player to output. */
        samplePlayer.output.connect(envPlayer.amplitude);

        output = envPlayer.output; // .connect(0, noteOut.input, 1);
        amplitude=samplePlayer.amplitude;
    }


    public void noteOn(int time, double freq,double amp) {
        samplePlayer.samplePort.clear(time);
        samplePlayer.samplePort.queue(time, sample);
        envPlayer.envelopePort.queue(time, envelope, 0, 1);
        amplitude.set(time,amp);
        start(time);
    }

    public void noteOff(int time) {
        stop(time);
    }


    public Sample(SynthContext c,
                  String sampName) throws Exception {
        this(c, God.resolveSampleURL(sampName + ".wav"));
        this.sampName = sampName;
    }

}
