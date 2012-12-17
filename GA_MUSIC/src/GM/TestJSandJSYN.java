package GM;

import javax.sound.sampled.*;
import com.softsynth.jsyn.*;
import com.softsynth.jsyn.util.*;

public class TestJSandJSYN {


    boolean doRead = true;
    boolean overrideValue = false;
    boolean doTestSleep = true;
    int framesPerRead = 512;
    int sampleQueueSize = framesPerRead * 32;
    int lineOutBufferSize = sampleQueueSize;

    int nChannel = 2;
    int sampSizeInBits = 16;

    Note note;
    SampleWriter_16F2 writer;
    SampleQueueInputStream inStream;
    SineOscillator sin;
    SourceDataLine line = null; // And write it here.

    public TestJSandJSYN() {

        Synth.requestVersion(141);
        Synth.startEngine(Synth.FLAG_NON_REAL_TIME, 44100);

        note = new Note();

        Thread t = new MyRunner();
        t.start();

        if (doTestSleep) {
            long tnow = System.currentTimeMillis();
            for (int i = 0; i < 100000; i++) {
                Synth.sleepUntilTick(10000 * i);
                long tlast = tnow;
                tnow = System.currentTimeMillis();
                System.out.println(tnow - tlast);
            }
        }
    }

    public static void main(String[] args) {
        new TestJSandJSYN();
    }

    class Note extends SynthNote {

        Note() {
            add(sin = new SineOscillator());
            sin.frequency.set(0, 200.0);
            sin.amplitude.set(0, 1.0);
            addPort(output = sin.output);
            add(writer = new SampleWriter_16F2());
            writer.input.connect(0, sin.output, 0);
            writer.input.connect(1, sin.output, 0);
            start();
            inStream = new SampleQueueInputStream(writer.samplePort,
                                                  sampleQueueSize, 2);
            inStream.start(0);
        }
    }

    void myassert(boolean x) {
        if (!x) System.exit(-1);
    }

    class MyRunner extends Thread {

        public void run() {
            int bytesPerFrame = framesPerRead * 4; // 2 16 bit numbers

            int nShort = framesPerRead * 2;

            try {
                DataLine.Info info = new DataLine.Info(SourceDataLine.class,
                        new AudioFormat(44100, sampSizeInBits, nChannel, true, false),
                        lineOutBufferSize);

                line = (SourceDataLine) AudioSystem.getLine(info);
                line.open();

                /* sanity check  */
                System.out.println("line BufferSize = " + line.getBufferSize());

                short[] sbuff = new short[framesPerRead * nChannel];
                byte[] buffer = new byte[framesPerRead * nChannel * 2];

                boolean started = false;
                int count = 0;
                for (; ; ) { // We'll loop forever

                    if (inStream.getOverflowed()) {
                        System.err.println(" OVERFLOW ");
                        System.exit( -1);
                    }

                    if (doRead) {
                        int nread = inStream.read(sbuff, 0, framesPerRead);
                        myassert (nread == framesPerRead);
                    }

                    if (overrideValue) {
                        for (int i = 0; i < framesPerRead; i++) {
                            short val = (short) (32000 *
                                                 Math.sin(2.0 * Math.PI * 200.0 *
                                    count++ / 44100));
                            sbuff[2 * i] = sbuff[2 * i + 1] = val;
                            count = count % (44100 * 2);
                        }
                    }

                    for (int i = 0; i < nShort; i++) {
                        buffer[2 * i] = (byte) (sbuff[i] & 0xff);
                        buffer[2 * i + 1] = (byte) ((sbuff[i] & 0xff00) >> 8);
                    }

                    if (!started) {
                        line.start();
                        started = true;
                    }

                    int n = line.write(buffer, 0, nShort * 2);
                    myassert (n == nShort * 2);
                }

            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
}
