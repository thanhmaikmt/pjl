package GM.jdbc;

//import plugin.*;

import java.awt.*;
import java.awt.event.*;
import java.applet.*;
import java.applet.Applet;
import java.awt.BorderLayout;
import javax.swing.*;


import GM.music.Simphoney;
import GM.gui.*;
import GM.music.Defaults;

public class LoginPanel extends JPanel {


    GridBagLayout layout = new GridBagLayout();
    JPasswordField passField;
    JTextField userField;
    JButton login;
    JButton newuser;
    LoginClient client;

    public LoginPanel(LoginClient client) {
        this.client = client;
        setLayout(layout);

        try {
            jbInit();
        } catch (Exception e) {
            e.printStackTrace();
        }
//        setEnabled(DataBase.the() != null);
    }

/*
    public void setVisible(boolean yes) {
        super.setVisible(yes);
        setEnabled(DataBase.the() != null);
    }
*/

    private void jbInit() throws Exception {
        this.add(new JLabel("Username:"),
                 new GridBagConstraints(0, 0, 1, 1, 1.0, 0.0
                                        , GridBagConstraints.WEST,
                                        GridBagConstraints.HORIZONTAL,
                                        new Insets(0, 0, 0, 0), 0, 0));

        this.add(userField = new JTextField(10),
                             new GridBagConstraints(1, 0, 1, 1, 1.0, 0.0
                , GridBagConstraints.EAST,
                GridBagConstraints.HORIZONTAL,
                new Insets(0, 0, 0, 0), 0, 0));

        userField.setText(Defaults.user);

        this.add(new JLabel("Password:"),
                 new GridBagConstraints(0, 1, 1, 1, 1.0, 0.0
                                        , GridBagConstraints.WEST,
                                        GridBagConstraints.HORIZONTAL,
                                        new Insets(0, 0, 0, 0), 0, 0));

        this.add(passField = new JPasswordField(10),
                             new GridBagConstraints(1, 1, 1, 1, 1.0, 0.0
                , GridBagConstraints.NORTH,
                GridBagConstraints.HORIZONTAL,
                new Insets(0, 0, 0, 0), 0, 0));

        this.add(login = new JButton("LOGIN"),
                         new GridBagConstraints(0, 2, 2, 1, 1.0, 0.0
                                                , GridBagConstraints.NORTH,
                                                GridBagConstraints.HORIZONTAL,
                                                new Insets(0, 0, 0, 0), 0, 0));


        login.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                login.setEnabled(false);
                newuser.setEnabled(false);
                if (SimphoneyApp.the() != null) return;
                char[] input = passField.getPassword();
                try {
                    client.showProgress("verifying password");
                    DataBase.the().logon(input,userField.getText());
                   // client.statusMessage("Login OK. Loading  . . . . . . "); // @TODO progress
                    client.showProgress("loading");
                    Thread t=new Thread() {
                        public void run() {
                            new SimphoneyApp(userField.getText());
                            client.loginOK();
                        }
                    };
                    t.start();

                } catch ( Exception ex ) {
                    client.statusMessage("Problem with password:" +ex.getMessage());
                    login.setEnabled(true);
                    newuser.setEnabled(true);

                }

                //Zero out the possible password, for security.
                for (int i = 0; i < input.length; i++) {
                    input[i] = 0;
                }

                passField.selectAll();
           //     resetFocus();

            }
        });

        this.add(newuser = new JButton("NEW USER"),
                            new GridBagConstraints(0, 3, 2, 1, 1.0, 0.0
                                                   , GridBagConstraints.NORTH,
                                                   GridBagConstraints.HORIZONTAL,
                                                   new Insets(0, 0, 0, 0), 0, 0));

        newuser.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                client.newUser();
            }
        });

    }

    public void setEnabled(boolean yes) {
        passField.setEnabled(yes);
        userField.setEnabled(yes);
    }
}
