package GM.gui.tweak;
import GM.tweak.*;
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.*;
import java.text.*;
import java.util.*;
import GM.music.Message;

public class SpinTweaker extends JPanel implements ChangeListener, Observer {


    Tweakable t;
    SpinnerNumberModel model;
    public JSpinner spin;


    public SpinTweaker(Tweakable t) {
	this.t=t;
        t.addObserver(this);
	model=
	    new SpinnerNumberModel(t.getNumber(),(Comparable)t.getMinimum(),
				   (Comparable)t.getMaximum(),
				   t.getStepSize());
	 spin=new JSpinner(model);
// 	model =   (SpinnerNumberModel)spin.getModel();
// 	model.setValue(t.getNumber());
// 	model.setMinimum((Comparable)t.getMinimum());
// 	model.setMaximum((Comparable)t.getMaximum());

	spin.addChangeListener(this);

 	//if (p!=null) p.add(new JLabel(t.getLabel()),spin);
    }

    public JComponent  getComponent() { return spin;}


    public void update(Observable o,Object arg) {
        if (arg instanceof Message) {
            if (arg == Message.ENABLE) {
                spin.setEnabled(true);
            } else if (arg == Message.DISABLE) {
                spin.setEnabled(false);

            }
        } else {
            model.setValue(t.getNumber());
        }
    }

    public void stateChanged(ChangeEvent e) {
	// System.out.println(" HI from spin" );
	t.setNumber(model.getNumber());
	model.setValue(t.getNumber());
    }
}
