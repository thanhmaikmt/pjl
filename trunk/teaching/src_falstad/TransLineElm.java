
import java.awt.*;
import java.util.StringTokenizer;

class TransLineElm extends CircuitElm {

    double delay, imped;
    double atten;          // PJL attenuation  of line (Vout/Vin)
    double attenArray[];   // precalculated attenuation along the line
    double voltageL[], voltageR[];
    int lenSteps, ptr, width;
    static int globalDispType = 1;  // PJL   should this really live here ?
    int myDispType = 2;               // we need to mess about when this changes
    private int sepFactor = 5;

    public TransLineElm(int xx, int yy) {
        super(xx, yy);
        delay = 1000 * sim.timeStep;
        imped = 75;
        atten = 1.0;
        noDiagonal = true;
        reset();
    }

    public TransLineElm(int xa, int ya, int xb, int yb, int f,
            StringTokenizer st) {
        super(xa, ya, xb, yb, f);
        delay = new Double(st.nextToken()).doubleValue();
        imped = new Double(st.nextToken()).doubleValue();
        width = new Integer(st.nextToken()).intValue();
        double attenInDb = new Double(st.nextToken()).doubleValue();
        setAttenuationFromDBPerMeter(attenInDb);

        // next slot is for resistance (losses), which is not implemented
        // st.nextToken();
        noDiagonal = true;

        reset();
    }

    int getDumpType() {
        return 171;
    }

    int getPostCount() {
        return 4;
    }

    int getInternalNodeCount() {
        return 2;
    }

    String dump() {
        return super.dump() + " " + delay + " " + imped + " " + width + " " + getAttenuationInDBperMeter();
    }

    void drag(int xx, int yy) {
        xx = sim.snapGrid(xx);
        yy = sim.snapGrid(yy);
        int w1 = max(sim.gridSize, abs(yy - y));
        int w2 = max(sim.gridSize, abs(xx - x));
        if (w1 > w2) {
            xx = x;
            width = w2;
        } else {
            yy = y;
            width = w1;
        }
        x2 = xx;
        y2 = yy;
        setPoints();
    }
    Point posts[], inner[];

    void reset() {
        if (sim.timeStep == 0) {
            return;
        }
        lenSteps = (int) (delay / sim.timeStep);
        System.out.println(lenSteps + " steps");
        if (lenSteps > 100000) {
            voltageL = voltageR = attenArray = null;
        } else {
            voltageL = new double[lenSteps];
            voltageR = new double[lenSteps];
            attenArray = new double[lenSteps];  // for the GUI PJL
            setAttenArray();
        }
        ptr = 0;
        super.reset();
    }

    /**
     * PJL
     *
     * recalculate attenuation along the line
     *
     */
    void setAttenArray() {

        attenArray[0] = 1.0;
        double attenPerSection = Math.pow(atten, 1.0 / lenSteps);

        for (int i = 1; i < lenSteps; i++) {
            attenArray[i] = attenArray[i - 1] * attenPerSection;
        }
    }

    void setPoints() {
        super.setPoints();
        int ds = (dy == 0) ? sign(dx) : -sign(dy);
        Point p3 = interpPoint(point1, point2, 0, -width * ds);
        Point p4 = interpPoint(point1, point2, 1, -width * ds);

        posts = new Point[]{p3, p4, point1, point2};

        int sep = (int) (((float) sim.gridSize) / sepFactor);
        Point p5 = interpPoint(point1, point2, 0, -(width / 2 - sep) * ds);
        Point p6 = interpPoint(point1, point2, 1, -(width / 2 - sep) * ds);
        Point p7 = interpPoint(point1, point2, 0, -(width / 2 + sep) * ds);
        Point p8 = interpPoint(point1, point2, 1, -(width / 2 + sep) * ds);

        // we number the posts like this because we want the lower-numbered
        // points to be on the bottom, so that if some of them are unconnected
        // (which is often true) then the bottom ones will get automatically
        // attached to ground.
       
        inner = new Point[]{p7, p8, p5, p6};
    }
    // temporary for GUI
    final Point lst = new Point();
    final Point lstF = new Point();
    final Point lstB = new Point();
    final Point nxt = new Point();
    final Point tmp = new Point();
    final Point mid = new Point();
    final Point nxtF = new Point();
    final Point nxtB = new Point();

