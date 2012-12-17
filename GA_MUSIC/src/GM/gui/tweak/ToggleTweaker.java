package GM.gui.tweak;
import GM.tweak.*;
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.*;
import java.util.*;

public class ToggleTweaker extends JToggleButton implements ChangeListener , Observer {


    Tweakable t;

    String on;
    String off;


    public ToggleTweaker(Tweakable t) {
        this(t,t.getLabel(),t.getLabel());
      }


    public ToggleTweaker(Tweakable t,String on,String off) {
        this.t=t;
        this.on=on;
        this.off=off;
        if (t.isOn()) {
            setText(on);
        } else {
            setText(off);
        }
        setSelected(t.isOn());
        addChangeListener(this);
        t.addObserver(this);
    }

    public void update(Observable o, Object arg) {
        setSelected(t.isOn());
    }

    public void stateChanged(ChangeEvent e) {
	// System.out.println(" HI " + t.isOn());
        boolean isOn = t.isOn();
	if (isSelected() && !isOn ){
            t.setNumber(1);
            setText(on);
         //   setSelected(true);
        } else if (!isSelected() && isOn) {
            t.setNumber(0);
            setText(off);
       //     setSelected(false);
        }
    }

}
