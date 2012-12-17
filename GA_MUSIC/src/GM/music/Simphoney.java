package GM.music;

import java.awt.*;
import javax.swing.*;
import GM.music.*;
import GM.jdbc.DataBase;
import java.sql.*;
import GM.jdbc.JDBCConnectDialog;
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

public class Simphoney {
    boolean packFrame = false;
    public static boolean isRunning = false;
//    public static TopFrame frame;
//    public static DataBase db = null;
    static Song song;
    static Simphoney the=null;

    static SimphoneyAppInterface app=null;
    /**
     * Construct and show the application.
     */


    static Simphoney the() { return the; }

    public void setApp(SimphoneyAppInterface app) {
        assert(Simphoney.app == null);
        this.app=app;
    }

    public Simphoney() {


        assert(the==null);



        setSong(new Song());
        Conductor.the().restart();
        the = this;
    }

    static public void kill() {
        if (song != null) song.kill();

        if (app != null) app.kill();
        song = null;
        the=null;
    }

    static public void setSong(Song newsong) {
        if (song != null) {
            song.kill();
        }
        song = newsong;
        if (app != null) app.setSong(newsong);
        Conductor.tempoBPM.setNumber(new Double(song.bpm));
        song.getBand().allocate(true);
        song.play();

    }

    static void displayException(Exception e) {
        app.displayException(e);
    }
    static public Song getSong() {
        return song;
    }

    /**
     * Application entry point.
     *
     * @param args String[]
     */

/*
    static public void connectToDataBase() {

        JDBCConnectDialog dialog= new JDBCConnectDialog();

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
        * /
    }

*/

}
