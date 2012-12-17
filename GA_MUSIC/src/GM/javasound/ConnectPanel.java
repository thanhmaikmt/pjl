package GM.javasound;

import java.awt.*;

import javax.swing.*;
import java.awt.event.*;
import javax.sound.midi.MidiDevice;
import javax.sound.midi.*;


public class ConnectPanel extends JPanel {
    JComboBox transCombo;
    JComboBox recvCombo;
    JToggleButton connect = new JToggleButton();
    MidiConnection con;

    public ConnectPanel() {
        setLayout(new BoxLayout(this,BoxLayout.X_AXIS));
        try {
            jbInit();
        } catch (Exception exception) {
            exception.printStackTrace();
        }
    }

    public ConnectPanel(MidiConnection c) {
        this();
        transCombo.setSelectedItem(c.transDev);
        recvCombo.setSelectedItem(c.recvDev);

        connect.setSelected(c.connected);//   assert(false);
        if (c.connected) connect.setText("Disconnect");
        con=c;
    }


    private void jbInit() throws Exception {

        recvCombo = new JComboBox(MidiHub.recvHandle);
        transCombo = new JComboBox(MidiHub.transHandle);
        connect.setText("Connect");

        connect.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e) {

               MidiHub.DeviceHandle trans=(MidiHub.DeviceHandle) transCombo.getSelectedItem();
               MidiHub.DeviceHandle recv=(MidiHub.DeviceHandle) recvCombo.getSelectedItem();

               if (connect.isSelected()) {
                   if (con != null) {
                       con.disconnect();
                       MidiConnection.remove(con);
                   }
                   con = new MidiConnection(trans, recv);
                   con.connect();
                   connect.setText("disconnect");
               } else {
                   con.disconnect();
                   MidiConnection.remove(con);
                   con=null;
                   connect.setText("connect");
               }
           }

       });

        add(transCombo);
        add(recvCombo);
        add(connect);

         // setTitle("Midi routing");

    }

}
