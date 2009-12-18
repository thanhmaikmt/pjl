// Matrix.java (C) 2001 by Paul Falstad, www.falstad.com

import java.io.InputStream;
import java.awt.*;
import java.awt.image.ImageProducer;
import java.applet.Applet;
import java.applet.AudioClip;
import java.util.Vector;
import java.util.Hashtable;
import java.util.Enumeration;
import java.io.File;
import java.net.URL;
import java.util.Random;
import java.awt.image.MemoryImageSource;
import java.lang.Math;
import java.text.NumberFormat;
import java.awt.event.*;

class MatrixCanvas extends Canvas {
    Matrix pg;
    MatrixCanvas(Matrix p) {
	pg = p;
    }
    public Dimension getPreferredSize() {
	return new Dimension(300,400);
    }
    public void update(Graphics g) {
	pg.updateMatrix(g);
    }
    public void paint(Graphics g) {
	pg.updateMatrix(g);
    }
};

class MatrixLayout implements LayoutManager {
    public MatrixLayout() {}
    public void addLayoutComponent(String name, Component c) {}
    public void removeLayoutComponent(Component c) {}
    public Dimension preferredLayoutSize(Container target) {
	return new Dimension(500, 500);
    }
    public Dimension minimumLayoutSize(Container target) {
	return new Dimension(100,100);
    }
    public void layoutContainer(Container target) {
	int cw = target.size().width;
	int cx = target.size().height;
	int ew = cw-cx;
	int ct = target.getComponentCount();
	target.getComponent(ct-1).move(0, 0);
	target.getComponent(ct-1).resize(cw, target.size().height);
	int i;
	int h = 0;
	for (i = 0; i < ct-1; i++) {
	    Component m = target.getComponent(i);
	    if (m.isVisible()) {
		Dimension d = m.getPreferredSize();
		m.move(cx+(ew-d.width)/2, h);
		m.resize(d.width, d.height);
		h += d.height;
	    }
	}
    }
};


