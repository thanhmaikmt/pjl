package GM.gui;

import GM.javasound.*;
import java.awt.*;
import GM.music.*;
import javax.swing.*;
import GM.audio.FramedFeed;



public class PeakPanel extends JPanel implements Runnable
{
    Thread thread;
    int pw;
    int ph;
    int sleepAmount=200;
    int xC=0;
    int nC=0;
    int nLag=10;
    short maxEver;
    short maxV;
    FramedFeed audioStr;

    public PeakPanel() { pw =8; ph = 40;}

    public void setFeed(FramedFeed f) {
        assert(f != null);
        audioStr=f; }

    PeakPanel(int w1,int h1,FramedFeed a) {
	pw=w1;
	ph=h1;
	audioStr=a;
    }

    public Dimension getMinimumSize() {
	return getPreferredSize();
    }

    public Dimension getMaximumSize() {
	return getPreferredSize();
    }

    public Dimension getPreferredSize() {
	return new Dimension(pw,ph);
    }


    public void start() {
	thread = new Thread(this);
        thread.setPriority(Thread.MIN_PRIORITY);
	thread.setName("PeakFollower");
	thread.start();
    }


    public synchronized void stop() {
	thread = null;
	//	notify();
    }


    public void paint(Graphics g) {
	int h=getHeight();
	int w=getWidth();
	int hMid=h/2;

	g.setColor(Color.black);
	g.fillRect(0,0,w,h);

//	h=h-4;

//      System.out.println(" HELLO FROM PAINT "+maxV +  " " + maxEver);
//  	int h1x = (int)(0.5*h*maxV)/Short.MAX_VALUE;
//  	int h2x = (int)(0.5*h*maxEver)/Short.MAX_VALUE;

  	int h1x = (int)(h*maxV)/Short.MAX_VALUE;
  	int h2x = (int)(h*maxEver)/Short.MAX_VALUE;



	g.setColor(Color.green);
	g.fillRect(0,h-h1x,w,h1x);

	g.setColor(Color.white);
	g.drawLine(0,h-h2x,w,h-h2x);

//  	g.setColor(Color.green);
//  	g.fillRect(0,hMid-h1n,w,hMid);
//  	g.setColor(Color.red);
//  	g.drawLine(0,hMid-h2x,w,hMid-h2x);

    }

    public synchronized void run() {

	Thread me = Thread.currentThread();


       // System.out.println(isShowing());
	while (thread == me)  {

	//    minV = audioStr.getMinV(true);
	    maxV = audioStr.peakValue(true);
        //    System.out.println(Conductor.getTime());
	    if (xC > nLag) {
		xC=0;
		maxEver=maxV;
	    } else {
		if ( maxEver < maxV) maxEver=maxV;
		xC++;
	    }


	    //	    System.out.println(" minV="+minV+" maxV="+maxV+" minEver="+minEver+" maxEver="+maxEver);
	    if (isShowing()) repaint();
	    try {
		wait(sleepAmount);
	    } catch (InterruptedException e) {
		break;
	    }
	}
	thread = null;
    }
}
