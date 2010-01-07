
import java.awt.Choice;

class EditOptions implements Editable {
    CirSim sim;
    public EditOptions(CirSim s) { sim = s; }
    public EditInfo getEditInfo(int n) {
	if (n == 0)
	    return new EditInfo("Time step size (ns)", sim.timeStep*1e9, 0, 0);
	if (n == 1)
	    return new EditInfo("Range for voltage color (V)",
				CircuitElm.voltageRange, 0, 0);

       if (n == 2) { // PJL

        // 0 - just colour
        // 1 - just main line
        // 2 - colour + line
        // 3 - lines main + forward and back
        // 4 - 3 + colour
            Choice choice = new Choice();
            choice.add("Coloured");
            choice.add("Line");
            choice.add("Colour & Line ");
            choice.add("Line with Forward and Back");
            choice.add("Colour & Line with Forward and Back");
            choice.select(TransLineElm.globalDispType);
            EditInfo inf = new EditInfo("TL Voltage Display", 0, 0, 0);
            inf.choice = choice;
            return inf;
        }
	return null;
    }
    public void setEditValue(int n, EditInfo ei) {
	if (n == 0 && ei.value > 0)
	    sim.timeStep = ei.value * 1e-9;
	if (n == 1 && ei.value > 0)
	    CircuitElm.voltageRange = ei.value;
        if (n == 2) { //PJL
            TransLineElm.globalDispType = ei.choice.getSelectedIndex();
        }
    }
};
