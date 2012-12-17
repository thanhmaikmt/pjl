package GM.gui;

import javax.swing.JFrame;

public class VoiceSelectFrame extends JFrame {
    VoiceSelectPanel voiceSelectPanel;
    public VoiceSelectFrame() {
        voiceSelectPanel=new VoiceSelectPanel();
        setContentPane(voiceSelectPanel);
        pack();
    }
}
