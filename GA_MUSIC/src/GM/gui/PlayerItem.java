package GM.gui;

import GM.music.*;

import java.awt.*;
import javax.swing.*;
import GM.music.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
//import com.borland.jbcl.layout.VerticalFlowLayout;
import javax.swing.border.TitledBorder;
import GM.gui.tweak.ToggleTweaker;
import java.util.*;
import javax.swing.event.MouseInputAdapter;
import java.awt.event.MouseEvent;

public class PlayerItem extends JPanel implements Observer {

    JButton close = new JButton();

    JButton voice = new JButton();
    JButton mutate = new JButton();
    JToggleButton calib = new JToggleButton();
    JToggleButton mute;
    JToggleButton solo;
    Color selectedColor;
    Color defaultColor;
    Player player;
    Calibrator calibrator;
    boolean selected = false;

    public PlayerItem(Player p) {
        this.player = p;
        jbInit();
        player.addObserver(this);
        addMouseListener(new MouseInputAdapter() {
            public void mousePressed(MouseEvent e) {
           //     System.out.println(" HELLO FROM EDIT ");
                player.getBand().setSelectedPlayer(player);
            }

        });
        defaultColor = getBackground();
        selectedColor = Color.PINK;
        // paramPanel = new VoiceCntrl(player.getVoice());
    }

    public void update(Observable o, Object arg) {
        assert (o == player);
        if (arg == Message.KILLED) {
            player.deleteObserver(this);
        }
        if (arg == Message.MODIFIED) {
            voice.setText(player.getName());
        }
        if (selected != player.isSelected()) {
            repaint();
        }
    }


    public void paintComponent(Graphics g) {
   //     System.out.println(" REPAINT ");
        super.paintComponent(g);

        if (player.isSelected()) {
            if (!selected) {
           //     System.out.println(" SELECTED ");

                setBackground(selectedColor);
                selected = true;
            }
        } else {
            if (selected) {
            //    System.out.println(" NOT SELECTED ");
                setBackground(defaultColor);
                selected = false;
            }
        }
    }

    void jbInit() {
        close.setText("X");
        close.setToolTipText("Delete this player and it's phrases (no undo)");
        close.addActionListener(new PlayerPanel_close_actionAdapter(this));
        this.setLayout(new GridBagLayout());

        int dy = Layout.trackHeight;

        setPreferredSize(new Dimension(Layout.playerViewWidth, dy));
        setMaximumSize(new Dimension(10000, dy));
        setMinimumSize(new Dimension(50, dy));
        //  topPanel.setLayout(gridBagLayout2);
        voice.setText(player.getName());
        voice.setToolTipText("Click to slect this player");
        setToolTipText("Click to slect this player");
        voice.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                player.getBand().setSelectedPlayer(player);
           //     TopFrame.the().voiceSelectFrame.setVisible(true);
            }
        });

        //mutate.setText("mutate");
        //mutate.addActionListener(new PlayerPanel_voice_actionAdapter(this));

        mute = new ToggleTweaker(player.mute);
        mute.setToolTipText("Mute this voice");
//        mute.setText("M");
//        mute.addActionListener(new PlayerPanel_mute_actionAdapter(this));

        //     edit.setText("e");
        //     edit.addActionListener(new PlayerPanel_edit_actionAdapter(this));

        calib.setText("calib");
        calib.addActionListener(new PlayerPanel_calib_actionAdapter(this));

        solo = new ToggleTweaker(player.solo);
        mute.setToolTipText("Solo this voice");
        solo.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                player.getBand().setSelectedPlayer(player);
            }
        });

        this.setBorder(BorderFactory.createLineBorder(Color.black));

        int ii = 0;
        add(voice, new GridBagConstraints(ii++, 0, 1, 1, 1.0, 0.0
                                          , GridBagConstraints.WEST,
                                          GridBagConstraints.HORIZONTAL,
                                          new Insets(0, 0, 0, 0), 0, 0));

        add(solo, new GridBagConstraints(ii++, 0, 1, 1, 0.0, 0.0
                                         , GridBagConstraints.EAST,
                                         GridBagConstraints.NONE,
                                         new Insets(0, 0, 0, 0), 0, 0));
        add(mute, new GridBagConstraints(ii++, 0, 1, 1, 0.0, 0.0
                                         , GridBagConstraints.EAST,
                                         GridBagConstraints.NONE,
                                         new Insets(0, 0, 0, 0), 0, 0));

        add(close, new GridBagConstraints(ii++, 0, 1, 1, 0.0, 0.0
                                          , GridBagConstraints.EAST,
                                          GridBagConstraints.NONE,
                                          new Insets(0, 0, 0, 0), 0, 0));

    }


    public void calib_actionPerformed(ActionEvent e) {
        System.out.println(" HELLO FROM CALIB ");
        JToggleButton but = (JToggleButton) e.getSource();
        if (but.isSelected()) {
            player.getBand().silenceAll();
            calibrator = new Calibrator(player);
            new Thread(calibrator).start();
        } else {
            player.getBand().updatePlayerState();
            calibrator.halt();
        }

    }

    public Player getPlayer() {
        return player;
    }


    public void close_actionPerformed(ActionEvent e) {
        Container p = getParent();
        p.remove(this);
        p.validate();
        p.repaint();
        // Song song=player.getBand().getSong();
        //   player.kill();
        player.getBand().removePlayer(player);
    }


    public void mutate_actionPerformed(ActionEvent e) {

        // player.createPhrase();
        //   MutateFrame frame = new MutateFrame();
        //   frame.setPlayer(player);
        //      player.start();
        synchronized(player) {
            ((Phrase) (player.getPhrases().elementAt(0))).mutate(); //@TODO
        }
    }

}


class PlayerPanel_voice_actionAdapter implements ActionListener {
    private PlayerItem adaptee;
    PlayerPanel_voice_actionAdapter(PlayerItem adaptee) {
        this.adaptee = adaptee;
    }

    public void actionPerformed(ActionEvent e) {

        adaptee.mutate_actionPerformed(e);
    }
}


class PlayerPanel_close_actionAdapter implements ActionListener {
    private PlayerItem adaptee;
    PlayerPanel_close_actionAdapter(PlayerItem adaptee) {
        this.adaptee = adaptee;
    }

    public void actionPerformed(ActionEvent e) {
        adaptee.close_actionPerformed(e);
    }
}


class PlayerPanel_calib_actionAdapter implements ActionListener {
    private PlayerItem adaptee;
    PlayerPanel_calib_actionAdapter(PlayerItem adaptee) {
        this.adaptee = adaptee;
    }

    public void actionPerformed(ActionEvent e) {
        adaptee.calib_actionPerformed(e);
    }
}
