/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package redcode;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.JApplet;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;

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

    public void init() {
        try {
            // TODO start asynchronous download of heavy resources
            Machine mach = null;
            mach = new Machine(500);
            mainPanel = new MainPanel(mach);
            setContentPane(mainPanel);


        } catch (RedCodeParseException ex) {
            Logger.getLogger(RedcodeApplet.class.getName()).log(Level.SEVERE, null, ex);
        }

        JMenuBar bar = new JMenuBar();
        setJMenuBar(bar);

        String fna = getCodeBase() + "/prog";
        final URL url;
        try {
            url = new URL(fna);


            System.out.println(url);

            java.net.URLConnection con;
            con = url.openConnection();

            con.connect();

            java.io.BufferedReader in = new java.io.BufferedReader(new java.io.InputStreamReader(con.getInputStream()));
            String line;
            JMenu menu = new JMenu("file");
            bar.add(menu);
            while ((line = in.readLine()) != null) {

                System.out.println(line);
                final JMenuItem item = new JMenuItem(line);
                menu.add(item);
                item.addActionListener(new ActionListener() {

                    public void actionPerformed(ActionEvent e) {
                        String fna = item.getActionCommand();
                        System.out.println(item.getActionCommand());
                        try {
                            loadFromURL(new URL(url.toString() + "/" + fna));
                        } catch (IOException ex) {
                            Logger.getLogger(RedcodeApplet.class.getName()).log(Level.SEVERE, null, ex);
                        }
                    }
                });
            }

        } catch (MalformedURLException ex) {
            Logger.getLogger(RedcodeApplet.class.getName()).log(Level.SEVERE, null, ex);
        } catch (IOException ex) {
            Logger.getLogger(RedcodeApplet.class.getName()).log(Level.SEVERE, null, ex);
        }
        // TODO overwrite start(), stop() and destroy() methods
    }

    void loadFromURL(URL name) throws IOException {
        String str="";
        BufferedReader in = new BufferedReader(
                new InputStreamReader(
                name.openStream()));

        String inputLine;

        while ((inputLine = in.readLine()) != null) {
            System.out.println(inputLine);
            str = str + inputLine+"\n";
        }

        in.close();

        mainPanel.setEditText(str);
    }
}
