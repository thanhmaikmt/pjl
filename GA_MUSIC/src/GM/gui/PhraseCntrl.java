package GM.gui;

import javax.swing.*;
import java.awt.Container;
import java.awt.event.*;
import java.util.*;
import GM.music.*;
import javax.swing.border.TitledBorder;
import java.awt.*;
import java.awt.geom.*;
import GM.tweak.TweakableInt;
import GM.tweak.Tweakable;
import GM.tweak.Tweakables;

public class PhraseCntrl extends JPanel implements Observer, ActionListener , Tweakables {

    JLabel name = new JLabel();
    JButton mutate = new JButton();
    JButton redo=new JButton();
    JButton undo=new JButton();
    JButton copy=new JButton();

    JToggleButton kill=new JToggleButton();

    FlowLayout flowLayout1 = new FlowLayout();
    GridBagLayout gridBagLayout1 = new GridBagLayout();
    TitledBorder titledBorder1 = new TitledBorder("");

    GridBagLayout gridBagLayout2 = new GridBagLayout();
    GridBagLayout gridBagLayout3 = new GridBagLayout();
    TweakPanel tweakPanel;
    JPanel cntrlPanel = new JPanel();

    boolean isVis;


    Vector<Tweakable> tweaks = new Vector<Tweakable>();

    TweakableInt pulsePerBeat;
    TweakableInt multiplier;


    void makeTweaks() {
        pulsePerBeat = new TweakableInt(1, 4, Defaults.pulsesPerBeat, "Pulses per beat");
        multiplier = new TweakableInt(1, 4, Defaults.pulsesPerBeatMult, "Multiplier");
        tweaks.add(multiplier);
        tweaks.add(pulsePerBeat);
        pulsePerBeat.addObserver(this);
        multiplier.addObserver(this);
    }

    public Vector<Tweakable> getTweaks() {
        return tweaks;
    }

    public PhraseCntrl() {
        setBorder(BorderFactory.createTitledBorder("Phrase edit"));
        makeTweaks();
        tweakPanel = new TweakPanel(this);
       // multiplier.setEnabled(false);
      //  pulsePerBeat.setEnabled(false);
      //  setEnabled(false);

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
            song.pasteSelectedPhrases();
        } else {
            forAllSelected(src);
        }
    }


    public void forAllSelected(Object o) {

        Song song= Simphoney.getSong();
        int jjj;
        synchronized(song) {
            Iterator<Part> iter = song.getParts().iterator();
            while(iter.hasNext()){
                Part part= iter.next();
                synchronized(part) {
                    Iterator<Phrase> piter=part.getPhrases().iterator();
                    while(piter.hasNext()) {
                        Phrase phrase=piter.next();
                        if (!phrase.isSelected()) continue;
                        if (o == pulsePerBeat)  {
                            phrase.pulsePerBeat.setNumber(jjj=pulsePerBeat.intValue());
                            Defaults.pulsesPerBeat=jjj;
                        } else if ( o == multiplier ) {
                            phrase.multiplier.setNumber(jjj=multiplier.intValue());
                            Defaults.pulsesPerBeatMult=jjj;
                        } else if ( o == mutate) {
                            phrase.mutate();
                        } else if ( o == undo) {
                            phrase.undo();
                        } else if ( o == redo) {
                            phrase.redo();
                        } else if ( o == kill) {
                            phrase.setMute(kill.isSelected());
                        }
                    }
                }
            }
        }


    }

    public void update(Observable o, Object cmd) {

     //   System.out.println(" HELLO FROM " + this);

        if (o == pulsePerBeat  && pulsePerBeat.isEnabled()) {
            forAllSelected(pulsePerBeat);
         //   System.out.println("pulse/beat");
        } else if (o == multiplier && multiplier.isEnabled()) {
            forAllSelected(multiplier);
         //   System.out.println("multiplier");
        } else if (o instanceof Song ) {
            kill.removeActionListener(this);
            kill.setSelected(false);
            kill.addActionListener(this);

            Message mess=(Message)cmd;
            if (mess == Message.SELECTION_CHANGE) {
                setSelection((Song)o);
            }
        }
    }

    void setSelection(Song song) {

      //  System.out.println(this + " SET SONG ");
        boolean first=true;
        int ppb=-1;
        int mult=-1;

        synchronized(song) {
            Iterator<Part> iter = song.getParts().iterator();
            while(iter.hasNext()){
                Part part= iter.next();
                synchronized(part) {
                    Iterator<Phrase> piter=part.getPhrases().iterator();
                    while(piter.hasNext()) {
                        Phrase phrase=piter.next();
                        if (!phrase.isSelected()) continue;
                        if (first == true) {
                            ppb  =phrase.pulsePerBeat.intValue();
                            mult  =phrase.multiplier.intValue();
                            first=false;
                        } else {
                            if (ppb>0 ) {
                                if (ppb != phrase.pulsePerBeat.intValue()) ppb=-1;
                            }
                            if (mult > 0 ) {
                                if (mult != phrase.multiplier.intValue()) mult=-1;
                            }
                        }
                    }
                }
            }
        }

      //  pulsePerBeat.setEnabled(ppb != -1);
      //  multiplier.setEnabled(mult != -1);
        if (ppb > 0 )  pulsePerBeat.setNumber(ppb);
        if (mult > 0 )  multiplier.setNumber(mult);
    }

    private void jbInit() throws Exception {

        add(tweakPanel);

        undo.setIcon(
                new ImageIcon(GM.gui.PhraseCntrl.class.getResource(
                "undo16.png")));
        undo.addActionListener(this);
        undo.setToolTipText("Undo mutate on selected phrases");
        cntrlPanel.add(undo);

        mutate.setIcon(
            new ImageIcon(GM.gui.PhraseCntrl.class.getResource(
                "mutate.png")));
        mutate.setToolTipText("Mutate selected phrases");
        mutate.addActionListener(this);
        cntrlPanel.add(mutate);


        redo.setIcon(
                new ImageIcon(GM.gui.PhraseCntrl.class.getResource(
                "redo16.png")));
        redo.setToolTipText("Redo mutate on selected phrases");
        redo.addActionListener(this);
        cntrlPanel.add(redo);


        copy.setIcon(
            new ImageIcon(GM.gui.PhraseCntrl.class.getResource(
                "editcopy16.png")));

        copy.addActionListener(this);
        copy.setToolTipText("Copy selected phrases to insert point");


        cntrlPanel.add(copy);
        kill.setIcon(
                new ImageIcon(GM.gui.PhraseCntrl.class.getResource(
                        "kill16.png")));

        kill.addActionListener(this);
        kill.setToolTipText("Mute selected phrases");
        cntrlPanel.add(kill);



       // this.setBorder(BorderFactory.createLineBorder(Color.black));
        add(cntrlPanel);


    }



}

