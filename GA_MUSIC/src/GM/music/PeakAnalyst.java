package GM.music;
import java.util.*;
import GM.util.*;
import GM.javasound.*;
import GM.audio.FramedFeed;


public class PeakAnalyst implements Observer {
    double  peakShort;
    double  peakLong;
    double  decayShort;
    double  decayLong;
    double  riseShort;
    double  riseLong;
    double  decayShort1;
    double  decayLong1;
    double  riseShort1;
    double  riseLong1;
    double  riseInf;
    double  decayInf;
    double  riseInf1;
    double  decayInf1;
    double  average;
    double  noiseLevel;

  //  double  hsyterFact; //
  //  boolean hold;
    double  rate;
    int frameSize;
    Thread pulseWaitThread;
    int pulseTimeInSamples;
    long sampleCount;
    long pulseCount;

    static PeakAnalyst the;

    /**
     *
     * @param feed FramedFeed
     * @param shortT double decay time to smooth out freq time scale stuff.
     * @param longT double  decay Time to suss out pulses in the music.
     */


    static public PeakAnalyst the() {
        return the;
    }

    public PeakAnalyst(FramedFeed feed) {

        assert(the== null);
        the=this;

        rate=feed.getSampleRate();


        feed.addObserver(this);


        decayShort= MyMath.halfLifeToLambda(rate/100);
        riseShort = MyMath.halfLifeToLambda(rate/500);
        decayLong = MyMath.halfLifeToLambda(rate*0.2);
        riseLong  = MyMath.halfLifeToLambda(rate*0.02);
        decayInf  = MyMath.halfLifeToLambda(rate*5);
        riseInf   = MyMath.halfLifeToLambda(rate*5);

      /*
         System.out.println( decayShort);
        System.out.println( riseShort);
        System.out.println( decayLong);
        System.out.println( riseLong);
        System.out.println( decayInf);
        System.out.println( riseInf);
       */

        decayShort1=1.0-decayShort;
        riseShort1=1.0-riseShort;

        decayLong1=1.0-decayLong;
        riseLong1=1.0-riseLong;

        decayInf1=1.0-decayInf;
        riseInf1=1.0-riseInf;

        frameSize = feed.getWindowSize();


    }

    public void update(Observable o,Object arg) {
      //  System.out.println(" Listener.update() ");
        short v[] = (short []) arg;
        int n=v.length;
        for (int i=0;i< n;i++) {
            sampleCount++;
            double val = Math.abs(v[i]);

            if (val < peakShort) peakShort = peakShort*decayShort + val*decayShort1;
            else                 peakShort = peakShort*riseShort  + val*riseShort1;

            if (peakShort < peakLong) peakLong = peakLong*decayLong + peakShort*decayLong1;
            else                      peakLong = peakLong*riseLong  + peakShort*riseLong1;

            if (peakLong < average)   average = average*decayInf + peakLong*decayInf1;
            else                      average = average*riseInf  + peakLong*riseInf1;

            if (peakLong > average && pulseWaitThread != null) {
                pulseCount=sampleCount;
                pulseWaitThread.interrupt();
                pulseWaitThread=null;
            }
        }
      //  System.out.println(peakShort + " " + peakLong + " " + average);
    }

    public synchronized long waitForPulse(long milliMax) {
        assert(pulseWaitThread == null);
        pulseWaitThread=Thread.currentThread();
        try {
            wait(milliMax);
            System.out.println(" waitForPulse timed out" );
            pulseWaitThread=null;
        } catch(InterruptedException ex) {
            pulseWaitThread=null;
            return (long)((pulseCount*1000.0)/rate);
        }
        return -1;
    }
}
