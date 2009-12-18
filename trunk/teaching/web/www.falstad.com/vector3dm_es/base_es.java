//line 1 "origbase.java"


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
import java.awt.event.*;
//line 31 "origbase.java"
class Vec3DemoCanvas extends Canvas {
    Vec3DemoFrame pg;
    Vec3DemoCanvas(Vec3DemoFrame p) {
	pg = p;
    }
    public Dimension getPreferredSize() {
	return new Dimension(300,400);
    }
    public void update(Graphics g) {
	pg.updateVec3Demo(g);
    }
    public void paint(Graphics g) {
	pg.updateVec3Demo(g);
    }
};

class Vec3DemoLayout implements LayoutManager {
    public Vec3DemoLayout() {}
    public void addLayoutComponent(String name, Component c) {}
    public void removeLayoutComponent(Component c) {}
    public Dimension preferredLayoutSize(Container target) {
	return new Dimension(500, 500);
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
		if (m instanceof Scrollbar || m instanceof TextComponent)
		    d.width = barwidth;
		if (m instanceof Choice && d.width > barwidth)
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

class Vec3DemoFrame extends Frame
    implements ComponentListener, ActionListener, AdjustmentListener,
	       MouseMotionListener, MouseListener, ItemListener {

    Thread engine = null;

    Dimension winSize;
    Rectangle viewMain, viewAxes;
    Image dbimage;

    Vec3Demo applet;
    Random random;

    public String getAppletInfo() {
	return "Vec3Demo by Paul Falstad";
    }

    static final double pi = 3.14159265358979323846;

    int getrand(int x) {
	int q = random.nextInt();
	if (q < 0) q = -q;
	return q % x;
    }
    Vec3DemoCanvas cv;
    Checkbox stoppedCheck;
    Button resetButton;
    Button kickButton;
    Checkbox reverseCheck;
    Button infoButton;
    Choice functionChooser;
    Choice dispChooser;
//line 185 "origbase.java"
    static final int DISP_PART_VELOC = 0;
    static final int DISP_PART_VELOC_A = 1;
    static final int DISP_VECTORS = 2;
    static final int DISP_VECTORS_A = 3;
    static final int DISP_LINES = 4;
    static final int DISP_PART_MAG = 5;
    static final int DISP_VIEW_PAPER = 6;
    static final int DISP_EQUIPS = -1;
    static final int DISP_PART_FORCE = -4;

    Choice sliceChooser;
    static final int SLICE_NONE = 0;
    static final int SLICE_X = 1;
    static final int SLICE_Y = 2;
    static final int SLICE_Z = 3;
    Label partCountLabel;
    Label textFieldLabel;
    Label strengthLabel;
    Scrollbar partCountBar;
    Scrollbar strengthBar;
    Scrollbar aux1Bar;
    Scrollbar aux2Bar;
    Scrollbar aux3Bar;
    double fieldStrength, partMult;
    Color darkYellow = new Color(144, 144, 0);
    final double lineWidth = .01;
    class AuxBar {
	Scrollbar bar;
	Label label;
	AuxBar(Label l, Scrollbar b) { label = l; bar = b; }
    };
    AuxBar auxBars[];
    Label vecDensityLabel;
    Scrollbar vecDensityBar;
    Label potentialLabel;
    Scrollbar potentialBar;
    Label lineDensityLabel;
    Scrollbar lineDensityBar;
    Choice modeChooser;
    TextField textFields[];
    static final int MODE_ANGLE = 0;
    static final int MODE_ZOOM = 1;
    static final int MODE_SLICE = 2;
    int reverse;
    int xpoints[];
    int ypoints[];
    int slicerPoints[][];
    double sliceFaces[][];
    double sliceFace[];
    Particle particles[];
    FieldVector vectors[];
    int vecCount;
    int density[][][];
    double sliceval = 0;
    double rotmatrix[];
    double cameraPos[];
    double intersection[];
    double intersectionDistance;
    int vectorSpacing = 16;
    int currentStep;
    boolean selectedSlice, mouseDown, getPot;
    boolean showA;
    boolean parseError;
    Color fieldColors[];
    Color equipColors[];


    static final double densitygroupsize = 1./2;
    static final int densitygridsize = 4;
    static final int maxParticleCount = 5000;
    double zoom = 3;
    boolean dragging;
    int oldDragX, oldDragY, dragX, dragY, dragStartX, dragStartY;
    double dragZoomStart, lastXRot, lastYRot;
    Vector functionList;
    VecFunction curfunc;
    int pause = 20;

    Vec3DemoFrame(Vec3Demo a) {
	super("Campos vectoriales 3D Applet v1.3");
	applet = a;
    }

    public void init() {
	try {
	    String param = applet.getParameter("PAUSA");
	    if (param != null)
		pause = Integer.parseInt(param);
	} catch (Exception e) { }

	functionList = new Vector();
	VecFunction vf = new
	    InverseRotational() ;
//line 280 "origbase.java"
	while (vf != null) {
	    functionList.addElement(vf);
	    vf = vf.createNext();
	}
	random = new Random();
	particles = new Particle[maxParticleCount];
	int i;
	for (i = 0; i != maxParticleCount; i++)
	    particles[i] = new Particle();
	xpoints = new int[4];
	ypoints = new int[4];
	slicerPoints = new int[2][5*2];
	sliceFaces = new double[4][3];
	rotmatrix = new double[9];
	setXYView();
	density = new int[densitygridsize][densitygridsize][densitygridsize];
	setLayout(new Vec3DemoLayout());
	cv = new Vec3DemoCanvas(this);
	cv.addComponentListener(this);
	cv.addMouseMotionListener(this);
	cv.addMouseListener(this);
	add(cv);
//line 307 "origbase.java"
	add(new Label("Selección de Campo:"));
	functionChooser = new Choice();
	for (i = 0; i != functionList.size(); i++)
	    functionChooser.add(
	       ((VecFunction) functionList.elementAt(i)).getName());
	add(functionChooser);
	functionChooser.addItemListener(this);

	dispChooser = new Choice();
	dispChooser.addItemListener(this);
	setupDispChooser(true);
	add(dispChooser);

	modeChooser = new Choice();
	modeChooser.add("Ratón = Ajustar Ángulo");
	modeChooser.add("Ratón = Ajustar Zoom  ");
	modeChooser.addItemListener(this);
	add(modeChooser);

	sliceChooser = new Choice();
	sliceChooser.add("Sin corte");
	sliceChooser.add("Ver corte X");
	sliceChooser.add("Ver corte Y");
	sliceChooser.add("Ver corte Z");
	sliceChooser.addItemListener(this);
	add(sliceChooser);

	stoppedCheck = new Checkbox("Parado");
	stoppedCheck.addItemListener(this);
	add(stoppedCheck);

	reverseCheck = new Checkbox("Invertir");
	reverseCheck.addItemListener(this);
	add(reverseCheck);

	resetButton = new Button("Reiniciar");
	add(resetButton);
	resetButton.addActionListener(this);
	kickButton = new Button("Golpe");
//line 352 "origbase.java"
	add(strengthLabel = new Label("Intensidad del Campo", Label.CENTER));
	add(strengthBar = new Scrollbar(Scrollbar.HORIZONTAL, 10, 1, 0, 100));
	strengthBar.addAdjustmentListener(this);

	add(partCountLabel = new Label("Número de Partículas", Label.CENTER));
	add(partCountBar = new Scrollbar(Scrollbar.HORIZONTAL,
					 500, 1, 1,
					 maxParticleCount));
	partCountBar.addAdjustmentListener(this);

	add(vecDensityLabel = new Label("Densidad de Vectores", Label.CENTER));
	add(vecDensityBar = new Scrollbar(Scrollbar.HORIZONTAL, 16, 1, 2, 64));
	vecDensityBar.addAdjustmentListener(this);

	add(lineDensityLabel = new Label("Densidad de Líneas de Campo", Label.CENTER));
	add(lineDensityBar = new Scrollbar(Scrollbar.HORIZONTAL, 5, 1, 3, 16));
	lineDensityBar.addAdjustmentListener(this);

	add(potentialLabel = new Label("Potencial", Label.CENTER));
	add(potentialBar = new Scrollbar(Scrollbar.HORIZONTAL, 250,1, 0, 1000));
	potentialBar.addAdjustmentListener(this);

	Label lb;
	auxBars = new AuxBar[3];
	add(lb = new Label("Aux 1", Label.CENTER));
	add(aux1Bar = new Scrollbar(Scrollbar.HORIZONTAL, 0, 1, 0, 100));
	aux1Bar.addAdjustmentListener(this);
	auxBars[0] = new AuxBar(lb, aux1Bar);

	add(lb = new Label("Aux 2", Label.CENTER));
	add(aux2Bar = new Scrollbar(Scrollbar.HORIZONTAL, 0, 1, 0, 100));
	aux2Bar.addAdjustmentListener(this);
	auxBars[1] = new AuxBar(lb, aux2Bar);

	add(lb = new Label("Aux 3", Label.CENTER));
	add(aux3Bar = new Scrollbar(Scrollbar.HORIZONTAL, 0, 1, 0, 100));
	aux3Bar.addAdjustmentListener(this);
	auxBars[2] = new AuxBar(lb, aux3Bar);
//line 402 "origbase.java"
	textFields = new TextField[3];
	for (i = 0; i != 3; i++) {
	    add(textFields[i] = new TextField());
	    textFields[i].addActionListener(this);
	}
	fieldColors = new Color[513];
	for (i = 0; i != 256; i++) {
	    int col = (255<<24) | (i<<8);
	    fieldColors[i] = new Color(col);
	}
	for (i = 0; i != 256; i++) {
	    int col = (255<<24) | (255<<8) | (i * (0x10001));
	    fieldColors[i+256] = new Color(col);
	}
	fieldColors[512] = fieldColors[511];
	equipColors = new Color[513];
	for (i = 0; i != 256; i++) {
	    int r = 255-i/2;
	    int gb = i/2;
	    int col = (255<<24) | (r<<16) | (gb<<8) | gb;
	    equipColors[i] = new Color(col);
	}
	for (i = 0; i != 256; i++) {
	    int g = 128+i/2;
	    int rb = 128-i/2;
	    int col = (255<<24) | (rb<<16) | (g<<8) | rb;
	    equipColors[i+256] = new Color(col);
	}
	equipColors[512] = equipColors[511];
	
	add(new Label("Autor: Paul Falstad", Label.CENTER));
	add(new Label("http://www.falstad.com", Label.CENTER));
	add(new Label("Traducción: Juan M Fernández", Label.CENTER));
	add(new Label("http://www.iesjorgemanrique.com", Label.CENTER));
	intersection = new double[3];

	reinit();
	cv.setBackground(Color.black);
	cv.setForeground(Color.lightGray);

	resize(500, 500);
	handleResize();
	Dimension screen = getToolkit().getScreenSize();
	Dimension x = getSize();
	setLocation((screen.width - x.width)/2,
		    (screen.height - x.height)/2);
	functionChanged();
	dispChooserChanged();
	show();
	requestFocus();
    }

    void setViewMatrix(double a, double b) {
	int i;
	for (i = 0; i != 9; i++)
	    rotmatrix[i] = 0;
	rotmatrix[0] = rotmatrix[4] = rotmatrix[8] = 1;
	rotate(a, b);
	lastXRot = lastYRot = 0;
    }

    void setXYView() {
	setViewMatrix(0, pi/11);
    }

    void setXYViewExact() {
	setViewMatrix(0, 0);
    }

    void setXZView() {
	setViewMatrix(0, pi/11-pi/2);
    }

    void setXZViewExact() {
	setViewMatrix(0, -pi/2);
    }

    void handleResize() {
        Dimension d = winSize = cv.getSize();
	if (winSize.width == 0)
	    return;
	dbimage = createImage(d.width, d.height);
	scaleworld();
	viewMain = new Rectangle(winSize);
	viewAxes = new Rectangle(winSize.width-100, 0, 100, 100);
    }

    void resetDensityGroups() {
	int i, j, k;
	for (i = 0; i != densitygridsize; i++)
	    for (j = 0; j != densitygridsize; j++)
		for (k = 0; k != densitygridsize; k++)
		    density[i][j][k] = 0;
	int slice = sliceChooser.getSelectedIndex();
	boolean sliced = (slice > 0);
	int pcount = getParticleCount();
	for (i = 0; i != pcount; i++) {
	    Particle p = particles[i];
	    if (sliced)
		p.pos[slice-SLICE_X] = sliceval;
	    addToDensityGroup(p);
	}




	for (; i != maxParticleCount; i++) {
	    Particle p = particles[i];
	    p.lifetime = -100;
	}
    }

    int addToDensityGroup(Particle p) {
	int a = (int)((p.pos[0]+1)*(densitygridsize/2));
	int b = (int)((p.pos[1]+1)*(densitygridsize/2));
	int c = (int)((p.pos[2]+1)*(densitygridsize/2));
	int n = 0;
	try {
	n = ++density[a][b][c];
	if (n > maxParticleCount)
	    System.out.print(a + " " + b + " " + c + " " + density[a][b][c] + "\n");
	} catch (Exception e) {
	    System.out.print(p.pos[0] + " " + p.pos[1] + " " + p.pos[2] + "\n");
	    e.printStackTrace();
	}
	return n;
    }

    void removeFromDensityGroup(Particle p) {
	int a = (int)((p.pos[0]+1)*(densitygridsize/2));
	int b = (int)((p.pos[1]+1)*(densitygridsize/2));
	int c = (int)((p.pos[2]+1)*(densitygridsize/2));
	try {
	    if (--density[a][b][c] < 0)
		System.out.print(a + " " + b + " " + c + " " + density[a][b][c] + "\n");
	} catch (Exception e) {
	    System.out.print(p.pos[0] + " " + p.pos[1] + " " + p.pos[2] + "\n");
	    e.printStackTrace();
	}
    }

    void positionParticle(Particle p) {
	int x, y, z;
	int bestx = 0, besty = 0, bestz = 0;
	int best = 10000;



	int randaddx = getrand(densitygridsize);
	int randaddy = getrand(densitygridsize);
	int randaddz = getrand(densitygridsize);
	for (x = 0; x != densitygridsize; x++)
	    for (y = 0; y != densitygridsize; y++)
		for (z = 0; z != densitygridsize; z++) {
		    int ix = (randaddx + x) % densitygridsize;
		    int iy = (randaddy + y) % densitygridsize;
		    int iz = (randaddz + z) % densitygridsize;
		    if (density[ix][iy][iz] <= best) {
			bestx = ix;
			besty = iy;
			bestz = iz;
			best = density[ix][iy][iz];
		    }
		}
	p.pos[0] = bestx*densitygroupsize +
	    getrand(100)*densitygroupsize/100.0 - 1;
	p.pos[1] = besty*densitygroupsize +
	    getrand(100)*densitygroupsize/100.0 - 1;
	p.pos[2] = bestz*densitygroupsize +
	    getrand(100)*densitygroupsize/100.0 - 1;
	p.lifetime = curfunc.redistribute() ? 500 : 5000;
	p.stepsize = 1;
	p.theta = (getrand(101)-50)*pi/50.;
	p.phi = (getrand(101)-50)*pi/50.;
	int j;
	for (j = 0; j != 3; j++)
	    p.vel[j] = 0;
    }

    int getParticleCount() {
	return partCountBar.getValue();
    }

    void resetParticles() {
	int pcount = getParticleCount();
	int i, j;
	for (i = 0; i != pcount; i++) {
	    Particle p = particles[i];
	    for (j = 0; j != 3; j++) {
		p.pos[j] = getrand(200)/100.0 - 1;
		p.vel[j] = 0;
	    }
	    p.lifetime = i*2;
	    p.stepsize = 1;
	}
	resetDensityGroups();
    }

    void kickParticles() {
	int i, j;
	for (i = 0; i != getParticleCount(); i++) {
	    Particle p = particles[i];
	    for (j = 0; j != 3; j++)
		p.vel[j] += (getrand(100)/99.0 - .5) * .04;
	}
    }



    void rotate(double angle1, double angle2) {
	double r1cos = java.lang.Math.cos(angle1);
	double r1sin = java.lang.Math.sin(angle1);
	double r2cos = java.lang.Math.cos(angle2);
	double r2sin = java.lang.Math.sin(angle2);
	double rotm2[] = new double[9];


	rotm2[0] = r1cos;
	rotm2[1] = -r1sin*r2sin;
	rotm2[2] = r2cos*r1sin;

	rotm2[3] = 0;
	rotm2[4] = r2cos;
	rotm2[5] = r2sin;

	rotm2[6] = -r1sin;
	rotm2[7] = -r1cos*r2sin;
	rotm2[8] = r1cos*r2cos;
	rotate(rotm2);
    }

    void rotate(double rotm2[]) {
	double rotm1[] = rotmatrix;
	rotmatrix = new double[9];

	int i, j, k;
	for (j = 0; j != 3; j++)
	    for (i = 0; i != 3; i++) {
		double v = 0;
		for (k = 0; k != 3; k++)
		    v += rotm1[k+j*3]*rotm2[i+k*3];
		rotmatrix[i+j*3] = v;
	    }
    }

    void reinit() {
	handleResize();
	resetParticles();
    }

    void centerString(Graphics g, String s, int y) {
	FontMetrics fm = g.getFontMetrics();
        g.drawString(s, (winSize.width-fm.stringWidth(s))/2, y);
    }

    public void paint(Graphics g) {
	cv.repaint();
    }

    static final double root2 = 1.4142135623730950488016887242096981;
    double scalex, scaley;
    static final double viewDistance = 5;

    void map3d(double x, double y, double z, int xpoints[],
	       int ypoints[], int pt) {
	map3d(x, y, z, xpoints, ypoints, pt, viewMain);
    }

    void map3d(double x, double y, double z,
	       int xpoints[], int ypoints[], int pt, Rectangle view) {
	double rotm[] = rotmatrix;
	double realx = x*rotm[0] + y*rotm[3] + z*rotm[6];
	double realy = x*rotm[1] + y*rotm[4] + z*rotm[7];
	double realz = viewDistance-(x*rotm[2] + y*rotm[5] + z*rotm[8]);
	double scalex = view.width*zoom/2;
	double scaley = view.height*zoom/2;
	double aratio = view.width/(double) view.height;

	if (aratio < 1)
	    scaley *= aratio;
	else
	    scalex /= aratio;
	xpoints[pt] = view.x + view.width /2 + (int) (scalex*realx/realz);
	ypoints[pt] = view.y + view.height/2 - (int) (scaley*realy/realz);
    }

    double getScalingFactor(double x, double y, double z) {
	double rotm[] = rotmatrix;
	double realz = viewDistance-(x*rotm[2] + y*rotm[5] + z*rotm[8]);
	double scalex = winSize.width*zoom/2;
	double scaley = winSize.height*zoom/2;
	double aratio = winSize.width/(double) winSize.height;

	if (aratio < 1)
	    scaley *= aratio;
	else
	    scalex /= aratio;

	return scalex/realz;
    }


    void unmap3d(double x3[], int x, int y, double z, Rectangle view) {
	double scalex = view.width*zoom/2;
	double scaley = view.height*zoom/2;

	double aratio = view.width/(double) view.height;

	if (aratio < 1)
	    scaley *= aratio;
	else
	    scalex /= aratio;

	double realz = viewDistance-z;
	double realx = (x-(view.width/2))*realz/scalex;
	double realy = -(y-(view.height/2))*realz/scaley;
	double rotm[] = rotmatrix;
	x3[0] = (realx*rotm[0] + realy*rotm[1] + z*rotm[2]);
	x3[1] = (realx*rotm[3] + realy*rotm[4] + z*rotm[5]);
	x3[2] = (realx*rotm[6] + realy*rotm[7] + z*rotm[8]);
    }


    void unmap3d(double x3[], int x, int y, double pn[], double pp[],
		 Rectangle view) {


	double scalex = view.width*zoom/2;
	double scaley = view.height*zoom/2;

	double aratio = view.width/(double) view.height;

	if (aratio < 1)
	    scaley *= aratio;
	else
	    scalex /= aratio;

	double vx = (x-(view.width/2))/scalex;
	double vy = -(y-(view.height/2))/scaley;




	double rotm[] = rotmatrix;
	double mvx = (vx*rotm[0] + vy*rotm[1] - rotm[2]);
	double mvy = (vx*rotm[3] + vy*rotm[4] - rotm[5]);
	double mvz = (vx*rotm[6] + vy*rotm[7] - rotm[8]);


	double t = ((pp[0]-cameraPos[0])*pn[0] +
		    (pp[1]-cameraPos[1])*pn[1] +
		    (pp[2]-cameraPos[2])*pn[2]) /
	    (pn[0]*mvx+pn[1]*mvy+pn[2]*mvz);

	x3[0] = cameraPos[0]+mvx*t;
	x3[1] = cameraPos[1]+mvy*t;
	x3[2] = cameraPos[2]+mvz*t;
    }

    void scaleworld() {
	scalex = winSize.width/2;
	scaley = winSize.height/2;
    }

    long lastTime;
    double timeStep;

    public void updateVec3Demo(Graphics realg) {
	Graphics g = dbimage.getGraphics();
	if (winSize == null || winSize.width == 0)
	    return;
	if (xpoints == null)
	    return;
	g.setColor(cv.getBackground());
	g.fillRect(0, 0, winSize.width, winSize.height);
	g.setColor(cv.getForeground());

	boolean allquiet = false;

	curfunc.setupFrame();
	int disp = dispChooser.getSelectedIndex();
	timeStep = 1;
	if (!stoppedCheck.getState()) {
	    if (lastTime > 0)
		timeStep = (System.currentTimeMillis()-lastTime)*.03;
	    if (timeStep > 3)
		timeStep = 3;
	    lastTime = System.currentTimeMillis();
	    if (disp != DISP_VECTORS && disp != DISP_VECTORS_A &&
		disp != DISP_LINES && disp != DISP_EQUIPS) {
		moveParticles();
		allquiet = false;
	    }
	    currentStep = (int)
		(reverse*(lastTime/30) % 800);
	    if (currentStep < 0)
		currentStep += 800;
	} else {
	    lastXRot = lastYRot = 0;
	    lastTime = 0;
	}

	drawCube(g, true);

	cameraPos = new double[3];
	unmap3d(cameraPos, winSize.width/2, winSize.height/2, viewDistance,
		viewMain);
	if (disp == DISP_VECTORS || disp == DISP_VECTORS_A)
	    drawVectors(g);
	else if (disp == DISP_LINES) {
	    genLines();
	    drawLines(g);
//line 816 "origbase.java"
	} else if (disp == DISP_VIEW_PAPER)
	    drawViewPaper(g);
	else
	    drawParticles(g);

	g.setColor(Color.gray);
	drawCube(g, false);

	drawAxes(g);
	curfunc.finishFrame();

	if (parseError)
	    centerString(g, "Can't parse expression", winSize.height-20);


	realg.drawImage(dbimage, 0, 0, this);
	long t = System.currentTimeMillis();
	frames++;
	if (firsttime == 0)
	    firsttime = t;
	else if (t-firsttime > 1000) {
	    framerate = frames;
	    firsttime = t;
	    frames = 0;
	}
	if (mouseDown)
	    lastXRot = lastYRot = 0;
	else if (lastXRot != 0 || lastYRot != 0) {
	    rotate(lastXRot*timeStep, lastYRot*timeStep);
	    allquiet = false;
	}
	if (!stoppedCheck.getState() && !allquiet)
	    cv.repaint(pause);
    }

    void drawCurrentArrow(Graphics g, int x1, int y1, int x2, int y2) {
	if (reverse == 1)
	    drawArrow(g, null, x1, y1, x2, y2, 7);
	else
	    drawArrow(g, null, x2, y2, x1, y1, 7);
    }

    void drawCurrentLine(Graphics g, int x1, int y1, int x2, int y2, int n,
			 boolean doArrow, int dir) {
	int i;
	if (dir == -1) {
	    int x3 = x1;
	    int y3 = y1;
	    x1 = x2; y1 = y2;
	    x2 = x3; y2 = y3;
	}
	int x0 = x1;
	int y0 = y1;
	n *= 3;
	for (i = 1; i <= n; i++) {
	    int x = (x2-x1)*i/n + x1;
	    int y = (y2-y1)*i/n + y1;
	    g.setColor(Color.yellow);
	    if (i == n && doArrow && reverse == 1)
		drawCurrentArrow(g, x0, y0, x, y);
	    else if (i == 1 && doArrow && reverse == -1)
		drawCurrentArrow(g, x0, y0, x, y);
	    else {
		g.setColor(getCurrentColor(i));
		g.drawLine(x0, y0, x, y);
	    }
	    x0 = x; y0 = y;
	}
    }

    Color getCurrentColor(int i) {
	return (((currentStep/2+400-i) & 4) > 0) ?
	    Color.yellow : Color.darkGray;
    }

    void drawSphere(Graphics g, double r, boolean back) {
	int i;
	int ct = 10;
	for (i = 0; i != ct; i++) {
	    double th1 = pi*2*i/ct;
	    double th2 = pi*2*(i+1)/ct;
	    double sinth1 = r*java.lang.Math.sin(th1);
	    double costh1 = r*java.lang.Math.cos(th1);
	    double sinth2 = r*java.lang.Math.sin(th2);
	    double costh2 = r*java.lang.Math.cos(th2);
	    if (backFacing(costh1, sinth1, 0, costh1, sinth1, 0) == back) {
		map3d(costh1, sinth1, 0, xpoints, ypoints, 0);
		map3d(costh2, sinth2, 0, xpoints, ypoints, 1);
		g.drawLine(xpoints[0], ypoints[0], xpoints[1], ypoints[1]);
	    }
	    if (backFacing(0, costh1, sinth1, 0, costh1, sinth1) == back) {
		map3d(0, costh1, sinth1, xpoints, ypoints, 0);
		map3d(0, costh2, sinth2, xpoints, ypoints, 1);
		g.drawLine(xpoints[0], ypoints[0], xpoints[1], ypoints[1]);
	    }
	    if (backFacing(costh1, 0, sinth1, costh1, 0, sinth1) == back) {
		map3d(costh1, 0, sinth1, xpoints, ypoints, 0);
		map3d(costh2, 0, sinth2, xpoints, ypoints, 1);
		g.drawLine(xpoints[0], ypoints[0], xpoints[1], ypoints[1]);
	    }
	}
    }

    void fillSphere(Graphics g, double r, double xoff) {
	int i, j;
	int ct = 20;
	for (i = 0; i != ct; i++) {
	    double th1 = pi*i/ct;
	    double th2 = pi*(i+1)/ct;
	    double costh1 = r*java.lang.Math.cos(th1);
	    double sinth1 = r*java.lang.Math.sin(th1);
	    double costh2 = r*java.lang.Math.cos(th2);
	    double sinth2 = r*java.lang.Math.sin(th2);
	    double cosph1 = 1, sinph1 = 0;
	    for (j = 0; j != ct; j++) {
		double ph2 = 2*pi*(j+1)/ct;
		double cosph2 = java.lang.Math.cos(ph2);
		double sinph2 = java.lang.Math.sin(ph2);
		double x1 = sinth1*cosph1;
		double y1 = sinth1*sinph1;
		double z1 = costh1;
		double x = cameraPos[0]-(x1+xoff);
		double y = cameraPos[1]-y1;
		double z = cameraPos[2]-z1;
		double d = x*x1+y*y1+z*z1;
		if (d > 0) {
		    int dd = (int) (d/r*40);
		    if (dd > 255)
			dd = 255;
		    g.setColor(new Color(dd, dd, 0));
		    map3d(xoff+x1, y1, z1, xpoints, ypoints, 0);
		    map3d(xoff+sinth1*cosph2, sinth1*sinph2, costh1,
			  xpoints, ypoints, 1);
		    map3d(xoff+sinth2*cosph2, sinth2*sinph2, costh2,
			  xpoints, ypoints, 2);
		    map3d(xoff+sinth2*cosph1, sinth2*sinph1, costh2,
			  xpoints, ypoints, 3);
		    g.fillPolygon(xpoints, ypoints, 4);
		}
		cosph1 = cosph2; sinph1 = sinph2;
	    }
	}
    }

    void drawCylinder(Graphics g, double r, double xoff, boolean back) {
	int i;
	int ct = 10;
	for (i = 0; i != ct; i++) {
	    double th1 = pi*2*i/ct;
	    double th2 = pi*2*(i+1)/ct;
	    double sinth1 = r*java.lang.Math.sin(th1);
	    double costh1 = r*java.lang.Math.cos(th1);
	    double sinth2 = r*java.lang.Math.sin(th2);
	    double costh2 = r*java.lang.Math.cos(th2);
	    if (backFacing(costh1, sinth1, 0, costh1, sinth1, 0) == back) {
		map3d(xoff+costh1, sinth1, -1, xpoints, ypoints, 0);
		map3d(xoff+costh2, sinth2, -1, xpoints, ypoints, 1);
		map3d(xoff+costh2, sinth2, +1, xpoints, ypoints, 2);
		map3d(xoff+costh1, sinth1, +1, xpoints, ypoints, 3);
		g.drawPolygon(xpoints, ypoints, 4);
	    }
	}
    }

    void setFaceColor(Graphics g, double d) {
	int dd = 32+(int) (d*40);
	if (dd > 255)
	    dd = 255;
	g.setColor(new Color(dd, dd, 0));
    }

    void fillCylinder(Graphics g, double r, double xoff) {
	int i;
	int ct = 30;
	int sidepoints[][];
	sidepoints = new int[4][ct];
	for (i = 0; i != ct; i++) {
	    double th1 = pi*2*i/ct;
	    double th2 = pi*2*(i+1)/ct;
	    double sinth1 = r*java.lang.Math.sin(th1);
	    double costh1 = r*java.lang.Math.cos(th1);
	    double sinth2 = r*java.lang.Math.sin(th2);
	    double costh2 = r*java.lang.Math.cos(th2);
	    double x = cameraPos[0]-(xoff+costh1);
	    double y = cameraPos[1]-sinth1;
	    double d = x*costh1+y*sinth1;
	    if (d > 0)
		setFaceColor(g, d/r);
	    map3d(xoff+costh1, sinth1, -1, xpoints, ypoints, 0);
	    map3d(xoff+costh2, sinth2, -1, xpoints, ypoints, 1);
	    map3d(xoff+costh2, sinth2, +1, xpoints, ypoints, 2);
	    map3d(xoff+costh1, sinth1, +1, xpoints, ypoints, 3);
	    sidepoints[0][i] = xpoints[0];
	    sidepoints[1][i] = ypoints[0];
	    sidepoints[2][i] = xpoints[3];
	    sidepoints[3][i] = ypoints[3];
	    if (d > 0)
		g.fillPolygon(xpoints, ypoints, 4);
	}
	if (!backFacing(0, 0, 1, 0, 0, 1)) {
	    setFaceColor(g, cameraPos[2]);
	    g.fillPolygon(sidepoints[2], sidepoints[3], ct);
	} else if (!backFacing(0, 0, -1, 0, 0, -1)) {
	    setFaceColor(g, -cameraPos[2]);
	    g.fillPolygon(sidepoints[0], sidepoints[1], ct);
	}
    }

    void drawAxes(Graphics g) {
	g.setColor(Color.white);
	map3d(0, 0, 0, xpoints, ypoints, 0, viewAxes);
	map3d(1, 0, 0, xpoints, ypoints, 1, viewAxes);
	drawArrow(g, "x", xpoints[0], ypoints[0], xpoints[1], ypoints[1]);
	map3d(0, 1, 0, xpoints, ypoints, 1, viewAxes);
	drawArrow(g, "y", xpoints[0], ypoints[0], xpoints[1], ypoints[1]);
	map3d(0, 0, 1, xpoints, ypoints, 1, viewAxes);
	drawArrow(g, "z", xpoints[0], ypoints[0], xpoints[1], ypoints[1]);
    }

    void drawViewPaper(Graphics g) {
	int i, j;
	int ct = vecDensityBar.getValue();
	ct = 24+(ct*56/64);
	double z = sliceval;
	double pos[] = new double[3];
	double field[] = new double[3];
	int slice = sliceChooser.getSelectedIndex()-SLICE_X;
	if (slice < 0)
	    slice = 0;
	int coord1 = (slice == 0) ? 1 : 0;
	int coord2 = (slice == 2) ? 1 : 2;
	for (i = 0; i != ct; i++) {
	    double x1 = i*2./ct - 1;
	    double x2 = (i+1.)*2/ct - 1;
	    for (j = 0; j != ct; j++) {
		double y1 = j*2./ct - 1;
		double y2 = (j+1.)*2/ct - 1;
		pos[coord1] = x1;
		pos[coord2] = y1;
		pos[slice] = z;
		curfunc.getField(field, pos);


		double prp = field[slice] < 0 ? -field[slice] : field[slice];
		double par = java.lang.Math.sqrt(field[coord1]*field[coord1]+
						 field[coord2]*field[coord2]);
		int dd = (int) ((par/2-prp)*strengthBar.getValue()*20000.+128);
		if (dd < 0)
		    dd = 0;
		if (dd > 255)
		    dd = 255;
		g.setColor(new Color(0, dd, 0));
		map3d(pos[0], pos[1], pos[2], xpoints, ypoints, 0);
		pos[coord1] = x2;
		map3d(pos[0], pos[1], pos[2], xpoints, ypoints, 1);
		pos[coord2] = y2;
		map3d(pos[0], pos[1], pos[2], xpoints, ypoints, 2);
		pos[coord1] = x1;
		map3d(pos[0], pos[1], pos[2], xpoints, ypoints, 3);
		g.fillPolygon(xpoints, ypoints, 4);
	    }
	}
    }

    void drawVectors(Graphics g) {
	int x, y, z;
	DrawData dd = new DrawData();
	dd.mult = strengthBar.getValue() * 80.;
	dd.g = g;
	dd.field = new double[3];
	dd.vv = new double[3];
	vectorSpacing = vecDensityBar.getValue();
	int slice = sliceChooser.getSelectedIndex();
	boolean sliced = (slice > 0);
	double vec[] = new double[3];

	if (vectors == null && sliced)
	    vectors = new FieldVector[vectorSpacing*vectorSpacing];
	vecCount = 0;

	if (!sliced) {
	    vectorSpacing /= 2;
	    if (vectors == null)
		vectors =
		    new FieldVector[vectorSpacing*vectorSpacing*vectorSpacing];
	    for (x = 0; x != vectorSpacing; x++) {
		vec[0] = x*(2.0/(vectorSpacing-1))-1;
		for (y = 0; y != vectorSpacing; y++) {
		    vec[1] = y*(2.0/(vectorSpacing-1))-1;
		    for (z = 0; z != vectorSpacing; z++) {
			vec[2] = z*(2.0/(vectorSpacing-1))-1;
			drawVector(dd, vec);
		    }
		}
	    }
	} else {
	    int coord1 = (slice == SLICE_X) ? 1 : 0;
	    int coord2 = (slice == SLICE_Z) ? 1 : 2;
	    int slicecoord = slice-SLICE_X;
	    vec[slicecoord] = sliceval;
	    for (x = 0; x != vectorSpacing; x++) {
		vec[coord1] = x*(2.0/(vectorSpacing-1))-1;
		for (y = 0; y != vectorSpacing; y++) {
		    vec[coord2] = y*(2.0/(vectorSpacing-1))-1;
		    drawVector(dd, vec);
		}
	    }
	}
	curfunc.render(g);
    }

    void genLines() {
	if (vectors != null)
	    return;
	partMult = fieldStrength = 10;
	int i;
	vecCount = 0;

	int lineGridSize = lineDensityBar.getValue();
	if (lineGridSize < 3)
	    lineGridSize = 3;
	if (lineGridSize > 16)
	    lineGridSize = 16;
	int slice = sliceChooser.getSelectedIndex();
	boolean sliced = (slice > 0);
	if (sliced)
	    lineGridSize *= 2;
	int ct = (sliced) ? 30*lineGridSize*lineGridSize :
	    30*lineGridSize*lineGridSize*lineGridSize;
	vectors = new FieldVector[ct];
	double brightmult = 160*strengthBar.getValue();

	boolean lineGrid[][][] =
	    new boolean[lineGridSize][lineGridSize][lineGridSize];
	double lineGridMult = lineGridSize/2.;
	if (sliced) {
	    int j, k;
	    int gp = (int) ((sliceval+1)*lineGridMult);
	    for (i = 0; i != lineGridSize; i++)
		for (j = 0; j != lineGridSize; j++)
		    for (k = 0; k != lineGridSize; k++) {
			switch (slice) {
			case SLICE_X: lineGrid[i][j][k] = i!=gp; break;
			case SLICE_Y: lineGrid[i][j][k] = j!=gp; break;
			case SLICE_Z: lineGrid[i][j][k] = k!=gp; break;
			}
		    }
	}

	double origp[] = new double[3];
	double field[] = new double[3];
	Particle p = new Particle();
	p.lifetime = -1;
	p.stepsize = 10;
	int dir = -1;
	int segs = 0;
	double lastdist = 0;
	for (i = 0; i != ct; i++) {
	    if (p.lifetime < 0) {
		p.lifetime = 1;
		p.stepsize = 10;
		segs = 0;
		lastdist = 0;
		if (dir == 1) {
		    int j;
		    for (j = 0; j != 3; j++)
			p.pos[j] = origp[j];
		    dir = -1;
		    continue;
		}
		dir = 1;
		int px = 0, py = 0, pz = 0;
		while (true) {
		    if (!lineGrid[px][py][pz])
			break;
		    if (++px < lineGridSize)
			continue;
		    px = 0;
		    if (++py < lineGridSize)
			continue;
		    py = 0;
		    if (++pz < lineGridSize)
			continue;
		    break;
		}
		if (pz == lineGridSize)
		    break;
		lineGrid[px][py][pz] = true;
		double offs = .5/lineGridMult;
		origp[0] = p.pos[0] = px/lineGridMult-1+offs;
		origp[1] = p.pos[1] = py/lineGridMult-1+offs;
		origp[2] = p.pos[2] = pz/lineGridMult-1+offs;
		if (sliced)
		    origp[slice-SLICE_X] = p.pos[slice-SLICE_X] = sliceval;
	    }

	    FieldVector fv = vectors[vecCount];
	    if (fv == null) {
		fv = vectors[vecCount] = new FieldVector();
		fv.p1 = new double[3];
		fv.p2 = new double[3];
	    }
	    vecCount++;
	    fv.p1[0] = p.pos[0]; fv.p1[1] = p.pos[1]; fv.p1[2] = p.pos[2];
	    double x[] = p.pos;
	    lineSegment(p, dir);

	    if (p.lifetime < 0) {
		vecCount--;
		continue;
	    }
	    int gx = (int) ((x[0]+1)*lineGridMult);
	    int gy = (int) ((x[1]+1)*lineGridMult);
	    int gz = (int) ((x[2]+1)*lineGridMult);
	    if (!lineGrid[gx][gy][gz])
		segs--;
	    lineGrid[gx][gy][gz] = true;
	    fv.p2[0] = p.pos[0]; fv.p2[1] = p.pos[1]; fv.p2[2] = p.pos[2];

	    double dn = brightmult*p.phi;
	    if (dn > 2)
		dn = 2;
	    fv.col = (int) (dn*255);

	    double d2 = dist2(origp, x);
	    if (d2 > lastdist)
		lastdist = d2;
	    else
		segs++;
	    if (segs > 10 || d2 < .001)
		p.lifetime = -1;
	}

    }

    void drawLines(Graphics g) {
	int i;
	for (i = 0; i != vecCount; i++) {
	    FieldVector fv = vectors[i];
	    double x[] = fv.p1;
	    map3d(x[0], x[1], x[2], xpoints, ypoints, 0);
	    int vp1 = curfunc.getViewPri(cameraPos, x);
	    x = fv.p2;
	    map3d(x[0], x[1], x[2], xpoints, ypoints, 1);

	    fv.sx1 = xpoints[0];
	    fv.sy1 = ypoints[0];
	    fv.sx2 = xpoints[1];
	    fv.sy2 = ypoints[1];
	    int vp2 = curfunc.getViewPri(cameraPos, x);
	    fv.viewPri = (vp1 > vp2) ? vp1 : vp2;
	}
	curfunc.render(g);
    }
//line 1455 "origbase.java"
    void drawVector(DrawData dd, double vec[]) {
	double field[] = dd.field;


	curfunc.getField(field, vec);
	double dn = java.lang.Math.sqrt(field[0]*field[0]+field[1]*field[1]+
					field[2]*field[2]);
	double dnr = dn*reverse;
	if (dn > 0) {
	    field[0] /= dnr;
	    field[1] /= dnr;
	    field[2] /= dnr;
	}
	dn *= dd.mult;
	if (dn > 2)
	    dn = 2;
	int col = (int) (dn*255);
	double sw2 = 1./(vectorSpacing-1);
	map3d(vec[0], vec[1], vec[2], xpoints, ypoints, 0);
	double vv[] = dd.vv;
	vv[0] = vec[0] + sw2*field[0];
	vv[1] = vec[1] + sw2*field[1];
	vv[2] = vec[2] + sw2*field[2];
	map3d(vv[0], vv[1], vv[2], xpoints, ypoints, 1);
	FieldVector fv = vectors[vecCount];
	if (fv == null)
	    fv = vectors[vecCount] = new FieldVector();
	fv.sx1 = xpoints[0];
	fv.sy1 = ypoints[0];
	fv.sx2 = xpoints[1];
	fv.sy2 = ypoints[1];
	fv.col = col;
	vecCount++;
	int vp1 = curfunc.getViewPri(cameraPos, vec);
	if (!curfunc.noSplitFieldVectors())
	    fv.viewPri = vp1;
	else {
	    int vp2 = curfunc.getViewPri(cameraPos, vv);
	    fv.viewPri = (vp1 == vp2) ? vp1 : -1;
	}
    }

    void drawParticles(Graphics g) {
	int i;
	int pcount = getParticleCount();
	for (i = 0; i < pcount; i++) {
	    Particle pt = particles[i];
	    pt.viewPri = curfunc.getViewPri(cameraPos, pt.pos);
	}
	curfunc.render(g);
    }

    void moveParticles() {
	fieldStrength = strengthBar.getValue();
	int bestd = 0;
	int i;
	int pcount = getParticleCount();
	int slice = sliceChooser.getSelectedIndex();
	boolean sliced = (slice > 0);
	partMult = fieldStrength * reverse * timeStep;
	for (i = 0; i != pcount; i++) {
	    Particle pt = particles[i];
	    removeFromDensityGroup(pt);
	    moveParticle(pt);
	    double x[] = pt.pos;
	    if (!(x[0] >= -1 && x[0] < 1 &&
		  x[1] >= -1 && x[1] < 1 &&
		  x[2] >= -1 && x[2] < 1) ||
		(pt.lifetime -= timeStep) < 0) {
		positionParticle(pt);
	    }
	    if (sliced)
		x[slice-SLICE_X] = sliceval;
	    int d = addToDensityGroup(pt);
	    if (d > bestd)
		bestd = d;
	}
	boolean withforce =
	    (dispChooser.getSelectedIndex() == DISP_PART_FORCE);
	int maxd = (10*getParticleCount()/(densitygridsize*densitygridsize*
					    densitygridsize));
	if (sliced)
	    maxd = 4*getParticleCount()/(densitygridsize*densitygridsize);
	if (!withforce && curfunc.redistribute() && bestd > maxd)
	    redistribute(bestd);
    }

    static int frames = 0;
    static int framerate = 0;
    static long firsttime = 0;




    void drawCube(Graphics g, boolean drawAll) {
	int i;
	int slice = sliceChooser.getSelectedIndex();
	int sp = (drawAll) ? 0 : 8;
	for (i = 0; i != 6; i++) {

	    int nx = (i == 0) ? -1 : (i == 1) ? 1 : 0;
	    int ny = (i == 2) ? -1 : (i == 3) ? 1 : 0;
	    int nz = (i == 4) ? -1 : (i == 5) ? 1 : 0;

	    if (!drawAll && backFacing(nx, ny, nz, nx, ny, nz))
		continue;
	    double pts[];
	    pts = new double[3];
	    int n;
	    for (n = 0; n != 4; n++) {
		computeFace(i, n, pts);
		map3d(pts[0], pts[1], pts[2], xpoints, ypoints, n);
	    }
	    g.setColor(Color.gray);
	    g.drawPolygon(xpoints, ypoints, 4);
	    if (slice != SLICE_NONE && i/2 != slice-SLICE_X) {
		if (selectedSlice)
		    g.setColor(Color.yellow);
		int coord1 = (slice == SLICE_X) ? 1 : 0;
		int coord2 = (slice == SLICE_Z) ? 1 : 2;
		computeFace(i, 0, pts);
		pts[slice-SLICE_X] = sliceval;
		map3d(pts[0], pts[1], pts[2],
		      slicerPoints[0], slicerPoints[1], sp);
		computeFace(i, 2, pts);
		pts[slice-SLICE_X] = sliceval;
		map3d(pts[0], pts[1], pts[2],
		      slicerPoints[0], slicerPoints[1], sp+1);
		g.drawLine(slicerPoints[0][sp ], slicerPoints[1][sp],
			   slicerPoints[0][sp+1], slicerPoints[1][sp+1]);
		if (drawAll) {






		    sliceFaces[sp/2][0] = nx;
		    sliceFaces[sp/2][1] = ny;
		    sliceFaces[sp/2][2] = nz;
		    sp += 2;
		}
	    }
	}
    }


    void computeFace(int b, int n, double pts[]) {


	int a = b >> 1;
	pts[a] = ((b & 1) == 0) ? -1 : 1;



	int i;
	for (i = 0; i != 3; i++) {
	    if (i == a) continue;
	    pts[i] = (((n>>1)^(n&1)) == 0) ? -1 : 1;
	    n >>= 1;
	}
    }

    void renderItems(Graphics g, int pri) {
	g.setColor(Color.white);
	int disp = dispChooser.getSelectedIndex();
	if (disp == DISP_VECTORS || disp == DISP_VECTORS_A) {
	    int i;
	    for (i = 0; i != vecCount; i++) {
		FieldVector fv = vectors[i];
		if (fv.viewPri != pri)
		    continue;
		g.setColor(fieldColors[fv.col]);
		drawArrow(g, null, fv.sx1, fv.sy1, fv.sx2, fv.sy2, 2);
	    }
	    return;
	}
	if (disp == DISP_LINES || disp == DISP_EQUIPS) {
	    int i;
	    g.setColor(Color.white);
	    Color colvec[] = (disp == DISP_EQUIPS) ? equipColors : fieldColors;
	    for (i = 0; i != vecCount; i++) {
		FieldVector fv = vectors[i];
		if (fv.viewPri != pri)
		    continue;
		if (fv.sx1 == fv.sx2 && fv.sy1 == fv.sy2)
		    continue;
		g.setColor(colvec[fv.col]);
		g.drawLine(fv.sx1, fv.sy1, fv.sx2, fv.sy2);
	    }
	    return;
	}
	int pcount = getParticleCount();
	int i;
	wooft += .3;
	for (i = 0; i < pcount; i++) {
	    Particle p = particles[i];
	    if (p.viewPri != pri)
		continue;
	    double pos[] = p.pos;
	    map3d(pos[0], pos[1], pos[2], xpoints, ypoints, 0);
	    if (xpoints[0] < 0 || xpoints[0] >= winSize.width ||
		ypoints[0] < 0 || ypoints[0] >= winSize.height)
		continue;
	    if (disp == DISP_PART_MAG) {
		double cosph = java.lang.Math.cos(p.phi);
		double sinph = java.lang.Math.sin(p.phi);
		double costh = java.lang.Math.cos(p.theta);
		double sinth = java.lang.Math.sin(p.theta);
		double al = .08;
		double rhatx = sinth*cosph*al;
		double rhaty = sinth*sinph*al;
		double rhatz = costh*al;
		map3d(pos[0]+rhatx, pos[1]+rhaty, pos[2]+rhatz,
		      xpoints, ypoints, 1);
		drawArrow(g, null, xpoints[0], ypoints[0],
			  xpoints[1], ypoints[1], 2);
	    } else
		g.fillRect(xpoints[0], ypoints[0]-1, 2, 2);
	}
    }

	double wooft = 0;

    void drawPlane(Graphics g, double sizex, double sizey, double z) {
	g.setColor(darkYellow);
	map3d(-sizex, -sizey, z, xpoints, ypoints, 0);
	map3d(+sizex, -sizey, z, xpoints, ypoints, 1);
	map3d(+sizex, +sizey, z, xpoints, ypoints, 2);
	map3d(-sizex, +sizey, z, xpoints, ypoints, 3);
	g.fillPolygon(xpoints, ypoints, 4);
    }

    void drawArrow(Graphics g, String text, int x1, int y1, int x2, int y2) {
	drawArrow(g, text, x1, y1, x2, y2, 5);
    }

    void drawArrow(Graphics g, String text,
		   int x1, int y1, int x2, int y2, int as) {
	g.drawLine(x1, y1, x2, y2);
	double l = java.lang.Math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1));
	if (l > as/2) {
	    double hatx = (x2-x1)/l;
	    double haty = (y2-y1)/l;
	    g.drawLine(x2, y2,
		       (int) (haty*as-hatx*as+x2),
		       (int) (-hatx*as-haty*as+y2));
	    g.drawLine(x2, y2,
		       (int) (-haty*as-hatx*as+x2),
		       (int) (hatx*as-haty*as+y2));
	    if (text != null)
		g.drawString(text, (int) (x2+hatx*10), (int) (y2+haty*10));
	}
    }

