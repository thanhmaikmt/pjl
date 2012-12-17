package GM.gui;

import java.awt.*;
import java.util.*;
import GM.tweak.*;
import GM.gui.tweak.*;
import javax.swing.*;
import GM.music.*;

/**
 * <p>Title: </p>
 *
 * <p>Description: </p>
 *
 * <p>Copyright: Copyright (c) 2005</p>
 *
 * <p>Company: </p>
 *
 * @author not attributable
 * @version 1.0
 */
public class PlayerCntrl extends JPanel implements Tweakables, Observer {
    Player playerSet;


    TweakableInt lowT = new TweakableInt(10, 120, 60, "Lowest");
    TweakableInt rangeT = new TweakableInt(12, 100, 24, "Range");

    protected Vector<Tweakable> tweaks = new Vector<Tweakable>();

    GridBagLayout gridBagLayout1 = new GridBagLayout();

    public PlayerCntrl() {
        //        this.voice=v;
        tweaks.add(lowT);
        tweaks.add(rangeT);
        lowT.addObserver(this);
        rangeT.addObserver(this);

        addMidiTweaks();

        try {
            jbInit();
        } catch (Exception exception) {
            exception.printStackTrace();
        }
        selectPlayer(null);
    }


    void addMidiTweaks() {
        Midi.Controller[] ctrl = Midi.cntrlTable;

        for (int i = 0; i < ctrl.length; i++) {
            TweakableMidiCtrl c = new TweakableMidiCtrl(ctrl[i].cntrl,
                    ctrl[i].defVal, ctrl[i].name);

            tweaks.add(c);
            c.addObserver(this);
        }

    }

    /**
     * Set control values the focused player
     *
     * @param p Player
     */
    void selectPlayer(Player p) {
      //  System.out.println("set Voice: " +  v);
        if (p == playerSet && p != null) {
            return;
        }



//        playerSet.lockId(true);


        for(Tweakable myt:getTweaks()) {
            if (p != null) {
                Tweakable t = Tweakable.getTweak(myt.getLabel(), p);
                assert (t != null);
                myt.setEnabled(true);
                myt.setNumber(t.getNumber());
            } else {
                myt.setEnabled(false);
            }
        }
        playerSet = p;
    }

    boolean xxxx = false;

    public void update(Observable o, Object arg) {

        System.out.println("PlayerCntrl update:" + o + " " + arg);

        Player player = null;
      //  Voice voice = null;
        Song song = Simphoney.getSong();
        if (song != null) {
          //  System.out.println(" SONG OK ");
            Band b = song.getBand();
            if (b != null) {
                player= b.getSelectedPlayer();
            }
        }


        if (o instanceof Tweakable) {
            if (xxxx) return;
            if (player == null ) return;
            Tweakable t = (Tweakable) o;
            Tweakable tv = Tweakable.getTweak(t.getLabel(), player);
            tv.setNumber(t.getNumber());
        } else if (o instanceof Player) {
            if (player == playerSet) return;
            xxxx = true;
            selectPlayer(player);
            xxxx = false;
        }else if (o instanceof Band) {
            if (arg == Message.SELECTION_CHANGE) {
                if (player == playerSet) return;
                xxxx = true;
                selectPlayer(player);
                xxxx = false;
            } else if ( arg == Message.ADD_PLAYER) {
                Player p = Simphoney.getSong().getBand().lastPlayer();
                p.addObserver(this);
            }
        } else {

        }

        // System.out.println(" Hi! You should probably override update() in your subclass of Voice !!!!");
    }

    public Vector<Tweakable> getTweaks() {
        return tweaks;
    }

    void makeGui() {

        Iterator<Tweakable> iter = getTweaks().iterator();

        int row = 0;
        while (iter.hasNext()) {
            Tweakable t = iter.next();
            SpinTweaker slider = new SpinTweaker(t);
            JLabel label = new JLabel(t.getLabel());

            add(label,
                new GridBagConstraints(0, row, 1, 1, 1.0, 0.0
                                       , GridBagConstraints.WEST,
                                       GridBagConstraints.NONE,
                                       new Insets(2, 2, 2, 2), 0, 0));

            add(slider.getComponent(),
                new GridBagConstraints(1, row, 1, 1, 1.0, 0.0
                                       , GridBagConstraints.CENTER,
                                       GridBagConstraints.BOTH,
                                       new Insets(2, 2, 2, 2), 0, 0));

            row++;

        }
    }


    private void jbInit() throws Exception {
        setLayout(gridBagLayout1);
        makeGui();
    }
}
