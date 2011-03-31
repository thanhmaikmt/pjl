/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package uk.co.drpj.chimera;

import java.awt.Color;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.TreeSet;
import javax.swing.BoxLayout;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextArea;
import javax.swing.JTextField;

/**
 *
 * @author pjl
 */
class HighScoreDialog extends JPanel {

    TreeSet<Score> highScore = new TreeSet<Score>();
    ChimeraApp outer;
    JTextField text;

    HighScoreDialog(final ChimeraApp outer) {
        this.outer=outer;
        setOpaque(false);
      

      //  setLayout(new BoxLayout(this, BoxLayout.X_AXIS));
//        JTextArea label;
//        add(label = new JTextArea("Enter your name:"));
//        label.setFont(outer.font);
//        label.setEditable(false);
//        label.setBackground(outer.opaqueBackGround);

        //    label.setForeground(Color.WHITE);
        text = new JTextField("                                     ");
        text.addActionListener(new ActionListener() {

            public void actionPerformed(ActionEvent arg0) {
                done();
            }
        });
        add(text);
        text.setFont(outer.font);
        text.setBackground(outer.opaqueBackGround);
//        JButton done = new JButton(" DONE ");
//        done.addActionListener(new ActionListener() {
//
//            public void actionPerformed(ActionEvent arg0) {
//                done();
//            }
//        });
//        add(done);
    }

    void setHighScore() {
        text.removeAll();
        setVisible(true);
        text.grabFocus();
    }

    void done() {
        highScore.add(new Score(text.getText(), outer.score));
        HighScoreDialog.this.setVisible(false);
    }
}