    boolean backFacing(double px, double py, double pz,
		       double nx, double ny, double nz) {
	double x = cameraPos[0]-px;
	double y = cameraPos[1]-py;
	double z = cameraPos[2]-pz;
	double d = x*nx+y*ny+z*nz;
	return d <= 0;
    }

    int intersectSphere(double cp[], double ptx, double pty, double ptz,
			double r) {
	return intersectSphere(cp, ptx, pty, ptz, 0, 0, 0, r);
    }






    int intersectSphere(double cp[], double ptx, double pty, double ptz,
			double sx, double sy, double sz, double r) {
	double vx = ptx-cp[0];
	double vy = pty-cp[1];
	double vz = ptz-cp[2];
	double qpx = cp[0]-sx;
	double qpy = cp[1]-sy;
	double qpz = cp[2]-sz;
	double a = vx*vx+vy*vy+vz*vz;
	double b = 2*(vx*qpx + vy*qpy + vz*qpz);
	double c = qpx*qpx + qpy*qpy + qpz*qpz - r*r;
	double discrim = b*b-4*a*c;
	if (discrim < 0)
	    return 0;
	discrim = java.lang.Math.sqrt(discrim);
	double b1 = (-b-discrim)/(2*a);
	double b2 = (-b+discrim)/(2*a);
	if (b1 < 1 && inViewBox(b1, cp, vx, vy, vz))
	    return (b2 < 1) ? 2 : 1;
	else
	    return 0;
    }




