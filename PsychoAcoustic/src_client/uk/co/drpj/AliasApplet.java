package uk.co.drpj;

import java.awt.BorderLayout;

import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.JApplet;




//@AppletServerClass
public class AliasApplet extends JApplet {

    private static final long serialVersionUID = 1L;

  // AudioSystem audioSystem;
    private AliasPanel panel;

    @Override
    public void init() {
        super.init();
        System.out.println(" INIT ");
    }

    @Override
    public void start() {
        System.out.println("START");
        if (panel != null) return;
        setLayout(new BorderLayout());
        try {
            panel = new AliasPanel();
        } catch (Exception ex) {
            Logger.getLogger(AliasApplet.class.getName()).log(Level.SEVERE, null, ex);
        }
        setContentPane(panel);

        panel.start();
    //    validate();
  
    }

    @Override
    public void stop() {
    System.out.println(" STOP ");
    if (panel == null) return;
        panel.dispose();
        //audioSystem.stop();
        remove(panel);
        panel=null;
    }

    @Override
    public void destroy() {
        stop();
        super.destroy();
    }
}
