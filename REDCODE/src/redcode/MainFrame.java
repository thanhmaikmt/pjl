/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package redcode;

import java.net.URL;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.JFrame;

/**
 *
 * @author pjl
 */
public class MainFrame {

    
    public static void main(String args[] ){
        Machine mach=null;
        try {
            mach = new Machine(30);
        } catch (RedCodeParseException ex) {
            Logger.getLogger(MainFrame.class.getName()).log(Level.SEVERE, null, ex);
        }
        JFrame frame =new JFrame();
        MainPanel p=new MainPanel(mach,null);
        frame.setContentPane(p);

        frame.setSize(800,600);
        frame.pack();

        frame.setVisible(true);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

    }

}