    double intersectZPlane(double cp[], double a,
			   double ptx, double pty, double ptz) {
	double vx = ptx-cp[0];
	double vy = pty-cp[1];
	double vz = ptz-cp[2];
	double t = intersectionDistance = -(cp[2]+a)/vz;
	if (t > 1)
	    return 0;
	if (!inViewBox(t, cp, vx, vy, vz))
	    return 0;
	return 2;
    }


    boolean inViewBox(double t, double cp[], double vx, double vy, double vz) {
	if (t < 0)
	    return false;
	double ix = intersection[0] = cp[0]+vx*t;
	double iy = intersection[1] = cp[1]+vy*t;
	double iz = intersection[2] = cp[2]+vz*t;

	if (ix < -1 || ix > 1 || iy < -1 || iy > 1 ||
	    iz < -1 || iz > 1)
	    return false;
	return true;
    }

    int intersectCylinder(double cp[], double ptx, double pty, double ptz,
			  double r, boolean vbTest) {
	return intersectCylinder(cp, ptx, pty, ptz, 0, 0, r, vbTest);
    }






    int intersectCylinder(double cp[], double ptx, double pty, double ptz,
			  double sx, double sy, double r, boolean vbTest) {
	double vx = ptx-cp[0];
	double vy = pty-cp[1];
	double qpx = cp[0]-sx;
	double qpy = cp[1]-sy;
	double a = vx*vx+vy*vy;
	double b = 2*(vx*qpx + vy*qpy);
	double c = qpx*qpx + qpy*qpy - r*r;
	double discrim = b*b-4*a*c;
	if (discrim < 0)
	    return 0;
	discrim = java.lang.Math.sqrt(discrim);
	double b1 = (-b-discrim)/(2*a);
	double b2 = (-b+discrim)/(2*a);



	if (b1 > 1)
	    return 0;


	if (!vbTest || inViewBox(b1, cp, vx, vy, ptz-cp[2]))


	    return (b2 < 1) ? 2 : 1;



	if (b2 > 1)
	    return 2;



	if (inViewBox(b2, cp, vx, vy, ptz-cp[2]))
	    return 2;


	return 0;
    }

