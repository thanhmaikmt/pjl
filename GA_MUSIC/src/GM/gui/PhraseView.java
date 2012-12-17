package GM.gui;

import java.awt.Rectangle;

import java.awt.Color;
import javax.swing.*;

import GM.music.*;
import GM.music.Time;
import GM.music.Player;
import GM.music.Phrase;
import java.awt.Dimension;
import java.awt.Container;
import java.awt.Component;
import javax.swing.JComponent;
import java.util.*;


public class PhraseView extends DragPanel  {


    PhraseView() {
        setLayout(null);
        setBackground(Color.GRAY);
    }

    void detachAll() {
        Component[] o = getComponents();
        for (int i = 0; i < o.length; i++) {
            if (o[i] instanceof PhraseItem) {
                PhraseItem pp = (PhraseItem) o[i];
                pp.phrase.deleteObserver(pp);
                remove(pp);
                pp.invalidate();
            }
        }
    }

    public Dimension getPreferredSize() {
        return bounds.getSize();
    }

    synchronized public void rePosition() {
      //  bounds.setBounds(new Rectangle(0, 0, 0, 0));

        int n = getComponentCount();
        for (int i = 0; i < n; i++) {
            Object o = getComponent(i);
            if (o instanceof PhraseItem) {
                PhraseItem pp = (PhraseItem) o;
                positionPhrasePanel(pp);
            }

        }
        myValidate();
    }

    synchronized void addPhrasePanel(PhraseItem panel) {
        positionPhrasePanel(panel);
        add(panel);
    }

    int [] locOf(PhraseItem item) {
        Phrase phrase=item.phrase;
        return Simphoney.getSong().posOfPhrase(phrase);
    }


    void positionPhrasePanel(PhraseItem phrasePanel) {
        Phrase phrase = phrasePanel.phrase;
        int x1 = (int) phrase.getStart().getTick();
        int x2 = (int) (phrase.getEnd().subtract(phrase.getStart()).getTick());
        Player p = phrase.getPlayer();
        assert(p != null);
        assert(p.getBand() != null);
        int pos = p.getBand().posOfPlayer(p);
        int yoff = 0; //LayoutData.headerHeight;
        int dy = Layout.trackHeight;
        Rectangle rect = new Rectangle((int) (x1 * Layout.pianoRollScale)+1,
                                       yoff + pos * dy+1,
                                       (int) (x2 * Layout.pianoRollScale)-2,
                                       dy-2);
        //      System.out.println(x1 + " " + pos*dy + " " +x2 + " "+(pos+1)*dy);
        phrasePanel.setBounds(rect);
        bounds.add(rect);
    }


    void setDragPhrase(Phrase phrase) {
        Component[] o = getComponents();
        for (int i = 0; i < o.length; i++) {
            if (o[i] instanceof PhraseItem) {
                PhraseItem pp = (PhraseItem) o[i];
                if (pp.phrase == phrase) {
                    Rectangle r=pp.getBounds();
                    dragPointScreen[0] = r.x;
                    dragPointScreen[1] = r.y;
                    dragPointLogical = Simphoney.getSong().posOfPhrase(phrase);
                }
            }
        }
    }

    void myValidate() {
     //   System.out.println("PhraseView myValidate ");
        if (!selector.dragging) {
            Phrase dragPhrase = Simphoney.getSong().dragPhrase();
            if (dragPhrase == null)
                dragPanel.setVisible(false);
            else {
                setDragPhrase(dragPhrase);
                rePositionDragPanel();
            }
        }

        setComponentZOrder(dragPanel,1);
        setComponentZOrder(selector,0);

        TopFrame.the().pianoRoll.validate();
        repaint();
    }

     public void releaseDrag(int x,int y) {
         dragPanel.setSelected(false);
         Simphoney.getSong().copySelectedPhrasesTo(dragPointLogical[0],dragPointLogical[1]);
     }

     void setDragToAt(int x,int y) {

         Rectangle bbb=new Rectangle();
         if ( dragItem!=null && dragItem.getBounds().contains(x,y)) return;

         int ix=indexOfPartAt(x);
         System.out.println( ix + " " + tmpX);
         dragPointLogical[0]=ix;
         dragPointScreen[0]=tmpX;
         int iy=indexOfPlayerAt(y);
         dragPointLogical[1]=iy;
         dragPointScreen[1]=tmpY;
     }




     int indexOfPlayerAt(int y) {
         int ii = y/Layout.trackHeight;
         tmpY = ii*Layout.trackHeight;
         return ii;
     }

}
