package GM.javasound;

import javax.sound.midi.*;
import com.sun.media.sound.AutoConnectSequencer;
import java.util.TimerTask;
import com.sun.media.sound.ReferenceCountingDevice;

/**
 * <p>Title: </p>
 *
 * <p>Description: </p>
 *
 * <p>Copyright: Copyright (c) 2005</p>
 *
 * <p>Company: </p>
 *
 * @author not attributable
 * @version 1.0
 */
public class Test{
    static Sequencer sequencer;
    static Sequence sequence;
    static Track track;
    static final int NOTEON = 144;
    static final int NOTEOFF = 128;

    public static Sequencer connectSequencer(Receiver rec)

            throws MidiUnavailableException {
        Sequencer seq = MidiSystem.getSequencer(false);

        // IMPORTANT: this code needs to be synch'ed with
        //            all AutoConnectSequencer instances,
        //            (e.g. RealTimeSequencer) because the
        //            same algorithm for synth retrieval
        //            needs to be used!

      //  Receiver rec = null;
        MidiUnavailableException mue = null;

        // first try to connect to the default synthesizer
        if (rec == null) {
            try {
                Synthesizer synth = MidiSystem.getSynthesizer();
                synth.open();
                try {
                    rec = synth.getReceiver();
                } finally {
                    // make sure that the synth is properly closed
                    if (rec == null) {
                        synth.close();
                    }
                }
            } catch (MidiUnavailableException e) {
                // something went wrong with synth
                if (e instanceof MidiUnavailableException) {
                    mue = (MidiUnavailableException) e;
                }
            }
        }

        if (rec == null) {
            // then try to connect to the default Receiver
            try {
                rec = MidiSystem.getReceiver();
            } catch (Exception e) {
                // something went wrong. Nothing to do then!
                if (e instanceof MidiUnavailableException) {
                    mue = (MidiUnavailableException) e;
                }
            }
        }

        if (rec != null) {
            seq.getTransmitter().setReceiver(rec);
            if (seq instanceof AutoConnectSequencer) {
                ((AutoConnectSequencer) seq).setAutoConnect(rec);
            }
        } else {
            if (mue != null) {
                throw mue;
            }
            throw new MidiUnavailableException("no receiver available");
        }

        return seq;
    }

    static int tPQ=10000;
    public static void main(String args[]) throws Exception {

        boolean worksOk = true;
        Sequencer sequencer;
        Sequence sequence;
        Receiver r;
       // Synthesizer synth = MidiSystem.getSynthesizer();
      //  synth.open();
        r=new MyReceiver("REC1"); // r=synth.getReceiver();
        sequencer = connectSequencer(r);
        sequencer.open();

        sequence = new Sequence(Sequence.PPQ, tPQ);
        track = sequence.createTrack();
        sequencer.setSequence(sequence);

        buildTrack();
        sequencer.start();
      //  r = sequencer.getTransmitter().getReceiver();
      //  System.out.println(" Reciever is now ==== " + r);

    }

    static void buildTrack() throws Exception {
        int ch = 0;
        long tick = 100;
        for (int pitch = 60; pitch < 80; pitch++, tick += 400) {
            ShortMessage message = new ShortMessage();
            message.setMessage(Test.NOTEON, ch, pitch, 100);
            MidiEvent event = new MidiEvent(message, tick);
            Test.track.add(event);
            message = new ShortMessage();
            message.setMessage(Test.NOTEOFF, ch, pitch, 0);
            event = new MidiEvent(message, tick + 200);
            Test.track.add(event);
        }
    }
}


class MyReceiver implements Receiver {

    long ref;
    String name;
    MyReceiver(String name) {
        this.name=name;
    }
    public void send(MidiMessage mess, long timeStamp) {
        long t=System.nanoTime();
        System.out.println(name + " " + mess + " " + (t-ref));
        ref=t;
    }

    public void close() {
        System.out.println(" CLOSED");
    }
}

