package GM.jdbc;

import java.awt.*;

import javax.swing.*;
import java.awt.BorderLayout;
import javax.swing.Box;
import java.awt.Dimension;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;

public class JDBCConnectPanel extends JPanel implements ActionListener {

    JComboBox hostCombo = new JComboBox(DataBase.hosts);
    GridBagLayout gridBagLayout1 = new GridBagLayout();
    JTextField userTxt = new JTextField();
    JPasswordField passTxt = new JPasswordField();
    JTextField serverTxt = new JTextField();
    JTextField portTxt = new JTextField();
    JButton connectBut = new JButton("Connect");
    JButton cancelBut = new JButton("Cancel");
    DataBase.MySqlHost host=null;
    DataBase.MySqlHost hostOrig=null;
    DataBase db=null;
    boolean xxx;

    ConnectThread connectThread=null;
    JDBCConnectionClient client;

    public JDBCConnectPanel(JDBCConnectionClient c) {
        this.client = c;
        try {
            jbInit();
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public DataBase getDataBase() {
        return db;
    }

    private void jbInit() throws Exception {
        setLayout(gridBagLayout1);
        hostCombo.setMaximumSize(new Dimension(600, 24));



        int row=0;


        setBorder(BorderFactory.createTitledBorder("MySql host connector"));

        /*
        this.add(new JLabel(" MySql connection   "),
                                             new GridBagConstraints(0, row++, 2, 1, 1.0, 1.0
                 , GridBagConstraints.CENTER, GridBagConstraints.HORIZONTAL,
                 new Insets(0, 0, 0, 0), 0, 0));
*/

        this.add(new JLabel("MySql data base"),
                                  new GridBagConstraints(0, row, 1, 1, 1.0, 0.0
                , GridBagConstraints.WEST, GridBagConstraints.HORIZONTAL,
                new Insets(0, 0, 0, 0), 0, 0));

        this.add(hostCombo,
                                  new GridBagConstraints(1, row++, 1, 1, 1.0, 0.0
                , GridBagConstraints.EAST, GridBagConstraints.HORIZONTAL,
                new Insets(0, 0, 0, 0), 0, 0));

        hostCombo.addActionListener(this);


        this.add(new JLabel("Hostname"),
                                  new GridBagConstraints(0, row, 1, 1, 1.0, 0.0
                , GridBagConstraints.WEST, GridBagConstraints.HORIZONTAL,
                new Insets(0, 0, 0, 0), 0, 0));

        this.add(serverTxt,
                                  new GridBagConstraints(1, row++, 1, 1, 1.0, 0.0
                , GridBagConstraints.EAST, GridBagConstraints.HORIZONTAL,
                new Insets(0, 0, 0, 0), 0, 0));
        serverTxt.addActionListener(this);


        this.add(new JLabel("(MySql)Username"),
                                  new GridBagConstraints(0, row, 1, 1, 1.0, 0.0
                , GridBagConstraints.WEST, GridBagConstraints.HORIZONTAL,
                new Insets(0, 0, 0, 0), 0, 0));


        this.add(userTxt,
                                  new GridBagConstraints(1, row++, 1, 1, 1.0, 0.0
                , GridBagConstraints.EAST, GridBagConstraints.HORIZONTAL,
                new Insets(0, 0, 0, 0), 0, 0));
        userTxt.addActionListener(this);


        this.add(new JLabel("(MySql)Password"),
                                  new GridBagConstraints(0, row, 1, 1, 1.0, 0.0
                , GridBagConstraints.WEST, GridBagConstraints.HORIZONTAL,
                new Insets(0, 0, 0, 0), 0, 0));


        this.add(passTxt,
                                  new GridBagConstraints(1, row++, 1, 1, 1.0, 0.0
                , GridBagConstraints.EAST, GridBagConstraints.HORIZONTAL,
                new Insets(0, 0, 0, 0), 0, 0));
        passTxt.addActionListener(this);



        this.add(new JLabel("Port (3306)"),
                                  new GridBagConstraints(0, row, 1, 1, 1.0, 0.0
                , GridBagConstraints.WEST, GridBagConstraints.HORIZONTAL,
                new Insets(0, 0, 0, 0), 0, 0));


        this.add(portTxt,
                                      new GridBagConstraints(1, row++, 1, 1, 1.0, 0.0
                    , GridBagConstraints.EAST, GridBagConstraints.HORIZONTAL,
                    new Insets(0, 0, 0, 0), 0, 0));
        portTxt.addActionListener(this);


        this.add(connectBut,
                                  new GridBagConstraints(0, row, 1, 1, 0.0, 0.0
                , GridBagConstraints.CENTER, GridBagConstraints.NONE,
                new Insets(0, 0, 0, 0), 0, 0));
        connectBut.addActionListener(this);


        this.add(cancelBut,
                 new GridBagConstraints(1, row++, 1, 1, 0.0, 0.0
                                        , GridBagConstraints.CENTER, GridBagConstraints.NONE,
                                        new Insets(0, 0, 0, 0), 0, 0));

        cancelBut.addActionListener(this);


        setHostFromName();

    }


    public void setHostFromName() {
        hostOrig = (DataBase.MySqlHost) hostCombo.getSelectedItem();
        host=hostOrig;
        serverTxt.setText(host.server);
        userTxt.setText(host.user);
        passTxt.setText(host.passwd);
        portTxt.setText(String.valueOf(host.port));
      //  xxx=host.xxx;
    }

    public void setHostFromText() {
        xxx = hostOrig.xxx && (new String(passTxt.getPassword()).equals(hostOrig.passwd));
        host = new DataBase.MySqlHost("",
                                      serverTxt.getText(),
                                      (byte[])null,
                                      userTxt.getText(),
                                      new String(passTxt.getPassword()),
                                      Integer.valueOf(portTxt.getText()),
                                      xxx);

    }




    /*
    public void getFields() {
        host=new DataBase.MySqlHost(hostCombo.getSelectedItem().toString(),
                                    serverTxt.getText(),
                                    null,
                                    userTxt.getText(),
                                    passTxt.getText(),
                                    Integer.valueOf(portTxt.getText()));
    }
*/

    public void actionPerformed(ActionEvent e) {
        Object src=e.getSource();
 //       System.out.println(src);
        if (src == hostCombo) {
            setHostFromName();
        } else if (src == userTxt ||
                   src == serverTxt ||
                   src == passTxt ||
                   src == portTxt) {

        } else if (src == cancelBut) {
            if (connectThread == null) {
                client.statusMessage("Nothing to cancel!");
            }else {
                System.out.println(" cancel but pressed ");
                connectThread.interrupt();
            }


        } else if (src == connectBut) {
            try {
                setHostFromText();
                connectThread = new ConnectThread();
                connectThread.start();
                client.showProgress("attempting to connect");
            } catch (Exception ex) {
                db=null;
                ex.printStackTrace();
            }
        }


    }

    class ConnectThread extends Thread {

        public void run() {
            try {
                db = new DataBase(host);
                client.statusMessage(" Connected OK. Opening" + db.getHost().dbName);
                db.open();
                client.statusMessage(" Connected to "+ db.getHost().dbName+" : Now login. ");
                client.connectedOK();
            } catch (InterruptedException e) {
                e.printStackTrace();
                client.statusMessage(" Connection aborted. See JAVA console for details ");
            } catch (ClassNotFoundException e) {
                e.printStackTrace();
                client.statusMessage(" Check com.mysql.jdbc.Driver is in CLASSPATH ");

            }catch (Exception e) {

                e.printStackTrace();
                client.statusMessage(" Error during connection. See JAVA console for details ");
            } finally {

                connectThread = null;
            }
        }

    }

}
