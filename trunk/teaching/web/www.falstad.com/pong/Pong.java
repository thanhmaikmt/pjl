// Pong.java by Paul Falstad, www.falstad.com
// Copyright (C) 1996 or something

// I had all kinds of problems getting sleep() to work for values less
// than 50 under Windows, so the frame rate isn't as good as it could be...

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

class Bounceable {
    static final int numcols = 10;
    static final int topCounter = 3;
    Color cols[];
    int bounceno, counter;
    int rbase, gbase, bbase;
    public Color scoreColor;
    Bounceable() {
	bounceno = 0;
	counter = topCounter;
    }
    public void setColor(Graphics g) {
	g.setColor(cols[bounceno]);
	if (bounceno > 0 && counter-- <= 0) {
	    bounceno--;
	    counter = topCounter;
	}
    }
    public void bounceIt() {
	bounceno = numcols-1;
    }
    public void setColorBase(int rx, int gx, int bx) {
	rbase = rx;
	gbase = gx;
	bbase = bx;
	int i;
	cols = new Color[numcols];
	for (i = 0; i != numcols; i++) {
	    int val = 255*i/(numcols-1);
	    cols[i] = new Color(rbase*val, gbase*val, bbase*val);
	}
	scoreColor = cols[numcols-1];
    }
}

// this should be "player", probably
class Paddle extends Bounceable {
    int varpos;
    int fixedpos;
    int targetpos;
    public int scorePos;
    int width, dir, rangemin, rangemax, thick;
    public int score;
    public Paddle(int vp, int fp, int sp, int w) {
    	varpos = vp;
	fixedpos = fp;
	scorePos = sp;
	width = w;
	dir = 5;
	thick = 8;
	targetpos = vp;
    }
    public Rectangle getRect() {
	return new Rectangle(varpos, fixedpos-thick/2, width, thick);
    }
    public void setTarget(int x) {
	targetpos = x-width/2;
    }
    public int getVarPos() {
	return varpos;
    }
    public int getFixedPos() {
	return fixedpos;
    }
    public int getWidth() {
	return width;
    }
    void move(int x) {
    	varpos = x;
	if (varpos < rangemin)
	    varpos = rangemin;
	if (varpos > rangemax)
	    varpos = rangemax;
    }
    public void move() {
	int d = targetpos - varpos;
	if (d < -dir)
	    d = -dir;
	if (d > dir)
	    d = dir;
	move(varpos+d);
    }
    public void setRange(int mn, int mx) {
	rangemin = mn;
	rangemax = mx-width+1;
    }
    public void draw(Graphics g) {
        setColor(g);
    	g.fillRect(varpos, fixedpos-thick/2, width, thick);
    }
}

class Ball extends Bounceable {
    Point pos, startPos;
    Pong game;
    int dx, dy;
    int sz;
    int xrangemin, xrangemax, yrangemin, yrangemax;
    public boolean inPlay;
    Random random;
    public Ball(Point ps, int s, Pong g) {
	pos = ps;
	startPos = new Point(pos.x, pos.y);
	game = g;
	sz = s;
	dx = 4;
	dy = 6;
	inPlay = false;
	random = new Random();
	setColorBase(1, 1, 0);
    }
    public void startPlay() {
	if (inPlay)
	    return;
	inPlay = true;
	dx = 4;
	dy = 6;
	// XXX better way to copy?
	pos = new Point(startPos.x, startPos.y);
    }
    int randBounce(int d) {
	int dd = (d < 0) ? -1 : 1;
	int n = random.nextInt();
	if (n <= 0)
	    n = 1-n;
	return ((n % 6)+2) * -dd;
    }
    public boolean bounce(Paddle pd) {
	int fp = pd.getFixedPos();
	int vp = pd.getVarPos();
	int w = pd.getWidth();
	if (pos.x < vp || pos.x >= vp+w)
	    return false;
	boolean bounced = false;
	Rectangle xrg = new Rectangle(pos.x-sz/2, pos.y-sz/2, sz, sz);
	Rectangle prg = pd.getRect();
	xrg.translate(dx, 0);
	if (prg.intersects(xrg)) {
	    dx = randBounce(dx);
	    bounced = true;
	}
	Rectangle yrg = new Rectangle(pos.x-sz/2, pos.y-sz/2, sz, sz);
	yrg.translate(dx, dy);
	if (prg.intersects(yrg)) {
	    dy = randBounce(dy);
	    bounceIt();
	    bounced = true;
	}
	return bounced;
    }
    public void move() {
	if (!inPlay)
	    return;
	pos.x += dx;
	pos.y += dy;
	if (pos.x < xrangemin) {
	    pos.x = xrangemin;
	    dx = -dx;
	}
	if (pos.x > xrangemax) {
	    pos.x = xrangemax;
	    dx = -dx;
	}
	if (pos.y < yrangemin) {
	    inPlay = false;
	    game.updateScore(0);
	}
	if (pos.y > yrangemax) {
	    inPlay = false;
	    game.updateScore(1);
	}
    }
    public int getPaddlePos() {
	return pos.x;
    }
    public void setRange(int mnx, int mxx, int mny, int mxy) {
	xrangemin = mnx+sz/2;
	xrangemax = mxx-sz/2;
	yrangemin = mny+sz/2;
	yrangemax = mxy-sz/2;
    }
    public void draw(Graphics g) {
	if (!inPlay)
	    return;
        setColor(g);
	g.fillOval(pos.x-sz/2, pos.y-sz/2, sz, sz);
    }
}

