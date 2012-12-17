package GM.gui;

import java.awt.*;
import javax.swing.*;
import GM.music.*;
import GM.jdbc.JDBCConnectDialog;
import GM.music.*;
import GM.jsyn.*;
import GM.javasound.*;

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

public class SimphoneyAppNODB implements SimphoneyAppInterface {

    boolean packFrame = false;

    String user; // = Defaults.user;

   static  SimphoneyAppNODB the;

    static public SimphoneyAppNODB the() { return the; }


    public String  getUser() {
        return user;
    }


    public SimphoneyAppNODB(String user) {

        this.user=user;

        assert(the == null);
        the=this;

        String jversion = System.getProperty("java.version");

        int ans;

        if (false) {
            ans = JOptionPane.showConfirmDialog(null,
                                                    "Your java version is" +
                                                    jversion +
                                                    "\n javasound midi did not work before 1.5.0_03 \n " +
                                                    " Enable javasound midi ? \n"+
                                                    " Say NO if you want to try the JSyn engine. ",
                                                    " Enable javasound midi ?",
                                                    JOptionPane.YES_NO_OPTION);

                System.out.println(ans);

        }else {
            ans = JOptionPane.YES_OPTION;
        }


      //  new JavaSoundHub();
        new JsynHub();

        Simphoney simp=new Simphoney();

        assert(TopFrame.the() == null);
        TopFrame frame = new TopFrame();

        simp.setApp(this);
        frame.setSong(simp.getSong());

/*
        Hub.javasoundMidi = (ans == JOptionPane.YES_OPTION);

        if (!Hub.javasoundMidi) {
            JsynConductor.slave = Hub.javasoundMidi;

            JsynConductor c = JsynConductor.the();

            if (JsynConductor.status == JsynConductor.FAIL) {
                JOptionPane.showMessageDialog(null,
                                              "Problem initializing jsyn.\n Please check installation.\n" +
                                              " visit http://www.softsynth.com/jsyn/ for more info.",
                                              " Error starting jsyn engine",
                                              JOptionPane.INFORMATION_MESSAGE);

                Hub.jsyn = false;

            } else {
                Hub.jsyn = true;
                JsynConductor.slave = Hub.javasoundMidi;
            }
        } else {
            Hub.jsyn = false;
        }

        isRunning = true; /// Crappy hack to get Jbuilder to do design Yuckkkk
        //   System.out.println("A");
        Hub.init();

*/

        // System.out.println("B");

        //   System.out.println("C");

        // Validate frames that have preset sizes
        // Pack frames that have useful preferred size info, e.g. from their layout
        if (packFrame) {
            frame.pack();
        } else {
            frame.validate();
        }

        // Center the window
        Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
    //    frame.setSize(screenSize);
        Dimension frameSize = frame.getSize();
        if (frameSize.height > screenSize.height) {
            frameSize.height = screenSize.height;
        }
        if (frameSize.width > screenSize.width) {
            frameSize.width = screenSize.width;
        }

        Point p = GraphicsEnvironment.getLocalGraphicsEnvironment().
                  getCenterPoint();
        frame.setLocation(p.x - frameSize.width / 2,
                          p.y - frameSize.height / 2);

        frame.setVisible(true);

    }


    public void setSong(Song song) {
        TopFrame.the().setSong(song);
    }

    public void kill() {
        TopFrame.the().kill();
    }
    /**
     * Application entry point.
     *
     * @param args String[]
     */

    static public void connectToDataBase() {

        JDBCConnectDialog dialog= new JDBCConnectDialog(true);

        dialog.setVisible(true);

        dialog.getDataBase();

        /*
        boolean ok = false;
        for (int timeout = 1000; !ok && timeout < 20000; timeout += 1000) {
            for (int i = 0; !ok && i < DataBase.n(); i++) {
                try {
                    db = new DataBase(i, timeout);
                    ok = true;
                    break;
                } catch (Exception ex) {
                    ex.printStackTrace();
                }
            }
            if (!ok) {
                System.out.println(
                        " Unable to connect. \n Increasing timeout to " +
                        timeout / 1000 + " secs");
            }
        }
        */
    }

    public void displayException(Exception e) {
        TopFrame.the().displayException(e);
    }
    public static void main(String[] args) {

        connectToDataBase();
   //     new SimphoneyApp();
    }

}
