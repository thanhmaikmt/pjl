package GM.gui.tweak;
import GM.tweak.*;
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.*;
import java.text.*;
import java.util.*;

public class SpinListTweaker extends JPanel implements ChangeListener, Observer , TweakComponent  {


    TweakableList t;
    SpinnerListModel model;
    public JSpinner spin;

    public SpinListTweaker(TweakableList t) {
	this.t=t;
        t.addObserver(this);
	model= new SpinnerListModel(t.getList());
        spin=new JSpinner(model);
// 	model =   (SpinnerNumberModel)spin.getModel();
// 	model.setValue(t.getNumber());
// 	model.setMinimum((Comparable)t.getMinimum());
// 	model.setMaximum((Comparable)t.getMaximum());

	spin.addChangeListener(this);


    }

    public JComponent  getComponent() { return spin;}


    public void update(Observable o,Object arg) {
        model.setValue(t.getObject());
    }

    public void stateChanged(ChangeEvent e) {
	// System.out.println(" HI from spin  list --- " + model.getValue());
	t.set(model.getValue().toString());
        model.setValue(t.getObject());
    }
}
