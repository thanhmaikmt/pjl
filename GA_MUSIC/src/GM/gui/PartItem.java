package GM.gui;

import javax.swing.*;
import java.awt.Container;

import java.util.*;
import GM.music.*;

import java.awt.Color;
import javax.swing.border.BevelBorder;
import javax.swing.border.Border;
import java.awt.Dimension;

public class PartItem extends PianoRollItem implements  Observer , RectSelectable {
    Part part;

    PianoRoll pianoRoll;
    Border selectedBorder=BorderFactory.createRaisedBevelBorder();
    Border unSelectedBorder=BorderFactory.createLoweredBevelBorder();
//    Border selectedBorder=BorderFactory.createBevelBorder(BevelBorder.RAISED,Color.white,Color.lightGray);
//    Border unSelectedBorder=BorderFactory.createBevelBorder(BevelBorder.RAISED,Color.darkGray,Color.black);

    private PartItem() {

    }

    public PartItem(Part part,PianoRoll pr) {
        this();
        this.part = part;
        this.pianoRoll=pr;

        update(null, Message.CREATEGUI);
        validate();
        part.addObserver(this);
    }


    public void setSelected(boolean yes) {
        part.setSelected(yes);
    }


    public void update(Observable o, Object arg) {

        Message mess= (Message)arg;
        if (mess == Message.KILLED) {
       //     System.out.println("PART KILLED");
            Container p = getParent();
            if (p != null) {
                p.remove(this);
                p.validate();
                p.repaint();
            }
        } else if (mess == Message.SOLO_ON || mess == Message.SOLO_OFF) {
     //       solo.setSelected(part.isSolo());
        } else if (mess == Message.MODIFIED ||
                   mess==Message.CREATEGUI ||
                   mess == Message.SELECT_CHANGE) {
            int hash = part.colorHashCode();
     //       System.out.println("part update " + part + " " + hash);
            setBackground(new Color(hash));
            if (part.isSelected() ) setBorder(selectedBorder);
            else setBorder(unSelectedBorder);

            pianoRoll.partView.myValidate();
        } else {
            mess.unhandled(this,o,arg);
        }

       // pianoRoll.partView.rePosition();

    }

    public Dimension getPreferredSize() {
        return new Dimension((int)(Layout.pianoRollScale*part.getLength().getTick())-2,Layout.partViewHeight-2);
    }

    public Dimension getMinimumSize() {
        return getPreferredSize();
   }

   public Dimension getMaximumSize() {
       return getPreferredSize();
   }




}