    int rediscount;
    void redistribute(int mostd) {
	if (mostd < 5)
	    return;
	rediscount++;
	int maxd = (10*getParticleCount()/
		    (densitygridsize*densitygridsize*densitygridsize));
	int i;
	int pn = 0;
	int pcount = getParticleCount();
	for (i = rediscount % 4; i < pcount; i+=4) {
	    Particle p = particles[i];
	    int a = (int)((p.pos[0]+1)*(densitygridsize/2));
	    int b = (int)((p.pos[1]+1)*(densitygridsize/2));
	    int c = (int)((p.pos[2]+1)*(densitygridsize/2));
	    if (density[a][b][c] <= maxd)
		continue;
	    p.lifetime = -1;
	    pn++;
	}

    }

    double distance(Particle p) {
	return distance(p.pos[0], p.pos[1], p.pos[2]);
    }

    double distance(double y[]) {
	return distance(y[0], y[1], y[2]);
    }

    double distance(double x, double y, double z) {
	return java.lang.Math.sqrt(x*x+y*y+z*z+.000000001);
    }

    double distance(double x, double y) {
	return java.lang.Math.sqrt(x*x+y*y+.000000001);
    }

    void rotateParticleAdd(double result[], double y[], double mult,
			double cx, double cy) {
	result[0] += -mult*(y[1]-cy);
	result[1] += mult*(y[0]-cx);
	result[2] += 0;
    }

    void rotateParticle(double result[], double y[], double mult) {
	result[0] = -mult*y[1];
	result[1] = mult*y[0];
	result[2] = 0;
    }

    public void componentHidden(ComponentEvent e){}
    public void componentMoved(ComponentEvent e){}
    public void componentShown(ComponentEvent e) {
	cv.repaint(pause);
    }

    public void componentResized(ComponentEvent e) {
	handleResize();
	cv.repaint(pause);
    }
    public void actionPerformed(ActionEvent e) {
	vectors = null;
	if (e.getSource() == resetButton)
	    resetParticles();
	if (e.getSource() == kickButton)
	    kickParticles();
	if (e.getSource() == infoButton) {
	    String s = curfunc.getClass().getName();
	    try {
		s = s.substring(s.lastIndexOf('.')+1);
		applet.getAppletContext().showDocument(
			new URL(applet.getCodeBase(),
				"functions.html" + '#' + s),
			"functionHelp");
	    } catch (Exception ex) {
	    }
	}
	curfunc.actionPerformed();
    }

    public boolean handleEvent(Event ev) {
	if (ev.id == Event.WINDOW_DESTROY) {
	    applet.destroyFrame();
	    return true;
	}
	return super.handleEvent(ev);
    }

    public void adjustmentValueChanged(AdjustmentEvent e) {
	vectors = null;
	System.out.print(((Scrollbar) e.getSource()).getValue() + "\n");
	if (e.getSource() == partCountBar)
	    resetDensityGroups();
	cv.repaint(pause);
    }

    public void mouseDragged(MouseEvent e) {
	dragging = true;
	oldDragX = dragX;
	oldDragY = dragY;
	dragX = e.getX(); dragY = e.getY();
	int mode = modeChooser.getSelectedIndex();
	if (selectedSlice)
	    mode = MODE_SLICE;
	if (mode == MODE_ANGLE) {
	    int xo = oldDragX-dragX;
	    int yo = oldDragY-dragY;
	    rotate(lastXRot = xo/40., lastYRot = -yo/40.);
	    double lr = Math.sqrt(lastXRot*lastXRot + lastYRot*lastYRot);
	    if (lr > .06) {
		lr /= .06;
		lastXRot /= lr;
		lastYRot /= lr;
	    }
	    cv.repaint(pause);
	} else if (mode == MODE_ZOOM) {
	    int xo = dragX-dragStartX;
	    zoom = dragZoomStart + xo/20.;
	    if (zoom < .1)
		zoom = .1;
	    cv.repaint(pause);
	} else if (mode == MODE_SLICE) {
	    double x3[] = new double[3];
	    unmap3d(x3, dragX, dragY, sliceFace, sliceFace, viewMain);
	    switch (sliceChooser.getSelectedIndex()) {
	    case SLICE_X: sliceval = x3[0]; break;
	    case SLICE_Y: sliceval = x3[1]; break;
	    case SLICE_Z: sliceval = x3[2]; break;
	    }



	    if (sliceval < -.99)
		sliceval = -.99;
	    if (sliceval > .99)
		sliceval = .99;
	    resetDensityGroups();

	    cv.repaint(pause);
	    vectors = null;
	}

    }

    boolean csInRange(int x, int xa, int xb) {
	if (xa < xb)
	    return x >= xa-5 && x <= xb+5;
	return x >= xb-5 && x <= xa+5;
    }

    void checkSlice(int x, int y) {
	if (sliceChooser.getSelectedIndex() == SLICE_NONE) {
	    selectedSlice = false;
	    return;
	}
	int n;
	selectedSlice = false;
	for (n = 0; n != 8; n += 2) {
	    int xa = slicerPoints[0][n];
	    int xb = slicerPoints[0][n+1];
	    int ya = slicerPoints[1][n];
	    int yb = slicerPoints[1][n+1];
	    if (!csInRange(x, xa, xb) || !csInRange(y, ya, yb))
		continue;

	    double d;
	    if (xa == xb)
		d = java.lang.Math.abs(x-xa);
	    else {

		double b = (yb-ya)/(double) (xb-xa);
		double a = ya-b*xa;


		double d1 = y-(a+b*x);
		if (d1 < 0)
		    d1 = -d1;
		d = d1/java.lang.Math.sqrt(1+b*b);
	    }
	    if (d < 6) {
		selectedSlice = true;
		sliceFace = sliceFaces[n/2];
		break;
	    }
	}
    }

    public void mouseMoved(MouseEvent e) {
	dragX = e.getX(); dragY = e.getY();
	dragStartX = dragX;
	dragStartY = dragY;
	dragZoomStart = zoom;
	boolean ss = selectedSlice;
	checkSlice(dragX, dragY);
	if (ss != selectedSlice)
	    cv.repaint(pause);
    }
    public void mouseClicked(MouseEvent e) {
    }
    public void mouseEntered(MouseEvent e) {
    }
    public void mouseExited(MouseEvent e) {
    }
    public void mousePressed(MouseEvent e) {
	mouseDown = true;
    }
    public void mouseReleased(MouseEvent e) {
	mouseDown = false;
    }

    void dispChooserChanged() {
	int disp = dispChooser.getSelectedIndex();
	showA = (disp == DISP_PART_VELOC_A || disp == DISP_VECTORS_A);
	getPot = (disp == DISP_EQUIPS);
	if (disp == DISP_PART_FORCE)
	    kickButton.enable();
	else
	    kickButton.disable();
	potentialLabel.hide();
	potentialBar.hide();
	vecDensityLabel.hide();
	vecDensityBar.hide();
	lineDensityLabel.hide();
	lineDensityBar.hide();
	partCountLabel.hide();
	partCountBar.hide();
	strengthLabel.show();
	strengthBar.show();
	if (disp == DISP_VECTORS || disp == DISP_VECTORS_A ||
	    disp == DISP_VIEW_PAPER) {
	    vecDensityLabel.show();
	    vecDensityBar.show();
	} else if (disp == DISP_LINES) {
	    lineDensityLabel.show();
	    lineDensityBar.show();
	} else if (disp == DISP_EQUIPS) {
	    potentialLabel.show();
	    potentialBar.show();
	} else {
	    partCountLabel.show();
	    partCountBar.show();
	}
	vecDensityLabel.setText(disp == DISP_VIEW_PAPER ?
				"Resolución" : "Densidad de Vectores");
	if (disp == DISP_EQUIPS) {
	    strengthLabel.hide();
	    strengthBar.hide();
	}
	if ((disp == DISP_VIEW_PAPER || disp == DISP_EQUIPS) &&
	      sliceChooser.getSelectedIndex() == SLICE_NONE) {
	    sliceChooser.select(curfunc.getBestSlice());
	    potentialBar.disable();
	}
	validate();
	resetParticles();
    }

    public void itemStateChanged(ItemEvent e) {
	vectors = null;
	cv.repaint(pause);
	reverse = (reverseCheck.getState()) ? -1 : 1;
	if (e.getItemSelectable() == dispChooser) {
	    dispChooserChanged();
	    resetParticles();
	}
	if (e.getItemSelectable() == sliceChooser) {
	    resetParticles();
	    if (modeChooser.getSelectedIndex() == MODE_SLICE)
		modeChooser.select(MODE_ANGLE);
	    if (sliceChooser.getSelectedIndex() == SLICE_NONE)
		potentialBar.enable();
	    else
		potentialBar.disable();
	}
	if (e.getStateChange() != ItemEvent.SELECTED)
	    return;
	if (e.getItemSelectable() == functionChooser)
	    functionChanged();
    }

    void functionChanged() {
	reverse = 1;
	reverseCheck.setState(false);
	parseError = false;
	curfunc = (VecFunction)
	    functionList.elementAt(functionChooser.getSelectedIndex());
	int i;
	for (i = 0; i != 3; i++) {
	    auxBars[i].label.hide();
	    auxBars[i].bar.hide();
	    textFields[i].hide();
	    if (textFieldLabel != null)
		textFieldLabel.hide();
	}
	strengthBar.setValue(20);
	int x = dispChooser.getSelectedIndex();
	setupDispChooser(!curfunc.nonGradient());
	try {
	    dispChooser.select(x);
	} catch (Exception e) { }
	curfunc.setup();
	sliceChooser.select(SLICE_NONE);
	validate();
	resetParticles();
	dispChooserChanged();
    }

    void setupDispChooser(boolean potential) {
	dispChooser.removeAll();
	dispChooser.add("Ver : Partículas (Vel.)");
	

	dispChooser.add("Ver : Parts (Pot.Vector A , Vel.)");
	dispChooser.add("Ver : Vectores Campo");
	dispChooser.add("Ver : Vectores Campo (A)");
//line 2156 "origbase.java"
	dispChooser.add("Ver : Líneas de Campo");


	dispChooser.add("Ver : Parts (Magnéticas)");
	dispChooser.add("Ver : Película Magnética");
//line 2166 "origbase.java"
    }

