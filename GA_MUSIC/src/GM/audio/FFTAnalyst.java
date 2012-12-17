package GM.audio;
import java.util.*;
import GM.fft.*;




public class FFTAnalyst extends Observable implements Observer {
    double  rate;
    int frameSize;
    Thread pulseWaitThread;
    FFTArrays fftArrays;
    double data[][];
    double mag[];

    double ref=Math.log(1.0);
    double peak=ref*10;

    static FFTAnalyst the;

    /**

     */


    static public FFTAnalyst the() {
        return the;
    }

    public FFTAnalyst(FramedFeed feed) {

        assert(the== null);
        the=this;

        rate=feed.getSampleRate();


        feed.addObserver(this);


        frameSize = feed.getWindowSize();
        fftArrays = new FFTArrays(frameSize);
        data = new double[frameSize][2];
        mag = new double[frameSize/2];
    }

    public void update(Observable o,Object arg) {
      //  System.out.println(" Listener.update() ");
        short v[] = (short []) arg;
        int n=v.length;
        assert(n == frameSize);


        for (int i=0;i<n;i++) {
            double w=Math.sin(i*Math.PI/(n-1));

            data[i][0]=(double)v[i]*w;
            data[i][1]=0.0;
        }
        FFT.fft(data,fftArrays);

        for(int i=0;i<mag.length;i++) {
            mag[i]=Math.log(Math.sqrt(data[i][0]*data[i][0]+ data[i][1]*data[i][1])+1.0);
            if (mag[i] > peak) peak = mag[i];
      //      if (mag[i] < mpeak) mpeak = mag[i];
        }

        assert(peak != 0.0);

        for(int i=0;i< mag.length ; i++ ) {
            if (mag[i] > ref)
                mag[i] = (mag[i] - ref) / (peak - ref);
            else
                mag[i] = 0;
        }
      //  for(double d : mag) System.out.print(d + " " );


        setChanged();
        notifyObservers(mag);

    }

    public int size() { return mag.length; }


}
