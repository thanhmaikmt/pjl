// Diffraction.java (c) 2001 by Paul Falstad, www.falstad.com.
// Algorithm used for circular apertures is from "Simulation and Study
// of Fresnel Diffraction for Arbitrary Two-Dimensional Apertures", by
// Dean Dauger, published in Computers In Physics, Nov/Dec 1996,
// except I use ray tracing to find edges instead of the (more general)
// method he describes.

import java.io.InputStream;
import java.awt.*;
import java.awt.image.ImageProducer;
import java.applet.Applet;
import java.util.Vector;
import java.util.Hashtable;
import java.util.Enumeration;
import java.io.File;
import java.util.Random;
import java.util.Arrays;
import java.awt.image.MemoryImageSource;
import java.lang.Math;
import java.text.NumberFormat;
import java.awt.event.*;

class DiffractionCanvas extends Canvas {
    DiffractionFrame pg;
    DiffractionCanvas(DiffractionFrame p) {
	pg = p;
    }
    public Dimension getPreferredSize() {
	return new Dimension(300,400);
    }
    public void update(Graphics g) {
	pg.updateDiffraction(g);
    }
    public void paint(Graphics g) {
	pg.updateDiffraction(g);
    }
};

class DiffractionLayout implements LayoutManager {
    public DiffractionLayout() {}
    public void addLayoutComponent(String name, Component c) {}
    public void removeLayoutComponent(Component c) {}
    public Dimension preferredLayoutSize(Container target) {
	return new Dimension(550, 400);
    }
    public Dimension minimumLayoutSize(Container target) {
	return new Dimension(100,100);
    }
    public void layoutContainer(Container target) {
	int barwidth = 0;
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

public class Diffraction extends Applet {
    DiffractionFrame mf;
    void destroyFrame() {
	if (mf != null)
	    mf.dispose();
	mf = null;
    }
    public void init() {
	mf = new DiffractionFrame(this);
	mf.init();
    }
    public void destroy() {
	if (mf != null)
	    mf.dispose();
	mf = null;
    }
};

class DiffractionFrame extends Frame
  implements ComponentListener, ActionListener, AdjustmentListener,
             MouseMotionListener, MouseListener, ItemListener {
    
    Thread engine = null;

    Dimension winSize, fullWinSize;
    Image dbimage;
    
    Random random;
    int gridSizeX = 200;
    int gridSizeY = 200;
    
    public String getAppletInfo() {
	return "Diffraction by Paul Falstad";
    }

    Button defaultsButton;
    Checkbox colorCheck;
    Checkbox reversedCheck;
    Checkbox memoryImageSourceCheck;
    Checkbox sizeCheck;
    Choice apertureChooser;
    Scrollbar gridBar;
    Scrollbar lengthBar;
    Scrollbar zoomBar;
    Scrollbar brightnessBar;
    double colorMult;
    double zbase;
    static final double pi = 3.14159265358979323846;
    static final double pi2 = pi*2;
    double func[][][];
    boolean functionChanged;
    boolean dragging = false;
    MemoryImageSource imageSource;
    int pixels[];
    
    int getrand(int x) {
	int q = random.nextInt();
	if (q < 0) q = -q;
	return q % x;
    }
    DiffractionCanvas cv;
    Vector apertureList;
    Aperture aperture;
    Diffraction applet;

    DiffractionFrame(Diffraction a) {
	super("Diffraction Applet");
	applet = a;
    }

    public void init() {
	apertureList = new Vector();
	Aperture a = new CircularAperture();
	while (a != null) {
	    apertureList.addElement(a);
	    a = a.createNext();
	}
	setLayout(new DiffractionLayout());
	cv = new DiffractionCanvas(this);
	cv.addComponentListener(this);
	cv.addMouseMotionListener(this);
	cv.addMouseListener(this);
	add(cv);

	add(defaultsButton = new Button("Set to Defaults"));
	defaultsButton.addActionListener(this);
	
	colorCheck = new Checkbox("Tri-chromatic");
	colorCheck.addItemListener(this);
	add(colorCheck);
	
	reversedCheck = new Checkbox("Reversed");
	reversedCheck.addItemListener(this);
	add(reversedCheck);
	
	sizeCheck = new Checkbox("Show Dimensions");
	sizeCheck.addItemListener(this);
	add(sizeCheck);
	
	String os = System.getProperty("os.name");
	String jv = System.getProperty("java.version");
	boolean altRender = false;
	// change settings to speed things up where possible
	if (os.indexOf("Windows") == 0) {
	    if (jv.indexOf("1.1") == 0)
		altRender = true;
	}

	memoryImageSourceCheck = new Checkbox("Alternate Rendering", altRender);
	memoryImageSourceCheck.addItemListener(this);
	add(memoryImageSourceCheck);
	
	apertureChooser = new Choice();
	int i;
	for (i = 0; i != apertureList.size(); i++)
	    apertureChooser.add("Aperture: " +
		((Aperture) apertureList.elementAt(i)).getName());
	add(apertureChooser);
	aperture = (Aperture) apertureList.elementAt(0);
	apertureChooser.addItemListener(this);

	add(new Label("Aperture Scale", Label.CENTER));
	add(lengthBar = new Scrollbar(Scrollbar.HORIZONTAL, 260, 1, 35, 500));
	lengthBar.addAdjustmentListener(this);

	add(new Label("Zoom", Label.CENTER));
	add(zoomBar = new Scrollbar(Scrollbar.HORIZONTAL, 200, 1, 30, 400));
	zoomBar.addAdjustmentListener(this);

	add(new Label("Brightness", Label.CENTER));
	add(brightnessBar = new Scrollbar(Scrollbar.HORIZONTAL, 50, 1, 1,
					  500));
	brightnessBar.addAdjustmentListener(this);

	add(new Label("Image Resolution", Label.CENTER));
	add(gridBar = new Scrollbar(Scrollbar.HORIZONTAL, 90, 2, 10, 300));
	gridBar.addAdjustmentListener(this);

	add(new Label("http://www.falstad.com", Label.CENTER));

	random = new Random();
	functionChanged = true;
	reinit();
	cv.setBackground(Color.black);
	cv.setForeground(Color.white);
	zbase = 1/java.lang.Math.exp(200/50);

	resize(550, 450);
	handleResize();
	show();
    }

    void reinit() {
	handleResize();
    }

    void handleResize() {
        winSize = cv.getSize();
	if (winSize.width == 0)
	    return;
	Dimension d = fullWinSize = cv.getSize();
        int w = (winSize.width > winSize.height) ? winSize.height : winSize.width;
        winSize.width = winSize.height = w;
	dbimage = createImage(d.width, d.height);
	d = winSize;
	pixels = new int[d.width*d.height];
	imageSource = new MemoryImageSource(d.width, d.height, pixels, 0,
					    d.width);
    }
    
    int angleSteps;
    int angleStepsMask;
    double angleStep;
    double angcos1[], angsin1[];
    int angdirx1[], angdiry1[];
    long angcos2[], angsin2[];
    int angleSteps2;
    int angleSteps2Mask;
    static final int fixedPoint = 256;
    int accumR[], accumI[];
    double apertureArgMult;
    double apertureArgMultRed;
    double apertureArgMultBlue;
    double colorLenMults[];
    boolean reversed;
    boolean color;
    int selection = -1;
    double zoomFactor;
    int oldZoom = 200;

    void computeFunction() {
	accumR = new int[3];
	accumI = new int[3];
	aperture = (Aperture)
	    apertureList.elementAt(apertureChooser.getSelectedIndex());
	gridSizeX = gridSizeY = (gridBar.getValue() & ~1);
	if (aperture.oneDimensional()) {
	    gridSizeX *= 2;
	    gridSizeY = 1;
	}
	func = new double[gridSizeX][gridSizeY][3];
	int i, j;
	color = colorCheck.getState();
	angleSteps = (gridBar.getValue() >= 195) ? 1024 : 256;
	if (aperture.oneDimensional())
	    angleSteps = (gridBar.getValue() >= 195) ? 2048 : 1024;
	angleStepsMask = angleSteps-1;
	angleStep = pi2/angleSteps;
	zoomFactor = java.lang.Math.exp(zoomBar.getValue()/50.)*zbase;
	double baselen = java.lang.Math.exp(lengthBar.getValue()/110.)
	    /zoomFactor;
	angcos1 = new double[angleSteps];
	angsin1 = new double[angleSteps];
	angdirx1 = new int[angleSteps];
	angdiry1 = new int[angleSteps];
	// precompute sines and cosines, one for each angle step
	for (i = 0; i != angleSteps; i++) {
	    angcos1[i] = java.lang.Math.cos(i*pi2/angleSteps);
	    angsin1[i] = java.lang.Math.sin(i*pi2/angleSteps);
	    angdirx1[i] = (angcos1[i] < 0) ? -1 : 1;
	    angdiry1[i] = (angsin1[i] < 0) ? -1 : 1;
	}
	angleSteps2 = 4096;
	angleSteps2Mask = angleSteps2-1;
	angcos2 = new long[angleSteps2];
	angsin2 = new long[angleSteps2];
	reversed = reversedCheck.getState();
	float sign = (reversed) ? -1 : 1;
	colorLenMults = new double[3];

	// precompute another set of sines and cosines.  this one
	// is used to generate the complex number we add into the
	// accumulator in apertureStart/apertureStop.  The array is
	// reversed if the reversed check is set.  That causes all
	// the apertureStart() calls to act like apertureStop() and
	// vice versa.  We used fixed-point integer arithmetic for
	// all this.
	for (i = 0; i != angleSteps2; i++) {
	    angcos2[i] = (long)
		(java.lang.Math.cos(i*pi2/angleSteps2) * fixedPoint*sign);
	    angsin2[i] = (long)
		(java.lang.Math.sin(i*pi2/angleSteps2) * fixedPoint*sign);
	}

	// generate different multipliers for red and blue light.
	// red = 650 nm, green = 510 nm, blue = 475 nm
	colorLenMults[0] = baselen / (650./510.);
	colorLenMults[1] = baselen;
	colorLenMults[2] = baselen / (475./510.);
	
	apertureArgMult = angleSteps2*.25;
	apertureArgMult *= baselen*baselen;

	apertureArgMultRed  = apertureArgMult / (650*650./(510*510));
	apertureArgMultBlue = apertureArgMult / (475*475./(510*510));

	aperture.compute();

	// take advantage of symmetry
	int maxx = aperture.hasXSymmetry() ? gridSizeX/2 : gridSizeX;
	int maxy = aperture.hasYSymmetry() ? gridSizeY/2 : gridSizeY;
	int mink = (color) ? 0 : 1;
	int maxk = (color) ? 2 : 1;
	int k;
	if (aperture.hasDiagonalSymmetry())
	    for (k = mink; k <= maxk; k++)
		for (i = 0; i != maxx; i++)
		    for (j = 0; j <= i; j++)
			func[j][i][k] = func[i][j][k];
	if (aperture.hasXSymmetry()) 
	    for (k = mink; k <= maxk; k++)
		for (i = 0; i != maxx; i++)
		    for (j = 0; j != maxy; j++)
			func[gridSizeX-1-i][j][k] = func[i][j][k];
	if (aperture.hasYSymmetry())
	    for (k = mink; k <= maxk; k++)
		for (i = 0; i != gridSizeX; i++)
		    for (j = 0; j != maxy; j++)
			func[i][gridSizeX-1-j][k] = func[i][j][k];
	functionChanged = false;
    }

    void setFunction(int i, int j) {
	// by default we use only green light.
	int mink = 1, maxk = 1;
	if (color) {
	    mink = 0;
	    maxk = 2;
	}
	int k;
	for (k = mink; k <= maxk; k++) {
	    double ard = ((double) accumR[k])/(angleSteps*fixedPoint);
	    double aid = ((double) accumI[k])/(angleSteps*fixedPoint);
	    double mag = ard*ard + aid*aid;
	    func[i][j][k] = mag;
	}
    }

    void clearAccum() {
	int i;
	for (i = 0; i != 3; i++)
	    accumR[i] = accumI[i] = 0;
    }

    void apertureStart(double r) {
	// report the fact that we found the start of an opening
	// at radius r.
	double r2 = r*r;
	int arg = ((int) (r2*apertureArgMult)) & angleSteps2Mask;
	accumR[1] -= angcos2[arg];
	accumI[1] -= angsin2[arg];
	if (color) {
	    // we did green, now do red and blue
	    arg = ((int) (r2*apertureArgMultRed)) & angleSteps2Mask;
	    accumR[0] -= angcos2[arg];
	    accumI[0] -= angsin2[arg];
	    arg = ((int) (r2*apertureArgMultBlue)) & angleSteps2Mask;
	    accumR[2] -= angcos2[arg];
	    accumI[2] -= angsin2[arg];
	}
    }

    void apertureStop(double r) {
	// report the fact that we found the end of an opening
	// at radius r.
	double r2 = r*r;
	int arg = ((int) (r2*apertureArgMult)) & angleSteps2Mask;
	accumR[1] += angcos2[arg];
	accumI[1] += angsin2[arg];
	if (color) {
	    arg = ((int) (r2*apertureArgMultRed)) & angleSteps2Mask;
	    accumR[0] += angcos2[arg];
	    accumI[0] += angsin2[arg];
	    arg = ((int) (r2*apertureArgMultBlue)) & angleSteps2Mask;
	    accumR[2] += angcos2[arg];
	    accumI[2] += angsin2[arg];
	}
    }

    void apertureStartOrigin(boolean x) {
	// if x is true, that means the origin is at a transparent
	// spot.  Otherwise it's at an opaque spot.
	if (reversed)
	    x = !x;
	if (x) {
	    accumR[1] -= fixedPoint*angleSteps;
	    if (color) {
		accumR[0] -= fixedPoint*angleSteps;
		accumR[2] -= fixedPoint*angleSteps;
	    }
	}
    }

    int sign(double x) {
	return x < 0 ? -1 : 1;
    }

    public void paint(Graphics g) {
	cv.repaint();
    }

    public void updateDiffraction(Graphics realg) {
	boolean hideFunction = dragging && aperture.hideWhileDragging();
	if (functionChanged) {
	    realg.setColor(cv.getBackground());
	    FontMetrics fm = realg.getFontMetrics();
	    String cs = "Calculating...";
	    realg.fillRect(0, fullWinSize.height-30,
			   20+fm.stringWidth(cs), 30);
	    realg.setColor(Color.white);
	    realg.drawString(cs, 10, fullWinSize.height-10);
	    computeFunction();
	}

	Graphics g = null;
	if (winSize == null || winSize.width == 0)
	    return;
	boolean mis = memoryImageSourceCheck.getState();
	g = dbimage.getGraphics();
	g.setColor(cv.getBackground());
	g.fillRect(0, 0, fullWinSize.width, fullWinSize.height);
	g.setColor(cv.getForeground());

	int i, j;
	colorMult = 70*java.lang.Math.exp(brightnessBar.getValue()/50.);
	if (!hideFunction) {
	    for (i = 0; i != gridSizeX; i++)
		for (j = 0; j != gridSizeY; j++) {
		    int x = i*winSize.width/gridSizeX;
		    int y = j*winSize.height/gridSizeY;
		    int x2 = (i+1)*winSize.width/gridSizeX;
		    int y2 = (j+1)*winSize.height/gridSizeY;
		    int colval = 0;
		    if (!color) {
			int col = getColorValue(i, j, 1);
			colval = 0xFF000000 | (col*0X010101);
		    } else {
			colval = 0xFF000000 +
			    (getColorValue(i, j, 0) << 16) |
			    (getColorValue(i, j, 1) << 8) |
			    (getColorValue(i, j, 2));
		    }
		    if (mis) {
			int k, l;
			for (k = x; k < x2; k++)
			    for (l = y; l < y2; l++)
				pixels[k+l*winSize.width] = colval;
		    } else {
			g.setColor(new Color(colval));
			g.fillRect(x, y, x2-x, y2-y);
		    }
		}
	}
	if (mis && !hideFunction) {
	    Image dbimage2 = cv.createImage(imageSource);
	    g.drawImage(dbimage2, 0, 0, null);
	}
	g.setColor(Color.red);
	aperture.drawGeometricShadow(g);
	if (sizeCheck.getState()) {
	    g.setColor(cv.getBackground());
	    FontMetrics fm = realg.getFontMetrics();
	    double wl = 510e-9;
	    NumberFormat nf = NumberFormat.getInstance();
	    nf.setMaximumFractionDigits(2);
	    double baselen = java.lang.Math.exp(lengthBar.getValue()/110.)/
		zoomFactor;
	    double dim = aperture.getDimension()*baselen*
		java.lang.Math.sqrt(wl*2);
	    String cs = "width = ";
	    if (dim > .001)
		cs += nf.format(dim*1000) + " mm";
	    else if (dim > 1e-6)
		cs += nf.format(dim*1e6) + " \u00b5m";
	    else
		cs += nf.format(dim*1e9) + " nm";
	    int sw = fm.stringWidth(cs);
	    if (dim > 0) {
		g.fillRect(fullWinSize.width-(20+sw), fullWinSize.height-30,
			   20+sw, 30);
		g.setColor(Color.white);
		g.drawString(cs, fullWinSize.width-(10+sw),
			     fullWinSize.height-10);
	    }
	}
	realg.drawImage(dbimage, 0, 0, this);
    }

    int getColorValue(int i, int j, int k) {
	int val = (int) (func[i][j][k] * colorMult);
	if (val > 255)
	    val = 255;
	return val;
    }

    void doZoom() {
	double z = java.lang.Math.exp(zoomBar.getValue()/50.)*zbase;
	double oz = java.lang.Math.exp(oldZoom/50.)*zbase;
	double zoomChange = z/oz;
	oldZoom = zoomBar.getValue();
	aperture.rezoom(zoomChange);
    }

    public void componentHidden(ComponentEvent e){}
    public void componentMoved(ComponentEvent e){}
    public void componentShown(ComponentEvent e) {
	cv.repaint();
    }

    public void componentResized(ComponentEvent e) {
	handleResize();
	cv.repaint(100);
    }
    public void actionPerformed(ActionEvent e) {
	if (e.getSource() == defaultsButton) {
	    colorCheck.setState(false);
	    reversedCheck.setState(false);
	    lengthBar.setValue(260);
	    gridBar.setValue(90);
	    zoomBar.setValue(oldZoom = 200);
	    functionChanged = true;
	    brightnessBar.setValue(aperture.defaultBrightness());
	    aperture.setToDefaults();
	    cv.repaint();
	}
    }

    public void adjustmentValueChanged(AdjustmentEvent e) {
	System.out.print(((Scrollbar) e.getSource()).getValue() + "\n");
	if (e.getSource() != brightnessBar)
	    functionChanged = true;
	if (e.getSource() == zoomBar)
	    doZoom();
	cv.repaint(100);
    }

    public void mouseDragged(MouseEvent e) {
	if (selection != -1) {
	    dragging = true;
	    if (aperture.drag(e.getX(), e.getY()))
		cv.repaint();
	}
    }
    public void mouseMoved(MouseEvent e) {
	if ((e.getModifiers() & MouseEvent.BUTTON1_MASK) != 0) {
	    if (selection != -1) {
		dragging = true;
		if (aperture.drag(e.getX(), e.getY()))
		    cv.repaint();
	    }
	    return;
	}
	int sel = selection;
	selection = aperture.getSelection(e.getX(), e.getY());
	if (selection != sel)
	    cv.repaint();
    }
    public void mouseClicked(MouseEvent e) {
    }
    public void mouseEntered(MouseEvent e) {
    }
    public void mouseExited(MouseEvent e) {
	if (!dragging && selection != -1) {
	    selection = -1;
	    cv.repaint();
	}
    }
    public void mousePressed(MouseEvent e) {
	if ((e.getModifiers() & MouseEvent.BUTTON1_MASK) == 0)
	    return;
	if (selection != -1) {
	    dragging = true;
	    if (aperture.drag(e.getX(), e.getY()))
		cv.repaint();
	}
    }
    public void mouseReleased(MouseEvent e) {
	if (dragging) {
	    functionChanged = true;
	    cv.repaint();
	}
	dragging = false;
    }
    public void itemStateChanged(ItemEvent e) {
	if (e.getSource() != memoryImageSourceCheck &&
	    e.getSource() != sizeCheck)
	    functionChanged = true;
	if (e.getSource() == apertureChooser) {
	    aperture = (Aperture)
		apertureList.elementAt(apertureChooser.getSelectedIndex());
	    brightnessBar.setValue(aperture.defaultBrightness());
	    zoomBar.setValue(oldZoom = 200);
	}
	cv.repaint(100);
    }

    public boolean handleEvent(Event ev) {
        if (ev.id == Event.WINDOW_DESTROY) {
            applet.destroyFrame();
            return true;
        }
        return super.handleEvent(ev);
    }
    
    abstract class Aperture {
	abstract String getName();
	abstract void compute();
	abstract Aperture createNext();
	abstract void drawGeometricShadow(Graphics g);
	abstract int getSelection(int x, int y);
	abstract boolean drag(int x, int y);
	abstract void setToDefaults();
	int defaultBrightness() { return 50; }
	boolean oneDimensional() { return false; }
	boolean hasXSymmetry() { return false; }
	boolean hasYSymmetry() { return false; }
	boolean hasDiagonalSymmetry() { return false; }
	boolean hideWhileDragging() { return true; }
	void rezoom(double x) {}
	abstract double getDimension();
	Aperture() { setToDefaults(); }
    };

    class CircularAperture extends Aperture {
	double radius;
	String getName() { return "circle"; }
	Aperture createNext() { return new HalfPlaneAperture(); }
	boolean hasXSymmetry() { return true; }
	boolean hasYSymmetry() { return true; }
	boolean hasDiagonalSymmetry() { return true; }
	void setToDefaults() { radius = .25; }
	void rezoom(double z) { radius *= z; }
	void compute() {
	    int i, j;
	    for (i = 0; i != gridSizeX/2; i++) {
		for (j = 0; j <= i; j++) {
		    clearAccum();
		    double x0 = (i/(double) gridSizeX)-.5;
		    double y0 = (j/(double) gridSizeY)-.5;
		    int th;
		    double cx = -x0;
		    double cy = -y0;
		    double c2 = cx*cx+cy*cy;
		    double cr = radius;
		    double c = c2 - cr*cr;
		    double ac4 = c*4;
		    double th1 = 0;
		    double th2 = pi2;
		    if (c <= 0) {
			// need to do all of them
		    } else {
			// figure out what angle range we need to do
			double r = java.lang.Math.sqrt(c2);
			double cx1 = cx/r;
			double cy1 = cy/r;
			double a1 = java.lang.Math.atan2(cy-cx1*cr, cx+cy1*cr);
			double a2 = java.lang.Math.atan2(cy+cx1*cr, cx-cy1*cr);
			th1 = (a1 < a2) ? a1 : a2;
			th2 = (a1 > a2) ? a1 : a2;
			if (th2-th1 > pi) {
			    th1 = (a1 > a2) ? a1 : a2;
			    th2 = (a1 < a2) ? a1 : a2;
			    th2 += pi2;
			}
		    }
		    int th1i = (int) ((th1*angleSteps)/pi2);
		    int th2i = (int) ((th2*angleSteps)/pi2);
		    while (th1i < 0) {
			th1i += angleSteps;
			th2i += angleSteps;
		    }
		    for (th = th1i; th < th2i; th++) {
			// find intersection of this ray with circle
			double costh = angcos1[th & angleStepsMask];
			double sinth = angsin1[th & angleStepsMask];
			double b = -2*(costh*cx+sinth*cy);
			double discrim = b*b-ac4;
			if (discrim < 0)
			    continue;
			discrim = java.lang.Math.sqrt(discrim);
			double r1 = .5*(-b-discrim);
			double r2 = .5*(-b+discrim);
			if (r1 < 0 && r2 < 0)
			    continue;
			if (r1 > 0)
			    apertureStart(r1);
			apertureStop(r2);
		    }
		    apertureStartOrigin(c < 0);
		    setFunction(i, j);
		}
	    }
	}

	void drawGeometricShadow(Graphics g) {
	    if (selection == 1)
		g.setColor(Color.yellow);
	    int r = (int) (winSize.width*radius);
	    g.drawOval(winSize.width/2-r, winSize.height/2-r,
		       r*2, r*2);
	}

	int getSelection(int x, int y) {
	    int rx = winSize.width/2-x;
	    int ry = winSize.height/2-y;
	    double r = java.lang.Math.sqrt(rx*rx+ry*ry)/winSize.width;
	    return (java.lang.Math.abs(r-radius) < 5./winSize.width) ? 1 : -1;
	}

	boolean drag(int x, int y) {
	    int rx = winSize.width/2-x;
	    int ry = winSize.height/2-y;
	    double r = java.lang.Math.sqrt(rx*rx+ry*ry)/winSize.width;
	    if (r == radius)
		return false;
	    radius = r;
	    return true;
	}
	
	double getDimension() { return radius*2; }
    }

    // general class to describe an aperture consisting entirely
    // of vertical lines.
    abstract class OneDimensionalAperture extends Aperture {
	public double lineLocations[];
	public int lineCount;
	boolean oneDimensional() { return true; }

	void compute() {
	    int i, j;
	    double result[] = new double[2];
	    // by default we use only green light.
	    int mink = 1, maxk = 1;
	    if (color) {
		mink = 0;
		maxk = 2;
	    }
	    int k;
	    int xlim = (hasXSymmetry()) ? gridSizeX/2 : gridSizeX;
	    double astart = (reversedCheck.getState()) ? -1 : 0;

	    // add in a right side at infinity if only one line
	    if (lineCount == 1)
		astart += .5;

	    for (i = 0; i != xlim; i++) {
		double x0 = (i/(double) gridSizeX)-.5;
		for (k = mink; k <= maxk; k++) {
		    double mult = colorLenMults[k];
		    double ar = astart, ai = astart;
		    int d = 1;
		    for (j = 0; j != lineCount; j++) {
			fresnl((x0-lineLocations[j])*mult, result);
			ar += d*result[0];
			ai += d*result[1];
			d = -d;
		    }
		    func[i][0][k] = .5*(ar*ar + ai*ai);
		}
	    }
	}

	double getDimension() {
	    return lineLocations[lineCount-1]-lineLocations[0];
	}

	void drawGeometricShadow(Graphics g) {
	    int i;
	    int symsel = -1;
	    if (selection != -1 && hasXSymmetry())
		symsel = lineCount-1-selection;
	    for (i = 0; i != lineCount; i++) {
		int x = (int) ((lineLocations[i]+.5) * winSize.width);
		g.setColor((selection == i || symsel == i) ?
			   Color.yellow : Color.red);
		g.drawLine(x, 0, x, winSize.height-1);
	    }
	}

	int getSelection(int x, int y) {
	    double xf = ((double) x)/winSize.width - .5;
	    double thresh = 3./winSize.width;
	    int sel = -1;
	    int i;
	    for (i = 0; i != lineCount; i++) {
		double dist = java.lang.Math.abs(lineLocations[i]-xf);
		if (dist < thresh) {
		    sel = i;
		    thresh = dist;
		}
	    }
	    return sel;
	}

	boolean drag(int x, int y) {
	    double xf = ((double) x)/winSize.width - .5;
	    if (selection > 0 && xf <= lineLocations[selection-1])
		return false;
	    if (selection < lineCount-1 && xf >= lineLocations[selection+1])
		return false;
	    if (hasXSymmetry() &&
		sign(lineLocations[selection]) != sign(xf))
		return false;
	    lineLocations[selection] = xf;
	    if (hasXSymmetry()) {
		int symsel = lineCount-1-selection;
		lineLocations[symsel] = -xf;
	    }
	    functionChanged = true;
	    return true;
	}

	boolean hideWhileDragging() { return false; }

	void rezoom(double z) {
	    int i;
	    for (i = 0; i != lineCount; i++)
		lineLocations[i] *= z;
	}
    }

    class HalfPlaneAperture extends OneDimensionalAperture {
	void setToDefaults() {
	    lineLocations = new double[lineCount = 1];
	    lineLocations[0] = 0;
	}
	String getName() { return "half plane"; }
	Aperture createNext() { return new SlitAperture(); }
	double getDimension() { return .5-lineLocations[0]; }
    }

    class SlitAperture extends OneDimensionalAperture {
	void setToDefaults() {
	    lineLocations = new double[lineCount = 2];
	    lineLocations[0] = -.06;
	    lineLocations[1] =  .06;
	}
	int defaultBrightness() { return 200; }
	String getName() { return "slit"; }
	Aperture createNext() { return new DoubleSlitAperture(); }
	boolean hasXSymmetry() { return true; }
    }

    class DoubleSlitAperture extends OneDimensionalAperture {
	void setToDefaults() {
	    lineLocations = new double[lineCount = 4];
	    lineLocations[0] = -.17;
	    lineLocations[1] = -1/8.0;
	    lineLocations[2] =  1/8.0;
	    lineLocations[3] =  .17;
	}
	int defaultBrightness() { return 140; }
	String getName() { return "double slit"; }
	Aperture createNext() { return new TripleSlitAperture(); }
	boolean hasXSymmetry() { return true; }
    }

    class TripleSlitAperture extends OneDimensionalAperture {
	void setToDefaults() {
	    lineLocations = new double[lineCount = 6];
	    lineLocations[0] = -.1533;
	    lineLocations[1] = -.1133;
	    lineLocations[2] = -.02;
	    lineLocations[3] =  .02;
	    lineLocations[4] =  .1133;
	    lineLocations[5] =  .1533;
	}
	int defaultBrightness() { return 210; }
	String getName() { return "triple slit"; }
	Aperture createNext() { return new SquareAperture(); }
	boolean hasXSymmetry() { return true; }
    }

    class SquareAperture extends BlockAperture {
	String getName() { return "square"; }
	Aperture createNext() { return new RectangularAperture(); }
	boolean hasXSymmetry() { return true; }
	boolean hasYSymmetry() { return true; }
	boolean hasDiagonalSymmetry() { return true; }
	void setToDefaults() {
	    double sqdim = .25;
	    blockCountX = blockCountY = 5;
	    blocks = new boolean[blockCountX][blockCountY];
	    blocks[2][2] = true;
	    lineXLocations = new double[blockCountX];
	    lineYLocations = new double[blockCountY];
	    lineXLocations[1] = -sqdim;
	    lineXLocations[3] =  sqdim;
	    lineYLocations[1] = -sqdim;
	    lineYLocations[3] =  sqdim;
	}
	void setupRects() {
	    rectCount = 1;
	    rects = new double[1][5];
	    double sqdim = lineXLocations[3];
	    rects[0][0] = -sqdim;
	    rects[0][1] = -sqdim;
	    rects[0][2] = sqdim;
	    rects[0][3] = sqdim;
	    rects[0][4] = .5;
	}
    }

    class RectangularAperture extends BlockAperture {
	String getName() { return "rectangle"; }
	Aperture createNext() { return new CornerAperture(); }
	boolean hasXSymmetry() { return true; }
	boolean hasYSymmetry() { return true; }
	void setToDefaults() {
	    blockCountX = blockCountY = 5;
	    blocks = new boolean[blockCountX][blockCountY];
	    blocks[2][2] = true;
	    lineXLocations = new double[blockCountX];
	    lineYLocations = new double[blockCountY];
	    lineXLocations[1] = -.25;
	    lineXLocations[3] =  .25;
	    lineYLocations[1] = -.4;
	    lineYLocations[3] =  .4;
	}
	void setupRects() {
	    rectCount = 1;
	    rects = new double[1][5];
	    rects[0][0] = lineXLocations[1];
	    rects[0][1] = lineYLocations[1];
	    rects[0][2] = lineXLocations[3];
	    rects[0][3] = lineYLocations[3];
	    rects[0][4] = .5;
	}
    }

    class CornerAperture extends BlockAperture {
	String getName() { return "corner"; }
	Aperture createNext() { return new CrossAperture(); }
	boolean hasDiagonalSymmetry() { return true; }
	void setToDefaults() {
	    blockCountX = blockCountY = 3;
	    blocks = new boolean[blockCountX][blockCountY];
	    blocks[2][2] = true;
	    lineXLocations = new double[blockCountX];
	    lineYLocations = new double[blockCountY];
	    lineXLocations[1] = 0;
	    lineYLocations[1] = 0;
	}
	void setupRects() {
	    rectCount = 1;
	    rects = new double[1][5];
	    double sqdim = lineXLocations[1];
	    rects[0][0] = sqdim;
	    rects[0][1] = sqdim;
	    rects[0][2] = 1e8;
	    rects[0][3] = 1e8;
	    rects[0][4] = .5;
	}
	double getDimension() { return .5-lineXLocations[1]; }
    }

    class CrossAperture extends BlockAperture {
	String getName() { return "cross"; }
	Aperture createNext() { return new RectanglesAperture(); }
	boolean hasXSymmetry() { return true; }
	boolean hasYSymmetry() { return true; }
	boolean hasDiagonalSymmetry() { return true; }
	void setToDefaults() {
	    double sqdim = 1/16.0;
	    blockCountX = blockCountY = 5;
	    blocks = new boolean[blockCountX][blockCountY];
	    blocks[0][2] = blocks[2][2] = blocks[4][2] =
		blocks[2][0] = blocks[2][4] = true;
	    lineXLocations = new double[blockCountX];
	    lineYLocations = new double[blockCountY];
	    lineXLocations[1] = -sqdim;
	    lineXLocations[3] =  sqdim;
	    lineYLocations[1] = -sqdim;
	    lineYLocations[3] =  sqdim;
	}
	void setupRects() {
	    rectCount = 3;
	    rects = new double[3][5];
	    double sqdim = lineXLocations[3];

	    // the cross aperture is made up of two intersecting rectangles
	    // and then a third rectangle (their intersection) which prevents
	    // that area from being counted twice

	    rects[0][0] = -sqdim;
	    rects[0][1] = -1e8;
	    rects[0][2] =  sqdim;
	    rects[0][3] = 1e8;
	    rects[0][4] = .5;

	    rects[1][0] = -1e8;
	    rects[1][1] = -sqdim;
	    rects[1][2] = 1e8;
	    rects[1][3] = sqdim;
	    rects[1][4] = .5;

	    rects[2][0] = -sqdim;
	    rects[2][1] = -sqdim;
	    rects[2][2] = sqdim;
	    rects[2][3] = sqdim;
	    rects[2][4] = -.5;
	}
	double getDimension() { return 1; }
    }

    class RectanglesAperture extends BlockAperture {
	String getName() { return "2 rectangles"; }
	Aperture createNext() { return new FrameAperture(); }
	boolean hasXSymmetry() { return true; }
	boolean hasYSymmetry() { return true; }
	void setToDefaults() {
	    blockCountX = 9;
	    blockCountY = 5;
	    blocks = new boolean[blockCountX][blockCountY];
	    blocks[2][2] = blocks[6][2] = true;
	    lineXLocations = new double[blockCountX];
	    lineYLocations = new double[blockCountY];
	    lineXLocations[1] = -.375;
	    lineXLocations[3] = -.125;
	    lineXLocations[5] =  .125;
	    lineXLocations[7] =  .375;
	    lineYLocations[1] = -.25;
	    lineYLocations[3] =  .25;
	}
	void setupRects() {
	    rectCount = 2;
	    rects = new double[2][5];
	    double sqdim = lineXLocations[1];
	    rects[0][0] = lineXLocations[1];
	    rects[0][1] = lineYLocations[1];
	    rects[0][2] = lineXLocations[3];
	    rects[0][3] = lineYLocations[3];
	    rects[0][4] = .5;
	    rects[1][0] = lineXLocations[5];
	    rects[1][1] = lineYLocations[1];
	    rects[1][2] = lineXLocations[7];
	    rects[1][3] = lineYLocations[3];
	    rects[1][4] = .5;
	}
    }

    class FrameAperture extends BlockAperture {
	String getName() { return "frame"; }
	Aperture createNext() { return new PlusAperture(); }
	boolean hasXSymmetry() { return true; }
	boolean hasYSymmetry() { return true; }
	boolean hasDiagonalSymmetry() { return true; }
	void setToDefaults() {
	    blockCountX = blockCountY = 9;
	    blocks = new boolean[blockCountX][blockCountY];
	    int i;
	    for (i = 2; i <= 6; i += 2)
		blocks[i][2] = blocks[i][6] =
		blocks[2][i] = blocks[6][i] = true;
	    lineXLocations = new double[blockCountX];
	    lineYLocations = new double[blockCountY];
	    lineXLocations[1] = -.375;
	    lineXLocations[3] = -.125;
	    lineXLocations[5] =  .125;
	    lineXLocations[7] =  .375;
	    lineYLocations[1] = -.375;
	    lineYLocations[3] = -.125;
	    lineYLocations[5] =  .125;
	    lineYLocations[7] =  .375;
	}
	void setupRects() {
	    rectCount = 2;
	    rects = new double[2][5];
	    // outer frame
	    rects[0][0] = lineXLocations[1];
	    rects[0][1] = lineYLocations[1];
	    rects[0][2] = lineXLocations[7];
	    rects[0][3] = lineYLocations[7];
	    rects[0][4] = .5;
	    // remove inner frame rectangle
	    rects[1][0] = lineXLocations[3];
	    rects[1][1] = lineYLocations[3];
	    rects[1][2] = lineXLocations[5];
	    rects[1][3] = lineYLocations[5];
	    rects[1][4] = -.5;
	}
    }

    class PlusAperture extends BlockAperture {
	String getName() { return "plus"; }
	Aperture createNext() { return new IntersectingSquaresAperture(); }
	boolean hasXSymmetry() { return true; }
	boolean hasYSymmetry() { return true; }
	boolean hasDiagonalSymmetry() { return true; }
	void setToDefaults() {
	    blockCountX = blockCountY = 9;
	    blocks = new boolean[blockCountX][blockCountY];
	    int i;
	    for (i = 2; i <= 6; i += 2)
		blocks[i][4] = blocks[4][i] = true;
	    lineXLocations = new double[blockCountX];
	    lineYLocations = new double[blockCountY];
	    lineXLocations[1] = -.375;
	    lineXLocations[3] = -.125;
	    lineXLocations[5] =  .125;
	    lineXLocations[7] =  .375;
	    lineYLocations[1] = -.375;
	    lineYLocations[3] = -.125;
	    lineYLocations[5] =  .125;
	    lineYLocations[7] =  .375;
	}
	void setupRects() {
	    rectCount = 3;
	    rects = new double[3][5];
	    rects[0][0] = lineXLocations[1];
	    rects[0][1] = lineYLocations[3];
	    rects[0][2] = lineXLocations[7];
	    rects[0][3] = lineYLocations[5];
	    rects[0][4] = .5;

	    rects[1][0] = lineXLocations[3];
	    rects[1][1] = lineYLocations[1];
	    rects[1][2] = lineXLocations[5];
	    rects[1][3] = lineYLocations[7];
	    rects[1][4] = .5;

	    rects[2][0] = lineXLocations[3];
	    rects[2][1] = lineYLocations[3];
	    rects[2][2] = lineXLocations[5];
	    rects[2][3] = lineYLocations[5];
	    rects[2][4] = -.5;

	}
    }

    class IntersectingSquaresAperture extends BlockAperture {
	String getName() { return "2 squares"; }
	Aperture createNext() { return new DoubleCircleAperture(); }
	boolean hasDiagonalSymmetry() { return true; }
	void setToDefaults() {
	    blockCountX = blockCountY = 9;
	    blocks = new boolean[blockCountX][blockCountY];
	    int i;
	    for (i = 2; i <= 6; i += 2)
		blocks[i][4] = blocks[4][i] = true;
	    blocks[2][2] = blocks[6][6] = true;
	    lineXLocations = new double[blockCountX];
	    lineYLocations = new double[blockCountY];
	    lineXLocations[1] = -.375;
	    lineXLocations[3] = -.125;
	    lineXLocations[5] =  .125;
	    lineXLocations[7] =  .375;
	    lineYLocations[1] = -.375;
	    lineYLocations[3] = -.125;
	    lineYLocations[5] =  .125;
	    lineYLocations[7] =  .375;
	}
	void setupRects() {
	    rectCount = 3;
	    rects = new double[3][5];
	    rects[0][0] = lineXLocations[1];
	    rects[0][1] = lineYLocations[1];
	    rects[0][2] = lineXLocations[5];
	    rects[0][3] = lineYLocations[5];
	    rects[0][4] = .5;

	    rects[1][0] = lineXLocations[3];
	    rects[1][1] = lineYLocations[3];
	    rects[1][2] = lineXLocations[7];
	    rects[1][3] = lineYLocations[7];
	    rects[1][4] = .5;

	    rects[2][0] = lineXLocations[3];
	    rects[2][1] = lineYLocations[3];
	    rects[2][2] = lineXLocations[5];
	    rects[2][3] = lineYLocations[5];
	    rects[2][4] = -.5;

	}
    }

    // general class used to describe apertures that consist of
    // rectangles, some of which may extend to infinity.  Each
    // rectangle may or may not be opaque.
    abstract class BlockAperture extends Aperture {
	int blockCountX, blockCountY;

	// All these arrays use a very strange system of indices.
	// Even numbers are blocks (areas between lines), and odd
	// numbers are lines.  The blocks at index n are bounded by
	// lines n-1 and n+1.  The blocks at index 0 are bounded by
	// -infinity and line 1.

	// true if a block is transparent.  Because we are talking
	// about blocks, only even indices are used.
	boolean blocks[][];

	// Lines.  Only odd indices used.
	double lineXLocations[];
	double lineYLocations[];

	int rectCount;
	double rects[][];
	abstract void setupRects();

	void compute() {
	    setupRects();
	    int i, j;
	    double result1[] = new double[2];
	    double result2[] = new double[2];
	    double result3[] = new double[2];
	    double result4[] = new double[2];
	    // by default we use only green light.
	    int mink = 1, maxk = 1;
	    if (color) {
		mink = 0;
		maxk = 2;
	    }
	    int k;
	    double astart = (reversedCheck.getState()) ? -1 : 0;
	    int xlim = (hasXSymmetry()) ? gridSizeX/2 : gridSizeX;
	    int ylim = (hasYSymmetry()) ? gridSizeY/2 : gridSizeY;
	    for (i = 0; i != xlim; i++) {
		if (hasDiagonalSymmetry())
		    ylim = i+1;
		double x0 = (i/(double) gridSizeX)-.5;
		for (j = 0; j != ylim; j++) {
		    double y0 = (j/(double) gridSizeY)-.5;
		    for (k = mink; k <= maxk; k++) {
			double mult = colorLenMults[k];
			double ar = 0, ai = astart;
			int l;
			// add up contributions from all rectangles
			for (l = 0; l != rectCount; l++) {
			    fresnl((rects[l][0]-x0)*mult, result1);
			    fresnl((rects[l][2]-x0)*mult, result2);
			    fresnl((rects[l][1]-y0)*mult, result3);
			    fresnl((rects[l][3]-y0)*mult, result4);
			    double ar1 = result1[0]-result2[0];
			    double ai1 = result1[1]-result2[1];
			    double ar2 = result3[0]-result4[0];
			    double ai2 = result3[1]-result4[1];
			    ar += rects[l][4]*(ar1*ar2 - ai1*ai2);
			    ai += rects[l][4]*(ar1*ai2 + ai1*ar2);
			}
			func[i][j][k] = ar*ar + ai*ai;
		    }
		}
	    }
	}

	void drawGeometricShadow(Graphics g) {
	    int i, j;
	    // go through each line and determine if the blocks on either
	    // side of it have different opacity, if so then draw a
	    // line there.
	    for (i = 1; i < blockCountX; i += 2)
		for (j = 0; j < blockCountY; j += 2) {
		    if (blocks[i-1][j] == blocks[i+1][j])
			continue;
		    int x  = (int) ((lineXLocations[i]+.5)*winSize.width);
		    int y1 = 0;
		    int y2 = winSize.height;
		    try {
			y1 = (int) ((lineYLocations[j-1]+.5)*winSize.height);
		    } catch (Exception e) { }
		    try {
			y2 = (int) ((lineYLocations[j+1]+.5)*winSize.height);
		    } catch (Exception e) { }
		    g.setColor(isSelected(i, -1) ? Color.yellow : Color.red);
		    g.drawLine(x, y1, x, y2);
		}
	    for (i = 0; i < blockCountX; i += 2)
		for (j = 1; j < blockCountY; j += 2) {
		    if (blocks[i][j-1] == blocks[i][j+1])
			continue;
		    int y  = (int) ((lineYLocations[j]+.5)*winSize.height);
		    int x1 = 0;
		    int x2 = winSize.width;
		    try {
			x1 = (int) ((lineXLocations[i-1]+.5)*winSize.width);
		    } catch (Exception e) { }
		    try {
			x2 = (int) ((lineXLocations[i+1]+.5)*winSize.width);
		    } catch (Exception e) { }
		    g.setColor(isSelected(-1, j) ? Color.yellow : Color.red);
		    g.drawLine(x1, y, x2, y);
		}
	}

	boolean isSelected(int x, int y) {
	    return isSelected(x, y, 0);
	}

	boolean isSelected(int x, int y, int iter) {
	    // determine if a line is selected, accounting for
	    // symmetry.
	    if (selection == -1)
		return false;
	    if (selection == x+100 || selection == y+200)
		return true;
	    if (hasXSymmetry() && iter < 1 && blockCountX > 3 &&
		isSelected(blockCountX-1-x, y, 1))
		return true;
	    if (hasYSymmetry() && iter < 2 && blockCountY > 3 &&
		isSelected(x, blockCountY-1-y, 2))
		return true;
	    if (hasDiagonalSymmetry() && iter < 3 &&
		isSelected(y, x, 3))
		return true;
	    return false;
	}

	int getSelection(int x, int y) {
	    double xf = ((double) x)/winSize.width - .5;
	    double yf = ((double) y)/winSize.width - .5;
	    double thresh = 3./winSize.width;
	    int sel = -1;
	    int i;
	    for (i = 1; i < blockCountX; i += 2) {
		double dist = java.lang.Math.abs(lineXLocations[i]-xf);
		if (dist < thresh) {
		    sel = 100+i;
		    thresh = dist;
		}
	    }
	    for (i = 1; i < blockCountY; i += 2) {
		double dist = java.lang.Math.abs(lineYLocations[i]-yf);
		if (dist < thresh) {
		    sel = 200+i;
		    thresh = dist;
		}
	    }
	    return sel;
	}

	boolean drag(int x, int y) {
	    double xf = ((double) x)/winSize.width - .5;
	    double yf = ((double) y)/winSize.width - .5;
	    if (selection >= 200)
		return dragLine(-1, selection-200, yf, 0);
	    else
		return dragLine(selection-100, -1, xf, 0);
	}

	void rezoom(double z) {
	    int i;
	    for (i = 1; i < blockCountX; i += 2)
		lineXLocations[i] *= z;
	    for (i = 1; i < blockCountY; i += 2)
		lineYLocations[i] *= z;
	}

	boolean dragLine(int x, int y, double loc, int iter) {
	    // drag a line and all lines it is related to by symmetry.
	    if (x != -1) {
		if (hasXSymmetry() && sign(lineXLocations[x]) != sign(loc))
		    return false;
		if (x > 1 && loc <= lineXLocations[x-2])
		    return false;
		if (x < blockCountX-2 && loc >= lineXLocations[x+2])
		    return false;
	    }
	    if (y != -1) {
		if (hasYSymmetry() && sign(lineYLocations[y]) != sign(loc))
		    return false;
		if (y > 1 && loc <= lineYLocations[y-2])
		    return false;
		if (y < blockCountY-2 && loc >= lineYLocations[y+2])
		    return false;
	    }
	    if (x != -1 && hasXSymmetry() && iter < 1)
		dragLine(blockCountX-1-x, y, -loc, 1);
	    if (y != -1 && hasYSymmetry() && iter < 2)
		dragLine(x, blockCountY-1-y, -loc, 2);
	    if (hasDiagonalSymmetry() && iter < 3)
		dragLine(y, x, loc, 3);
	    if (x != -1)
		lineXLocations[x] = loc;
	    if (y != -1)
		lineYLocations[y] = loc;
	    return true;
	}

	double getDimension() { return lineXLocations[blockCountX-2]-
				    lineXLocations[1]; }
    }

    class DoubleCircleAperture extends Aperture {
	double radius;
	double offset;
	String getName() { return "2 circles"; }
	Aperture createNext() { return null; }
	boolean hasXSymmetry() { return true; }
	boolean hasYSymmetry() { return true; }
	void setToDefaults() { radius = .3; offset = .25; }
	double getDimension() { return (radius+offset)*2; }
	void compute() {
	    int i, j;
	    double points[] = new double[4];
	    double dx = offset;
	    double dy = 0;
	    boolean intersecting = (offset < radius);
	    if (intersecting) {
		dy = java.lang.Math.sqrt(radius*radius-offset*offset);
		double overflow = radius-2*offset;
		if (overflow > 0)
		    dx = offset+overflow;
	    }
	    for (i = 0; i != gridSizeX/2; i++) {
		for (j = 0; j != gridSizeY/2; j++) {
		    clearAccum();
		    double x0 = (i/(double) gridSizeX)-.5;
		    double y0 = (j/(double) gridSizeY)-.5;
		    int th;
		    double cx1 = -x0+offset;
		    double cx2 = -x0-offset;
		    double cy = -y0;
		    double c21 = cx1*cx1+cy*cy;
		    double c22 = cx2*cx2+cy*cy;
		    double cr2 = radius*radius;
		    double cd1 = c21 - cr2;
		    double cd2 = c22 - cr2;
		    double ac41 = cd1*4;
		    double ac42 = cd2*4;
		    double th1 = 0;
		    double th2 = pi2;
		    int th1i = (int) ((th1*angleSteps)/pi2);
		    int th2i = (int) ((th2*angleSteps)/pi2);
		    while (th1i < 0) {
			th1i += angleSteps;
			th2i += angleSteps;
		    }
		    boolean open = cd1 < 0 || cd2 < 0;
		    apertureStartOrigin(open);
		    for (th = th1i; th < th2i; th++) {
			double costh = angcos1[th & angleStepsMask];
			double sinth = angsin1[th & angleStepsMask];
			double b1 = -2*(costh*cx1+sinth*cy);
			double b2 = -2*(costh*cx2+sinth*cy);
			double discrim1 = b1*b1-ac41;
			double discrim2 = b2*b2-ac42;
			if (discrim1 < 0 && discrim2 < 0)
			    continue;
			int ct = 0;
			if (discrim1 >= 0) {
			    discrim1 = java.lang.Math.sqrt(discrim1);
			    points[ct++] = .5*(-b1-discrim1);
			    points[ct++] = .5*(-b1+discrim1);
			}
			if (discrim2 >= 0) {
			    discrim2 = java.lang.Math.sqrt(discrim2);
			    points[ct++] = .5*(-b2-discrim2);
			    points[ct++] = .5*(-b2+discrim2);
			}
			int si, sj;
			// sort the points
			for (si = 1; si < ct; si++) {
			    double v = points[si];
			    sj = si;
			    while (points[sj-1] > v) {
				points[sj] = points[sj-1]; sj--;
				if (sj <= 0) break;
			    }
			    points[sj] = v;
			}
			// go through the sorted points and call start/stop
			// alternately for each one
			boolean inOpen = open;
			for (si = 0; si != ct; si++) {
			    double r = points[si];
			    if (r < 0) continue;
			    double x1 = x0+costh*r;
			    double y1 = y0+sinth*r;
			    if (intersecting &&
				x1 > -dx && x1 < dx &&
				y1 > -dy && y1 < dy) {
				double y12 = y1*y1;
				if ((x1-offset)*(x1-offset)+y12 < cr2 ||
				    (x1+offset)*(x1+offset)+y12 < cr2)
				    continue;
			    }
			    if (!inOpen) {
				apertureStart(points[si]);
				inOpen = true;
			    } else {
				apertureStop(points[si]);
				inOpen = false;
			    }
			}
		    }
		    setFunction(i, j);
		}
	    }
	}

	void drawGeometricShadow(Graphics g) {
	    int r = (int) (winSize.width*radius);
	    int o = (int) (winSize.width*offset);
	    if (selection != -1) {
		g.setColor(selection == 0 ? Color.yellow : Color.red);
		int or = 5;
		g.fillOval(winSize.width/2-o-or, winSize.height/2-or,
			   or*2, or*2);
		g.fillOval(winSize.width/2+o-or, winSize.height/2-or,
			   or*2, or*2);
	    }
	    g.setColor(selection > 0 ? Color.yellow : Color.red);
	    int th = 0;
	    if (offset < radius)
		th = (int) (java.lang.Math.acos(offset/radius)*(180/pi));
	    g.drawArc(winSize.width/2-r-o, winSize.height/2-r,
		      r*2, r*2, th, 360-2*th);
	    g.drawArc(winSize.width/2-r+o, winSize.height/2-r,
		      r*2, r*2, 180+th, 360-2*th);
	}

	int getSelection(int x, int y) {
	    int o = (int) (winSize.width*offset);
	    int rx1 = (winSize.width/2-o)-x;
	    int rx2 = (winSize.width/2+o)-x;
	    int ry = winSize.height/2-y;
	    double r = java.lang.Math.sqrt(rx1*rx1+ry*ry)/winSize.width;
	    if (java.lang.Math.abs(r-radius) < 5./winSize.width)
		return 1;
	    if (r < 5./winSize.width)
		return 0;
	    r = java.lang.Math.sqrt(rx2*rx2+ry*ry)/winSize.width;
	    if (java.lang.Math.abs(r-radius) < 5./winSize.width)
		return 2;
	    if (r < 5./winSize.width)
		return 0;
	    return -1;
	}

	boolean drag(int x, int y) {
	    if (selection == 0) {
		// modify separation of circles
		double xf = ((double) x)/winSize.width - .5;
		double o = java.lang.Math.abs(xf);
		if (o == offset)
		    return false;
		offset = o;
		return true;
	    }
	    // modify radius of circles
	    int o = (int) (winSize.width*offset);
	    int rx1 = (winSize.width/2-o)-x;
	    int rx2 = (winSize.width/2+o)-x;
	    int ry = winSize.height/2-y;
	    double rr;
	    if (selection == 2)
		rr = rx2*rx2;
	    else
		rr = rx1*rx1;
	    double r = java.lang.Math.sqrt(rr+ry*ry)/winSize.width;
	    if (r == radius)
		return false;
	    radius = r;
	    return true;
	}
	void rezoom(double z) {
	    radius *= z;
	    offset *= z;
	}
    }

    // fresnel integral routines from Cephes Math Library

    /* S(x) for small x */
    static final double sn[] = {
	-2.99181919401019853726E3,
	7.08840045257738576863E5,
	-6.29741486205862506537E7,
	2.54890880573376359104E9,
	-4.42979518059697779103E10,
	3.18016297876567817986E11,
    };
    static final double sd[] = {
	2.81376268889994315696E2,
	4.55847810806532581675E4,
	5.17343888770096400730E6,
	4.19320245898111231129E8,
	2.24411795645340920940E10,
	6.07366389490084639049E11,
    };
    
    static final double cn[] = {
	-4.98843114573573548651E-8,
	9.50428062829859605134E-6,
	-6.45191435683965050962E-4,
	1.88843319396703850064E-2,
	-2.05525900955013891793E-1,
	9.99999999999999998822E-1,
    };
    static final double cd[] = {
	3.99982968972495980367E-12,
	9.15439215774657478799E-10,
	1.25001862479598821474E-7,
	1.22262789024179030997E-5,
	8.68029542941784300606E-4,
	4.12142090722199792936E-2,
	1.00000000000000000118E0,
    };

    /* Auxiliary function f(x) */
    static final double fn[] = {
	4.21543555043677546506E-1,
	1.43407919780758885261E-1,
	1.15220955073585758835E-2,
	3.45017939782574027900E-4,
	4.63613749287867322088E-6,
	3.05568983790257605827E-8,
	1.02304514164907233465E-10,
	1.72010743268161828879E-13,
	1.34283276233062758925E-16,
	3.76329711269987889006E-20,
    };
    static final double fd[] = {
	/*  1.00000000000000000000E0, */
	7.51586398353378947175E-1,
	1.16888925859191382142E-1,
	6.44051526508858611005E-3,
	1.55934409164153020873E-4,
	1.84627567348930545870E-6,
	1.12699224763999035261E-8,
	3.60140029589371370404E-11,
	5.88754533621578410010E-14,
	4.52001434074129701496E-17,
	1.25443237090011264384E-20,
    };
    
    /* Auxiliary function g(x) */
    static final double gn[] = {
	5.04442073643383265887E-1,
	1.97102833525523411709E-1,
	1.87648584092575249293E-2,
	6.84079380915393090172E-4,
	1.15138826111884280931E-5,
	9.82852443688422223854E-8,
	4.45344415861750144738E-10,
	1.08268041139020870318E-12,
	1.37555460633261799868E-15,
	8.36354435630677421531E-19,
	1.86958710162783235106E-22,
    };

    static final double gd[] = {
	/*  1.00000000000000000000E0, */
	1.47495759925128324529E0,
	3.37748989120019970451E-1,
	2.53603741420338795122E-2,
	8.14679107184306179049E-4,
	1.27545075667729118702E-5,
	1.04314589657571990585E-7,
	4.60680728146520428211E-10,
	1.10273215066240270757E-12,
	1.38796531259578871258E-15,
	8.39158816283118707363E-19,
	1.86958710162783236342E-22,
    };

    static final double PI = pi;
    static final double PIBYTWO = pi/2;

    int fresnl(double xxa, double result[]) {
	double f, g, cc, ss, c, s, t, u;
	double x, x2;

	while (true) {
	    x = java.lang.Math.abs(xxa);
	    x2 = x * x;
	    if (x2 < 2.5625) {
		t = x2 * x2;
		ss = x * x2 * polevl(t, sn, 5) / p1evl(t, sd, 6);
		cc = x * polevl(t, cn, 5) / polevl(t, cd, 6);
		break;
	    }
	    if (x > 36974.0) {
		cc = 0.5;
		ss = 0.5;
		break;
	    }
	    /* Auxiliary functions for large argument  */
	    x2 = x * x;
	    t = PI * x2;
	    u = 1.0 / (t * t);
	    t = 1.0 / t;
	    f = 1.0 - u * polevl(u, fn, 9) / p1evl(u, fd, 10);
	    g = t * polevl(u, gn, 10) / p1evl(u, gd, 11);
	    t = PIBYTWO * x2;
	    c = java.lang.Math.cos(t);
	    s = java.lang.Math.sin(t);
	    t = PI * x;
	    cc = 0.5 + (f * s - g * c) / t;
	    ss = 0.5 - (f * c + g * s) / t;
	    break;
	}
	
	if (xxa < 0.0) {
	    cc = -cc;
	    ss = -ss;
	}
	result[0] = cc;
	result[1] = ss;
	return (0);
    }

    double polevl(double x, double coef[], int N) {
	double ans;
	int i;
	int p = 0;
	
	ans = coef[p++];
	i = N;
	
	do
	    ans = ans * x + coef[p++];
	while (--i > 0);
	
	return (ans);
    }

    double p1evl(double x, double coef[], int N) {
	double ans;
	int p = 0;
	int i;
	
	ans = x + coef[p++];
	i = N - 1;
	
	do
	    ans = ans * x + coef[p++];
	while (--i > 0);
	
	return (ans);
    }
}
