package GM.javasound;

import java.lang.*;
import javax.sound.sampled.*;
import GM.audio.FramedFeed;

/**

  Implements a FramedFeed using a TargetData line

 */

public class TargetDataLineFeed extends FramedFeed {

    private TargetDataLine line;

    public TargetDataLineFeed(double rate) throws Exception
    {
	super(rate,512);

        new JavaSoundMixer();
	int bitsPerSample=16;
	AudioFormat format = new AudioFormat((int)rate,bitsPerSample,1,true,false);
	DataLine.Info info = new DataLine.Info(TargetDataLine.class,
					       format);

	if (!AudioSystem.isLineSupported(info)) {
	    throw new Exception("Line matching " + info + " not supported.");
	}

	// get and open the target data line for capture.

	line = (TargetDataLine) AudioSystem.getLine(info);
	line.open(format, line.getBufferSize());

	AudioFormat formatA = line.getFormat();
	System.out.println("Line opened --> " + formatA.toString());

	//	chunkSizeInBytes = chunkSize * bitsPerSample/8;

    }


    public short maxValue() { return  Short.MAX_VALUE; }


    protected synchronized int read(short d[],int off,int size) {

	if (size != chunkSizeInBytes/2 ) {
	    System.out.println(" Size should equal chunk size ");
	}

	int numBytesRead = line.read(byteData, 0 , size*2);


	int ii=off;
	for (int i=0 ; i < size ; i++,ii++ ) {
	    short v = (short) ((byteData[i*2] & 0x00FF) |
			       (byteData[i*2 + 1] <<8));
	    d[ii]=v;
	}
	return numBytesRead/2;
    }

    public void start() {
	line.start();
	isRunning=true;
    }

    public void stop() {
	// we reached the end of the stream.  stop and close the line.
	isRunning=false;
 	line.stop();
  	line.close();
   }

   public static void main(String args[]) throws Exception  {
       TargetDataLineFeed feed=new TargetDataLineFeed(44100.0);
       new Thread(feed).start();

   }

}
