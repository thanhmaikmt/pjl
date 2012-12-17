package GM.music;

import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import GM.gui.TopFrame;

public class PlayTimer implements ActionListener {

    static long playTime;

    public PlayTimer() {
       // new javax.swing.Timer(1000,this).start();
    }

    static public void reset() {
        playTime=0;
        TopFrame.the().setFrameTitle();
    }
    public void actionPerformed(ActionEvent e) {
        if (Conductor.the() == null ) return;
        if (Conductor.the().isMute()) return;
        if (Simphoney.getSong() == null) return;
        if (Simphoney.getSong().getId() <= 0 ) return;
        playTime += 1;
        if (TopFrame.the() == null) return;
        TopFrame.the().setFrameTitle();

    }

    static public long getPlayTime() { return playTime; }
}
