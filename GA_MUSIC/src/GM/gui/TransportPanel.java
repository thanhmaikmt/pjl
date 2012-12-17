package GM.gui;

import javax.swing.JPanel;
import java.awt.event.ActionEvent;
import javax.swing.JLabel;
import javax.swing.JToggleButton;
import java.awt.event.ActionListener;
import GM.music.Hub;
import java.awt.Dimension;
import GM.gui.tweak.SpinTweaker;
import GM.gui.tweak.ToggleTweaker;
import GM.music.Conductor;
import GM.music.Simphoney;

public class TransportPanel extends JPanel {
    ToggleTweaker startStop = new ToggleTweaker(Conductor.state, "quiet","play");
    SpinTweaker tempoCntrl = new SpinTweaker(Conductor.tempoBPM);

    public TransportPanel() {
        JToggleButton but;
        JPanel ctrl = new JPanel();
        ctrl.add(startStop);
       // ctrl.add(new JLabel("tempo"));
        tempoCntrl.getComponent().setMaximumSize(new Dimension(40, 30));
        ctrl.add(tempoCntrl.getComponent());

        ctrl.add(but = new JToggleButton("Loop"));
        but.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                JToggleButton but = (JToggleButton) e.getSource();
                if (Simphoney.getSong() == null) return;
                Simphoney.getSong().setLoopSelected(but.isSelected());
            }
        });

        add(ctrl); //,BorderLayout.WEST);

        if (Hub.the().getFeed() != null) {
            PeakPanel peakPanel = new PeakPanel();
            add(peakPanel); //,BorderLayout.EAST);
            peakPanel.setFeed(Hub.the().getFeed());
            peakPanel.start();
        }
    }
}
