package GM.gui;

import java.awt.Rectangle;

import java.awt.Color;

import javax.swing.JPanel;

import GM.music.*;

import GM.music.Time;

import GM.music.Part;

import java.awt.Dimension;
import java.awt.Container;
import java.awt.Component;
import javax.swing.BoxLayout;
import javax.swing.Box;

//import java.awt.Cursor;


public class PartView extends DragPanel implements DragListener {


    PhraseView phraseView;
    Box.Filler filler;

    PartView(PhraseView phraseView) {
        this.phraseView = phraseView;
        setBackground(Color.black);

        setPreferredSize(new Dimension(10000, Layout.partViewHeight));
        setLayout(null);
    }


    void detachAll() {
        //   System.out.println("PRP DETACH ALL");

        Component[] o = getComponents();
        for (int i = 0; i < o.length; i++) {
            if (o[i] instanceof PartItem) {
                PartItem pp = (PartItem) o[i];
                pp.part.deleteObserver(pp);
                remove(pp);
                pp.invalidate();

            }
        }
        validate();
        repaint();
    }


    public void rePosition() {

        int n = getComponentCount();
        for (int i = 0; i < n; i++) {
            Object o = getComponent(i);
            if (o instanceof PartItem) {
                PartItem pp = (PartItem) o;
                positionPartItem(pp);
            }
        }
        myValidate();
    }

    void positionPartItem(PartItem partPanel) {
        Part part = partPanel.part;
        int x1 = (int) part.getStart().getTick();
        int x2 = (int) (part.getEnd().subtract(part.getStart()).getTick());
        int dy = Layout.partViewHeight;
        Rectangle rect = new Rectangle((int) (x1 * Layout.pianoRollScale) + 1,
                                       1,
                                       (int) (x2 * Layout.pianoRollScale) - 2,
                                       dy - 2);
        //      System.out.println(x1 + " " + pos*dy + " " +x2 + " "+(pos+1)*dy);
        partPanel.setBounds(rect);
//            bounds.add(rect);
    }



    void addPartPanel(PartItem panel) {

        //    System.out.println(" addPartItem " + panel.getPreferredSize());
        //     setPreferredSize(bounds.getSize());
        positionPartItem(panel);
        add(panel);

    //    validate();
    //    repaint();
        phraseView.addToBounds(panel.getBounds());
        myValidate();
    }

    int locOf(PartItem item) {
        Part part = item.part;
        return Simphoney.getSong().posOfPart(part);
    }

    void setDragPart(Part part) {

        Component[] o = getComponents();
        for (int i = 0; i < o.length; i++) {
            if (o[i] instanceof PartItem) {
                PartItem pp = (PartItem) o[i];
                if (pp.part == part) {
                    Rectangle r = pp.getBounds();
                    dragPointScreen[0] = r.x;
                    dragPointScreen[1] = r.y;
                    dragPointLogical[0] = Simphoney.getSong().posOfPart(part);
                }
            }
        }
    }

    void setDstPartAt(int x, int y) {
        if (dragItem != null && dragItem.getBounds().contains(x, y)) {
            return;
        }
        Component[] o = getComponents();
        for (int i = 0; i < o.length; i++) {

            if (o[i] instanceof PartItem) {
                PartItem pp = (PartItem) o[i];
                pp.getBounds().contains(x, y);
                dragItem = pp;
                return;
            }
        }


    }


    public void releaseDrag(int x, int y) {
        dragPanel.setSelected(false);
        Simphoney.getSong().copySelectedPartsTo(dragPointLogical[0]);
    }


    void setDragToAt(int x, int y) {

        Rectangle bbb = new Rectangle();
        if (dragItem != null && dragItem.getBounds().contains(x, y)) {
            return;
        }

        int ix = indexOfPartAt(x);
        System.out.println(ix + " " + tmpX);
        dragPointLogical[0] = ix;
        dragPointScreen[0] = tmpX;
        int iy = 0;
        dragPointLogical[1] = iy;
        dragPointScreen[1] = tmpY;
    }

    void myValidate() {
      //  System.out.println("PartView myValidate ");
        if (!selector.dragging) {
            Part dragPart = Simphoney.getSong().dragPart();
            if (dragPart == null) {
                dragPanel.setVisible(false);
            } else {
                setDragPart(dragPart);
                dragPanel.setVisible(true);
                rePositionDragPanel();
            }
        }

        setComponentZOrder(dragPanel, 1);
        setComponentZOrder(selector, 0);

        TopFrame.the().pianoRoll.validate();
        repaint();
    }


}
