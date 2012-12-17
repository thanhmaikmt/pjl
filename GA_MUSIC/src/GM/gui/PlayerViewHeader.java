package GM.gui;

import javax.swing.*;
import java.awt.Container;
import java.awt.event.*;
import java.util.*;
import GM.music.*;
import javax.swing.border.TitledBorder;
import java.awt.*;
import java.awt.geom.*;
import GM.javasound.*;

public class PlayerViewHeader extends JPanel implements Observer, ActionListener {

    JButton unMute = new JButton();
    JButton unSolo = new JButton();
    JButton addPlayer= new JButton();

    public PlayerViewHeader() {

        try {
            jbInit();
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }


    public void actionPerformed(ActionEvent e) {
        Object src = e.getSource();

        if (src == unMute) {
            Simphoney.getSong().getBand().unMuteAll();
        } else if (src == unSolo) {
            Simphoney.getSong().getBand().unSoloAll();
        } else if (src== addPlayer) {
            try {
                Simphoney.getSong().createPlayer(Hub.the().createDefaultVoice());
            } catch (Exception ex) {
                ex.printStackTrace();
            }
        }

    }



    public void update(Observable o, Object cmd) {
      //  System.out.println("Overview.update: " + o + " " + cmd);
    }

    private void jbInit() throws Exception {

        this.setLayout(new GridBagLayout());

        unMute.setText("|M|");
        unMute.addActionListener(this);

        unSolo.setText("|S|");
        unSolo.addActionListener(this);

        addPlayer.setText("New Player");
        addPlayer.addActionListener(this);


        JButton but;

        add(but=new JButton(new AbstractAction("New Part") {
            public void actionPerformed(ActionEvent e) {
                if (Simphoney.getSong() == null) {
                    return;
                }
                Simphoney.getSong().newPart();
            }
        }));

        int i=0;
        int row=0;

        add(but,new GridBagConstraints(i++, row++, 3, 1, 0.1, 0.0
                                       , GridBagConstraints.CENTER, GridBagConstraints.HORIZONTAL,
                                       new Insets(0, 0, 0, 0), 0, 0));

        i=0;
        add(addPlayer, new GridBagConstraints(i++, row, 1, 1, 0.1, 0.0
                    , GridBagConstraints.CENTER, GridBagConstraints.HORIZONTAL,
                    new Insets(0, 0, 0, 0), 0, 0));

        add(unSolo, new GridBagConstraints(i++, row, 1, 1, 0.1, 0.0
                , GridBagConstraints.CENTER, GridBagConstraints.NONE,
                new Insets(0, 0, 0, 0), 0, 0));

        add(unMute, new GridBagConstraints(i++, row, 1, 1, 0.1, 0.0
                , GridBagConstraints.CENTER, GridBagConstraints.NONE,
                new Insets(0, 0, 0, 0), 0, 0));


         this.setBorder(BorderFactory.createLineBorder(Color.black));

    }
}