    void setupBar(int n, String text, int val) {
	auxBars[n].label.setText(text);
	auxBars[n].label.show();
	auxBars[n].bar.setValue(val);
	auxBars[n].bar.show();
    }

    boolean useMagnetMove() {
	int disp = dispChooser.getSelectedIndex();
	return (disp == DISP_PART_MAG);
    }


    MagnetState mstates[];

    void magneticMoveParticle(Particle p) {
	int i;
	if (mstates == null) {
	    mstates = new MagnetState[3];
	    for (i = 0; i != 3; i++)
		mstates[i] = new MagnetState();
	}
	MagnetState ms = mstates[0];
	MagnetState mshalf = mstates[1];
	MagnetState oldms = mstates[2];
	for (i = 0; i != 3; i++) {
	    ms.pos[i] = p.pos[i];
	    ms.vel[i] = p.vel[i];
	    ms.theta = p.theta;
	    ms.thetav = p.thetav;
	    ms.phi = p.phi;
	    ms.phiv = p.phiv;
	}
	mshalf.copy(ms);
	oldms.copy(ms);

	double h = 1;
	final double minh = .01;
	final double maxh = 1;
	final double E = .1;
	int steps = 0;
	boolean adapt = curfunc.useAdaptiveRungeKutta() &&
	    curfunc.useRungeKutta();
	boundCheck = false;

	double t = 0;
	while (t < 1) {

	    magnetMove(ms, h);
	    if (boundCheck) {
		p.pos[0] = -100;
		return;
	    }
	    if (curfunc.checkBounds(ms.pos, oldms.pos)) {
		p.pos[0] = -100;
		return;
	    }

	    if (!adapt)
		break;


	    magnetMove(mshalf, h*.5);
	    magnetMove(mshalf, h*.5);


	    double localError =
		java.lang.Math.abs(ms.pos[0] - mshalf.pos[0]) +
		java.lang.Math.abs(ms.pos[1] - mshalf.pos[1]) +
		java.lang.Math.abs(ms.pos[2] - mshalf.pos[2]) +
		java.lang.Math.abs(ms.theta - mshalf.theta) +
		java.lang.Math.abs(ms.phi - mshalf.phi);

	    if (localError > E && h > minh) {
		h *= 0.75;
		if (h < minh)
		    h = minh;
		ms.copy(oldms);
		continue;
	    } else if (localError < (E * 0.5)) {
		h *= 1.25;
		if (h > maxh)
		    h = maxh;
	    }

	    mshalf.copy(ms);
	    t += h;
	    steps++;
	}
//line 2260 "origbase.java"
	for (i = 0; i != 3; i++) {
	    p.pos[i] = ms.pos[i];
	    p.vel[i] = ms.vel[i];
	    p.theta = ms.theta;
	    p.thetav = ms.thetav;
	    p.phi = ms.phi;
	    p.phiv = ms.phiv;
	}
    }

    void magnetMove(MagnetState ms, double stepsize) {
	double cosph = java.lang.Math.cos(ms.phi);
	double sinph = java.lang.Math.sin(ms.phi);
	double costh = java.lang.Math.cos(ms.theta);
	double sinth = java.lang.Math.sin(ms.theta);









	double thhat[] = new double[3];
	double phhat[] = new double[3];
	double thhatn[] = new double[3];
	double phhatn[] = new double[3];
	double force[] = new double[3];
	double torque[] = new double[3];
	thhat[0] = costh*cosph; thhat[1] = costh*sinph; thhat[2] = -sinth;
	phhat[0] = -sinph; phhat[1] = cosph; phhat[2] = 0;
	int i;
	for (i = 0; i != 3; i++) {
	    thhatn[i] = -thhat[i];
	    phhatn[i] = -phhat[i];
	    force[i] = torque[i] = 0;
	}
	getMagForce(ms.pos, thhat, phhat, force, torque);
	getMagForce(ms.pos, phhat, thhatn, force, torque);
	getMagForce(ms.pos, thhatn, phhatn, force, torque);
	getMagForce(ms.pos, phhatn, thhat, force, torque);
	for (i = 0; i != 3; i++) {
	    ms.vel[i] += force[i]*stepsize;
	    ms.pos[i] += ms.vel[i]*stepsize;
	}

	ms.thetav += dot(torque, phhat)*1000*stepsize;

	ms.phiv += torque[2]*1000*stepsize;


	ms.thetav *= java.lang.Math.exp(-.2*stepsize);
	ms.phiv *= java.lang.Math.exp(-.2*stepsize);

	ms.theta += ms.thetav*stepsize;
	ms.phi += ms.phiv*stepsize;
    }

    void getMagForce(double pos[], double off[], double j[], double f[],
		     double torque[]) {
	int i;
	double offs[] = new double[3];
	for (i = 0; i != 3; i++) {
	    offs[i] = off[i] * .02;
	    rk_yn[i] = pos[i] + offs[i];
	}
	curfunc.getField(rk_k1, rk_yn);
	double fmult = reverse * strengthBar.getValue();
	for (i = 0; i != 3; i++)
	    rk_k1[i] *= fmult;
	double newf[] = new double[3];
	double newtorque[] = new double[3];
	cross(newf, j, rk_k1);
	cross(newtorque, offs, newf);
	for (i = 0; i != 3; i++) {
	    f[i] += newf[i];
	    torque[i] += newtorque[i];
	}
    }

    class MagnetState {
	MagnetState() { pos = new double[3]; vel = new double[3]; }
	double pos[], vel[], theta, phi, thetav, phiv;
	void copy(MagnetState ms) {
	    int i;
	    for (i = 0; i != 3; i++) {
		pos[i] = ms.pos[i];
		vel[i] = ms.vel[i];
		theta = ms.theta;
		thetav = ms.thetav;
		phi = ms.phi;
		phiv = ms.phiv;
	    }
	}
    };


    void cross(double res[], double v1[], double v2[]) {
	res[0] = v1[1]*v2[2] - v1[2]*v2[1];
	res[1] = v1[2]*v2[0] - v1[0]*v2[2];
	res[2] = v1[0]*v2[1] - v1[1]*v2[0];
    }

    double dot(double v1[], double v2[]) {
	return v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2];
    }

    boolean boundCheck;
    double oldY[];
    double rk_k1[] = new double[6];
    double rk_k2[] = new double[6];
    double rk_k3[] = new double[6];
    double rk_k4[] = new double[6];
    double rk_yn[] = new double[6];

    void rk(int order, double x, double Y[], double stepsize) {
	int i;



	if (order == 3) {

	    double fmult = stepsize * partMult;
	    for (i = 0; i != order; i++)
		rk_yn[i] = Y[i];
	    curfunc.getField(rk_k1, rk_yn);
	    for (i = 0; i != order; i++)
		rk_yn[i] = (Y[i] + 0.5*fmult*rk_k1[i]);
	    curfunc.getField(rk_k2, rk_yn);
	    for (i = 0; i != order; i++)
		rk_yn[i] = (Y[i] + 0.5*fmult*rk_k2[i]);
	    curfunc.getField(rk_k3, rk_yn);

	    for (i = 0; i != order; i++)
		rk_yn[i] = (Y[i] + fmult*rk_k3[i]);
	    curfunc.getField(rk_k4, rk_yn);
	    for (i = 0; i != order; i++)
		Y[i] = Y[i] + fmult*(rk_k1[i]+2*(rk_k2[i]+rk_k3[i])+rk_k4[i])/6;
	} else {


	    double fmult = stepsize * partMult;
	    for (i = 0; i != order; i++)
		rk_yn[i] = Y[i];
	    getForceField(rk_k1, rk_yn, stepsize, fmult);
	    for (i = 0; i != order; i++)
		rk_yn[i] = (Y[i] + 0.5*rk_k1[i]);
	    getForceField(rk_k2, rk_yn, stepsize, fmult);
	    for (i = 0; i != order; i++)
		rk_yn[i] = (Y[i] + 0.5*rk_k2[i]);
	    getForceField(rk_k3, rk_yn, stepsize, fmult);

	    for (i = 0; i != order; i++)
		rk_yn[i] = (Y[i] + rk_k3[i]);
	    getForceField(rk_k4, rk_yn, stepsize, fmult);
	    for (i = 0; i != order; i++)
		Y[i] = Y[i] + (rk_k1[i]+2*(rk_k2[i]+rk_k3[i])+rk_k4[i])/6;
	}
    }

    void getForceField(double result[], double y[],
		       double stepsize, double fmult) {

	curfunc.getField(result, y);







	int i;
	for (i = 0; i != 3; i++)
	    result[i+3] = .1*fmult*result[i];



	for (i = 0; i != 3; i++)
	    result[i] = stepsize*timeStep*rk_yn[i+3];
    }

    double rk_Y[] = new double[6];
    double rk_Yhalf[] = new double[6];
    double rk_oldY[] = new double[6];
    double ls_fieldavg[] = new double[3];

    void moveParticle(Particle p)
    {
	int disp = dispChooser.getSelectedIndex();

	if (disp == DISP_PART_MAG) {
	    magneticMoveParticle(p);
	    return;
	}


	int numIter=0;
	double maxh=1;
	double error=0.0, E = .001, localError;
	boolean useForce = (disp == DISP_PART_FORCE);
	int order = useForce ? 6 : 3;
	double Y[] = rk_Y;
	double Yhalf[] = rk_Yhalf;
	oldY = rk_oldY;
	int i;

	for (i = 0; i != 3; i++)
	    oldY[i] = Y[i] = Yhalf[i] = p.pos[i];
	if (useForce)
	    for (i = 0; i != 3; i++)
		Y[i+3] = Yhalf[i+3] = p.vel[i];
	double t = 0;

	if (!curfunc.useRungeKutta()) {
	    boundCheck = false;
	    curfunc.getField(Yhalf, Y);
	    if (boundCheck && (!useForce || curfunc.checkBoundsWithForce())) {
		p.pos[0] = -100;
		return;
	    }
	    double fmult = partMult;
	    if (useForce) {
		fmult *= .1;
		for (i = 0; i != 3; i++) {
		    p.vel[i] += fmult*Yhalf[i];
		    p.pos[i] += timeStep*p.vel[i];
		}
	    } else {
		for (i = 0; i != 3; i++)
		    p.pos[i] += fmult*Yhalf[i];
	    }
	    for (i = 0; i != 3; i++)
		Y[i] = p.pos[i];
	    if (curfunc.checkBounds(Y, oldY))
		p.pos[0] = -100;
	    return;
	}

	boolean adapt = curfunc.useAdaptiveRungeKutta();
	double h = (adapt) ? p.stepsize : 1;

	int steps = 0;
	double minh = .0001;
	while (t >= 0 && t < 1) {
	    if (t+h > 1)
		h = 1-t;

	    boundCheck = false;


	    rk(order, 0, Y, h);


	    if (!adapt)
		break;


	    rk(order, 0, Yhalf, h*0.5);
	    rk(order, 0, Yhalf, h*0.5);

	    if (boundCheck && (!useForce || curfunc.checkBoundsWithForce())) {
		p.pos[0] = -100;
		return;
	    }


	    localError = java.lang.Math.abs(Y[0] - Yhalf[0]) +
		java.lang.Math.abs(Y[1] - Yhalf[1]) +
		java.lang.Math.abs(Y[2] - Yhalf[2]);

	    if (localError > E && h > minh) {

		h *= 0.75;
		if (h < minh)
		    h = minh;
		for (i = 0; i != order; i++)
		    Y[i] = Yhalf[i] = oldY[i];
		continue;
	    } else if (localError < (E * 0.5)) {
		h *= 1.25;
		if (h > maxh)
		    h = maxh;
	    }

	    for (i = 0; i != order; i++)
		oldY[i] = Yhalf[i] = Y[i];

	    t += h;
	    steps++;
	}

	if (boundCheck && (!useForce || curfunc.checkBoundsWithForce())) {
	    p.pos[0] = -100;
	    return;
	}

	p.stepsize = h;
	for (i = 0; i != 3; i++)
	    p.pos[i] = Y[i];
	if (useForce) {
	    for (i = 0; i != 3; i++)
		p.vel[i] = Y[i+3];
	}
    }

    double dist2(double a[], double b[]) {
	double c0 = a[0]-b[0];
	double c1 = a[1]-b[1];
	double c2 = a[2]-b[2];
	return c0*c0+c1*c1+c2*c2;
    }

    void lineSegment(Particle p, int dir)
    {
	int numIter=0;
	double maxh=20;
	double error=0.0, E = .001, localError;
	int order = 3;
	double Y[] = rk_Y;
	double Yhalf[] = rk_Yhalf;
	oldY = rk_oldY;
	int i;
	int slice = sliceChooser.getSelectedIndex();
	boolean sliced = (slice > 0);
	slice -= SLICE_X;

	for (i = 0; i != 3; i++)
	    oldY[i] = Y[i] = Yhalf[i] = p.pos[i];
	double h = p.stepsize;
	ls_fieldavg[0] = ls_fieldavg[1] = ls_fieldavg[2] = 0;

	int steps = 0;
	double minh = .1;
	double segSize2min = .04*.04;
	double segSize2max = .08*.08;
	double lastd = 0;
	int avgct = 0;
	while (true) {
	    boundCheck = false;
	    steps++;
	    if (steps > 100) {

		p.lifetime = -1;
		break;
	    }



	    rk(order, 0, Y, dir*h);


	    rk(order, 0, Yhalf, dir*h*0.5);
	    rk(order, 0, Yhalf, dir*h*0.5);

	    if (sliced)
		Y[slice] = Yhalf[slice] = sliceval;


	    if (boundCheck) {
		for (i = 0; i != order; i++)
		    Y[i] = Yhalf[i] = oldY[i];
		h /= 2;
		if (h < minh) {
		    p.lifetime = -1;
		    break;
		}
		continue;
	    }
	    if (Y[0] < -1 || Y[0] >= .999 ||
		Y[1] < -1 || Y[1] >= .999 ||
		Y[2] < -1 || Y[2] >= .999) {
		for (i = 0; i != order; i++)
		    Y[i] = Yhalf[i] = oldY[i];
		h /= 2;
		if (h < minh) {

		    p.lifetime = -1;
		    break;
		}
		continue;
	    }


	    localError = java.lang.Math.abs(Y[0] - Yhalf[0]) +
		java.lang.Math.abs(Y[1] - Yhalf[1]) +
		java.lang.Math.abs(Y[2] - Yhalf[2]);

	    if (localError > E && h > minh) {
		h *= 0.75;
		if (h < minh)
		    h = minh;
		for (i = 0; i != order; i++)
		    Y[i] = Yhalf[i] = oldY[i];
		continue;
	    } else if (localError < (E * 0.5)) {
		h *= 1.25;
		if (h > maxh)
		    h = maxh;
	    }

	    double d = dist2(p.pos, Y);
	    if (!(d-lastd > 1e-10)) {


		p.lifetime = -1;
		break;
	    }
	    if (d > segSize2max) {
		h /= 2;
		if (h < minh)
		    break;
		for (i = 0; i != order; i++)
		    Y[i] = Yhalf[i] = oldY[i];
		continue;
	    }
	    ls_fieldavg[0] += rk_k1[0];
	    ls_fieldavg[1] += rk_k1[1];
	    ls_fieldavg[2] += rk_k1[2];
	    avgct++;

	    if (d > segSize2min)
		break;
	    lastd = d;

	    for (i = 0; i != order; i++)
		oldY[i] = Yhalf[i] = Y[i];
	}


	p.stepsize = h;
	for (i = 0; i != 3; i++)
	    p.pos[i] = Y[i];
	p.phi = java.lang.Math.sqrt(ls_fieldavg[0]*ls_fieldavg[0]+
				    ls_fieldavg[1]*ls_fieldavg[1]+
				    ls_fieldavg[2]*ls_fieldavg[2])/avgct;
    }

    abstract class VecFunction {
	abstract String getName();
	abstract VecFunction createNext();
	boolean nonGradient() { return false; }
	boolean useRungeKutta() { return true; }
	boolean useAdaptiveRungeKutta() { return true; }
	boolean checkBoundsWithForce() { return true; }
	boolean noSplitFieldVectors() { return true; }
	int getViewPri(double cameraPos[], double pos[]) {
	    return 0;
	}
	void render(Graphics g) {
	    renderItems(g, 0);
	}
	boolean checkBounds(double y[], double oldY[]) { return false; }
	abstract void getField(double result[], double y[]);
	boolean redistribute() { return true; }
	void setup() {}
	void setupFrame() {}
	void finishFrame() {}
	void actionPerformed() {}

	int getBestSlice() {
	    double y[] = new double[3];
	    double r1[] = new double[3];
	    double r2[] = new double[3];
	    double r3[] = new double[3];
	    y[0] = y[1] = y[2] = .9;
	    curfunc.getField(r1, y);
	    y[0] = .91;
	    curfunc.getField(r2, y);
	    y[0] = .9; y[1] = .91;
	    curfunc.getField(r3, y);
	    if (r1[0] == r2[0] && r1[1] == r2[1] && r1[2] == r2[2])
		return SLICE_X;
	    if (r1[0] == r3[0] && r1[1] == r3[1] && r1[2] == r3[2])
		return SLICE_Y;
	    return SLICE_Z;
	}

	void renderSphere(Graphics g, double sz) {

	    renderItems(g, 2);


	    g.setColor(darkYellow);
	    drawSphere(g, sz, true);


	    renderItems(g, 1);


	    g.setColor(darkYellow);
	    map3d(0, 0, 0, xpoints, ypoints, 0);
	    int r = (int) (getScalingFactor(0, 0, 0) * sz);
	    g.drawOval(xpoints[0]-r, ypoints[0]-r, r*2, r*2);
	    drawSphere(g, sz, false);


	    renderItems(g, 0);
	}
    };

    class InverseSquaredRadial extends VecFunction {
	String getName() { return  null ;
//line 2763 "origbase.java"
 }
	void getField(double result[], double y[]) {
	    double r = distance(y);
	    if (r < chargeSize)
		boundCheck = true;
	    if (getPot) {
		result[0] = -.1/r;
		return;
	    }
	    double r3 = r*r*r;
	    double q = .0003/r3;
	    result[0] = -y[0]*q;
	    result[1] = -y[1]*q;
	    result[2] = -y[2]*q;
	}

	static final double chargeSize = .06;

	void drawCharge(Graphics g, double x, double y, double z) {
	    drawCharge(g, x, y, z, 0);
	}

	void drawCharge(Graphics g, double x, double y, double z, int dir) {
	    map3d(x, y, z, xpoints, ypoints, 0);
	    map3d(x, y, z+.3*dir*reverse, xpoints, ypoints, 1);
	    g.setColor(darkYellow);
	    int r = (int) (getScalingFactor(x, y, z) * chargeSize);
	    g.fillOval(xpoints[0]-r, ypoints[0]-r, r*2, r*2);
	    if (dir != 0)
		drawArrow(g, null, xpoints[0], ypoints[0],
			  xpoints[1], ypoints[1], 5);
	}

	void render(Graphics g) {
	    drawCharge(g, 0, 0, 0);
	    renderItems(g, 1);
	}
	int getViewPri(double cameraPos[], double x[]) {
	    int i;
	    i = intersectSphere(cameraPos, x[0], x[1], x[2], chargeSize);
	    if (i == 0)
		return 1;
	    if (i == 1)
		return -1;
	    return 0;
	}
	VecFunction createNext() { return new InverseSquaredRadialDouble(); }
    };

    class InverseSquaredRadialDouble extends InverseSquaredRadial {
	String getName() { return  null ;
//line 2814 "origbase.java"
 }
	double sign2;
	int getBestSlice() { return SLICE_Y; }
	void getField(double result[], double y[]) {
	    double sep = aux1Bar.getValue()/100.;
	    double xx1 = y[0]-sep;
	    double xx2 = y[0]+sep;
	    double r1 = distance(xx1, y[1], y[2]);
	    if (r1 < chargeSize)
		boundCheck = true;
	    double r2 = distance(xx2, y[1], y[2]);
	    if (r2 < chargeSize)
		boundCheck = true;
	    if (getPot) {
		result[0] = -.05/r1 - .05*sign2/r2;
		if (sign2 == -1)
		    result[0] *= 2;
		return;
	    }
	    double q = .0003;
	    double rq1 = q/(r1*r1*r1);
	    double rq2 = q/(r2*r2*r2) * sign2;
	    result[0] = -xx1 *rq1-xx2 *rq2;
	    result[1] = -y[1]*rq1-y[1]*rq2;
	    result[2] = -y[2]*rq1-y[2]*rq2;
	}
	void setup() {
	    setXZView();
	    sign2 = 1;
	    setupBar(0, "Separación de Cargas", 30);
	}
	void render(Graphics g) {
	    double sep = aux1Bar.getValue()/100.;
	    drawCharge(g, +sep, 0, 0);
	    drawCharge(g, -sep, 0, 0);
	    renderItems(g, 1);
	}
	int getViewPri(double cameraPos[], double x[]) {
	    double sep = aux1Bar.getValue()/100.;
	    if (intersectSphere(cameraPos, x[0], x[1], x[2],
				+sep, 0, 0, chargeSize)== 0 &&
		intersectSphere(cameraPos, x[0], x[1], x[2],
				-sep, 0, 0, chargeSize) == 0)
		return 1;
	    return 0;
	}
	VecFunction createNext() { return
	    null ;
//line 2862 "origbase.java"
 }
    };
