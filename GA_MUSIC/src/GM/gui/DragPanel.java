package GM.gui;

import javax.swing.JPanel;
import java.awt.Rectangle;
import java.util.Iterator;
import GM.music.Part;
import GM.music.Simphoney;

abstract public class DragPanel extends JPanel implements DragListener {


    RectSelector selector;
    Rectangle bounds = new Rectangle(0,0);
    DragPanelIcon dragPanel;
    JPanel dragItem;

    int    dragPointScreen [] = new int[2];
    int    dragPointLogical [] = new int[2];
    int tmpX;
    int tmpY;

    DragPanel() {
        dragPanel = new DragPanelIcon();
        selector = new RectSelector(this,dragPanel);
        add(selector);
        addMouseListener(selector);
        addMouseMotionListener(selector);
        add(dragPanel);
    }

    int tickToX(long tick) {
        return (int)(Layout.pianoRollScale*tick);
    }

    void rePositionDragPanel() {
          int x1= dragPointScreen[0];
          int y1= dragPointScreen[1];
          Rectangle rect
                  = new Rectangle(
                      x1 ,
                      y1 ,
                      Layout.dragPanelWidth,
                      Layout.dragPanelHeight);
          dragPanel.setBounds(rect);
          dragPanel.setVisible(true);
          setComponentZOrder(dragPanel,1);
          setComponentZOrder(selector,0);
    }

   // abstract void releaseDrag(int x,int y);

    abstract void setDragToAt(int x,int y);

    public void setDragPoint(int x,int y) {

        setDragToAt(x,y);
        dragPanel.setSelected(true);
        rePositionDragPanel();
    }

     int indexOfPartAt(int x) {
         tmpX=0;
         Iterator<Part> iter = Simphoney.getSong().getParts().iterator();
         int cc=0;
         while(iter.hasNext()) {
             int x1 = tickToX(iter.next().getEnd().getTick());
             if (x <= x1) {
                 return cc;
             }
             tmpX=x1;
             cc++;
         }

         return cc;
     }

     abstract void myValidate();

     void addToBounds(Rectangle rect) {
        bounds.add(rect);
        myValidate();
    }

}
