import java.awt.*;
import java.util.StringTokenizer;

    class CapacitorElm extends CircuitElm {
	double capacitance;
	double compResistance, voltdiff;
	Point plate1[], plate2[];
	public CapacitorElm(int xx, int yy) {
	    super(xx, yy);
	    capacitance = 1e-5;
	}
	public CapacitorElm(int xa, int ya, int xb, int yb, int f,
			    StringTokenizer st) {
	    super(xa, ya, xb, yb, f);
	    capacitance = new Double(st.nextToken()).doubleValue();
	    voltdiff = new Double(st.nextToken()).doubleValue();
	}
	void setNodeVoltage(int n, double c) {
	    super.setNodeVoltage(n, c);
	    voltdiff = volts[0]-volts[1];
	}
	void reset() {
	    current = curcount = 0;
	    // put small charge on caps when reset to start oscillators
	    voltdiff = 1e-3;
	}
	int getDumpType() { return 'c'; }
	String dump() {
	    return super.dump() + " " + capacitance + " " + voltdiff;
	}
	void setPoints() {
	    super.setPoints();
	    double f = (dn/2-4)/dn;
	    // calc leads
	    lead1 = interpPoint(point1, point2, f);
	    lead2 = interpPoint(point1, point2, 1-f);
	    // calc plates
	    plate1 = newPointArray(2);
	    plate2 = newPointArray(2);
	    interpPoint2(point1, point2, plate1[0], plate1[1], f, 12);
	    interpPoint2(point1, point2, plate2[0], plate2[1], 1-f, 12);
	}
	
	void draw(Graphics g) {
	    int hs = 12;
	    setBbox(point1, point2, hs);
	    
	    // draw first lead and plate
	    setVoltageColor(g, volts[0]);
	    drawThickLine(g, point1, lead1);
	    setPowerColor(g, false);
	    drawThickLine(g, plate1[0], plate1[1]);
	    if (sim.powerCheckItem.getState())
		g.setColor(Color.gray);

	    // draw second lead and plate
	    setVoltageColor(g, volts[1]);
	    drawThickLine(g, point2, lead2);
	    setPowerColor(g, false);
	    drawThickLine(g, plate2[0], plate2[1]);
	    
	    updateDotCount();
	    if (sim.dragElm != this) {
		drawDots(g, point1, lead1, curcount);
		drawDots(g, point2, lead2, -curcount);
	    }
	    drawPosts(g);
	    if (sim.showValuesCheckItem.getState()) {
		String s = getShortUnitText(capacitance, "F");
		drawValues(g, s, hs);
	    }
	}
	void stamp() {
	    // capacitor companion model using trapezoidal approximation
	    // (Thevenin equivalent) consists of a voltage source in
	    // series with a resistor
	    sim.stampVoltageSource(nodes[0], nodes[2], voltSource);
	    compResistance = sim.timeStep/(2*capacitance);
	    sim.stampResistor(nodes[2], nodes[1], compResistance);
	}
	void startIteration() {
	    voltSourceValue = -voltdiff-current*compResistance;
	}
	double voltSourceValue;
	void doStep() {
	    sim.updateVoltageSource(nodes[0], nodes[2], voltSource,
				voltSourceValue);
 	}
	int getVoltageSourceCount() { return 1; }
	int getInternalNodeCount() { return 1; }
	void getInfo(String arr[]) {
	    arr[0] = "capacitor";
	    getBasicInfo(arr);
	    arr[3] = "C = " + getUnitText(capacitance, "F");
	    arr[4] = "P = " + getUnitText(getPower(), "W");
	    //double v = getVoltageDiff();
	    //arr[4] = "U = " + getUnitText(.5*capacitance*v*v, "J");
	}
	public EditInfo getEditInfo(int n) {
	    if (n == 0)
		return new EditInfo("Capacitance (uF)", capacitance*1e6, 0, 0);
	    return null;
	}
	public void setEditValue(int n, EditInfo ei) {
	    capacitance = ei.value*1e-6;
	}
	boolean needsShortcut() { return true; }
    }
