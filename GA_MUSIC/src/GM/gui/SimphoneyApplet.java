package GM.gui;

//import plugin.*;

import java.awt.*;
import java.awt.event.*;
import java.applet.*;
import java.applet.Applet;
import java.awt.BorderLayout;
import javax.swing.*;
import GM.jdbc.*;
import GM.music.Simphoney;
import GM.jdbc.*;
import GM.javasound.*;

public class SimphoneyApplet extends JApplet implements JDBCConnectionClient,
        LoginClient {


    static public boolean isApplet = false;

    //   Simphoney sim = null;
    JLabel status = new JLabel();
    JPanel panel;
    JProgressBar progressPanel=new JProgressBar();
    JTextArea    loginText;

    //Get a parameter value
    public String getParameter(String key, String def) {
        return!isApplet ? System.getProperty(key, def) :
                (getParameter(key) != null ? getParameter(key) : def);
    }

    //Initialize the applet

    public void init() {
        isApplet = true;
        //  new SimphoneyApp();
        setLayout(new BorderLayout());

        System.out.println(" init ");
        add(panel = new JDBCConnectPanel(this), BorderLayout.CENTER);

        status.setBorder(BorderFactory.createLoweredBevelBorder());
        status.setPreferredSize(new Dimension(100, 20));

        add(status, BorderLayout.SOUTH);

    }


    public void connectedOK() {
        System.out.println("CONNECTEDOK");
        statusMessage("Connected");
        remove(panel);
        add(panel = (new LoginPanel(this)), BorderLayout.CENTER);
        validate();
        // if (Simphoney.the() == null)
    }

    public void loginOK() {
        System.out.println("LOGINOK");
        statusMessage("Logon succeeded");
        //  new SimphoneyApp(DataBase.the().getUser());
        JButton but = new JButton("Show/Hide main app");
        add(but, BorderLayout.NORTH);
//      but.setEnabled(false);
        but.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {

                //   JButton b= (JButton)e.getSource();
                if (TopFrame.the() == null) {
                    System.out.println(" TopFrame.the() == null ");
                    return;
                } else {
                    TopFrame.the().setVisible(!TopFrame.the.isVisible());
                }
            }
        });
        remove(panel);
        add(panel = (new SongSelectPanel()), BorderLayout.CENTER);
//        remove(progressPanel);
        validate();
    }


    public void newUser() {
        System.out.println("NEWUSER");
        statusMessage(" enter name and password");
        remove(panel);
        add(panel = (new NewUserPanel(this)), BorderLayout.CENTER);
        validate();
    }

    public void showProgress(String txt) {

        System.out.println("LOADINGAPP");
   //     loginText=new JTextArea(" Loading main application. \n Please wait. ");
        panel.setEnabled(false);
        remove(status);

   //     add(loginText, BorderLayout.CENTER);

        add(progressPanel, BorderLayout.SOUTH);
        progressPanel.setStringPainted(true);
        progressPanel.setString(txt);
        progressPanel.setIndeterminate(true);
        validate();

    }

    public void statusMessage(String str) {
        remove(progressPanel);
        status.setText(str);
    }

    //Start the applet
    public void start() {
        System.out.println(" start applet (todo)");
    }

    //Stop the applet
    public void stop() {
        System.out.println(" stop applet (todo)");

    }

    //Destroy the applet
    public void destroy() {
        System.out.println(" destroy applet");
        Simphoney.getSong().setId(0);
        Simphoney.kill();
        DataBase.kill();
        new MidiHub.ExitHandler().run();
    }

    //Get Applet information
    public String getAppletInfo() {
        return "This is the simphoney Applet (so there)!";
    }

    //Get parameter info
    public String[][] getParameterInfo() {
        return null;
    }

}
