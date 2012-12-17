package GM;

import com.softsynth.jsyn.*;
import com.softsynth.jsyn.util.*;

public class TestJSYN2 extends Thread {

    int oneK=1028;
    int framesPerRead = oneK;
    int sampleQueueSize = oneK*10;

    final static int Fs=44100;
    final static double freq=1;

    SampleWriter_16F1 writer;
    SampleQueueInputStream inStream;
    SineOscillator sin;

    public TestJSYN2() {
        Synth.requestVersion(142);
        Synth.startEngine(Synth.FLAG_NON_REAL_TIME, Fs);
     //   Synth.startEngine(0,Fs);
        sin = new SineOscillator();
        sin.frequency.set(0, freq);
        sin.amplitude.set(0, .9);
        writer = new SampleWriter_16F1();
        writer.input.connect(sin.output);

        inStream = new SampleQueueInputStream(writer.samplePort,
                                              sampleQueueSize, 1);
    }

    public void run() {
        inStream.start(0);
        writer.start();
        sin.start();
        short last = 0;
        short[] sbuff = new short[framesPerRead];
        int count = 0;
        boolean up = true;
        for (;;) { // We'll loop forever

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

    public static void main(String[] args) {
        System.out.println( 2*Fs/freq);
        new TestJSYN2().start();
    //   Synth.sleepUntilTick(100000000);
    }

}
