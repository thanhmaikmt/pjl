package GM.music;

import java.util.*;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class SongSequencer extends Thread implements Observer {


    boolean stop;
    boolean killed = false;
    Time startTime=null;
    Time nextStartTime=null;
    static Time nextFreeTime=null;

   // long playTimeTotal;
   // long totalPlayTimeMilli;

    Song song;
    Part part;


    public SongSequencer(Song song) {
        this.song = song;
        stop = true;
    }

    public void update(Observable o, Object arg) {
        String str = (String) arg;
        if (str.equals("START")) {
            interrupt();
        }
    }

   /* public long playTimeInMillis() {
        return playTimeTotal;
    }
    */

    public synchronized void run() {

        stop = false;
        Conductor.the().addObserver(this);

        setPriority(Thread.MAX_PRIORITY);

        if (PhraseSequencer.monitor) {
            System.out.println(" Song player ");
        }

  //      startTimeMilli =System.currentTimeMillis();

        Time now = Conductor.getAbsoluteTime();

        if (nextFreeTime == null) {
            nextStartTime=now;
        } else {
            if (nextFreeTime.compareTo(now) <=0 ) {
                nextStartTime = now;
            } else {
                nextStartTime = nextFreeTime;
            }
        }
        //@ TODO  what does flag that voice is no longer being used ?
        while (true) {

            if (killed) {
                return;
            }

            while (!Conductor.isRunning() || stop) {
                //        System.out.println("Waiting " + stop);
                try {
                    stop = true;
                    wait();
                    System.out.println(" SHOULD NOT HAPPEN ");
                } catch (InterruptedException ex) {
                    stop = false;

                    now = Conductor.getAbsoluteTime();
                    nextStartTime = now;

//                 //   System.out.println(" INTERUPTED ");
                    //                  sync();
                }
            }

            if (killed) {
                return;
            }

            startTime = nextStartTime;
            part = song.nextPartToPlay();

            if (part != null) {
                synchronized (part) {
                    Iterator<Phrase> iter = part.getPhrases().iterator();
                    while (iter.hasNext()) {
                        Phrase phrase = iter.next();
                        PhraseSequencer seq = new PhraseSequencer(phrase, startTime);
                        seq.start();
                    }
                }

                nextStartTime = startTime.add(part.len);
         //       playTimeTotal += part.len.getBND()[0];
                nextFreeTime =nextStartTime; // .add(part.len);
                if (PhraseSequencer.monitor) System.out.println(" nxtStart" + nextStartTime  + "   " + part.len);

            } else {
             //   if (Sequencer.monitor) System.out.println(" NULL PART");
                nextStartTime = startTime.add(new Time(4,0,1));

            }

            try {
                Conductor.the().sleepUntilJustBefore(nextStartTime);
            } catch (Exception e) {
                e.printStackTrace();
            }
            /* possibly been killed whilst asleep  . .. .. ahhhh :-) */
            if (killed) return;

        }
    }

    public Time getDisplayTime() {
        if (stop) {
            return Time.ZERO;
        }

        if (startTime == null) {
            return Time.ZERO;
        }

        Time off=Time.ZERO;

        if (part != null) {
            off=part.start;
        }

        return Conductor.the().getAbsoluteTime().subtract(startTime).add(off);
    }

    void kill() {
        Conductor.the().deleteObserver(this); //  System.out.println(" KILL SEQ" );
        killed = true;
    }


}