//line 2929 "origbase.java"
    class InverseRadial extends VecFunction {
	double lineLen;
	String getName() { return  null ;
//line 2932 "origbase.java"
 }
	void getField(double result[], double y[]) {
	    double r = distance(y[0], y[1], 0);
	    if (r < lineWidth)
		boundCheck = true;
	    if (getPot) {
		result[0] = .4*java.lang.Math.log(r+1e-20);
		return;
	    }
	    double r2 = r*r;
	    result[0] = -.0003*y[0]/r2;
	    result[1] = -.0003*y[1]/r2;
	    result[2] = 0;
	}
	void setup() {
	    setXZView();
	    lineLen = 1;
	}
	void render(Graphics g) {
	    g.setColor(darkYellow);
	    map3d(0, 0, -lineLen, xpoints, ypoints, 0);
	    map3d(0, 0, +lineLen, xpoints, ypoints, 1);
	    g.drawLine(xpoints[0], ypoints[0], xpoints[1], ypoints[1]);
	    renderItems(g, 1);
	}
	int getViewPri(double cameraPos[], double x[]) {
	    if (intersectCylinder(cameraPos, x[0], x[1], x[2], lineWidth,
				  true) == 0)
		return 1;
	    if (intersection[2] >= -lineLen && intersection[2] <= lineLen)
		return 0;
	    return 1;
	}
	VecFunction createNext() { return new InverseRadialDouble(); }
    };

    class InverseRadialDouble extends VecFunction {
	InverseRadialDouble() { sign = 1; }
	String getName() { return  null ;
//line 2971 "origbase.java"
 }
	double sign;
	void getField(double result[], double y[]) {
	    double sep = aux1Bar.getValue()/100.;
	    double xx1 = y[0] - sep;
	    double xx2 = y[0] + sep;
	    double r1 = distance(xx1, y[1]);
	    double r2 = distance(xx2, y[1]);
	    if (r1 < lineWidth || r2 < lineWidth)
		boundCheck = true;
	    if (getPot) {
		result[0] = .2*(java.lang.Math.log(r1+1e-20)+
				sign*java.lang.Math.log(r2+1e-20));
		return;
	    }
	    double q = .0003;
	    double r1s = 1/(r1*r1);
	    double r2s = 1/(r2*r2*sign);
	    result[0] = q*(-xx1 *r1s-xx2 *r2s);
	    result[1] = q*(-y[1]*r1s-y[1]*r2s);
	    result[2] = 0;
	}
	void setup() {
	    setupBar(0, "Separación de Líneas", 30);
	    setXZView();
	}
	void render(Graphics g) {
	    double sep = aux1Bar.getValue()/100.;
	    g.setColor(darkYellow);
	    int i;
	    for (i = -1; i <= 1; i += 2) {
		map3d(sep*i, 0, -1, xpoints, ypoints, 0);
		map3d(sep*i, 0, +1, xpoints, ypoints, 1);
		g.drawLine(xpoints[0], ypoints[0], xpoints[1], ypoints[1]);
	    }
	    renderItems(g, 1);
	}
	int getViewPri(double cameraPos[], double x[]) {
	    int i;
	    double sep = aux1Bar.getValue()/100.;
	    for (i = -1; i <= 1; i += 2) {
		if (intersectCylinder(cameraPos, x[0], x[1], x[2],
				      i*sep, 0, lineWidth, true) != 0)
		    return 0;
	    }
	    return 1;
	}
	VecFunction createNext() { return
	    null ;
//line 3020 "origbase.java"
 }
    };
