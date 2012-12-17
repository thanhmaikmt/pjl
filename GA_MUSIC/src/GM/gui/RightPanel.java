package GM.gui;

import java.awt.*;

import javax.swing.*;
import java.awt.BorderLayout;

public class RightPanel extends JPanel {

    public RightPanel() {
        try {
            jbInit();
        } catch (Exception exception) {
            exception.printStackTrace();
        }
    }

    private void jbInit() throws Exception {

        setLayout(new GridBagLayout());

        TopFrame tf=TopFrame.the();

        this.add(tf.partCntrl,new GridBagConstraints(0, 0, 1, 1, 1.0, 0.0
                , GridBagConstraints.CENTER, GridBagConstraints.HORIZONTAL,
                new Insets(0, 0, 0, 0), 0, 0));


        this.add(tf.pianoRoll,new GridBagConstraints(0, 1, 1, 1, 1.0, 1.0
                , GridBagConstraints.CENTER, GridBagConstraints.BOTH,
                new Insets(0, 0, 0, 0), 0, 0));

        this.add(tf.phraseCntrl,new GridBagConstraints(0, 2, 1, 1, 1.0, 0.0
                , GridBagConstraints.CENTER, GridBagConstraints.HORIZONTAL,
                new Insets(0, 0, 0, 0), 0, 0));

    }

/*
    public void paintComponent(Graphics g) {
        super.paintComponent(g);
        Layout.phraseCntrlHeight= phraseCntrl.getHeight();
        TopFrame.the().leftMiddlePanel.repaint();
    }
*/

}

