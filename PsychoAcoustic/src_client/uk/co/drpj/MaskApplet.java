package uk.co.drpj;

import java.awt.BorderLayout;

import java.awt.Color;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.JApplet;
import javax.swing.UIManager;

//@AppletServerClass
public class MaskApplet extends JApplet {

    private static final long serialVersionUID = 1L;
    // AudioSystem audioSystem;
    private MaskPanel1 panel;

    @Override
    public void init() {
        super.init();


        System.out.println(" INIT ");
    }

    @Override
    public void start() {
        System.out.println("START");

//        for (Object key : UIManager.getDefaults().keySet()) {
//            System.out.println(key);
//        }
        UIManager.put("Panel.background", Color.WHITE);

        if (panel != null) {
            return;
        }
        setLayout(new BorderLayout());
        try {
            panel = new MaskPanel1();
        } catch (Exception ex) {
            Logger.getLogger(MaskApplet.class.getName()).log(Level.SEVERE, null, ex);
        }
        setContentPane(panel);
        // panel.setBackground(Color.WHITE);
        panel.start();
        //    validate();

    }

    @Override
    public void stop() {
        System.out.println(" STOP ");
        if (panel == null) {
            return;
        }
        panel.dispose();
        //audioSystem.stop();
        remove(panel);
        panel = null;
    }

    @Override
    public void destroy() {
        stop();
        super.destroy();
    }
}