//line 4048 "origbase.java"
    class InverseRotational extends InverseRadial {
	String getName() { return  "línea de corriente" ;
//line 4050 "origbase.java"
 }
	void setup() {
	    setXYViewExact();
	}
	void getField(double result[], double y[]) {
	    double r = distance(y[0], y[1]);
	    if (showA) {
		result[0] = result[1] = 0;
		result[2] = -.001*(java.lang.Math.log(r)-.5);
	    } else {
		if (r < lineWidth*2)
		    boundCheck = true;
		rotateParticle(result, y, .0001/(r*r));
	    }
	}
	void render(Graphics g) {
	    g.setColor(darkYellow);
	    map3d(0, 0, -1, xpoints, ypoints, 0);
	    map3d(0, 0, +1, xpoints, ypoints, 1);
	    drawCurrentLine(g, xpoints[0], ypoints[0], xpoints[1], ypoints[1],
			    12, true, 1);
	    renderItems(g, 1);
	}
	boolean nonGradient() { return true; }
	VecFunction createNext() { return new InverseRotationalDouble(); }
    };
    class InverseRotationalDouble extends InverseRadialDouble {
	InverseRotationalDouble() { dir2 = 1; ext = false; }
	int dir2;
	boolean ext;
	String getName() { return  "línea doble de corriente" ;
//line 4081 "origbase.java"
 }
	void getField(double result[], double y[]) {
	    double sep = aux1Bar.getValue()/100.;
	    double r = distance(y[0] - sep, y[1]);
	    double r2 = distance(y[0] + sep, y[1]);
	    if (ext) {
		double p = aux3Bar.getValue()*pi/50.;
		double s = aux2Bar.getValue()/30.;
		getDirectionField(result, y, pi/2, p);
		result[0] *= s;
		result[1] *= s;
		result[2] *= s;
	    } else
		result[0] = result[1] = result[2] = 0;
	    if (showA) {
		if (dir2 == 1)
		    result[2] += -.001*(java.lang.Math.log(r)+
				       java.lang.Math.log(r2)-1);
		else
		    result[2] += .001*(java.lang.Math.log(r)-
				       java.lang.Math.log(r2));
	    } else {
		if (r < lineWidth*2)
		    boundCheck = true;
		rotateParticleAdd(result, y, .0001/(r*r), sep, 0);
		if (r2 < lineWidth*2)
		    boundCheck = true;
		rotateParticleAdd(result, y, dir2*.0001/(r2*r2), -sep, 0);
	    }
	}
	void setup() {
	    setupBar(0, "Separación de Líneas", 30);
	    if (ext) {
		setupBar(1, "Ext. Intensidad", 28);
		setupBar(2, "Ext. Dirección", 0);
	    }
	    setXYViewExact();
	}
	void render(Graphics g) {
	    double sep = aux1Bar.getValue()/100.;
	    g.setColor(darkYellow);
	    int i;
	    for (i = -1; i <= 1; i += 2) {
		map3d(sep*i, 0, -1, xpoints, ypoints, 0);
		map3d(sep*i, 0, +1, xpoints, ypoints, 1);
		int dir = (i == -1) ? 1 : dir2;
		drawCurrentLine(g, xpoints[0], ypoints[0],
				xpoints[1], ypoints[1], 12, true, dir);
	    }
	    renderItems(g, 1);
	}
	boolean nonGradient() { return true; }
	VecFunction createNext() { return new InverseRotationalDoubleExt(); }
    };
    class InverseRotationalDoubleExt extends InverseRotationalDouble {
	InverseRotationalDoubleExt() { ext = true; }
	String getName() { return  "línea corr doble + ext" ;
//line 4138 "origbase.java"
 }
	VecFunction createNext() { return new InverseRotationalDipole(); }
    };
    class InverseRotationalDipole extends InverseRotationalDouble {
	InverseRotationalDipole() { dir2 = -1; }
	String getName() { return  "línea corriente dipolo" ;
//line 4144 "origbase.java"
 }
	VecFunction createNext() { return new InverseRotationalDipoleExt(); }
    };
    class InverseRotationalDipoleExt extends InverseRotationalDouble {
	InverseRotationalDipoleExt() { dir2 = -1; ext = true; }
	void setup() {
	    super.setup();
	    aux2Bar.setValue(17);
	    aux3Bar.setValue(25);
	}
	String getName() { return  "lín corr dipolo + ext" ;
//line 4155 "origbase.java"
 }
	VecFunction createNext() { return new OneDirectionFunction(); }
    };
    class OneDirectionFunction extends VecFunction {
	String getName() { return  "campo uniforme" ;
//line 4160 "origbase.java"
 }
	void getField(double result[], double y[]) {
	    double th = aux1Bar.getValue() * pi /50.;
	    double ph = aux2Bar.getValue() * pi /50.;
	    getDirectionField(result, y, th, ph);
	}

	void setup() {
	    setupBar(0, "Theta", 25);
	    setupBar(1, "Fi", 0);
	    setXYView();
	}
	VecFunction createNext() { return
	    new MovingChargeField() ;
//line 4174 "origbase.java"
 }
    };

    void getDirectionField(double result[], double y[],
			   double th, double ph) {
	double sinth = java.lang.Math.sin(th);
	double costh = java.lang.Math.cos(th);
	double sinph = java.lang.Math.sin(ph);
	double cosph = java.lang.Math.cos(ph);
	if (!showA) {
	    if (getPot) {
		result[0] = -.4*(y[0]*sinth*cosph + y[1]*sinth*sinph +
				 y[2]*costh);
		return;
	    }
	    result[0] = .0003*sinth*cosph;
	    result[1] = .0003*sinth*sinph;
	    result[2] = .0003*costh;
	} else {



	    double axis[] = new double[3];
	    axis[0] = sinth*cosph;
	    axis[1] = sinth*sinph;
	    axis[2] = costh;

	    double d = dot(axis, y);


	    double r[] = new double[3];
	    int i;
	    for (i = 0; i != 3; i++)
		r[i] = .0006*(y[i] - axis[i]*d);

	    cross(result, axis, r);
	}
    }



    class MovingChargeField extends InverseSquaredRadial {
	String getName() { return "carga móvil"; }
	void getField(double result[], double y[]) {
	    double rz = distance(y);
	    if (showA) {
		result[0] = result[1] = 0;
		result[2] = .0003/rz;
	    } else {
		double r = distance(y[0], y[1]);
		if (rz < chargeSize)
		    boundCheck = true;
		rotateParticle(result, y, .0001/(rz*rz*rz));
	    }
	}
	void render(Graphics g) {
	    drawCharge(g, 0, 0, 0, 1);
	    renderItems(g, 1);
	}
	void setup() {
	    setXZView();
	}
	boolean nonGradient() { return true; }
	VecFunction createNext() { return
	       new FastChargeField() ; }
    };


    class FastChargeField extends MovingChargeField {
	String getName() { return "carga rápida"; }
	double getFieldStrength(double y[]) {
	    double rz = distance(y);
	    if (rz < chargeSize)
		boundCheck = true;
	    double r = distance(y[0], y[1]);

	    double sinth = r/rz;
	    double beta = (aux1Bar.getValue()+1)/102.;






	    double b = .001*(1-beta*beta)*beta/
		(rz*rz*java.lang.Math.pow(1-beta*beta*sinth*sinth, 1.5));
	    return b;
	}
	void setup() {
	    super.setup();
	    setupBar(0, "velocidad/C", 60);
	}
	void render(Graphics g) {


	    drawCharge(g, 0, 0, 0, reverse);
	    renderItems(g, 1);
	}
	void getField(double result[], double y[]) {
	    if (showA) {
		double rz = distance(y);
		double r = distance(y[0], y[1]);

		double sinth = r/rz;
		double beta = (aux1Bar.getValue()+1)/102.;
		result[0] = result[1] = 0;
		result[2] = .003*beta/
		    (rz*java.lang.Math.pow(1-beta*beta*sinth*sinth, .5));
	    } else
		rotateParticle(result, y, getFieldStrength(y));
	}
	VecFunction createNext() { return new MovingChargeFieldDouble(); }
    };

    class MovingChargeFieldDouble extends InverseSquaredRadialDouble {
	String getName() { return "doble carga móvil"; }
	MovingChargeFieldDouble() { dir2 = 1; }
	int dir2;
	void getField(double result[], double y[]) {
	    result[0] = result[1] = result[2] = 0;
	    double sep = aux1Bar.getValue()/100.;
	    double rz1 = distance(y[0] - sep, y[1], y[2]);
	    double rz2 = distance(y[0] + sep, y[1], y[2]);
	    if (showA) {
		result[0] = result[1] = 0;
		result[2] = .0003*(1/rz1 + dir2/rz2);
	    } else {
		double r = distance(y[0] - sep, y[1]);
		if (rz1 < chargeSize)
		    boundCheck = true;
		rotateParticleAdd(result, y, .0001/(rz1*rz1*rz1), sep, 0);
		if (rz2 < chargeSize)
		    boundCheck = true;
		r = distance(y[0] + sep, y[1]);
		rotateParticleAdd(result, y, dir2*.0001/(rz2*rz2*rz2),
				  -sep, 0);
	    }
	}
	void setup() {
	    setupBar(0, "Separación cargas", 30);
	    super.setup();
	}
	void render(Graphics g) {
	    double sep = aux1Bar.getValue()/100.;
	    drawCharge(g, +sep, 0, 0, 1);
	    drawCharge(g, -sep, 0, 0, dir2);
	    renderItems(g, 1);
	}
	boolean nonGradient() { return true; }
	VecFunction createNext() { return new MovingChargeDipole(); }
    };
    class MovingChargeDipole extends MovingChargeFieldDouble {
	MovingChargeDipole() { dir2 = -1; }
	String getName() { return "carga móvil dipolo"; }
	VecFunction createNext() { return new CurrentLoopField(); }
    };


    class CurrentLoopField extends VecFunction {
	CurrentLoopField() { useColor = true; }
	Color colors[];
	boolean useColor;
	double size;
	String getName() { return "espira"; }
	boolean useAdaptiveRungeKutta() { return false; }
	void setup() {
	    setXZView();
	    setupBar(0, "Tamaño espira", 40);
	}
	void setupFrame() {
	    size = (aux1Bar.getValue()+1)/100.;
	}
	void getField(double result[], double y[]) {
	    getLoopField(result, y, 0, 0, 1, size);
	}
	void getLoopField(double result[], double y[], double xoff,
			  double zoff, int dir, double size) {
	    double xx = y[0]+xoff;
	    double yy = y[1];
	    double zz = y[2]+zoff;
	    int i;
	    result[0] = result[1] = result[2] = 0;
	    int ct = 8;
	    double q = .0006*dir/(size*ct);
	    double ang0 = java.lang.Math.atan2(y[1], y[0]);
	    for (i = 0; i != ct; i ++) {
		double ang = pi*2*i/ct;
		double jxx = size*java.lang.Math.cos(ang+ang0);
		double jyy = size*java.lang.Math.sin(ang+ang0);
		double lxx = -jyy*q;
		double lyy = jxx*q;
		double rx = xx-jxx;
		double ry = yy-jyy;
		double rz = zz;
		double r = java.lang.Math.sqrt(rx*rx+ry*ry+rz*rz);
		if (!showA) {
		    double r3 = r*r*r;
		    if (r < .04 && useMagnetMove())
			boundCheck = true;





		    double cx = lyy*rz/r3;
		    double cy = -lxx*rz/r3;
		    double cz = (lxx*ry - lyy*rx)/r3;
		    result[0] += cx;
		    result[1] += cy;
		    result[2] += cz;
		} else {

		    result[0] += 6*lxx/r;
		    result[1] += 6*lyy/r;
		}
	    }
	}
	boolean checkBounds(double y[], double oldY[]) {
	    if (!useMagnetMove())
		return false;
	    if ((y[2] > 0 && oldY[2] < 0) ||
		(y[2] < 0 && oldY[2] > 0)) {
		double r = java.lang.Math.sqrt(y[0]*y[0]+y[1]*y[1]);
		if (r < size)
		    return true;
	    }
	    return false;
	}

	void render(Graphics g) {
	    renderItems(g, 1);
	    renderLoop(g, 0, 0, 1, size);
	    renderItems(g, 0);
	}

	void renderLoop(Graphics g, double xoff, double zoff, int dir,
			double size) {
	    final int loopSegments = 72;
	    int i;
	    if (!useColor)
		g.setColor(darkYellow);
	    for (i = 0; i != loopSegments; i++) {
		double ang1 = pi*2*i/loopSegments;
		double ang2 = pi*2*(i+dir)/loopSegments;
		double jxx1 = size*java.lang.Math.cos(ang1) + xoff;
		double jyy1 = size*java.lang.Math.sin(ang1);
		double jxx2 = size*java.lang.Math.cos(ang2) + xoff;
		double jyy2 = size*java.lang.Math.sin(ang2);
		map3d(jxx1, jyy1, zoff, xpoints, ypoints, 0);
		map3d(jxx2, jyy2, zoff, xpoints, ypoints, 1);
		if (useColor)
		    g.setColor(getCurrentColor(i*dir));
		if (i == 0 && useColor)
		    drawCurrentArrow(g, xpoints[0], ypoints[0],
				     xpoints[1], ypoints[1]);
		else
		    g.drawLine(xpoints[0], ypoints[0], xpoints[1], ypoints[1]);
	    }
	}

	int getViewPri(double cameraPos[], double x[]) {
	    if (intersectZPlane(cameraPos, 0, x[0], x[1], x[2]) != 0)
		return 1;
	    return 0;
	}
	boolean noSplitFieldVectors() { return false; }
	boolean nonGradient() { return true; }
	VecFunction createNext() { return
	     new CurrentLoopsSideField() ; }
    };


    class CurrentLoopsSideField extends CurrentLoopField {
	String getName() { return "par espiras"; }
	int dir2;
	double offx, offz, size;
	double tres1[], tres2[];
	CurrentLoopsSideField() {
	    tres1 = new double[3];
	    tres2 = new double[3];
	}
	void setup() {
	    setXZView();
	    setupBar(0, "Tamaño espiras", 40);
	    setupBar(1, "Separación espiras", 10);
	    setupBar(2, "Desplazamiento", 0);
	}
	void setupFrame() {
	    size = (aux1Bar.getValue()+1)/100.;
	    double sep = aux2Bar.getValue()/100.;
	    double sep2 = aux3Bar.getValue()/100.;
	    offx = sep*(1-size)+size; offz = sep2;
	    dir2 = 1;
	}
	void getField(double result[], double y[]) {
	    getLoopField(tres1, y, +offx, +offz, 1, size);
	    getLoopField(tres2, y, -offx, -offz, dir2, size);
	    int i;
	    for (i = 0; i != 3; i++)
		result[i] = tres1[i] + tres2[i];
	}
	void render(Graphics g) {
	    renderItems(g, 0);
	    renderLoop(g, +offx, +offz, 1, size);
	    renderLoop(g, -offx, -offz, dir2, size);
	    renderItems(g, 1);
	}
	boolean checkBounds(double y[], double oldY[]) {
	    if (!useMagnetMove())
		return false;
	    if ((y[2] > offz && oldY[2] < offz) ||
		(y[2] < offz && oldY[2] > offz)) {
		double x = y[0]-offx;
		double r = java.lang.Math.sqrt(x*x+y[1]*y[1]);
		if (r < size)
		    return true;
	    }
	    if ((y[2] > -offz && oldY[2] < -offz) ||
		(y[2] < -offz && oldY[2] > -offz)) {
		double x = y[0]+offx;
		double r = java.lang.Math.sqrt(x*x+y[1]*y[1]);
		if (r < size)
		    return true;
	    }
	    return false;
	}
	VecFunction createNext() { return new CurrentLoopsSideOppField(); }
    };
    class CurrentLoopsSideOppField extends CurrentLoopsSideField {
	String getName() { return "par espiras oposición"; }
	void setupFrame() {
	    size = (aux1Bar.getValue()+1)/100.;
	    double sep = aux2Bar.getValue()/100.;
	    double sep2 = aux3Bar.getValue()/100.;
	    offx = sep*(1-size)+size; offz = sep2;
	    dir2 = -1;
	}
	VecFunction createNext() { return new CurrentLoopsStackedField(); }
    };
    class CurrentLoopsStackedField extends CurrentLoopsSideField {
	String getName() { return "par espiras bobina"; }
	void setupFrame() {
	    size = (aux1Bar.getValue()+1)/100.;
	    double sep = (aux2Bar.getValue()+1)/100.;
	    double sep2 = aux3Bar.getValue()/100.;
	    offx = sep2; offz = sep;
	    dir2 = 1;
	}
	VecFunction createNext() { return new CurrentLoopsStackedOppField(); }
    };
    class CurrentLoopsStackedOppField extends CurrentLoopsSideField {
	String getName() { return "par espiras apiladas en op."; }
	void setupFrame() {
	    size = (aux1Bar.getValue()+1)/100.;
	    double sep = (aux2Bar.getValue()+1)/100.;
	    double sep2 = aux3Bar.getValue()/100.;
	    offx = sep2; offz = sep;
	    dir2 = -1;
	}
	VecFunction createNext() { return new CurrentLoopsOpposingConcentric(); }
    };
    class CurrentLoopsOpposingConcentric extends CurrentLoopField {
	String getName() { return "espiras concéntricas"; }
	int dir2;
	double tres1[], tres2[];
	double size2;
	CurrentLoopsOpposingConcentric() {
	    tres1 = new double[3];
	    tres2 = new double[3];
	}
	void setup() {
	    setXZView();
	    setupBar(0, "Tamaño espira exterior", 75);
	    setupBar(1, "Tamaño espira interior", 50);
	}
	void setupFrame() {
	    size = (aux1Bar.getValue()+1)/101.;
	    size2 = size*(aux2Bar.getValue()+1)/101.;
	}
	void getField(double result[], double y[]) {
	    getLoopField(tres1, y, 0, 0, 1, size);
	    getLoopField(tres2, y, 0, 0, -1, size2);









	    double mult = size2/size;
	    int i;
	    for (i = 0; i != 3; i++)
		result[i] = tres1[i] + mult*tres2[i];
	}
	void render(Graphics g) {
	    renderItems(g, 0);
	    renderLoop(g, 0, 0, 1, size);
	    renderLoop(g, 0, 0, -1, size2);
	    renderItems(g, 1);
	}
	VecFunction createNext() { return new SolenoidField(); }
    };
    class SolenoidField extends VecFunction {
	String getName() { return "solenoide"; }
	boolean useRungeKutta() { return false; }
	double height, size;
	int turns;
	void setupFrame() {
	    size = (aux1Bar.getValue()+1)/100.;
	    turns = (aux3Bar.getValue()/4)+1;
	    height = (aux2Bar.getValue()+1)/25.;
	}
	void getField(double result[], double y[]) {
	    int i, j, n;
	    result[0] = result[1] = result[2] = 0;
	    int angct = 8;
	    if (turns < 9)
		angct = 80/turns;
	    double ang0 = java.lang.Math.atan2(y[1], y[0]);
	    double zcoilstep = height/turns;
	    double zangstep = zcoilstep/angct;
	    double zbase = -height/2;
	    double q = .003/(turns*angct);
	    double lzz = q*zangstep;
	    if (ang0 < 0)
		ang0 += 2*pi;
	    if (ang0 < 0)
		System.out.print("-ang0?? " + ang0 + "\n");
	    ang0 %= zangstep;
	    zbase += zcoilstep*ang0/(2*pi);
	    for (i = 0; i != angct; i++) {
		double ang = pi*2*i/angct;
		double jxx = size*java.lang.Math.cos(ang+ang0);
		double jyy = size*java.lang.Math.sin(ang+ang0);
		double jzz = zbase+zangstep*i;
		double lxx = -jyy*q;
		double lyy = jxx*q;
		double rx = y[0]-jxx;
		double ry = y[1]-jyy;
		double rx2ry2 = rx*rx+ry*ry;
		for (j = 0; j != turns; j++) {
		    double rz = y[2]-jzz;
		    double r = java.lang.Math.sqrt(rx2ry2+rz*rz);
		    if (!showA) {
			if (r < .04 && useMagnetMove())
			    boundCheck = true;






			double r3 = r*r*r;
			double cx = (lyy*rz-lzz*ry)/r3;
			double cy = (lzz*rx-lxx*rz)/r3;
			double cz = (lxx*ry-lyy*rx)/r3;
			result[0] += cx;
			result[1] += cy;
			result[2] += cz;
		    } else {
			result[0] += 6*lxx/r;
			result[1] += 6*lyy/r;
			result[2] += 6*lzz/r;
		    }
		    jzz += zcoilstep;
		}
	    }
	}
	void setup() {
	    setupBar(0, "Diámetro", 40);
	    setupBar(1, "Altura", 30);
	    setupBar(2, "# de vueltas", 36);
	    setXZView();
	}
	int getViewPri(double cameraPos[], double x[]) {
	    return intersectCylinder(cameraPos, x[0], x[1], x[2], 2, false);
	}
	boolean checkBounds(double y[], double oldY[]) {
	    if (!useMagnetMove())
		return false;
	    double height2 = height*2;
	    double r = java.lang.Math.sqrt(y[0]*y[0]+y[1]*y[1]);
	    double or = java.lang.Math.sqrt(oldY[0]*oldY[0]+oldY[1]*oldY[1]);

	    if (y[2] < height2 && y[2] > -height2) {
		if ((r < size && or > size) ||
		    (or < size && r > size))
		    return true;
	    }

	    if ((y[2] > 0 && oldY[2] < 0) ||
		(y[2] < 0 && oldY[2] > 0)) {
		if (r < size)
		    return true;
	    }
	    return false;
	}
	void render(Graphics g) {
	    renderItems(g, 2);

	    renderItems(g, 1);
	    g.setColor(darkYellow);
	    int i, j;
	    int angct = 48;
	    if (turns < 10)
		angct = 480/turns;
	    double zcoilstep = height/turns;
	    double zangstep = zcoilstep/angct;
	    double zbase = -height/2;
	    for (i = 0; i != angct; i++) {
		double ang1 = pi*2*i/angct;
		double ang2 = pi*2*(i+1)/angct;
		double jxx1 = size*java.lang.Math.cos(ang1);
		double jyy1 = size*java.lang.Math.sin(ang1);
		double jxx2 = size*java.lang.Math.cos(ang2);
		double jyy2 = size*java.lang.Math.sin(ang2);
		double jzz1 = zbase + zangstep*i;
		for (j = 0; j != turns; j++) {
		    double jzz2 = jzz1 + zangstep;
		    map3d(jxx1, jyy1, jzz1, xpoints, ypoints, 0);
		    map3d(jxx2, jyy2, jzz2, xpoints, ypoints, 1);
		    g.setColor(getCurrentColor(j*angct+i));
		    if (i == 0 && j == turns/2)
			drawCurrentArrow(g, xpoints[0], ypoints[0],
					 xpoints[1], ypoints[1]);
		    else
			g.drawLine(xpoints[0], ypoints[0], xpoints[1], ypoints[1]);
		    jzz1 += zcoilstep;
		}
	    }
	    renderItems(g, 0);
	}
	boolean nonGradient() { return true; }
	VecFunction createNext() { return new ToroidalSolenoidField(); }
    };
    class ToroidalSolenoidField extends VecFunction {
	ToroidalSolenoidField() { turnmult = 1; }
	String getName() { return "solenoide toroidal"; }
	boolean useRungeKutta() { return false; }
	double size1, size2, q;
	int turns, angct = 8;
	int turnmult;
	double costab1[], sintab1[];
	double costab2[][], sintab2[][];

	void setupFrame() {
	    size1 = aux1Bar.getValue()/100.;
	    size2 = aux2Bar.getValue()*size1/100.;
	    turns = aux3Bar.getValue()/3+6;
	    q = .0003/(angct*turns);
	    costab1 = new double[angct];
	    sintab1 = new double[angct];
	    costab2 = new double[angct][turns];
	    sintab2 = new double[angct][turns];
	    int i, j;
	    for (i = 0; i != angct; i++) {
		double ang = pi*2*i/angct;
		costab1[i] = java.lang.Math.cos(ang);
		sintab1[i] = java.lang.Math.sin(ang);
		for (j = 0; j != turns; j++) {
		    double ang2 = (pi*2*j+ang)/(turnmult*turns);
		    costab2[i][j] = java.lang.Math.cos(ang2);
		    sintab2[i][j] = java.lang.Math.sin(ang2);
		}
	    }
	}
	void finishFrame() {
	    costab1 = sintab1 = null;
	    costab2 = sintab2 = null;
	}

	void setup() {
	    setupBar(0, "Radio Central", 60);
	    setupBar(1, "Radio Exterior", 80);
	    setupBar(2, "# de vueltas", 18);
	}

	void getField(double result[], double y[]) {
	    int i, j, n;
	    result[0] = result[1] = result[2] = 0;
	    for (i = 0; i != angct; i++) {
		double cosp = costab1[i];
		double sinp = sintab1[i];
		double jzz = size2*sinp;
		double lzz = q*turns*size2*cosp;
		double rz = y[2]-jzz;
		for (j = 0; j != turns; j++) {
		    double cosa = costab2[i][j];
		    double sina = sintab2[i][j];
		    double jxx = cosa*(size1+size2*cosp);
		    double jyy = sina*(size1+size2*cosp);
		    double lxx = q*
			(-(size1+size2*cosp)*sina - turns*size2*cosa*sinp);
		    double lyy = q*
			((size1+size2*cosp)*cosa - turns*size2*sina*sinp);
		    double rx = y[0]-jxx;
		    double ry = y[1]-jyy;
		    double r = distance(rx, ry, rz);
		    if (!showA) {
			double r3 = r*r*r;
			if (r < .04 && useMagnetMove())
			    boundCheck = true;






			double cx = (lyy*rz-lzz*ry)/r3;
			double cy = (lzz*rx-lxx*rz)/r3;
			double cz = (lxx*ry-lyy*rx)/r3;
			result[0] += cx;
			result[1] += cy;
			result[2] += cz;
		    } else {
			result[0] += 6*lxx/r;
			result[1] += 6*lyy/r;
			result[2] += 6*lzz/r;
		    }
		}
	    }
	}
	int getViewPri(double cameraPos[], double x[]) {
	    return intersectCylinder(cameraPos, x[0], x[1], x[2], 2, false);
	}
	void render(Graphics g) {
	    renderItems(g, 2);

	    renderItems(g, 1);
	    g.setColor(darkYellow);
	    int jzz, i;
	    int steps = turns*48;
	    for (i = 0; i != steps; i++) {
		getToroidPoint(xpoints, ypoints, size1, size2, turns, i, 0);
		getToroidPoint(xpoints, ypoints, size1, size2, turns, i+1, 1);
		g.setColor(getCurrentColor(i));
		if (i == 50)
		    drawArrow(g, null, xpoints[0], ypoints[0],
			      xpoints[1], ypoints[1], 7);
		else
		    g.drawLine(xpoints[0], ypoints[0], xpoints[1], ypoints[1]);
	    }
	    renderItems(g, 0);
	}
	void getToroidPoint(int xpoints[], int ypoints[], double size1,
			    double size2, int turns, int i, int n) {
	    int angct = 48;
	    double ang = pi*2*(i % angct)/angct;
	    double cosp = java.lang.Math.cos(ang);
	    double sinp = java.lang.Math.sin(ang);
	    double ang2 = (pi*2*(i/angct)+ang)/(turns*turnmult);
	    double cosa = java.lang.Math.cos(ang2);
	    double sina = java.lang.Math.sin(ang2);
	    map3d(cosa*(size1+size2*cosp),
		  sina*(size1+size2*cosp),
		  size2*sinp,
		  xpoints, ypoints, n);
	}
	boolean nonGradient() { return true; }
	VecFunction createNext() { return new HorseshoeElectromagnetField(); }
    };
    class HorseshoeElectromagnetField extends ToroidalSolenoidField {
	HorseshoeElectromagnetField() { turnmult = 2; }
	String getName() { return "imán herradura"; }
	void setup() {
	    setupBar(0, "Radio Central", 40);
	    setupBar(1, "Radio Exterior", 50);
	    setupBar(2, "# de vueltas", 18);
	    setXYView();
	}
	VecFunction createNext() { return new SquareLoopField(); }
    };
    class SquareLoopField extends VecFunction {
	String getName() { return "espira cuadrada"; }
	double lstart, lstop, size;

	void setup() {
	    setupBar(0, "Tamaño espira", 60);
	    setXZView();
	}

	void setupFrame() {
	    size = aux1Bar.getValue()/100.;
	    lstart = -size;
	    lstop = size;
	}

	void getField(double result[], double y[]) {
	    getLoopField(result, y, 0, 1);
	}

	void getLineField(double result[], double y[], double offo,
			  double offt, int lcoord, int ocoord, int tcoord,
			  int dir) {
	    double a1 = lstart-y[lcoord];
	    double a2 = lstop-y[lcoord];
	    double r = distance(y[ocoord]-offo, y[tcoord]-offt);
	    if (r < lineWidth && a1 <= 0 && a2 >= 0)
		boundCheck = true;
	    double y2 = r*r;
	    double a12 = a1*a1;
	    double a22 = a2*a2;
	    double a12y2 = java.lang.Math.sqrt(a12+y2);
	    double a22y2 = java.lang.Math.sqrt(a22+y2);
	    if (showA) {
		if (lcoord < ocoord)
		    dir = -dir;
		result[lcoord] +=
		    dir*.0003*java.lang.Math.log((a2+a22y2)/(a1+a12y2))/size;
		return;
	    }
	    double q = dir*.0001/size;
	    double fth =
		q* (-1/(a12+y2+a1*a12y2)+1/(a22+y2+a2*a22y2));
	    result[tcoord] += fth*(y[ocoord]-offo);
	    result[ocoord] -= fth*(y[tcoord]-offt);
	}

	void getLoopField(double result[], double y[], double zoff, int dir) {
	    result[0] = result[1] = result[2] = 0;
	    getLineField(result, y, size, zoff, 0, 1, 2, dir);
	    getLineField(result, y, -size, zoff, 0, 1, 2, -dir);
	    getLineField(result, y, size, zoff, 1, 0, 2, dir);
	    getLineField(result, y, -size, zoff, 1, 0, 2, -dir);
	}
	boolean checkBounds(double y[], double oldY[]) {
	    if (!useMagnetMove())
		return false;
	    if ((y[2] > 0 && oldY[2] < 0) ||
		(y[2] < 0 && oldY[2] > 0)) {
		if (y[0] < size && y[1] < size &&
		    y[0] > -size && y[1] > -size)
		    return true;
	    }
	    return false;
	}
	void render(Graphics g) {
	    renderItems(g, 0);
	    g.setColor(darkYellow);
	    map3d(-size, -size, 0, xpoints, ypoints, 0);
	    map3d(+size, -size, 0, xpoints, ypoints, 1);
	    map3d(+size, +size, 0, xpoints, ypoints, 2);
	    map3d(-size, +size, 0, xpoints, ypoints, 3);
	    int i;
	    for (i = 0; i != 4; i++) {
		int j = (i + 1) & 3;
		drawCurrentLine(g, xpoints[i], ypoints[i],
				xpoints[j], ypoints[j], 8, i == 0, 1);
	    }
	    renderItems(g, 1);
	}
	int getViewPri(double cameraPos[], double x[]) {
	    if (intersectZPlane(cameraPos, 0, x[0], x[1], x[2]) == 0)
		return 1;
	    return 0;
	}
	boolean noSplitFieldVectors() { return false; }
	boolean nonGradient() { return true; }
	VecFunction createNext() { return new CornerField(); }
    };
    class CornerField extends SquareLoopField {
	String getName() { return "esquina"; }
	void setup() {
	    setXZView();
	    setupBar(0, "Desplazamiento", 50);
	}
	double offset;
	void setupFrame() {
	    size = 2;
	    offset = aux1Bar.getValue()/50.-1;
	    lstart = offset;
	    lstop = 10+offset;
	}

	void getField(double result[], double y[]) {
	    result[0] = result[1] = result[2] = 0;
	    getLineField(result, y, offset, 0, 0, 1, 2, -1);
	    getLineField(result, y, offset, 0, 1, 0, 2, -1);
	}
	void render(Graphics g) {
	    renderItems(g, 0);
	    g.setColor(darkYellow);
	    map3d(offset, offset, 0, xpoints, ypoints, 0);
	    map3d(1, offset, 0, xpoints, ypoints, 1);
	    map3d(offset, 1, 0, xpoints, ypoints, 2);
	    drawCurrentLine(g,
			    xpoints[0], ypoints[0],
			    xpoints[1], ypoints[1], 8, true, 1);
	    drawCurrentLine(g,
			    xpoints[2], ypoints[2],
			    xpoints[0], ypoints[0], 8, false, 1);
	    renderItems(g, 1);
	}
	VecFunction createNext() { return new MagneticSphereB(); }
    };
    class MagneticSphereB extends VecFunction {
	String getName() { return "esfera magnética"; }
	void getField(double result[], double y[]) {
	    double a = aux1Bar.getValue()/100.;
	    double r = distance(y);
	    if (r < a) {
		boundCheck = true;
		result[0] = result[1] = result[2] = 0;
		return;
	    }
	    double rz = distance(y[0], y[1]);
	    double costh = y[2]/r;
	    double sinth = rz/r;
	    double sinph = y[1]/rz;
	    double cosph = y[0]/rz;
	    if (!showA) {


		double r3 = .003*a*a*a/(r*r*r);
		double eth = 2*sinth*r3;
		double er = costh*r3;
		result[0] = sinth*cosph*er + costh*cosph*eth;
		result[1] = sinth*sinph*er + costh*sinph*eth;
		result[2] = costh *er - sinth* eth;
	    } else {

		double aph = .003*a*a*a*sinth/(r*r);
		result[0] = -sinph*aph;
		result[1] = cosph*aph;
		result[2] = 0;
	    }
	}
	void setup() {
	    setupBar(0, "Tamaño esfera", 50);
	    setXZView();
	}
	void render(Graphics g) {
	    double a = aux1Bar.getValue()/100.;
	    fillSphere(g, a, 0);
	    renderItems(g, 0);
	}
	int getViewPri(double cameraPos[], double x[]) {
	    double a = aux1Bar.getValue()/100.;
	    return intersectSphere(cameraPos, x[0], x[1], x[2], a);
	}
	boolean nonGradient() { return true; }
	VecFunction createNext() { return new MonopoleAttempt(); }
    };
    class MonopoleAttempt extends SquareLoopField {
	String getName() { return "intento de monopolo"; }
	double tres[][], yflip[], rad, size;
	int count;
	MonopoleAttempt() {
	    tres = new double[8][3];
	    yflip = new double[3];
	}
	void setup() {
	    setXZView();
	    setupBar(0, "Tamaño espira", 40);
	    setupBar(1, "Separación", 10);
	    setupBar(2, "Núm.Espiras", 100);
	    dispChooser.select(DISP_VECTORS);
	}
	void setupFrame() {
	    super.setupFrame();
	    size = (aux1Bar.getValue())/100.;
	    rad = aux2Bar.getValue()/100. + size;
	    count = (aux3Bar.getValue()*6)/101 + 1;
	}
	void drawLoop(Graphics g) {
	    int i;
	    for (i = 0; i != 4; i++) {
		int j = (i + 1) & 3;
		drawCurrentLine(g, xpoints[i], ypoints[i],
				xpoints[j], ypoints[j], 8, i == 0, 1);
	    }
	}
	void render(Graphics g) {
	    renderItems(g, 0);
	    g.setColor(darkYellow);
	    double size = aux1Bar.getValue()/100.;

	    int i;
	    int ct = count;
	    for (i = -1; i <= 1; i += 2) {
		if (--ct < 0)
		    break;
		map3d(-size, -size, rad*i, xpoints, ypoints, 0);
		map3d(+size*i, -size*i, rad*i, xpoints, ypoints, 1);
		map3d(+size, +size, rad*i, xpoints, ypoints, 2);
		map3d(-size*i, +size*i, rad*i, xpoints, ypoints, 3);
		drawLoop(g);
	    }

	    for (i = -1; i <= 1; i += 2) {
		if (--ct < 0)
		    break;
		map3d(-size, rad*i, -size, xpoints, ypoints, 0);
		map3d(-size*i, rad*i, +size*i, xpoints, ypoints, 1);
		map3d(+size, rad*i, +size, xpoints, ypoints, 2);
		map3d(+size*i, rad*i, -size*i, xpoints, ypoints, 3);
		drawLoop(g);
	    }

	    for (i = -1; i <= 1; i += 2) {
		if (--ct < 0)
		    break;
		map3d(rad*i, -size, -size, xpoints, ypoints, 0);
		map3d(rad*i, +size*i, -size*i, xpoints, ypoints, 1);
		map3d(rad*i, +size, +size, xpoints, ypoints, 2);
		map3d(rad*i, -size*i, +size*i, xpoints, ypoints, 3);
		drawLoop(g);
	    }

	    renderItems(g, 1);
	}
	void getField(double result[], double y[]) {
	    int i;
	    for (i = 0; i != 6; i++)
		tres[i][0] = tres[i][1] = tres[i][2] = 0;
	    getLoopField(tres[0], y, -rad, -1);
	    if (count > 1)
		getLoopField(tres[1], y, rad, 1);
	    yflip[1] = y[0];
	    yflip[2] = y[1];
	    yflip[0] = y[2];
	    if (count > 2)
		getLoopField(tres[2], yflip, -rad, -1);
	    if (count > 3)
		getLoopField(tres[3], yflip, rad, 1);
	    yflip[2] = y[0];
	    yflip[0] = y[1];
	    yflip[1] = y[2];
	    if (count > 4)
		getLoopField(tres[4], yflip, -rad, -1);
	    if (count > 5)
		getLoopField(tres[5], yflip, rad, 1);
	    for (i = 0; i != 3; i++)
		result[i] = tres[0][i] + tres[1][i] +
		    tres[2][(i+1)%3] + tres[3][(i+1)%3] +
		    tres[4][(i+2)%3] + tres[5][(i+2)%3];
	}
	VecFunction createNext() { return null; }
    };
//line 5676 "origbase.java"
    class DrawData {
	public Graphics g;
	public double mult;
	public double field[], vv[];
    };

    class Particle {
	public double pos[];
	public double vel[];
	public int viewPri;
	public double lifetime;
	public double phi, theta, phiv, thetav;
	public double stepsize;
	Particle() {
	    pos = new double[3]; vel = new double[3];
	    stepsize = 1;
	}
    };

    class FieldVector {
	public int sx1, sy1, sx2, sy2;
	public double p1[], p2[];
	public int col;
	public int viewPri;
    };
//line 5762 "origbase.java"
};
