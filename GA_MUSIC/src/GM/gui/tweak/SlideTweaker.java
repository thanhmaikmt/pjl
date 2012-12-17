package GM.gui.tweak;
import GM.tweak.*;

import javax.swing.*;
import javax.swing.event.*;
import java.awt.*;


public class SlideTweaker implements ChangeListener, TweakComponent  {


    JPanel panel;
    JSlider slider;
    Tweakable t;
    JTextField   txt;

    public SlideTweaker(Tweakable t) {
        this.t=t;
        panel= new JPanel(new GridLayout(1,2));
        int n=t.getNumber().intValue();
        slider = new JSlider(((Number)t.getMinimum()).intValue(),
                             ((Number)t.getMaximum()).intValue(),
                             n);
        panel.add(slider);
        slider.addChangeListener(this);
        txt=new JTextField(String.valueOf(n));
        int textWMin=3;
        int textH=1;  ;
        txt.setMinimumSize(new Dimension(textWMin, textH));
        panel.add(txt);


//        if (p!= null) p.add(new JLabel(t.getLabel()),slider);
        panel.validate();
    }


/*
    public SlideTweaker(Tweakable t) {
        this.t=t;
        int n=t.getNumber().intValue();
        slider = new JSlider(((Number)t.getMinimum()).intValue(),
                             ((Number)t.getMaximum()).intValue(),
                             n);
        slider.addChangeListener(this);
    }
*/

    public JComponent  getComponent() { return panel; }

    public void stateChanged(ChangeEvent e) {
        int n=slider.getValue();
	txt.setText(String.valueOf(n));
        t.setNumber(new Integer(n));
    }
}
