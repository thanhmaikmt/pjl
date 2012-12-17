package GM.audio;

import java.lang.*;
import java.util.*;

/** Abstract class for audio grabbers.
    To view the data you add an observer which is notified when
    a frame is ready to be read.

                     |-----------window2-------------|
    |------------window1--------------|
    |                |---------chunk--|
    PLEASE add Obserervers before starting this !
 */

public abstract class FramedFeed extends Observable implements Runnable {

    private short peakV = 0;

    private int chunkSize;
    private int windowSize;
    protected double sampRate;
    protected int chunkSizeInBytes;
    protected byte[] byteData;

    private short[] windowData;
    private boolean bigendian;
    protected boolean isRunning = false;

    public FramedFeed(double rate,int frameSize) {
        //	setChunkSize(chunkSizeX);
        //      setWindowSize(windowSizeX);
        setChunkSize(frameSize);
        setWindowSize(frameSize);
        sampRate = rate;
    }

    public synchronized void setWindowSize(int size) {
        // @TODO fill this with old window
        windowData = new short[size];
        windowSize = size;
    }

    public synchronized void setChunkSize(int chunkSizeX) {
        chunkSize = chunkSizeX;
        chunkSizeInBytes = chunkSizeX * 2;
        byteData = new byte[chunkSizeInBytes];
    }

    public abstract void start();

    public abstract void stop();


    /**
     *  subclass must read form the audioinput
     */

    protected abstract int read(short[] data, int off, int n);

    public abstract short maxValue();

    private synchronized void doit() {

        for (int i = 0; i < windowSize - chunkSize; i++) {
            short v = windowData[i] = windowData[i + chunkSize]; /// @TODO System array copy here
        }

        // This read must block until data is available
        int n = read(windowData, windowSize - chunkSize, chunkSize);

        for (int i = windowSize - chunkSize ; i< chunkSize; i++) {
            short  v = windowData[i];
            if (v > peakV) {
                peakV = v;
            }
            if ( -v > peakV) {
                peakV = (short) ( -(int) v);
            }
        }

        if (n != chunkSize) {
            System.out.println(" Did not read a whole chunk " + n);
        }
        setChanged();
        notifyObservers(windowData);
//      System.out.println(" BOT OF RUN ");
    }

    public void run() {
        start();
   //     System.out.println(" Framed Feed: STARTED ");
        do {
            doit();
        } while (isRunning);
        System.out.println(" MyStream line not active ");
    }

    public short peakValue(boolean reset) {
        short tmp = peakV;
        if (reset) {
            peakV = 0;
        }
        return tmp;
    }

    public int getChunkSize() {
        return chunkSize;
    }

    public int getWindowSize() {
        return windowSize;
    }

    public double getSampleRate() {
        return sampRate;
    }

}
