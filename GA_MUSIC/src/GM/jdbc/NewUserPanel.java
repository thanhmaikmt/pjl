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

public class NewUserPanel extends JPanel {


    GridBagLayout layout = new GridBagLayout();
    JPasswordField passField;
    JPasswordField confField;
    JTextField userField;
    JButton login;
    LoginClient client;

    public NewUserPanel(LoginClient client) {
        this.client = client;
        setLayout(layout);

        try {
            jbInit();
        } catch (Exception e) {
            e.printStackTrace();
        }
//        setEnabled(DataBase.the() != null);
    }

    public void setVisible(boolean yes) {
        super.setVisible(yes);
        setEnabled(DataBase.the() != null);
    }

    private void jbInit() throws Exception {
        int row=0;
        this.add(new JLabel("Username:"),
                 new GridBagConstraints(0, row, 1, 1, 1.0, 0.0
                                        , GridBagConstraints.WEST,
                                        GridBagConstraints.HORIZONTAL,
                                        new Insets(0, 0, 0, 0), 0, 0));

        this.add(userField = new JTextField(10),
                             new GridBagConstraints(1, row++, 1, 1, 1.0, 0.0
                , GridBagConstraints.EAST,
                GridBagConstraints.HORIZONTAL,
                new Insets(0, 0, 0, 0), 0, 0));

        userField.setText("");

        this.add(new JLabel("Password:"),
                 new GridBagConstraints(0, row, 1, 1, 1.0, 0.0
                                        , GridBagConstraints.WEST,
                                        GridBagConstraints.HORIZONTAL,
                                        new Insets(0, 0, 0, 0), 0, 0));

        this.add(passField = new JPasswordField(10),
                             new GridBagConstraints(1, row++, 1, 1, 1.0, 0.0
                , GridBagConstraints.NORTH,
                GridBagConstraints.HORIZONTAL,
                new Insets(0, 0, 0, 0), 0, 0));


        this.add(new JLabel("confirm:"),
                 new GridBagConstraints(0, row, 1, 1, 1.0, 0.0
                                        , GridBagConstraints.WEST,
                                        GridBagConstraints.HORIZONTAL,
                                        new Insets(0, 0, 0, 0), 0, 0));

        this.add(confField = new JPasswordField(10),
                             new GridBagConstraints(1, row++, 1, 1, 1.0, 0.0
                , GridBagConstraints.NORTH,
                GridBagConstraints.HORIZONTAL,
                new Insets(0, 0, 0, 0), 0, 0));


        this.add(login = new JButton("LOGIN"),
                         new GridBagConstraints(0, row++, 2, 1, 1.0, 0.0
                                                , GridBagConstraints.NORTH,
                                                GridBagConstraints.HORIZONTAL,
                                                new Insets(0, 0, 0, 0), 0, 0));


        login.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                String user = userField.getText();
                char[] input = passField.getPassword();
                char[] confirm = passField.getPassword();
                try {
                    if (DataBase.the().userExists(user)) {
                        client.statusMessage(user + " already exists");
                    } else {
                        if (String.copyValueOf(input).equals(String.copyValueOf(
                                confirm))) {
                            DataBase.the().addUser(user,String.copyValueOf(input));
                            client.statusMessage(
                                    "Logon OK. Starting simphoney  . . . please wait.");
                            new SimphoneyApp(userField.getText());
                            client.loginOK();
                        } else {
                            client.statusMessage(
                                    " password and confirm do not match");
                        }

                    }
                } catch (Exception ex) {
                    ex.printStackTrace();
                }
           }
        });
    }

    public void setEnabled(boolean yes) {
        passField.setEnabled(yes);
        userField.setEnabled(yes);
    }
}
