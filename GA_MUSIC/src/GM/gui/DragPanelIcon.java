package GM.gui;

import javax.swing.*;
import java.awt.event.*;
import javax.swing.border.Border;
import java.awt.Cursor;

public class DragPanelIcon extends JLabel {


    Border unSelectedBorder=BorderFactory.createRaisedBevelBorder();//BevelBorder.RAISED,Color.WHITE,Color.LIGHT_GRAY);
    Border selectedBorder=BorderFactory.createLoweredBevelBorder();//
    public DragPanelIcon() {

        setIcon(new ImageIcon(GM.gui.DragPanelIcon.class.getResource(
            "editcopy16.png")));
        setOpaque(false);
        setBorder(unSelectedBorder);
        setCursor(new Cursor(Cursor.MOVE_CURSOR));
    }

    public void setSelected(boolean yes) {
      //  System.out.println("DragPanel select "+ yes);
        if (yes)  setBorder(selectedBorder);
        else setBorder(unSelectedBorder);
    }
}
