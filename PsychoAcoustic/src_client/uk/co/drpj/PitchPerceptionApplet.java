package uk.co.drpj;

import uk.co.drpj.audio.AudioSystem;
import uk.co.drpj.psycho.experiment.MyAudioClient;
import java.awt.BorderLayout;

import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.JApplet;
import javax.swing.JPanel;


import uk.co.drpj.psycho.experiment.pitch.PitchExperiment;
import uk.co.drpj.psycho.experiment.ThreeChoiceExperiment;
import uk.org.toot.audio.server.AudioServer;


//@AppletServerClass
public class PitchPerceptionApplet extends JApplet {

    private static final long serialVersionUID = 1L;

    AudioSystem audioSystem;
    private JPanel panel;

    @Override
    public void init() {
     //   super.init();

    }

    @Override
    public void start() {
        System.out.println("START");

        setLayout(new BorderLayout());

        audioSystem = AudioSystem.instance();
        AudioServer server = audioSystem.getServer();
        MyAudioClient client = new MyAudioClient(audioSystem.getOut(), server.getSampleRate());
        server.setClient(client);

        String e[] = {"Pitch", "LowFreqQ", "Grain"};

        ThreeChoiceExperiment exp;

        exp = new PitchExperiment(client);
        panel = exp.getGUIPanel();
        add(panel);
        try {
            audioSystem.start();
        } catch (Exception ex) {
            Logger.getLogger(PitchPerceptionApplet.class.getName()).log(Level.SEVERE, null, ex);
        }

    }

    @Override
    public void stop() {
        System.out.println("STOP");
        audioSystem.stop();
        remove(panel);
    }

    @Override
    public void destroy() {

        stop();
        super.destroy();
    }
}
