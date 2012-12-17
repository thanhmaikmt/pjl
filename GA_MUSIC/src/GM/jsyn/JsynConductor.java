package GM.jsyn;

import GM.music.*;


import java.util.*;


/**
 * MContext description.
 *
 * @author P.J.Leonard
 * @version (0.1)
 */

import com.softsynth.jsyn.*;

//import com.softsynth.jsyn.view102.*;


public final class JsynConductor extends Conductor {

  //  protected double tickRateTPS = 0.0; // master ticks per second
    protected double ticksPerBeat;
    protected Time refTime;
    protected long refTick;
    protected long tickOff;
    protected boolean isRunning = false;
    protected long startTimeSystemMilli;
    protected double sampleRate;
    long latencyInTicks;
    public static boolean slave = false;

    SynthContext context;

    static JsynConductor the = null;
    final public static int INIT=0;
    final public static int OK=1;
    final public static int FAIL=-1;

    static public  int status = INIT;

    static public JsynConductor the() {
        if (the == null) {
            the = new JsynConductor();
        }
        return the;
    }

    private JsynConductor() {

        try {
            com.softsynth.jsyn.Synth.requestVersion(141);
            // for SynthContext
            //   Synth.setTrace(Synth.VERBOSE);

            if (slave) {
                sampleRate = 44100.0;
                com.softsynth.jsyn.Synth.startEngine(Synth.FLAG_NON_REAL_TIME,
                                                     sampleRate);
            } else {
                com.softsynth.jsyn.Synth.startEngine(0);
            }

            context = Synth.getSharedContext();

            if (sampleRate <= 0.0) {
                sampleRate = Synth.getFrameRate();
            }

            if (tickRateTPS > 0.0)
                System.err.println(
                        " tickRateTPS has already been set. You should create JSynConductor first ");
            tickRateTPS = context.getTickRate();
            latencyInTicks = (int) (tickRate() * 0.1);
            status=OK;
        } catch(SynthException ex) {
            ex.printStackTrace();
            status=FAIL;
        }

    }

    public void setMute(boolean yes) {
        assert(false);
    }


    public boolean isMute() { assert(false); return true; }

    public double sampleRate() {
        return sampleRate;
    }

    public final void _start() {
        System.out.println(" Starting Jsyn CONDUCTOR ");

        refTime = new Time(0);
        tickOff = _getTickNow();
        refTick = tickOff;
        startTimeSystemMilli = System.currentTimeMillis();
        isRunning = true;
    }


    protected void _kill() {
        isRunning = false;
        assert (false);
    }

    public boolean _isRunning() {
        return isRunning;
    }

    public final double tickRate() {
        return context.getTickRate();
    }



    private long getLatencyInTicks() {
        return latencyInTicks;
    }

    public void setLatencyInTicks(long ticks) {
        latencyInTicks=ticks;
    }

    public void sleepUntilJustBefore(long time) throws Exception {
        long diff=context.getTickCount()-time;

        if (diff> 0) throw new GMSyncException(diff);
        int tick = (int) (time - getLatencyInTicks());
        context.sleepUntilTick(tick);
    }


    public void sleepUntilJustBefore(Time time) throws Exception {
        assert (isRunning);
        //     System.out.println("Sleep untill" + time);
        long tick = getTickAt(time) - getLatencyInTicks();
        context.sleepUntilTick((int) tick);
        //    System.out.println(" YAWN");
    }


    public final long getTickAt(Time t) {
        return (long) (t.getBeat() * ticksPerBeat) + tickOff;
    }


    public Time _getTime() {
        long tick = _getTickNow();
        double t = ((double) (tick - tickOff)) / (double) ticksPerBeat;
        return new Time(t);
    }


    protected void _setTempo(double tempo, Time when) {
        refTime = when;
        refTick = getTickAt(when);
        ticksPerBeat = tickRateTPS * 60.0 / tempo;
        tickOff = refTick - (long) (((double) when.getBeat()) * ticksPerBeat);
        // ticksPerMilli = masterRateTPS/1000.0;
    }


    public final long _getTickNow() {
        return context.getTickCount();
    }


    public SynthContext getContext() {
        return context;
    }

}
