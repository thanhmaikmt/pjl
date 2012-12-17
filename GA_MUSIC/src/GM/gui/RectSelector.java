package GM.gui;

import javax.swing.JComponent;
import java.awt.Rectangle;
import javax.swing.JPanel;
import java.awt.event.MouseMotionListener;
import java.awt.event.MouseListener;
import java.awt.event.MouseEvent;
import java.awt.Color;
import java.awt.Graphics;
import java.awt.Component;
import GM.music.Simphoney;

class RectSelector extends JPanel implements MouseMotionListener, MouseListener {


    Rectangle selectedRect = null;

    Rectangle currentRect = null;
    Rectangle rectToDraw = null;
    Rectangle previousRectDrawn = new Rectangle();
    JComponent parent;
    JComponent dragPanel;
    DragListener dragListener;
    boolean dragging=false;

    RectSelector(JComponent parent,JComponent dragPanel) {
        this.parent = parent;
        this.dragPanel=dragPanel;
        this.dragListener=(DragListener)parent;
        setOpaque(false);
    }

    synchronized void display(boolean yes) {
//            if (getParent() == null ) return;
        setSize(parent.getSize());
        setVisible(yes);
        if (yes) {
            repaint();
        }
    }


    private void updateDrawableRect(int compWidth, int compHeight) {
        int x = currentRect.x;
        int y = currentRect.y;
        int width = currentRect.width;
        int height = currentRect.height;

        //Make the width and height positive, if necessary.
        if (width < 0) {
            width = 0 - width;
            x = x - width + 1;
            if (x < 0) {
                width += x;
                x = 0;
            }
        }
        if (height < 0) {
            height = 0 - height;
            y = y - height + 1;
            if (y < 0) {
                height += y;
                y = 0;
            }
        }

        //The rectangle shouldn't extend past the drawing area.
        if ((x + width) > compWidth) {
            width = compWidth - x;
        }
        if ((y + height) > compHeight) {
            height = compHeight - y;
        }

        //Update rectToDraw after saving old value.
        if (rectToDraw != null) {
            previousRectDrawn.setBounds(
                    rectToDraw.x, rectToDraw.y,
                    rectToDraw.width, rectToDraw.height);
            rectToDraw.setBounds(x, y, width, height);
        } else {
            rectToDraw = new Rectangle(x, y, width, height);
        }
    }

    void updateSize(MouseEvent e) {
        int x = e.getX();
        int y = e.getY();
        currentRect.setSize(x - currentRect.x,
                            y - currentRect.y);
        updateDrawableRect(getWidth(), getHeight());
        Rectangle totalRepaint = rectToDraw.union(previousRectDrawn);
        repaint(totalRepaint.x, totalRepaint.y,
                totalRepaint.width, totalRepaint.height);
    }

    protected synchronized void paintComponent(Graphics g) {
        super.paintComponent(g); //paints the background and image
        g.setXORMode(Color.WHITE); //Color of line varies

        if (currentRect != null) {
            g.drawRect(rectToDraw.x, rectToDraw.y,
                       rectToDraw.width - 1, rectToDraw.height - 1);
        }

        g.setPaintMode();

    }


    synchronized void selectNotInRect(boolean yes) {
        int n = parent.getComponentCount();
        Rectangle pb = new Rectangle();
        for (int i = 0; i < n; i++) {
            Component o = parent.getComponent(i);
            if (o instanceof RectSelectable) {
                RectSelectable rs = (RectSelectable) o;
                o.getBounds(pb);
                if (!rectToDraw.intersects(pb)) {
                    rs.setSelected(yes);
                    // selectedRect = selectedRect.union(pb);
                }
            }
        }
    }

    synchronized void selectInRect(boolean yes) {
        int n = parent.getComponentCount();
        Rectangle pb = new Rectangle();
        for (int i = 0; i < n; i++) {
            Component o = parent.getComponent(i);
            if (o instanceof RectSelectable) {
//                PhraseItem pp = (PhraseItem) o;
                RectSelectable rs = (RectSelectable) o;

                o.getBounds(pb);
                if (rectToDraw.intersects(pb)) {
                    rs.setSelected(yes);
                    selectedRect = selectedRect.union(pb);
                }
            }
        }
    }

    synchronized void selectContainsPoint(int x,int y,boolean yes) {
        int n = parent.getComponentCount();
        Rectangle pb = new Rectangle();
        for (int i = 0; i < n; i++) {
            Component o = parent.getComponent(i);
            if (o instanceof RectSelectable) {
//                PhraseItem pp = (PhraseItem) o;
                RectSelectable rs = (RectSelectable) o;

                o.getBounds(pb);
                if (pb.contains(x,y)) {
                    rs.setSelected(yes);
                  if (selectedRect != null)   selectedRect = selectedRect.union(pb);
                }
            }
        }
    }



    public void mousePressed(MouseEvent e) {
       //  System.out.println(" mPressed");
          int x = e.getX();
          int y = e.getY();
          if (dragPanel.isVisible() && dragPanel.getBounds().contains(x,y)) {
              dragging = true;
              dragListener.setDragPoint(x,y);
              return;
          }

          currentRect = new Rectangle(x, y, 0, 0);
          updateDrawableRect(getWidth(), getHeight());
          selectNotInRect(false);
          selectInRect(true);
          selectContainsPoint(x,y,true);
          display(true);
          Simphoney.getSong().notifySelectionChange();
    }

    public void mouseDragged(MouseEvent e) {
     //   System.out.println(" mDragged");
      if (!dragging)   updateSize(e);
      else dragListener.setDragPoint(e.getX(),e.getY());
        //  selectInRect(true);
        //  selectNotInRect(false);
    }


    public void mouseReleased(MouseEvent e) {
     //   System.out.println(" mRelease");
     if (dragging) {
         dragListener.releaseDrag(e.getX(),e.getY());
         dragging=false;
         return;
     }

     selectedRect = new Rectangle();
        //    updateSize(e);
        display(false);
        selectNotInRect(false);
        selectInRect(true);
        selectContainsPoint(e.getX(),e.getY(),true);
        currentRect = null;
        Simphoney.getSong().notifySelectionChange();
    }

    public void mouseMoved(MouseEvent e) {}

    public void mouseExited(MouseEvent e) {}

    public void mouseEntered(MouseEvent e) {}

    public void mouseClicked(MouseEvent e) {
     //   System.out.println(" mClicked");
        /*
                 if (currentRect!=null) return;
                 int x = e.getX();
                 int y = e.getY();
                 currentRect = new Rectangle(x, y, 1, 1);
                 updateDrawableRect(getWidth(), getHeight());
                 selectInRect(true);
                 selectNotInRect(false);
                 display(true);
         */
    }
}
