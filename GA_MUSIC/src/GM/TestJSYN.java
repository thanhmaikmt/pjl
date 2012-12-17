package GM;

import javax.sound.sampled.*;
import com.softsynth.jsyn.*;
import com.softsynth.jsyn.util.*;

public class TestJSYN {


    boolean doTestSleep = true;
    int framesPerRead = 512;
    int sampleQueueSize = framesPerRead*60;

    final static int Fs=44100;
    final static double freq=1;
    int nChannel = 1;
    int sampSizeInBits = 16;

    Note note;
    SampleWriter_16F1 writer;
    SampleQueueInputStream inStream;
    SineOscillator sin;

    public TestJSYN() {
        Synth.requestVersion(141);
        Synth.startEngine(0); // Synth.FLAG_NON_REAL_TIME, Fs);

        note = new Note();

        Thread t = new MyRunner();
        t.start();

        if (doTestSleep) {
            long tnow = System.currentTimeMillis();
            for (int i = 0; i < 1000000; i++) {
                Synth.sleepUntilTick(100 * i);
                long tlast = tnow;
                tnow = System.currentTimeMillis();
          //      System.out.println(tnow - tlast);
            }
        }
    }

    public static void main(String[] args) {
        System.out.println( 2*Fs/freq);
        new TestJSYN();
    }

    class Note extends SynthNote {

        Note() {
            add(sin = new SineOscillator());
            sin.frequency.set(0, freq);
            sin.amplitude.set(0, .9);
            addPort(output = sin.output);
            add(writer = new SampleWriter_16F1());
            writer.input.connect(sin.output);

            inStream = new SampleQueueInputStream(writer.samplePort,
                                                  sampleQueueSize, 1);
            inStream.start(0);
            start();

        }
    }


    class MyRunner extends Thread {

        public void run() {
            short last = 0;
            short[] sbuff = new short[framesPerRead];
            int count = 0;
            boolean up = true;
            for (; ; ) { // We'll loop forever

                if (inStream.getOverflowed()) {
                    System.err.println(" OVERFLOW ");
                    System.exit( -1);
                }

                int nread = inStream.read(sbuff, 0, framesPerRead);
                if (nread != framesPerRead) {
                    System.out.println(" Ooops lost some ");
                    System.exit( -1);
                }

                /** find period by looking for a change of slope */
                for (int i = 0; i < nread; i++) {
                    if (up && (sbuff[i] < last)) {
                        System.out.println(count);
                        up = false;
                        count = 0;
                    } else if (!up && (sbuff[i] > last)) {
                        System.out.println(count);
                        up = true;
                        count = 0;
                    }
                    count++;
                    last = sbuff[i];
                }

            }

        }
    }
}
