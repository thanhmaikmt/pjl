package GM.gui;

import java.awt.event.ActionEvent;
import GM.music.Time;
import javax.swing.JPanel;
import java.awt.event.ActionListener;
import java.awt.Color;
import java.awt.Component;
import java.awt.Dimension;
import GM.music.SongSequencer;
import GM.music.Conductor;
import GM.music.Song;
import GM.music.Simphoney;

public class TimeLinePanel extends JPanel {


    JPanel cp = new JPanel();

    Cursor cursor;

    TimeLinePanel() {
        setLayout(null);
        cursor = new Cursor();
        add(cp);
        setBackground(Color.black);
    }


    void myValidate() {
        setPreferredSize(new Dimension(getParent().getWidth(),
                                       Layout.timeLineHeight));
        getParent().validate();
        repaint();
    }


    private class Cursor implements ActionListener {

        int pos = -1;

        Cursor() {
            new javax.swing.Timer(100, this).start();
        }


        public synchronized void actionPerformed(ActionEvent e) {

            //   System.out.println(" XAE " + pos);
            if (!Conductor.isRunning()) {
                return;
            }
            Song song = Simphoney.getSong();
            Time t = null;

            if (song != null) {
                SongSequencer seq = song.getSequencer();
                if (seq != null) {
                    t = seq.getDisplayTime();
                }
            }

            int newpos = 0;
            if (t != null) {
                newpos = (int) (t.getTick() * Layout.pianoRollScale);
            }
            if (newpos == pos) {
                return;
            }
            //            repaint();
            pos = newpos;
            if (pos < 0) {
                return;
            }
            cp.setBounds(newpos, 0, 1, getHeight());
            cp.setVisible(true);
            repaint();
        }

    }

}
