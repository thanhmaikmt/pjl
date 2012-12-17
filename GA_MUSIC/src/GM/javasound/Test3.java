package GM.javasound;

import javax.sound.midi.*;

public class Test3 {
    static Sequencer sequencer;
    static Sequence sequence;
    static Track track;
    static final int NOTEON = 144;
    static final int NOTEOFF = 128;


    static int tPQ = 1000;
    public static void main(String args[]) throws Exception {

        Sequencer sequencer = MidiSystem.getSequencer();
        Sequence sequence;
        Receiver r;
        //     r=new MyReceiver3("REC1");
        sequencer.open();
        //   sequencer.getTransmitter().setReceiver(r);
        sequencer.setTempoInBPM(120.0f);

        sequence = new Sequence(Sequence.PPQ, tPQ);
        track = sequence.createTrack();
        sequencer.addMetaEventListener(new MetaClip());

        sequencer.setSequence(sequence);

        buildTrack();
        sequencer.start();

    }

    static void buildTrack() throws Exception {
        int ch = 0;
        long tick = 100;

        for (int count = 0; count < 30; count++, tick += tPQ) {
            ShortMessage message = new ShortMessage();

            message.setMessage(Test3.NOTEON, 1, 70, 100);
            MidiEvent event = new MidiEvent(message, tick);
            Test3.track.add(event);

            MetaMessage meta = new MetaMessage();
            meta.setMessage(127, "RIDE".getBytes(), 4);
            MidiEvent mevent = new MidiEvent(meta, tick);
            Test3.track.add(mevent);

        }

    }
}


class MyReceiver3 implements Receiver {

    long ref;
    String name;
    MyReceiver3(String name) {
        this.name = name;
    }

    public void send(MidiMessage mess, long timeStamp) {
        long t = System.nanoTime();
        byte b[] = mess.getMessage();
        System.out.println(b[0] + " " + b[1] + "       \t" +
                           (1.0 - (t - ref) / 1e9) + "   \t" + timeStamp);
        ref = t;
    }

    public void close() {
        System.out.println(" CLOSED");
    }
}
