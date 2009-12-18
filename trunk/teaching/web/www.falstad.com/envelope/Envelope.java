// Envelope.java (C) 2001 by Paul Falstad, www.falstad.com

import java.io.InputStream;
import java.awt.*;
import java.awt.image.ImageProducer;
import java.applet.Applet;
import java.applet.AudioClip;
import java.util.Vector;
import java.util.Hashtable;
import java.util.Enumeration;
import java.io.File;
import java.lang.Math;
import java.awt.event.*;
import javax.sound.sampled.*;

class EnvelopeCanvas extends Canvas {
    EnvelopeFrame pg;
    EnvelopeCanvas(EnvelopeFrame p) {
	pg = p;
    }
    public Dimension getPreferredSize() {
	return new Dimension(300,400);
    }
    public void update(Graphics g) {
	pg.updateEnvelope(g);
    }
    public void paint(Graphics g) {
	pg.updateEnvelope(g);
    }
};

class EnvelopeLayout implements LayoutManager {
    public EnvelopeLayout() {}
    public void addLayoutComponent(String name, Component c) {}
    public void removeLayoutComponent(Component c) {}
    public Dimension preferredLayoutSize(Container target) {
	return new Dimension(500, 500);
    }
    public Dimension minimumLayoutSize(Container target) {
	return new Dimension(100,100);
    }
    public void layoutContainer(Container target) {
	int barwidth = 200;
	int i;
	for (i = 1; i < target.getComponentCount(); i++) {
	    Component m = target.getComponent(i);
	    if (m.isVisible()) {
		Dimension d = m.getPreferredSize();
		if (d.width > barwidth)
		    barwidth = d.width;
	    }
	}
	Insets insets = target.insets();
	int targetw = target.size().width - insets.left - insets.right;
	int cw = targetw-barwidth;
	int targeth = target.size().height - (insets.top+insets.bottom);
	target.getComponent(0).move(insets.left, insets.top);
	target.getComponent(0).resize(cw, targeth);
	cw += insets.left;
	int h = insets.top;
	for (i = 1; i < target.getComponentCount(); i++) {
	    Component m = target.getComponent(i);
	    if (m.isVisible()) {
		Dimension d = m.getPreferredSize();
		if (m instanceof Scrollbar)
		    d.width = barwidth;
		if (m instanceof Label) {
		    h += d.height/5;
		    d.width = barwidth;
		}
		m.move(cw, h);
		m.resize(d.width, d.height);
		h += d.height;
	    }
	}
    }
};

public class Envelope extends Applet {
    EnvelopeFrame mf;
    void destroyFrame() {
	if (mf != null)
	    mf.dispose();
	mf = null;
    }
    public void init() {
	try {
	    mf = new EnvelopeFrame(this);
	    mf.init();
	} catch (Exception e) {
	    e.printStackTrace();
	    mf = null;
	    security = true;
	    repaint();
	}
    }
    boolean security = false;
    public void paint(Graphics g) {
	if (security) {
	    g.setColor(Color.black);
	    g.fillRect(0, 0, 800, 200);
	    g.setColor(Color.white);
	    g.drawString("Doesn't work with java 2", 0, 20);
	}
    }
    public void destroy() {
	if (mf != null)
	    mf.dispose();
	mf = null;
    }
};

