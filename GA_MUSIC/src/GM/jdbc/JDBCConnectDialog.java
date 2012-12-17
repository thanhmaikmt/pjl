package GM.jdbc;

import java.awt.*;

import javax.swing.*;
import java.awt.BorderLayout;
import javax.swing.Box;
import java.awt.Dimension;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;

public class JDBCConnectDialog extends JDialog implements JDBCConnectionClient ,LoginClient {


    JDBCConnectPanel mysqlPanel;
    JProgressBar progressPanel=new JProgressBar();
    LoginPanel loginPanel;
    NewUserPanel newPanel;
    JLabel  status = new JLabel();
    boolean login;



    public JDBCConnectDialog(Frame owner, String title, boolean modal) {
        super(owner, title, modal);
        try {
            setDefaultCloseOperation(DISPOSE_ON_CLOSE);
            jbInit();
            pack();
        } catch (Exception exception) {
            exception.printStackTrace();
        }
    }

    public JDBCConnectDialog(boolean login) {
        this(new Frame(), "JDBCConnectDialog", true);
        this.login=login;
    }

    public DataBase getDataBase() {
        return mysqlPanel.db;
    }


    public void connectedOK() {
        if (!login) {
            setVisible(false);
        } else {
            this.getContentPane().remove(mysqlPanel);
            this.getContentPane().add(loginPanel, BorderLayout.CENTER);
            //=new LoginPanel(this),BorderLayout.CENTER);
            validate();
        }
    }
    public void loginOK() {

        setVisible(false);

    }
    public void newUser() {
        this.getContentPane().remove(loginPanel);
        this.getContentPane().add(newPanel,BorderLayout.CENTER);
        validate();
    }

    private void jbInit() throws Exception {
        setLayout(new BorderLayout());
        mysqlPanel=new JDBCConnectPanel(this);
        loginPanel=new LoginPanel(this);
        newPanel=new NewUserPanel(this);
        this.getContentPane().add(mysqlPanel,BorderLayout.CENTER);

        status.setBorder(BorderFactory.createLoweredBevelBorder());
        status.setPreferredSize(new Dimension(100,20));


        this.getContentPane().add(status,BorderLayout.SOUTH);


        pack();

    }

    public void statusMessage(String str) {
        this.getContentPane().remove(progressPanel);
        this.getContentPane().add(status, BorderLayout.SOUTH);

        status.setText(str);
    }

    public void showProgress(String txt) {


        this.getContentPane().remove(status);
        this.getContentPane().add(progressPanel, BorderLayout.SOUTH);
        progressPanel.setIndeterminate(true);
        progressPanel.setStringPainted(true);
        progressPanel.setString(txt);
        validate();

    }

}
