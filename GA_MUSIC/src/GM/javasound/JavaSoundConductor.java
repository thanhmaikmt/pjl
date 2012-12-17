package GM.javasound;

import GM.music.*;
import GM.*;

import java.util.*;


/**
 * MContext description.
 *
 * @author P.J.Leonard
 * @version (0.1)
 */

import javax.sound.*;
import javax.sound.midi.*;
import GM.music.Simphoney;

public final class JavaSoundConductor extends Conductor {


    //  protected double tickRateTPS = 0.0; // master ticks per second
    protected double ticksPerBeat;
    protected Time refTime;
    protected long refTick;
    protected long tickOff;
    protected boolean isRunning = false;
    protected long startTimeSystemMilli;
    protected double sampleRate;

  //  private Vector<Track> tracks = new Vector<Track>();
    private Track track;
    private Track recTrack;

    private Sequence sequence;

    final int NOTEON = 144;
    final int NOTEOFF = 128;
    long syncTol = 100;
    javax.sound.midi.Sequencer sequencer;
    long latencyInMilli = 10; // put events into track before actual play time
    boolean mute;

    //  boolean isRunning = false;
    private static JavaSoundConductor the = null;

    MidiConnection defaultConnection;


    static public JavaSoundConductor the() {
        if (the == null) {
            the = new JavaSoundConductor();
            //  the.start();
        }
        return the;
    }


    public void printInfo() {
        System.out.println(sequencer);
    }

