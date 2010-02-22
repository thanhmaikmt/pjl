/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package redcode;

import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.JApplet;
import javax.swing.JComponent;
import javax.swing.JEditorPane;
import javax.swing.JScrollPane;
import javax.swing.JTabbedPane;

/**
 *
 * @author pjl
 */
public class RedcodeApplet extends JApplet {

    /**
     * Initialization method that will be called after the applet is loaded
     * into the browser.
     */
    MainPanel mainPanel;
    JTabbedPane tabPanel;

    @Override
    public void init() {
        try {
            // TODO start asynchronous download of heavy resources
            Machine mach = null;
            mach = new Machine(500);
            mainPanel = new MainPanel(mach, getCodeBase());
            tabPanel = new JTabbedPane();
            tabPanel.addTab("Simulator", mainPanel);
            tabPanel.addTab("Reference", createHtmlPanel());

            setContentPane(tabPanel);


        } catch (MalformedURLException ex) {
            Logger.getLogger(RedcodeApplet.class.getName()).log(Level.SEVERE, null, ex);
        } catch (RedCodeParseException ex) {
            Logger.getLogger(RedcodeApplet.class.getName()).log(Level.SEVERE, null, ex);
        }


    }

    private JComponent createHtmlPanel() throws MalformedURLException {

        String fna = getCodeBase() + "html/help.html";
        final URL helpURL = new URL(fna);


        System.out.println(helpURL);


        JScrollPane scroll = new JScrollPane();

        JEditorPane editorPane = new JEditorPane();
        editorPane.setEditable(false);

        if (helpURL != null) {
            try {
                editorPane.setPage(helpURL);
            } catch (IOException e) {
                System.err.println("Attempted to read a bad URL: " + helpURL);
            }
        } else {
            System.err.println("Couldn't find file: TextSampleDemoHelp.html");
        }

        scroll.setViewportView(editorPane);
        return scroll;

    }
}
