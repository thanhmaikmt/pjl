package GM.gui;
import javax.swing.*;
import java.awt.BorderLayout;
import java.awt.Dimension;
import GM.music.*;
import java.awt.*;
import java.util.*;

public class PlayerView extends JPanel implements Observer  {
  //  JScrollPane jScrollPane1 = new JScrollPane();
  //  JPanel content;
  Box.Filler filler;

    public PlayerView() {
        //setLayout(new BorderLayout());
     //   add(jScrollPane1, java.awt.BorderLayout.CENTER);
       // content=new JPanel();
     //   content.
       // jScrollPane1.getViewport().add(content);
       setLayout(new BoxLayout(this,BoxLayout.Y_AXIS));
       filler = new Box.Filler(new Dimension(Layout.playerViewWidth,0),
                          new Dimension(Layout.playerViewWidth,0),
                          new Dimension(Layout.playerViewWidth,0));

       add(filler);
//       setPreferredSize(new Dimension(1,Layout.playerViewWidth));
    }



    public void update(Observable o, Object arg) {

        Message mess=(Message)arg;
    //    System.out.println(o+ " " + mess);

        if (mess.str.equals("AddPlayer")) {
            Player player = (Player)mess.o;
                //getContent().add(new PlayerItem(player));
                add(new PlayerItem(player));
                TopFrame.the().pianoRoll.validate();
       //     validate();
        //    repaint();
        } else {
        //   mess.unhandled(this,o,arg);
        }

    }

    void rebuild(Band band) {
      //  content.removeAll();
      removeAll();

      add(filler);
      synchronized(band) {
          Iterator<Player> iter = band.getPlayers().iterator();

          //        while(iter.hasNext()) content.add(new PlayerItem(iter.next()));
          while (iter.hasNext())
              add(new PlayerItem(iter.next()));
      }
      TopFrame.the().pianoRoll.validate();
     // validate();
     // repaint();

    }

    void addPlayer(Player player) {
        //getContent().add(new PlayerItem(player));
        add(new PlayerItem(player));
        TopFrame.the().pianoRoll.validate();
       // validate();
      //  repaint();
    }


    public int indexOf(Player p) {
      //  Container content=getContent();
        int n = getComponentCount();
        for(int i=0;i<n;i++) {
            PlayerItem pp=(PlayerItem)getComponent(i);
            if (pp.getPlayer() == p) return i-1;
        }
        return -1;
    }



   // public JPanel getContent() { return content; }

}