public class Pong extends Applet implements Runnable {
    
    Thread engine = null;

    Paddle paddles[];
    Ball ball;
    Dimension winSize;
    Font scoreFont, smallBannerFont, largeBannerFont;
    Image dbimage;
    
    public static final int defaultPause = 10;
    int pause;
    
    public String getAppletInfo() {
	return "Pong by Paul Falstad";
    }

    public void init() {
	setBackground(Color.white);
        Dimension d = winSize = size();
	paddles = new Paddle[2];
    	paddles[0] = new Paddle(10, 40, 120, 50);
    	paddles[1] = new Paddle(d.width/2, d.height-40, d.height-120, 40);
	paddles[0].setRange(0, d.width-1);
	paddles[1].setRange(0, d.width-1);
	paddles[0].setColorBase(1, 0, 0);
	paddles[1].setColorBase(0, 0, 1);
	ball = new Ball(new Point(d.width/2, d.height/2), 9, this);
	ball.setRange(0, d.width-1, 0, d.height-1);
	pause = defaultPause;
	scoreFont = new Font("TimesRoman", Font.BOLD, 36);
	largeBannerFont = new Font("TimesRoman", Font.BOLD, 48);
	smallBannerFont = new Font("TimesRoman", Font.BOLD, 16);
	dbimage = createImage(d.width, d.height);
	try {
	    String param = getParameter("PAUSE");
	    if (param != null)
		pause = Integer.parseInt(param);
	} catch (Exception e) { }
    }

    public void updateScore(int which) {
	paddles[1-which].score++;
    }

    public void run() {
	while (true) {
	    try {
		for (int i = 0; i != 3; i++)
		    step();
		repaint();
    		Thread.currentThread().sleep(pause);
	    } catch (Exception e) {}
	}
    }

    public void step() {
	paddles[1].setTarget(ball.getPaddlePos());
	paddles[0].move();
	if (ball.inPlay)
	    paddles[1].move();
	if (ball.bounce(paddles[0]))
	    paddles[0].bounceIt();
	if (ball.bounce(paddles[1]))
	    paddles[1].bounceIt();
	ball.move();
    }

    public void centerString(Graphics g, FontMetrics fm, String str, int ypos) {
	g.drawString(str, (winSize.width-fm.stringWidth(str))/2, ypos);
    }

    public void drawBanner(Graphics g) {
	g.setFont(largeBannerFont);
	FontMetrics fm = g.getFontMetrics();
	g.setColor(Color.red);
	centerString(g, fm, "PONG", 100);
	g.setColor(Color.blue);
	g.setFont(scoreFont);
	fm = g.getFontMetrics();
	centerString(g, fm, "by Paul Falstad", 160);
	g.setFont(smallBannerFont);
	fm = g.getFontMetrics();
	centerString(g, fm, "www.falstad.com", 190);
	g.setColor(Color.black);
	centerString(g, fm, "Press mouse button to start", 300);
    }

    public void update(Graphics realg) {
	Graphics g = dbimage.getGraphics();
	g.setColor(getBackground());
	g.fillRect(0, 0, winSize.width, winSize.height);
	g.setColor(getForeground());
	if (!ball.inPlay) {
	    g.setFont(scoreFont);
	    FontMetrics fm = g.getFontMetrics();
	    if (paddles[0].score == 0 && paddles[1].score == 0)
		drawBanner(g);
	    else
		for (int i = 0; i != 2; i++) {
        	    String score = Integer.toString(paddles[i].score);
		    g.setColor(paddles[i].scoreColor);
		    centerString(g, fm, score, paddles[i].scorePos);
		}
	}
	for (int i = 0; i != 2; i++)
    	    paddles[i].draw(g);
	ball.draw(g);
	realg.drawImage(dbimage, 0, 0, this);
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

    public boolean handleEvent(Event evt) {
	if (evt.id == Event.MOUSE_MOVE) {
	    paddles[0].setTarget(evt.x);
	    return true;
	} else if (evt.id == Event.MOUSE_DOWN) {
	    ball.startPlay();
	    return true;
	} else {	    
	    return super.handleEvent(evt);
	}
    }
    
}

