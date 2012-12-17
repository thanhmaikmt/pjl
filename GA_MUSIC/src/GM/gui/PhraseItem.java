package GM.gui;

import javax.swing.*;
import java.awt.Container;
import java.util.*;
import GM.music.*;
import javax.swing.*;
import javax.swing.border.*;
import java.awt.*;


public class PhraseItem extends PianoRollItem implements Observer,RectSelectable { // , ActionListener {

    JFrame editFrame;
    Phrase phrase;
    String displayStr="not set";

  //  FlowLayout flowLayout1 = new FlowLayout();

    PianoRoll pianoRoll;

    Border selectedBorder=BorderFactory.createRaisedBevelBorder();//BevelBorder.RAISED,Color.WHITE,Color.LIGHT_GRAY);
    Border unSelectedBorder=BorderFactory.createLoweredBevelBorder();//BevelBorder.RAISED,Color.LIGHT_GRAY,Color.DARLIGHT_GRAY););

    boolean isVis;


    public PhraseItem(Phrase phrase, PianoRoll pr) {

        this.pianoRoll = pr;
        this.phrase = phrase;
      //  tweakPanel = new TweakPanel(phrase);
        phrase.addObserver(this);
        update(null, Message.MODIFIED);
    }

    public Phrase getPhrase() {
        return phrase;
    }

    public void setSelected(boolean yes) {
        phrase.setSelected(yes);
    }



    public void paintComponent(Graphics g) {
        super.paintComponent(g);
        g.setColor(Color.WHITE);
        g.drawString(displayStr,getWidth()-30,getHeight()-4);
    }



    public void update(Observable o, Object cmd) {

        //      assert (o == phrase);
        Message mess = (Message) cmd;

        if (mess== Message.KILLED) {

            Container p = getParent();
            if (p != null) {
                p.remove(this);
            }
            pianoRoll.phraseView.rePosition(); // @ TODO  no deleting of Phrases unless Player is killed ?
        } else {
            //  System.out.println(hash);

          Color c;

          if (phrase.isMute()) c=Color.darkGray;
          else c = new Color(phrase.colorHashCode());

          if (phrase.isSelected() ) setBorder(selectedBorder);
          else setBorder(unSelectedBorder);

          setBackground(c);


          displayStr=phrase.multiplier.intValue()+ "/" + phrase.pulsePerBeat.intValue();



            pianoRoll.phraseView.rePosition();

        }
    }


}
