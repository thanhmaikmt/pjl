package uk.ac.bath.redcode;

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

    MainPanel mainPanel;
    JTabbedPane tabPanel;
 //   boolean useJar = true;

    @Override
    public void init() {
        try {
            Machine mach = null;
            mach = new Machine(500);

            URL codeBase;

//            if (useJar) {
                codeBase = getClass().getResource("/prog/"); // getClass().getResource("/html/help.html"); //new URL(fna);
//            } else {
//                String fna = getCodeBase() + "/prog/";
//                codeBase = new URL(fna);
//            }

            mainPanel = new MainPanel(mach, codeBase);

            tabPanel = new JTabbedPane();
            tabPanel.addTab("Simulator", mainPanel);
            tabPanel.addTab("Help", createHtmlPanel("help"));
            tabPanel.addTab("Reference", createHtmlPanel("reference"));
            tabPanel.addTab("Exercises", createHtmlPanel("probs"));

            setContentPane(tabPanel);


        } catch (MalformedURLException ex) {
            Logger.getLogger(RedcodeApplet.class.getName()).log(Level.SEVERE, null, ex);
        } catch (RedCodeParseException ex) {
            Logger.getLogger(RedcodeApplet.class.getName()).log(Level.SEVERE, null, ex);
        }


    }

    private JComponent createHtmlPanel(String name) throws MalformedURLException {

        final URL url;

      // if (useJar) {
             url = getClass().getResource("/html/"+name+".html");
//        } else {
//            String fna = getCodeBase() + "html/"+name+".html";
//             url = new URL(fna);
//        }

        System.out.println( url);

        JScrollPane scroll = new JScrollPane();

        JEditorPane editorPane = new JEditorPane();
        editorPane.setEditable(false);

        if ( url != null) {
            try {
                editorPane.setPage( url);
            } catch (IOException e) {
                System.err.println("Attempted to read a bad URL: " +  url);
            }
        } else {
            System.err.println("Couldn't load :" +  url);
        }

        scroll.setViewportView(editorPane);
        return scroll;

    }
}
