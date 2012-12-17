package GM.gui;

import java.io.*;
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.filechooser.*;

public class FileChooserDemo extends JFrame {
    static private final String newline = "\n";

    public FileChooserDemo() {
        super("FileChooserDemo");

        //Create the log first, because the action listeners
        //need to refer to it.
        final JTextArea log = new JTextArea(5,20);
        log.setMargin(new Insets(5,5,5,5));
        log.setEditable(false);
        JScrollPane logScrollPane = new JScrollPane(log);

        //Create a file chooser
        final JFileChooser fc = new JFileChooser();

        //Create the open button
//        ImageIcon openIcon = new ImageIcon("images/open.gif");
//        JButton openButton = new JButton("Open a File...", openIcon);
//        openButton.addActionListener(new ActionListener() {
//            public void actionPerformed(ActionEvent e) {
                int returnVal = fc.showOpenDialog(FileChooserDemo.this);

                if (returnVal == JFileChooser.APPROVE_OPTION) {
                    File file = fc.getSelectedFile();
                    //this is where a real application would open the file.
                    log.append("Opening: " + file.getName() + "." + newline);
                } else {
                    log.append("Open command cancelled by user." + newline);
//                }
            }
//        });

        //For layout purposes, put the buttons in a separate panel
        JPanel buttonPanel = new JPanel();
//        buttonPanel.add(openButton);


        //Add the buttons and the log to the frame
        Container contentPane = getContentPane();
        contentPane.add(buttonPanel, BorderLayout.NORTH);
        contentPane.add(logScrollPane, BorderLayout.CENTER);
    }

    public static void main(String[] args) {
        JFrame frame = new FileChooserDemo();

        frame.addWindowListener(new WindowAdapter() {
            public void windowClosing(WindowEvent e) {
                System.exit(0);
            }
        });

        frame.pack();
        frame.setVisible(true);
    }
}








