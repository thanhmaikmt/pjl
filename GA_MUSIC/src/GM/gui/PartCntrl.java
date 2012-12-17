package GM.gui;

import javax.swing.*;
import java.awt.event.*;
import java.util.*;
import GM.music.*;
import javax.swing.border.TitledBorder;
import java.awt.*;
import GM.tweak.TweakableInt;
import GM.tweak.Tweakable;
import GM.tweak.Tweakables;

public class PartCntrl extends JPanel implements Observer, ActionListener,
        Tweakables {

    JLabel name = new JLabel();
    JButton mutate = new JButton();
    JButton redo = new JButton();
    JButton undo = new JButton();
    JButton kill = new JButton();
    JButton copy = new JButton();
    JButton paste = new JButton();

    FlowLayout flowLayout1 = new FlowLayout();

    TitledBorder titledBorder1 = new TitledBorder("");

    TweakPanel tweakPanel;
    JPanel cntrlPanel = new JPanel();

    boolean isVis;


    Vector<Tweakable> tweaks = new Vector<Tweakable>();

    TweakableInt length;
    TweakableInt chordsPerBeat;



    public PartCntrl() {
        makeTweaks();
        tweakPanel = new TweakPanel(this);

     //   length.setEnabled(false);
     //   chordsPerBeat.setEnabled(false);

        try {
            jbInit();
        } catch (Exception ex) {
            ex.printStackTrace();
        }
        update(null, Message.MODIFIED);
    }



    public void actionPerformed(ActionEvent e) {

        Object src = e.getSource();
        if (src == copy) {
            Song song = Simphoney.getSong();
            assert(song != null);
            song.copySelectedPartsToClip();
            song.appendClippedParts();
        } else {
            forAllSelected(src);
        }
    }

    void makeTweaks() {
         length = new TweakableInt(1, 8, Defaults.partLength, "Length");
         chordsPerBeat = new TweakableInt(1, 4, Defaults.chordsPerBeat, "Chords/beat");
         tweaks.add(length);
         tweaks.add(chordsPerBeat);

         length.addObserver(this);
         chordsPerBeat.addObserver(this);
     }

     public Vector<Tweakable> getTweaks() {
         return tweaks;
     }

    public void forAllSelected(Object o) {

        Song song = Simphoney.getSong();
        Vector<Part> killList = new Vector<Part>();

        synchronized (song) {
            Iterator<Part> iter = song.getParts().iterator();
            while (iter.hasNext()) {
                Part part = iter.next();
                if (!part.isSelected()) {
                    continue;
                }
                synchronized (part) {
                    if (o == chordsPerBeat) {
                        part.chordsPerBeat.setNumber(chordsPerBeat.intValue());
                        Defaults.chordsPerBeat=chordsPerBeat.intValue();
                    } else if (o == length) {
                        part.length.setNumber(length.intValue());
                        Defaults.partLength=length.intValue();
                    } else if (o == mutate) {
                        part.mutate();
                    } else if (o == kill) {
                        killList.add(part);
                    } else if (o== undo) {
                        part.undo();
                    } else if (o== redo) {
                        part.redo();
                    }
                }
            }

            if (o == kill) {
                Iterator<Part> kiter = killList.iterator();
                while (kiter.hasNext()) {
                    kiter.next().kill();
                }
            }
        }

    }

    public void update(Observable o, Object cmd) {

        //  System.out.println(" HELLO FROM " + this);

        if (o == chordsPerBeat && chordsPerBeat.isEnabled()) {
            forAllSelected(chordsPerBeat);
         //   System.out.println("chords per beat");
        } else if (o == length && length.isEnabled()) {
            forAllSelected(length);
         //   System.out.println("length");
        } else if (o instanceof Song) {
            Message mess = (Message) cmd;
            if (mess == Message.SELECTION_CHANGE) {
                setSelection((Song) o);
            }
        }
    }

    void setSelection(Song song) {

      //  System.out.println(this +" SET SONG ");
        boolean first = true;
        int cpb = -1;
        int len = -1;

        synchronized (song) {
            Iterator<Part> iter = song.getParts().iterator();
            while (iter.hasNext()) {
                Part part = iter.next();
                if (!part.isSelected()) {
                    continue;
                }

                synchronized (part) {

                    if (first == true) {
                        cpb = part.chordsPerBeat.intValue();
                        len = part.length.intValue();
                        first = false;
                    } else {
                        if (cpb > 0) {
                            if (cpb != part.chordsPerBeat.intValue()) {
                                cpb = -1;
                            }
                        }
                        if (len > 0) {
                            if (len != part.length.intValue()) {
                                len = -1;
                            }
                        }
                    }
                }
            }
        }

      //  chordsPerBeat.setEnabled(cpb != -1);
      //  length.setEnabled(len != -1);
        if (cpb > 0) {
            chordsPerBeat.setNumber(cpb);
        }
        if (len > 0) {
            length.setNumber(len);
        }
    }

    private void jbInit() throws Exception {

        add(tweakPanel);


        undo.setIcon(
                new ImageIcon(GM.gui.PhraseCntrl.class.getResource(
                        "undo16.png")));

        undo.setToolTipText("Undo mutate on selected parts");
        undo.addActionListener(this);

        cntrlPanel.add(undo);

        mutate.setIcon(
                new ImageIcon(GM.gui.PhraseCntrl.class.getResource(
                        "mutate.png")));

        mutate.setToolTipText("Mutate selected parts");
        mutate.addActionListener(this);

        cntrlPanel.add(mutate);

        redo.setIcon(
                new ImageIcon(GM.gui.PartCntrl.class.getResource(
                        "redo16.png")));

        redo.setToolTipText("Redo mutate on selected parts");
        redo.addActionListener(this);

        cntrlPanel.add(redo);


        copy.setIcon(
            new ImageIcon(GM.gui.PartCntrl.class.getResource(
                "editcopy16.png")));

        copy.addActionListener(this);
        copy.setToolTipText("Copy selected to insert point");

        cntrlPanel.add(copy);


        kill.setIcon(
                new ImageIcon(GM.gui.PhraseCntrl.class.getResource(
                        "kill16.png")));

        kill.addActionListener(this);

        kill.setToolTipText("Delete selected parts");

        cntrlPanel.add(kill);


        this.setBorder(BorderFactory.createTitledBorder("Part edit"));

        add(cntrlPanel);

    }


}
