package GM.gui;

import java.awt.*;

import javax.swing.*;
import java.awt.BorderLayout;

public class LeftMiddlePanel extends JPanel {


    JSplitPane splitPane;


    public LeftMiddlePanel() {
        try {
            jbInit();
        } catch (Exception exception) {
            exception.printStackTrace();
        }
    }

    private void jbInit() throws Exception {
        setLayout(new GridBagLayout());


        TopFrame tf = TopFrame.the();

        JPanel top = new JPanel();
        top.setLayout(new BorderLayout());
        top.add(tf.scaleTweakPanel, BorderLayout.NORTH);

        top.add(tf.voiceCntrl, BorderLayout.CENTER);

        add(top, new GridBagConstraints(0, 0, 1, 1, 1.0, 0.0
                                        , GridBagConstraints.NORTH,
                                        GridBagConstraints.HORIZONTAL,
                                        new Insets(0, 0, 0, 0), 0, 0));

        add(tf.voiceSelectPanel, new GridBagConstraints(0, 1, 1, 1, 1.0, 0.1
                , GridBagConstraints.CENTER,
                GridBagConstraints.BOTH,
                new Insets(0, 0, 0, 0), 0, 0));

        JPanel bot = new JPanel();
        bot.add(TopFrame.the().transportPanel);
        this.add(bot, new GridBagConstraints(0, 2, 1, 1, 1.0, 0.0
                                             , GridBagConstraints.CENTER,
                                             GridBagConstraints.HORIZONTAL,
                                             new Insets(0, 0, 0, 0), 0, 0));

    }


}
