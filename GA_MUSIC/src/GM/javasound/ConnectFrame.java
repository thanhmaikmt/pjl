package GM.javasound;

import java.awt.*;

import javax.swing.*;
import java.awt.event.*;
import javax.sound.midi.MidiDevice;
import javax.sound.midi.*;

public class ConnectFrame extends JFrame {

    JButton add = new JButton();
    JPanel panel = new JPanel();

    public ConnectFrame() {
        try {
            jbInit();
        } catch (Exception exception) {
            exception.printStackTrace();
        }
        pack();
    }


    private void jbInit() throws Exception {

        Container p=getContentPane();
        add.setText("New connection");
        p.add(add,BorderLayout.SOUTH);
        p.add(panel,BorderLayout.CENTER);
        panel.setLayout(new BoxLayout(panel,BoxLayout.Y_AXIS));
        add.addActionListener(new ActionListener(){
            public void actionPerformed(ActionEvent e) {
                panel.add(new ConnectPanel());
                pack();
           }
       });

        for (MidiConnection c: MidiConnection.connections)
            panel.add(new ConnectPanel(c));
         setTitle("Midi routing");
    }

    public static void main(String args[]) {
        new ConnectFrame().show();
    }

}
