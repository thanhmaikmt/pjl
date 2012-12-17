package GM.gui;

import javax.swing.*;
import java.awt.BorderLayout;
import java.util.*;
import GM.music.*;
import java.awt.*;
import java.awt.event.*;
import javax.swing.event.*;


public class PianoRoll extends JScrollPane implements Observer {

    PhraseView phraseView = new PhraseView();

    PartView partView = new PartView(phraseView);
    TimeLinePanel timeLine = new TimeLinePanel();
    JPanel headerPanel = new JPanel();
    PlayerView playerView = new PlayerView();
    PlayerViewHeader soloMutePanel = new PlayerViewHeader();

    public PianoRoll() {

        getViewport().add(phraseView);
        headerPanel.setLayout(new BoxLayout(headerPanel, BoxLayout.Y_AXIS));

        headerPanel.add(partView);
        timeLine.setPreferredSize(new Dimension(1000, Layout.timeLineHeight));
        headerPanel.add(timeLine);
        setColumnHeaderView(headerPanel);
        setRowHeaderView(playerView);
        setCorner(JScrollPane.UPPER_LEFT_CORNER, soloMutePanel);

    }

    public void update(Observable o, Object arg) {

        Message mess = (Message) arg;

        //  System.out.println(o + " " + arg);
        if (o instanceof Song) {
            if (mess.str.equals("AddPart")) {
                Part sec = (Part) mess.o;
                addSection(sec);
                //      partView.myValidate();
                //      phraseView.myValidate();
            } else if (mess.str.equals("AddPlayer")) {
                Player player = (Player) mess.o;
                addPlayer(player);
                //       phraseView.myValidate();
            } else if (mess.str.equals("Modified")) {
                partView.rePosition();
                phraseView.rePosition();
            } else {
                //     System.out.println(" PianoRollPanel: Unhandled Message >" +
                //                        mess.str);
            }
        } else if (o instanceof Player) {
            Player player = (Player) o;
            if (mess == Message.KILLED) {
                phraseView.rePosition();
            }
        }
    }


    private void addPlayer(Player p) {
        //  System.out.println("PRP ADD PLAYER" + p );
        synchronized(p) {
            p.addObserver(this);

            Iterator<Phrase> iter = p.getPhrases().iterator();

            while (iter.hasNext()) {
                addPhrase(iter.next());
            }
        }
    }

    synchronized void rebuild(Song song) {
        // System.out.println("PRP rebuild" + song);

        phraseView.detachAll();
        partView.detachAll();

        //   content.removeAll();
        // content.add(cursor);
        synchronized (song) {
            Iterator<Part> iter = song.getSections().iterator();
            while (iter.hasNext()) {
                addSection(iter.next());
            }
        }
        phraseView.myValidate();
        partView.myValidate();
    }

    private void addSection(Part sec) {
        // System.out.println("PRP ADD SECTION"+ sec);

        synchronized (sec) {
            Iterator<Phrase> iter = sec.getPhrases().iterator();
            while (iter.hasNext()) {
                Phrase phrase = iter.next();
                addPhrase(phrase);
            }
        }
        PartItem panel = new PartItem(sec, this);
        partView.addPartPanel(panel);
        //   partView.repaint();
    }


    private void addPhrase(Phrase phrase) {
        //   System.out.println("PRP ADD PHRASE" + phrase);


        PhraseItem panel = new PhraseItem(phrase, this);
        phraseView.addPhrasePanel(panel);

        //    System.out.println(panel.getBounds());
    }


}