    void draw(Graphics g) {

        // PJL see if we have change display mode

        boolean colour = false;
        boolean line = false;
        boolean waves = false;

        // 0 - just colour
        // 1 - just main line
        // 2 - colour + line
        // 3 - lines main + forward and back
        // 4 - 3 + colour
        switch (globalDispType) {

            case 0:
                colour = true;
                break;
            case 1:
                line = true;
                break;
            case 2:
                line = true;
                colour = true;
                break;
            case 3:
                line = true;
                waves = true;
                break;
            case 4:
                line = true;
                waves = true;
                colour = true;
                break;

        }

        if (line && sepFactor != 5) {
            System.out.println(" Line ");
            sepFactor = 5;
            setPoints();
        } else if (!line && sepFactor != 2) {
            System.out.println(" NOT Line ");

            sepFactor = 2;
            setPoints();
        }


        setBbox(posts[0], posts[3], 0);
        int segments = (int) (dn / 2);
        int ix0 = ptr - 1 + lenSteps;
        double segf = 1. / segments;
        int i;
        g.setColor(Color.darkGray);
        g.fillRect(inner[2].x, inner[2].y,
                inner[1].x - inner[2].x + 2, inner[1].y - inner[2].y + 2);
        for (i = 0; i != 4; i++) {
            setVoltageColor(g, volts[i]);
            drawThickLine(g, posts[i], inner[i]);
        }

        if (colour) {
            if (voltageL != null) {
                for (i = 0; i != segments; i++) {
                    int ii1 = (lenSteps * i) / segments;   // for attenuation
                    int ii2 = lenSteps - ii1 - 1;

                    int ix1 = (ix0 - lenSteps * i / segments) % lenSteps;
                    int ix2 = (ix0 - lenSteps * (segments - 1 - i) / segments) % lenSteps;
                    double vF = voltageL[ix1] * attenArray[ii1];
                    double vB = voltageR[ix2] * attenArray[ii2];

                    double v = vF + vB;

                    interpPoint(inner[0], inner[1], ps1, i * segf);
                    interpPoint(inner[2], inner[3], ps2, i * segf);

                    setVoltageColor(g, v / 2.0);
                    g.drawLine(ps1.x, ps1.y, ps2.x, ps2.y);
                    interpPoint(inner[2], inner[3], tmp, (i + 1) * segf);
                    drawThickLine(g, tmp, ps2);
                    interpPoint(inner[0], inner[1], tmp, (i + 1) * segf);
                    drawThickLine(g, tmp, ps1);

                }
            }
        }

        if (line) {
            int segmentsL=(int)dn;  // need finer resolution
            double segfL=1.0/segmentsL;
            for (i = 0; i != segmentsL; i++) {
                int ii1 = (lenSteps * i) / segmentsL;   // for attenuation
                int ii2 = lenSteps - ii1 - 1;

                int ix1 = (ix0 - lenSteps * i / segmentsL) % lenSteps;
                int ix2 = (ix0 - lenSteps * (segmentsL - 1 - i) / segmentsL) % lenSteps;
                double vF = voltageL[ix1] * attenArray[ii1];
                double vB = voltageR[ix2] * attenArray[ii2];

                double v = vF + vB;

                interpPoint(inner[0], inner[1], ps1, i * segfL);
                interpPoint(inner[2], inner[3], ps2, i * segfL);


                g.setColor(Color.WHITE);
                double h = -getVoltageHeight(v) * sepFactor;
                interpPoint(ps1, ps2, mid, 0.5);
                interpPoint(mid, ps1, nxt, h);
                if (i > 0) {
                    drawThickLine(g,lst, nxt);
                }
                
                lst.x = nxt.x;
                lst.y = nxt.y;

                if (waves) {
                    g.setColor(Color.YELLOW);
                    h = -getVoltageHeight(vF) * sepFactor;
                    interpPoint(mid, ps1, nxtF, h);
                    if (i > 0) {
                        g.drawLine(lstF.x, lstF.y, nxtF.x, nxtF.y);
                    }
                    lstF.x = nxtF.x;
                    lstF.y = nxtF.y;

                    g.setColor(Color.CYAN);
                    h = -getVoltageHeight(vB) * sepFactor;
                    interpPoint(mid, ps1, nxtB, h);
                    if (i > 0) {
                        g.drawLine(lstB.x, lstB.y, nxtB.x, nxtB.y);
                    }
                    lstB.x = nxtB.x;
                    lstB.y = nxtB.y;
                }
            }
        }


        drawPosts(g);

        curCount1 = updateDotCount(-current1, curCount1);
        curCount2 = updateDotCount(current2, curCount2);
        if (sim.dragElm != this) {
            drawDots(g, posts[0], inner[0], curCount1);
            drawDots(g, posts[2], inner[2], -curCount1);
            drawDots(g, posts[1], inner[1], -curCount2);
            drawDots(g, posts[3], inner[3], curCount2);
        }
    }
    int voltSource1, voltSource2;
    double current1, current2, curCount1, curCount2;