    private JavaSoundConductor() {

        defaultConnection = new MidiConnection(
            MidiHub.transHandleOf(sequencer=MidiHub.sequencer),
            MidiHub.recvHandleOf(MidiHub.defaultMidiOut));


        the = this;
        if (tickRateTPS <= 0.0) {
            tickRateTPS = 500;
        }
        try {
            jbInit();
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }


    public long getTickAt(Time t) {
        return (long) (t.getBeat() * ticksPerBeat) + tickOff;
    }


    public boolean _isRunning() {
        return isRunning;
    }


    public void _start() {
        System.out.println(" Starting JavaSound CONDUCTOR ");
        setMute(false); // setdefaultConnection.connect();
        if (isRunning) {
            return;
        }

        // Should open the sequencer
        defaultConnection.connect();


        refTime = new Time(0);
        startTimeSystemMilli = System.currentTimeMillis();
        refTick = tickOff;

        try {
            assert(tickRateTPS != 0);
            int irate = (int) tickRateTPS;
            sequence = new Sequence(Sequence.PPQ, irate);
            float mpq = (float) (1000000.0 * (tickRateTPS /
                                              irate));
            System.out.println(" Milli per quater = " + mpq);
            sequencer.setTempoInMPQ(mpq);
            System.out.println("Resolution =" + sequence.getResolution() +
                               " | " + tickRateTPS);

            track = sequence.createTrack();
            recTrack=sequence.createTrack();
            ShortMessage message = new ShortMessage();
            message.setMessage(NOTEON, 1, 0,0);
            MidiEvent event = new MidiEvent(message, 10000000);
            recTrack.add(event);
            sequencer.setSequence(sequence);
            addEvent(0, 10000000, 50, 1, 0);

            sequencer.recordEnable(recTrack,-1);
            sequencer.startRecording();


        } catch (Exception e) {
            e.printStackTrace();
        }

        tickOff = masterTickNow();


        isRunning = true;
        Song song = Simphoney.getSong();
        if (song != null) {
            Band band = song.getBand();
            band.allocate(true);
        }

    }

    protected long _getTickNow() {
        long timeNowMilli = System.currentTimeMillis() - startTimeSystemMilli;
        return (long) ((timeNowMilli * tickRateTPS) / 1000.0);
    }

    protected Time _getTime() {
        long tick = _getTickNow();
        double t = ((double) (tick - tickOff)) / (double) ticksPerBeat;
        return new Time(t);
    }

    public long latencyInTicks() {
        return (long) ((tickRateTPS * latencyInMilli) / 1000.0);
    }

    public void setLatencyInTicks(long ticks) {
        latencyInMilli = (long) ((1000.0 * ticks) / tickRateTPS);
        System.out.println(" JavbaSound latency set to " + latencyInMilli +
                           " mS");
    }


   public void setMute(boolean yes) {
       System.out.println(" SET MUTE = " + yes);
       mute=yes;
       if (yes)defaultConnection.disconnect();
        else defaultConnection.connect();
    }

    public boolean isMute() { return mute; }

    public void _kill() {
        System.out.println(" KILLED ");
        Song song = Simphoney.getSong();
        if (song != null) {
            Band band = song.getBand();
            band.allocate(false);
        }

        sequencer.stop();
        defaultConnection.disconnect();

        if (sequence != null) {
            if (track != null) {
                sequence.deleteTrack(track);
            }
        }
        isRunning = false;
        sequence=null;
        track=null;
    }


    protected void _setTempo(double tempo, Time when) {
        refTime = when;
        refTick = getTickAt(when);
        ticksPerBeat = tickRateTPS * 60.0 / tempo;
        tickOff = refTick - (long) (((double) when.getBeat()) * ticksPerBeat);
    }


    synchronized public void sleepUntilJustBefore(Time time) throws Exception {

        if (!isRunning) return;
        long tickWhen = getTickAt(time);
        sleepUntilJustBefore(tickWhen);
    }

    synchronized public void sleepUntilJustBefore(long tickWhen) throws
            Exception {

        assert (isRunning);
        long timeNowMilli = System.currentTimeMillis() - startTimeSystemMilli;
        long tickNow = masterTickNow();

        long dur = (long) ((tickWhen - tickNow) / tickRateTPS * 1000.0 -
                           latencyInMilli);
        //   try {

        //  assert(false);
        //       System.out.println(" SLEEP TILL " + time + " dur (ms) = " + dur +
        //                         " timeNow (ms) " + timeNowMilli + " tickWhen " +
        //                        tickWhen +
        //                       " tickNow " + tickNow);

        if (dur < 0) {
            /* if (dur <= -latencyInMilli) {
                 System.err.println(" Buffer time error of " +
                                    (latencyInMilli + dur));
             } */

            if (dur < -syncTol) {
                Exception ex = new GMSyncException( -dur);
                ex.fillInStackTrace();
                throw ex;
            }
        } else {

            if (dur > 0) {
                try {
                    wait(dur);
                } catch (InterruptedException ex) {
                    // may be interuppted by a Conductor start
                }
            }
        }

    }

    /** add a note on at when of length dur */

    void addEvent(int pitch, long when, long dur, int ch, int vel) {
        //  System.out.println(" addEvent ch = " + ch);
        if (track == null) return;
        try {

            ShortMessage message = new ShortMessage();
            message.setMessage(NOTEON, ch, pitch, vel);
            MidiEvent event = new MidiEvent(message, when);
            track.add(event);

            message = new ShortMessage();
            message.setMessage(NOTEOFF, ch, pitch, 0);
            event = new MidiEvent(message, (when + dur));
            track.add(event);

        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }


    void setController(int chan, int cntrl, int val) {

        //    System.out.println("chan:cntrl:val   " + chan + " " + cntrl +
        //                       " " + val);
        long tick = masterTickNow(); ///At(_getTime());
        try {
            ShortMessage message;
            MidiEvent event;
            message = new ShortMessage();
            message.setMessage(ShortMessage.CONTROL_CHANGE, chan, cntrl, val);
            event = new MidiEvent(message, tick);
            track.add(event);

            /* This does not seem to work
              MidiChannel chans[] =JavaSoundSynth.the().synth.getChannels();
              chans[chan].programChange(p.getBank(),p.getProgram());
             */
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    void setPatch(int chan, Patch p) {

         System.out.println("chan:prog:bank   " + chan + " " + p.getProgram() +
                           " " + p.getBank());
        /** need to be running to set the patch */
        //  _start();

        long tick = masterTickNow(); ///At(_getTime());
        //  System.out.println(" set prog ch = " + p + " " + chan);
        try {
            ShortMessage message;
            MidiEvent event;
            message = new ShortMessage();
            message.setMessage(ShortMessage.CONTROL_CHANGE, chan, 0, p.getBank());
            event = new MidiEvent(message, tick);
            track.add(event);
            message = new ShortMessage();
            message.setMessage(ShortMessage.PROGRAM_CHANGE, chan, p.getProgram(),
                               0);
            event = new MidiEvent(message, tick + 1);
            track.add(event);

            /* This does not seem to work
              MidiChannel chans[] =JavaSoundSynth.the().synth.getChannels();
              chans[chan].programChange(p.getBank(),p.getProgram());
             */

        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }


    public double tickRate() {
        return masterRate();
    }

    private void jbInit() throws Exception {

    }


}
