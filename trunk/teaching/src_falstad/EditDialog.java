import java.awt.*;
import java.awt.event.*;
import java.text.NumberFormat;
import java.text.DecimalFormat;

interface Editable {
    EditInfo getEditInfo(int n);
    void setEditValue(int n, EditInfo ei);
}

class EditDialog extends Dialog implements AdjustmentListener, ActionListener, ItemListener {
    Editable elm;
    CirSim cframe;
    Button applyButton, okButton;
    EditInfo einfos[];
    int einfocount;
    final int barmax = 1000;
    NumberFormat noCommaFormat;

    EditDialog(Editable ce, CirSim f) {
	super(f, "Edit Component", false);
	cframe = f;
	elm = ce;
	setLayout(new EditDialogLayout());
	einfos = new EditInfo[10];
	noCommaFormat = DecimalFormat.getInstance();
	noCommaFormat.setMaximumFractionDigits(10);
	noCommaFormat.setGroupingUsed(false);
	int i;
	for (i = 0; ; i++) {
	    einfos[i] = elm.getEditInfo(i);
	    if (einfos[i] == null)
		break;
	    EditInfo ei = einfos[i];
	    add(new Label(ei.name));
	    if (ei.choice != null) {
		add(ei.choice);
		ei.choice.addItemListener(this);
	    } else if (ei.checkbox != null) {
		add(ei.checkbox);
		ei.checkbox.addItemListener(this);
	    } else {
		add(ei.textf =
		    new TextField(noCommaFormat.format(ei.value), 10));
		if (ei.text != null)
		    ei.textf.setText(ei.text);
		ei.textf.addActionListener(this);
		if (ei.text == null) {
		    add(ei.bar = new Scrollbar(Scrollbar.HORIZONTAL,
					       50, 10, 0, barmax+2));
		    setBar(ei);
		    ei.bar.addAdjustmentListener(this);
		}
	    }
	}
	einfocount = i;
	add(applyButton = new Button("Apply"));
	applyButton.addActionListener(this);
	add(okButton = new Button("OK"));
	okButton.addActionListener(this);
	Point x = cframe.main.getLocationOnScreen();
	Dimension d = getSize();
	setLocation(x.x + (cframe.winSize.width-d.width)/2,
		    x.y + (cframe.winSize.height-d.height)/2);
    }

    void apply() {
	int i;
	for (i = 0; i != einfocount; i++) {
	    EditInfo ei = einfos[i];
	    if (ei.textf == null)
		continue;
	    if (ei.text == null) {
		try {
		    double d = noCommaFormat.parse(ei.textf.getText()).doubleValue();
		    ei.value = d;
		} catch (Exception ex) { /* ignored */ }
	    }
	    elm.setEditValue(i, ei);
	    if (ei.text == null)
		setBar(ei);
	}
	cframe.needAnalyze();
    }
	
    public void actionPerformed(ActionEvent e) {
	int i;
	Object src = e.getSource();
	for (i = 0; i != einfocount; i++) {
	    EditInfo ei = einfos[i];
	    if (src == ei.textf) {
		if (ei.text == null) {
		    try {
			double d = noCommaFormat.parse(ei.textf.getText()).doubleValue();
			ei.value = d;
		    } catch (Exception ex) { /* ignored */ }
		}
		elm.setEditValue(i, ei);
		if (ei.text == null)
		    setBar(ei);
		cframe.needAnalyze();
	    }
	}
	if (e.getSource() == okButton) {
	    apply();
	    cframe.main.requestFocus();
	    setVisible(false);
	    cframe.editDialog = null;
	}
	if (e.getSource() == applyButton)
	    apply();
    }
	
    public void adjustmentValueChanged(AdjustmentEvent e) {
	Object src = e.getSource();
	int i;
	for (i = 0; i != einfocount; i++) {
	    EditInfo ei = einfos[i];
	    if (ei.bar == src) {
		double v = ei.bar.getValue() / 1000.;
		if (v < 0)
		    v = 0;
		if (v > 1)
		    v = 1;
		ei.value = (ei.maxval-ei.minval)*v + ei.minval;
		if (ei.maxval-ei.minval > 100)
		    ei.value = Math.round(ei.value);
		else
		    ei.value = Math.round(ei.value*100)/100.;
		elm.setEditValue(i, ei);
		ei.textf.setText(noCommaFormat.format(ei.value));
		cframe.needAnalyze();
	    }
	}
    }

    public void itemStateChanged(ItemEvent e) {
	Object src = e.getItemSelectable();
	int i;
	boolean changed = false;
	for (i = 0; i != einfocount; i++) {
	    EditInfo ei = einfos[i];
	    if (ei.choice == src || ei.checkbox == src) {
		elm.setEditValue(i, ei);
		if (ei.newDialog)
		    changed = true;
		cframe.needAnalyze();
	    }
	}
	if (changed) {
	    setVisible(false);
	    cframe.editDialog = new EditDialog(elm, cframe);
	    cframe.editDialog.show();
	}
    }
	
    public boolean handleEvent(Event ev) {
	if (ev.id == Event.WINDOW_DESTROY) {
	    cframe.main.requestFocus();
	    setVisible(false);
	    cframe.editDialog = null;
	    return true;
	}
	return super.handleEvent(ev);
    }

    void setBar(EditInfo ei) {
	int x = (int) (barmax*(ei.value-ei.minval)/(ei.maxval-ei.minval));
	ei.bar.setValue(x);
    }
}

