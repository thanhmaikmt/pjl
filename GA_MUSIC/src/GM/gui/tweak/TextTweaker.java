package GM.gui.tweak;
import GM.tweak.*;
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.*;
import java.text.*;

class TextTweaker  implements ActionListener {

    Tweakable t;
    JTextField textField;


/*

    TextTweaker(TweakerPanel p,Tweakable t) {
	this.t=t;
	int len = t.getMaximum().toString().length();
	textField = new JTextField(String.valueOf(t.getNumber()),len);
	textField.addActionListener(this);
	p.add(new JLabel(t.getLabel()),textField);
    }
*/

    public void actionPerformed(ActionEvent e) {

	//	Object o=e.getSource();
	//	Object v = ((JFormattedTextField)o).getValue();
	t.set(textField.getText()); //.toString());
	textField.setText(t.toString());

    }


}