public class Matrix extends Applet
  implements ComponentListener, ActionListener, AdjustmentListener,
             MouseMotionListener, MouseListener {
    
    Thread engine = null;

    Dimension winSize;
    Image dbimage;
    
    Random random;
    
    public String getAppletInfo() {
	return "Matrix by Paul Falstad";
    }

    Button identityButton;
    Button transposeButton;
    Button invertButton;
    Button rotateCWButton;
    Button rotateCCWButton;
    Button reflectXButton;
    Button reflectYButton;
    double vecs[][];
    double origmatrix[][];
    double eigens[][];
    double pointX, pointY;
    boolean showPoint = false;
    boolean dragging = false;
    int selection = -1;
    Color darkCyan, darkRed, purple;

    int getrand(int x) {
	int q = random.nextInt();
	if (q < 0) q = -q;
	return q % x;
    }
    MatrixCanvas cv;

    public void init() {
	darkCyan = new Color(0, 128, 128);
	darkRed =  new Color(128, 0, 0);
	purple = new Color(192, 60, 206);
	setLayout(new MatrixLayout());
	cv = new MatrixCanvas(this);
	cv.addComponentListener(this);
	cv.addMouseMotionListener(this);
	cv.addMouseListener(this);
	add(identityButton = new Button("Identity"));
	identityButton.addActionListener(this);
	add(transposeButton = new Button("Transpose"));
	transposeButton.addActionListener(this);
	add(invertButton = new Button("Invert"));
	invertButton.addActionListener(this);
	add(rotateCWButton = new Button("Rotate CW"));
	rotateCWButton.addActionListener(this);
	add(rotateCCWButton = new Button("Rotate CCW"));
	rotateCCWButton.addActionListener(this);
	add(reflectXButton = new Button("Reflect X"));
	reflectXButton.addActionListener(this);
	add(reflectYButton = new Button("Reflect Y"));
	reflectYButton.addActionListener(this);
	add(cv);
	setBackground(Color.black);
	setForeground(Color.lightGray);
	random = new Random();
	vecs = new double[2][2];
	vecs[0][0] = 1; vecs[0][1] = 0;
	vecs[1][0] = 0; vecs[1][1] = 1;
	eigens = new double[2][2];
	reinit();
	repaint();
    }

    void reinit() {
        Dimension d = winSize = cv.getSize();
	if (winSize.width == 0)
	    return;
	dbimage = createImage(d.width, d.height);
    }
    
    public void paint(Graphics g) {
	cv.repaint();
    }

    void findVecCoords(double x, double y, int result[]) {
	int cy = winSize.height/4;
	int cx = cy;
	result[0] = (int) (cx*(x+2));
	result[1] = (int) (cy*(2-y));
    }

    void findVecCoords(int num, int result[]) {
	findVecCoords(vecs[num][0], vecs[num][1], result);
    }

    void findXformVecCoords(double x, double y, int result[]) {
	findVecCoords(vecs[0][0]*x+vecs[1][0]*y,
		      vecs[0][1]*x+vecs[1][1]*y, result);
    }

    void drawArrow(Graphics g, int x1, int y1, int x2, int y2) {
	g.drawLine(x1, y1, x2, y2);
	double l = java.lang.Math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1));
	if (l > 10) {
	    double hatx = (x2-x1)/l;
	    double haty = (y2-y1)/l;
	    int as = 10;
	    g.drawLine(x2, y2,
		       (int) (haty*as-hatx*as+x2),
		       (int) (-hatx*as-haty*as+y2));
	    g.drawLine(x2, y2,
		       (int) (-haty*as-hatx*as+x2),
		       (int) (hatx*as-haty*as+y2));
	}
    }

    void drawBar(Graphics g, int offset, double val) {
	int x = (int) (winSize.width * val/6);
	int cx = winSize.width/2;
	int h = 5;
	int y = winSize.height + h*offset;
	int y2 = y+h-1;
	if (val < 0)
	    g.fillRect(cx+x, y, -x, h);
	else
	    g.fillRect(cx, y, x, h);
    }

    boolean isZero(double a) {
	return (a >= -.00001 && a <= .00001);
    }

    void eigenfind(double ev, int num) {
	double a, b;
	b = vecs[0][0] - ev;
	a = -vecs[1][0];
	if (isZero(a) && isZero(b)) {
	    b = -vecs[0][1];
	    a = vecs[1][1]-ev;
	}
	double l = java.lang.Math.sqrt(a*a+b*b);
	if ((a < 0 && b < 0) || a < -b || b < -a)
	    l = -l;
	if (isZero(l))
	    eigens[num][0] = eigens[num][1] = 0;
	else {
	    eigens[num][0] = a/l;
	    eigens[num][1] = b/l;
	}
    }

    String eigenstring(int n, NumberFormat nf, double ev, boolean er,
		       double tr, double ed) {
	if (er)
	    return "lambda" + n + " = " + nf.format(ev);
	if (n == 1)
	    return "lambda1 = " + nf.format(tr*.5) + "+" + nf.format(ed*.5) + "i";
	return "lambda2 = " + nf.format(tr*.5) + "-" + nf.format(ed*.5) + "i";
    }

    public void updateMatrix(Graphics realg) {
	int i, j;
	for (i = 0; i != 2; i++)
	    for (j = 0; j != 2; j++)
		if (isZero(vecs[i][j])) vecs[i][j] = 0;
	double alen = java.lang.Math.sqrt(
	    vecs[0][0] * vecs[0][0] + vecs[0][1] * vecs[0][1]);
	double blen = java.lang.Math.sqrt(
	    vecs[1][0] * vecs[1][0] + vecs[1][1] * vecs[1][1]);
	double piadj = 180/3.14159265;
	double det = vecs[0][0] * vecs[1][1] - vecs[0][1] * vecs[1][0];
	if (isZero(det))
	    invertButton.disable();
	else
	    invertButton.enable();
	double trace = vecs[0][0] + vecs[1][1];
	double eigendisc = trace*trace - 4*det;
	double eigen1, eigen2;
	boolean eigenreal = true;
	if (eigendisc < 0) {
	    eigenreal = false;
	    eigendisc = -eigendisc;
	}
	eigendisc = java.lang.Math.sqrt(eigendisc);
	eigen1 = .5*(trace + eigendisc);
	eigen2 = .5*(trace - eigendisc);
	int eigenveccount = (eigenreal) ? 2 : 0;
	if (eigenreal && eigen1 == eigen2)
	    eigenveccount = (vecs[0][1] == 0 && vecs[1][0] == 0) ? 0 : 1;
	if (eigenveccount > 0)
	    eigenfind(eigen1, 0);
	if (eigenveccount > 1)
	    eigenfind(eigen2, 1);

	Graphics g = dbimage.getGraphics();
	if (winSize == null || winSize.width == 0)
	    return;
	g.setColor(getBackground());
	g.fillRect(0, 0, winSize.width, winSize.height);
	g.setColor(Color.gray);
	for (i = -2; i <= 2; i++) {
	    int x = winSize.height*(i+2)/4;
	    g.drawLine(x, 0, x, winSize.height);
	    g.drawLine(0, x, winSize.height, x);
	}
	int cy = winSize.height/2;
	int cx = cy;
	int vc[] = new int[2];
	int vc2[] = new int[2];

	int dotSize = 5;
	if (showPoint) {
	    g.setColor(Color.gray);
	    findXformVecCoords(pointX, pointY, vc);
	    findVecCoords(pointX, pointY, vc2);
	    drawArrow(g, vc2[0], vc2[1], vc[0], vc[1]);
	}

	g.setColor(Color.green);
	findXformVecCoords(1, 1, vc);
	findXformVecCoords(-1, 1, vc2);
	g.drawLine(vc[0], vc[1], vc2[0], vc2[1]);
	findXformVecCoords(-1, -1, vc);
	g.drawLine(vc[0], vc[1], vc2[0], vc2[1]);
	findXformVecCoords(1, -1, vc2);
	g.drawLine(vc[0], vc[1], vc2[0], vc2[1]);
	findXformVecCoords(1, 1, vc);
	g.drawLine(vc[0], vc[1], vc2[0], vc2[1]);

	findXformVecCoords(-.5, .5, vc);
	findXformVecCoords(.5, .5,  vc2);
	g.drawLine(vc[0], vc[1], vc2[0], vc2[1]);
	findXformVecCoords(-.5, -.5,  vc);
	g.drawLine(vc[0], vc[1], vc2[0], vc2[1]);
	findXformVecCoords(.5, -.5, vc2);
	g.drawLine(vc[0], vc[1], vc2[0], vc2[1]);
	findXformVecCoords(-.5, -.6,  vc);
	findXformVecCoords(.5, -.6, vc2);
	g.drawLine(vc[0], vc[1], vc2[0], vc2[1]);

	if (showPoint) {
	    g.setColor(purple);
	    findXformVecCoords(pointX, pointY, vc);
	    g.fillOval(vc[0]-dotSize/2, vc[1]-dotSize/2, dotSize, dotSize);
	}

	if (eigenveccount > 0) {
	    g.setColor(Color.yellow);
	    findVecCoords(eigens[0][0], eigens[0][1], vc);
	    drawArrow(g, cx, cy, vc[0], vc[1]);
	}
	if (eigenveccount > 1) {
	    g.setColor(Color.orange);
	    findVecCoords(eigens[1][0], eigens[1][1], vc);
	    drawArrow(g, cx, cy, vc[0], vc[1]);
	}

	if (!isZero(det)) {
	    g.setColor(darkRed);
	    findVecCoords(vecs[1][1]/det, -vecs[0][1]/det, vc);
	    g.fillOval(vc[0]-dotSize/2, vc[1]-dotSize/2, dotSize, dotSize);
	    g.setColor(darkCyan);
	    findVecCoords(-vecs[1][0]/det, vecs[0][0]/det, vc);
	    g.fillOval(vc[0]-dotSize/2, vc[1]-dotSize/2, dotSize, dotSize);
	}

	findVecCoords(0, vc);
	g.setColor(Color.red);
	drawArrow(g, cx, cy, vc[0], vc[1]);
	findVecCoords(1, vc);
	g.setColor(Color.cyan);
	drawArrow(g, cx, cy, vc[0], vc[1]);

	FontMetrics fm = g.getFontMetrics();
	int yl = fm.getHeight();
	int y = reflectYButton.getY() + reflectYButton.getHeight() +
	    5 + fm.getMaxAscent();
	NumberFormat nf = NumberFormat.getInstance();
	nf.setMaximumFractionDigits(3);

	String as = nf.format(vecs[0][0]);
	String bs = nf.format(vecs[1][0]);
	String cs = nf.format(vecs[0][1]);
	String ds = nf.format(vecs[1][1]);
	int c1w = fm.stringWidth(as);
	int w = fm.stringWidth(cs);
	if (w > c1w)
	    c1w = w;
	int c2w = fm.stringWidth(bs);
	w = fm.stringWidth(ds);
	if (w > c2w)
	    c2w = w;
	int spacing = 10;
	int totw = c1w+spacing+c2w;
	int x = winSize.height + (winSize.width - winSize.height - totw)/2;
	g.setColor(Color.red);
	g.drawString(as, x+(c1w-fm.stringWidth(as))/2, y);
	g.setColor(Color.cyan);
	g.drawString(bs, x+c1w+spacing+(c2w-fm.stringWidth(bs))/2, y);
	y += yl;
	g.setColor(Color.red);
	g.drawString(cs, x+(c1w-fm.stringWidth(cs))/2, y);
	g.setColor(Color.cyan);
	g.drawString(ds, x+c1w+spacing+(c2w-fm.stringWidth(ds))/2, y);
					      
	g.setColor(Color.white);
	int y1 = y-yl-fm.getMaxAscent();
	int y2 = y+fm.getMaxDescent();
	g.drawLine(x-5, y1, x-5, y2);
	g.drawLine(x-5, y1, x, y1);
	g.drawLine(x-5, y2, x, y2);
	g.drawLine(x+totw+5, y1, x+totw+5, y2);
	g.drawLine(x+totw, y1, x+totw+5, y1);
	g.drawLine(x+totw, y2, x+totw+5, y2);

	displayString(g, "det M = " + nf.format(det), y += yl);
	displayString(g, "tr M = " + nf.format(trace), y += yl);
	g.setColor(Color.yellow);
	displayString(g,
		      eigenstring(1, nf, eigen1, eigenreal, trace, eigendisc),
		      y += yl);
	g.setColor(Color.orange);
	displayString(g,
		      eigenstring(2, nf, eigen2, eigenreal, trace, eigendisc),
		      y += yl);
	realg.drawImage(dbimage, 0, 0, this);
    }

    void displayString(Graphics g, String s, int y) {
	int lx = winSize.height;
	int lw = winSize.width - lx;
	FontMetrics fm = g.getFontMetrics();
        g.drawString(s, lx+(lw-fm.stringWidth(s))/2, y);
    }

    void edit(MouseEvent e) {
	if (!dragging)
	    return;
	int x = e.getX();
	int y = e.getY();
	double cy = winSize.height/4;
	double cx = cy;
	double xf = x/cx-2;
	double yf = 2-y/cy;
	if (xf < -2) xf = -2;
	if (yf < -2) yf = -2;
	if (xf >  2) xf =  2;
	if (yf >  2) yf =  2;
	if (selection != -1) {
	    vecs[selection][0] = xf;
	    vecs[selection][1] = yf;
	} else {
	    double oldang = java.lang.Math.atan2(pointY, pointX);
	    double newang = java.lang.Math.atan2(yf, xf);
	    double oldr = java.lang.Math.sqrt(pointX*pointX + pointY*pointY);
	    double newr = java.lang.Math.sqrt(xf*xf+yf*yf);
	    double rmult = newr/oldr;
	    double costhr = java.lang.Math.cos(newang-oldang)*rmult;
	    double sinthr = java.lang.Math.sin(newang-oldang)*rmult;
	    vecs[0][0] = origmatrix[0][0] * costhr + origmatrix[1][0] * sinthr;
	    vecs[0][1] = origmatrix[0][1] * costhr + origmatrix[1][1] * sinthr;
	    vecs[1][0] = origmatrix[0][0] *-sinthr + origmatrix[1][0] * costhr;
	    vecs[1][1] = origmatrix[0][1] *-sinthr + origmatrix[1][1] * costhr;
	}
	cv.repaint();
    }

    public void componentHidden(ComponentEvent e){}
    public void componentMoved(ComponentEvent e){}
    public void componentShown(ComponentEvent e) {
	cv.repaint();
    }

    public void componentResized(ComponentEvent e) {
	reinit();
	cv.repaint(100);
    }
    public void actionPerformed(ActionEvent e) {
	if (e.getSource() == identityButton) {
	    vecs[0][0] = 1;
	    vecs[0][1] = 0;
	    vecs[1][0] = 0;
	    vecs[1][1] = 1;
	    cv.repaint();
	}
	if (e.getSource() == transposeButton) {
	    double x = vecs[1][0];
	    vecs[1][0] = vecs[0][1];
	    vecs[0][1] = x;
	    cv.repaint();
	}
	if (e.getSource() == invertButton) {
	    double det = vecs[0][0] * vecs[1][1] - vecs[0][1] * vecs[1][0];
	    if (det != 0) {
		double x;
		x = vecs[0][0];
		vecs[0][0] = vecs[1][1]/det;
		vecs[1][1] = x/det;
		vecs[1][0] /= -det;
		vecs[0][1] /= -det;
	    }
	    cv.repaint();
	}
	if (e.getSource() == rotateCCWButton) {
	    double cos30 = .8660254;
	    copyMatrix();
	    vecs[0][0] = origmatrix[0][0] * cos30 + origmatrix[1][0] * .5;
	    vecs[0][1] = origmatrix[0][1] * cos30 + origmatrix[1][1] * .5;
	    vecs[1][0] = origmatrix[0][0] *-.5 + origmatrix[1][0] * cos30;
	    vecs[1][1] = origmatrix[0][1] *-.5 + origmatrix[1][1] * cos30;
	    cv.repaint();
	}
	if (e.getSource() == rotateCWButton) {
	    double cos30 = .8660254;
	    copyMatrix();
	    vecs[0][0] = origmatrix[0][0] * cos30 + origmatrix[1][0] * -.5;
	    vecs[0][1] = origmatrix[0][1] * cos30 + origmatrix[1][1] * -.5;
	    vecs[1][0] = origmatrix[0][0] * .5 + origmatrix[1][0] * cos30;
	    vecs[1][1] = origmatrix[0][1] * .5 + origmatrix[1][1] * cos30;
	    cv.repaint();
	}
	if (e.getSource() == reflectXButton) {
	    vecs[0][1] = -vecs[0][1];
	    vecs[1][1] = -vecs[1][1];
	    cv.repaint();
	}
	if (e.getSource() == reflectYButton) {
	    vecs[0][0] = -vecs[0][0];
	    vecs[1][0] = -vecs[1][0];
	    cv.repaint();
	}
    }
    public void adjustmentValueChanged(AdjustmentEvent e) {
    }
    public void mouseDragged(MouseEvent e) {
	edit(e);
    }
    public void mouseMoved(MouseEvent e) {
	if ((e.getModifiers() & MouseEvent.BUTTON1_MASK) == 0) {
	    double cy = winSize.height/4;
	    double cx = cy;
	    double xf = e.getX()/cx-2;
	    double yf = 2-e.getY()/cy;
	    showPoint = true;
	    if (xf < -2) showPoint = false;
	    if (yf < -2) showPoint = false;
	    if (xf >  2) showPoint = false;
	    if (yf >  2) showPoint = false;
	    pointX = xf;
	    pointY = yf;
	    cv.repaint();
	    return;
	}
	edit(e);
    }
    public void mouseClicked(MouseEvent e) {
    }
    public void mouseEntered(MouseEvent e) {
    }
    public void mouseExited(MouseEvent e) {
	showPoint = false;
	cv.repaint();
    }
    public void mousePressed(MouseEvent e) {
	if ((e.getModifiers() & MouseEvent.BUTTON1_MASK) == 0)
	    return;
	int x = e.getX();
	int y = e.getY();
	int vc[] = new int[2];
	int i;
	selection = -1;
	showPoint = false;
	for (i = 0; i != 2; i++) {
	    findVecCoords(i, vc);
	    int space = 10;
	    if (vc[0] >= x-space && vc[0] <= x+space &&
		vc[1] >= y-space && vc[1] <= y+space) {
		selection = i;
		break;
	    }
	}
	if (selection == -1) {
	    double cy = winSize.height/4;
	    double cx = cy;
	    double xf = e.getX()/cx-2;
	    double yf = 2-e.getY()/cy;
	    if (xf < -2) return;
	    if (yf < -2) return;
	    if (xf >  2) return;
	    if (yf >  2) return;
	    if (isZero(xf) && isZero(yf))
		return;
	    dragging = true;
	    pointX = xf;
	    pointY = yf;
	    copyMatrix();
	    return;
	}
	dragging = true;
	edit(e);
    }
    void copyMatrix() {
	origmatrix = new double[2][2];
	int i, j;
	for (i = 0; i != 2; i++)
	    for (j = 0; j != 2; j++)
		origmatrix[i][j] = vecs[i][j];
    }
    public void mouseReleased(MouseEvent e) {
	if ((e.getModifiers() & MouseEvent.BUTTON1_MASK) == 0)
	    return;
	dragging = false;
	selection = -1;
    }
}

