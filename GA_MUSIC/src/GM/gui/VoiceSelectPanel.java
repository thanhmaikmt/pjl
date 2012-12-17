package GM.gui;

import java.awt.*;

import javax.swing.*;
import GM.music.Player;
import java.awt.event.ActionEvent;
import GM.music.GMPatch;
//import GM.javasound.Hub;
import GM.music.Voice;
import java.awt.event.ActionListener;
import GM.music.Song;


/**
 * <p>Title: </p>
 *
 * <p>Description: </p>
 *
 * <p>Copyright: Copyright (c) 2005</p>
 *
 * <p>Company: </p>
 *
 * @author not attributable
 * @version 1.0
 */
public class VoiceSelectPanel extends JPanel {
    JScrollPane jScrollPane1 = new JScrollPane();
    VoiceTree voiceTree;

    public VoiceSelectPanel() {
        try {
            jbInit();
        } catch (Exception exception) {
            exception.printStackTrace();
        }
        doLayout();
    }

    private void jbInit() throws Exception {
        setLayout(new BorderLayout());

        voiceTree = new VoiceTree();

      //  setSize(new Dimension(200, 500));
        add(jScrollPane1, BorderLayout.CENTER);
        jScrollPane1.getViewport().add(voiceTree);

//        add(voiceTree,BorderLayout.CENTER);

/*
        JButton createVoice = new JButton("Create Voice");

        createVoice.addActionListener(new ActionListener() {

            public void actionPerformed(ActionEvent e) {
                GMPatch patch = voiceTree.getSelectedPatch();
                if (patch != null)
                    Simphoney.getSong().createPlayer(patch);
            }

        });
  */
     //   add(createVoice, BorderLayout.SOUTH);
/*
        JButton setVoice = new JButton("Select");

        setVoice.addActionListener(new ActionListener() {

            public void actionPerformed(ActionEvent e) {
                Song song = Simphoney.getSong();
                Player player = song.getBand().getSelectedPlayer();
                if (player == null)
                    return;
                GMPatch patch = voiceTree.getSelectedPatch();
                if (patch == null)
                    return;
                try {
                    Voice voice = Pallete.createVoice(patch);
                    player.setVoice(voice);
                } catch (Exception ex) {
                    ex.printStackTrace();
                }

            }

        });

        add(setVoice, BorderLayout.NORTH);
*/
  }
}