class EnvelopeFrame extends Frame
    implements ComponentListener, AdjustmentListener, ItemListener, Runnable {
    
    Dimension winSize;
    
    public String getAppletInfo() {
	return "Envelope by Paul Falstad";
    }

    Checkbox soundCheck;
    Choice setupChooser;
    Scrollbar stepLengthBar;
    Scrollbar stepCountBars[];
    Scrollbar stepSizeBars[];
    Scrollbar pulseWidthBar;
    static final double pi = 3.14159265358979323846;
    int freqMap[];
    Thread engine = null;

    EnvelopeCanvas cv;
    Envelope applet;

    EnvelopeFrame(Envelope a) {
	super("Envelope Applet v1.1");
	applet = a;
    }

    public void init() {
	setLayout(new EnvelopeLayout());
	cv = new EnvelopeCanvas(this);
	cv.addComponentListener(this);
	add(cv);

	soundCheck = new Checkbox("Sound on", false);
	soundCheck.addItemListener(this);
	add(soundCheck);

	setupChooser = new Choice();
	int i;
	for (i = 0; i != 23; i++)
	    setupChooser.add("Preset #" + (i+1));
	setupChooser.addItemListener(this);
	add(setupChooser);

	add(new Label("Step Length", Label.CENTER));
	add(stepLengthBar = new Scrollbar(Scrollbar.HORIZONTAL, 1, 1, 1, 128));
	stepLengthBar.addAdjustmentListener(this);

	stepCountBars = new Scrollbar[3];
	stepSizeBars  = new Scrollbar[3];
	for (i = 0; i != 3; i++) {
	    add(new Label("Step Count " + (i+1), Label.CENTER));
	    add(stepCountBars[i] = new Scrollbar(Scrollbar.HORIZONTAL, 48,
						 1, 0, 256));
	    stepCountBars[i].addAdjustmentListener(this);
	    add(new Label("Step Size " + (i+1), Label.CENTER));
	    add(stepSizeBars[i] = new Scrollbar(Scrollbar.HORIZONTAL, 48,
						1, 0, 256));
	    stepSizeBars[i].addAdjustmentListener(this);
	}

	add(new Label("Pulse Width", Label.CENTER));
	add(pulseWidthBar = new Scrollbar(Scrollbar.HORIZONTAL, 128,
					  1, 1, 255));
	pulseWidthBar.addAdjustmentListener(this);

	freqMap = new int[256];
	for (i = 0; i != 256; i++) {
	    double q = java.lang.Math.exp(.69314718055994530941*(i-89)/48)*263;
	    freqMap[i] = (int) q;
	}
	cv.setBackground(Color.black);
	cv.setForeground(Color.lightGray);
	doSetup();

	resize(350, 450);
	handleResize();
	show();
    }

    void handleResize() {
        Dimension d = winSize = cv.getSize();
	if (winSize.width == 0)
	    return;
    }

    void centerString(Graphics g, String s, int y) {
	FontMetrics fm = g.getFontMetrics();
        g.drawString(s, (winSize.width-fm.stringWidth(s))/2, y);
    }

    public void paint(Graphics g) {
	cv.repaint();
    }

    public void updateEnvelope(Graphics g) {
	int i;
	g.setColor(Color.white);
	g.fillRect(0, 0, winSize.width, winSize.height);
	g.setColor(Color.black);
	int y = 20;
	centerString(g, "Step length: " + (stepLengthBar.getValue()*10) + " ms", y);
	for (i = 0; i != 3; i++) {
	    centerString(g, "Step count " + (i+1) + ": " + stepCountBars[i].getValue(), y += 20);
	    centerString(g, "Step size " + (i+1) + ": " + (stepSizeBars[i].getValue()-128), y += 20);
	}
	centerString(g, "Pulse width: " + pulseWidthBar.getValue(), y += 20);
    }

    public void componentHidden(ComponentEvent e) {
    }
    public void componentMoved(ComponentEvent e){}
    public void componentShown(ComponentEvent e) {
	cv.repaint();
    }

    public void componentResized(ComponentEvent e) {
	handleResize();
	cv.repaint();
    }

    public void adjustmentValueChanged(AdjustmentEvent e) {
	System.out.print(((Scrollbar) e.getSource()).getValue() + "\n");
	cv.repaint();
    }

    public boolean handleEvent(Event ev) {
        if (ev.id == Event.WINDOW_DESTROY) {
	    soundCheck.setState(false);
            applet.destroyFrame();
            return true;
        }
        return super.handleEvent(ev);
    }
    
    public void itemStateChanged(ItemEvent e) {
	if (e.getItemSelectable() == soundCheck) {
	    if (soundCheck.getState())
		doPlay();
	}
	if (e.getItemSelectable() == setupChooser) {
	    doSetup();
	}
    }

    void setBars(int l, int c1, int s1, int c2, int s2, int c3, int s3) {
	stepLengthBar.setValue(l);
	stepCountBars[0].setValue(c1);
	stepCountBars[1].setValue(c2);
	stepCountBars[2].setValue(c3);
	stepSizeBars[0].setValue(s1+128);
	stepSizeBars[1].setValue(s2+128);
	stepSizeBars[2].setValue(s3+128);
    }

    void doSetup() {
	switch (setupChooser.getSelectedIndex()) {
	case 0: setBars(4, 1, 12, 1, -10, 0, 0); break;
	case 1: setBars(1, 1, -2, 8, 32, 0, 0); break;
	case 2: setBars(1, 4, 1, 6, -1, 0, 0); break;
	case 3: setBars(2, 1, -76, 1, -38, 0, 0); break;
	case 4: setBars(2, 16, -72, 0, 0, 0, 0); break;
	case 5: setBars(2, 11, -64, 1, -27, 0, 0); break;
	case 6: setBars(1, 9, -32, 4, 0, 0, 0); break;
	case 7: setBars(1, 16, -32, 1, 1, 0, 0); break;
	case 8: setBars(1, 3, -49, 0, 0, 0, 0); break;
	case 9: setBars(1, 86, -53, 30, 32, 0, 0); break;
	case 10: setBars(1, 253, -19, 22, 8, 22, -8); break;
	case 11: setBars(1, 116, -91, 11, -92, 0, 0); break;
	case 12: setBars(6, 1, -49, 0, 0, 0, 0); break;
	case 13: setBars(8, 1, -14, 0, 0, 0, 0); break;
	case 14: setBars(2, 16, -14, 18, 12, 0, 0); break;
	case 15: setBars(8, 16, 48, 1, 13, 0, 0); break;
	case 16: setBars(2, 1, 48, 0, 0, 0, 0); break;
	case 17: setBars(3, 2, 48, 3, -48, 0, 0); break;
	case 18: setBars(3, 2, 48, 2, -48, 0, 0); break;
	case 19: setBars(3, 2, 48, 4, -18, 0, 0); break;
	case 20: setBars(4, 1, 48, 1, -96, 0, 0); break;
	case 21: setBars(4, 3, 48, 1, -97, 0, 0); break;
	case 22: setBars(2, 3, 48, 1, 111, 0, 0); break;
	default:
	    setBars(20, 1, 1, 1, 1, 1, 1);
	    break;
	}
	freq = 89;
	cv.repaint();
    }

    int freq, phase, steps;
    int skew;
    SourceDataLine line = null;
    final int bufferSize = 512;
    final int rate = 8000;
    
    void doPlay() {
	skew = 0;
	AudioFormat format = new AudioFormat(rate, 8, 1, true, false);
	DataLine.Info info = new DataLine.Info(SourceDataLine.class, format);
	if (line == null) {
	    try {
		line = (SourceDataLine) AudioSystem.getLine(info);
		line.open(format, bufferSize);
	    } catch (Exception e) {
		e.printStackTrace();
	    }
	    line.start();
	}
	freq = 89;
	phase = steps = 0;
	start();
    }

    public void start() {
	if (engine == null) {
	    engine = new Thread(this);
	    engine.start();
	}
    }

    public void stop() {
	if (engine != null && engine.isAlive()) {
	    engine.stop();
	}
	engine = null;
    }

    public void run() {
	try {
	    int offset = 0;
	    byte b[] = new byte[1];
	    while (true) {
		if (!soundCheck.getState())
		    break;
		int sampcount = 8000/100*stepLengthBar.getValue();
		if (b.length != sampcount)
		    b = new byte[sampcount];
		double n = 256.*freqMap[freq]/8000.;
		int pw = pulseWidthBar.getValue();
		int i;
		for (i = 0; i != sampcount; i++) {
		    int iskewn = (int) ((i+skew)*n);
		    int ph = iskewn & 255;
		    b[i] = (ph < pw) ? (byte)127 : (byte)-127;
		}
		skew += sampcount;
		freq = (freq+stepSizeBars[phase].getValue()-128) & 255;
		if (--steps <= 0) {
		    for (i = 3; i > 0; i--) {
			phase = (phase + 1) % 3;
			steps = stepCountBars[phase].getValue();
			if (steps > 0)
			    break;
		    }
		}
		line.write(b, 0, sampcount);
	    }
	} catch (Exception e) {
	    e.printStackTrace();
	}
	engine = null;
    }
};