    void setVoltageSource(int n, int v) {
        if (n == 0) {
            voltSource1 = v;
        } else {
            voltSource2 = v;
        }
    }

    void setCurrent(int v, double c) {
        if (v == voltSource1) {
            current1 = c;
        } else {
            current2 = c;
        }
    }

    void stamp() {
        sim.stampVoltageSource(nodes[4], nodes[0], voltSource1);
        sim.stampVoltageSource(nodes[5], nodes[1], voltSource2);
        sim.stampResistor(nodes[2], nodes[4], imped);
        sim.stampResistor(nodes[3], nodes[5], imped);
    }

    void startIteration() {
        // calculate voltages, currents sent over wire
        if (voltageL == null) {
            sim.stop("Transmission line delay too large!", this);
            return;
        }
        voltageL[ptr] = volts[2] - volts[0] + volts[2] - volts[4];
        voltageR[ptr] = volts[3] - volts[1] + volts[3] - volts[5];
        //System.out.println(volts[2] + " " + volts[0] + " " + (volts[2]-volts[0]) + " " + (imped*current1) + " " + voltageL[ptr]);
	/*System.out.println("sending fwd  " + currentL[ptr] + " " + current1);
        System.out.println("sending back " + currentR[ptr] + " " + current2);*/
        //System.out.println("sending back " + voltageR[ptr]);
        ptr = (ptr + 1) % lenSteps;
    }

    void doStep() {
        if (voltageL == null) {
            sim.stop("Transmission line delay too large!", this);
            return;
        }

        // Modified 2 lines to do the attenuation (a bit of a guess but seems to work)
        sim.updateVoltageSource(nodes[4], nodes[0], voltSource1, -voltageR[ptr] * atten);
        sim.updateVoltageSource(nodes[5], nodes[1], voltSource2, -voltageL[ptr] * atten);
        if (Math.abs(volts[0]) > 1e-5 || Math.abs(volts[1]) > 1e-5) {
            sim.stop("Need to ground transmission line!", this);
            return;
        }
    }

    Point getPost(int n) {
        return posts[n];
    }

    //double getVoltageDiff() { return volts[0]; }
    int getVoltageSourceCount() {
        return 2;
    }

    boolean hasGroundConnection(int n1) {
        return false;
    }

    boolean getConnection(int n1, int n2) {
        return false;
        /*if (comparePair(n1, n2, 0, 1))
        return true;
        if (comparePair(n1, n2, 2, 3))
        return true;
        return false;*/
    }

    // PJL helper
    double getAttenuationInDBperMeter() {
        double val = -20.0 * Math.log10(atten) / 2.9979e8 / delay;
        if (val <= 0.0) {
            return 0.0;   // get rid of annoying -0.0 in GUI !!!
        } else {
            return val;
        }
    }

    void setAttenuationFromDBPerMeter(double dBPerMeter) {
        atten = Math.pow(10, -dBPerMeter * 2.9979e8 * delay / 20.0);
    }
    //---------------------------

    void getInfo(String arr[]) {
        arr[0] = "transmission line";
        arr[1] = getUnitText(imped, sim.ohmString);
        arr[2] = "length = " + getUnitText(2.9979e8 * delay, "m");
        arr[3] = "delay = " + getUnitText(delay, "s");
        arr[4] = "atten =" + getUnitText(getAttenuationInDBperMeter(), "dB/m");
    }

    public EditInfo getEditInfo(int n) {
        if (n == 0) {
            return new EditInfo("Delay (ns)", delay * 1e9, 0, 0);
        }
        if (n == 1) {
            return new EditInfo("Impedance (ohms)", imped, 0, 0);
        }

        if (n == 2) { // PJL
            // double attenDB=20*Math.log10(atten);
            return new EditInfo("Attenuation (dB/m)", getAttenuationInDBperMeter(), 0, 20);
        }



        return null;
    }

    @Override
    public void setEditValue(int n, EditInfo ei) {
        if (n == 0) {
            delay = ei.value * 1e-9;
            reset();
        }
        if (n == 1) {
            imped = ei.value;
            reset();  //    do we need to reset here ?
        }

        if (n == 2) {
            // PJL maybe -ve  should not be allowed ?
            setAttenuationFromDBPerMeter(ei.value);
            reset();
        }
    }

    /**
     *  PJL
     * @param volts
     * @return height for display
     *
     */
    double getVoltageHeight(double volts) {
        if (!sim.voltsCheckItem.getState()) {
            return 0.0f;
        }

        return (volts) / (voltageRange);
    }
}

