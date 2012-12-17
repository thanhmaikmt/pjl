//@TODO  THIS A COMPLETE AND UTTER MESS.
//    Seperate timing and Player management

package GM.music;

import GM.tweak.*;
import java.util.*;
import GM.music.Simphoney;

public abstract class Conductor extends Observable implements Observer {

    static protected double tickRateTPS = 0.0;
   // static Vector<Player> players = new Vector();


   static Vector<Conductor> conductors = new Vector<Conductor>();
   static public final TweakableDouble tempoBPM = new TweakableDouble(10.0,
            300.0,
            120.0, 1.0, "Tempo");
    static public final TweakableInt state = new TweakableInt(0, 1, 1,
            "StartStop");
    static protected Conductor master;

    static boolean isRunningFlag;
    static Vector<Part> sections;

    protected Conductor() {
        conductors.add(this);
        if (conductors.size() == 1) {
            tempoBPM.addObserver(this);
            master = this;
            state.addObserver(this);
            sections = new Vector<Part>();
        }
    }


    static public Conductor the() {
        return master;
    }

    static public double masterRate() {
        assert (tickRateTPS > 0.0);
        return tickRateTPS;
    }

    static public long masterTickNow() {
        try {
            return master._getTickNow();
        } catch (Exception e) {
            e.printStackTrace();
            assert (false);
            return 0;
        }
    }




    protected abstract long _getTickNow();


    static public long getTickNow() {
        return master._getTickNow();
    }


    static public void restart() {
        System.out.println(" conductor restarted ");
        master._start();
        isRunningFlag = true;
        Simphoney.getSong().getBand().allocate(true);
        master.setChanged();
        master.notifyObservers("START");
    }


    static public void stop() {
        System.out.println(" conductor stop ");
        master._kill();
        isRunningFlag = false;
        master.setChanged();
        master.notifyObservers("STOP");
    }



    /** actual time relative to starting program
     *
     */

    static public Time getAbsoluteTime() {
        try {
            return master._getTime();
        } catch (Exception e) {
            e.printStackTrace();
            assert (false);
            return new Time(0);
        }
    }

    static public void init() throws Exception {

        master.update(null, null);
        Iterator iter = conductors.iterator();
        while (iter.hasNext()) {
            ((Conductor) iter.next())._start();
        }
    }

    abstract public void setMute(boolean yes);

    abstract public boolean isMute();

    public void update(Observable o, Object arg) {
        assert (this == master);
        if (o == tempoBPM || o == null) {
            double tt = tempoBPM.doubleValue();
            Time when = getAbsoluteTime();
            setTempo(tt, when);
        } else if (o == state) {
            setMute(!state.isOn());

            /*
            switch (state.intValue()) {
            case 0:
                stop();
                break;
            case 1:
                restart();
                break;
            default:
                System.err.println(" Unkown state ");
                break;
            }
*/
        } else {
            System.out.println(" unkown updater " + o + " arg " + arg);
        }
    }

    static private void setTempo(double bpm, Time when) {

       // System.out.println(" SET TEMPO " + bpm + " @ " + when);
        Iterator iter = conductors.iterator();

        while (iter.hasNext()) {
            ((Conductor) iter.next())._setTempo(bpm, when);
        }

    }

    static public long durationToTicks(Time dur) {
        return (int) ((tickRateTPS * dur.getBeat() * 60.0) /
                      tempoBPM.doubleValue());
    }

    //   abstract public double tickRate();

    abstract public long getTickAt(Time on);

    // abstract public long getTickNow();

    abstract public void sleepUntilJustBefore(Time time) throws Exception;

    abstract public void sleepUntilJustBefore(long tick) throws Exception;

    abstract public void setLatencyInTicks(long ticks);

    static public boolean isRunning() {
        return isRunningFlag;
    }

    static public boolean isLooping() {
        return true; //loopy;
    }

    abstract protected void _setTempo(double bpm, Time when);

    // abstract protected long _getTickCount();

    abstract protected Time _getTime();

    abstract protected void _start();

    abstract protected void _kill();


    static boolean exists() {
        return master != null;
    }

/*
    static void addSection(Section section) {
       // System.out.println(" ADD SECTION " + section.start + " " + section.end);
        master.addObserver(section);
        restart();
        master.setChanged();
        master.notifyObservers("SECTION");

    }
*/
}
