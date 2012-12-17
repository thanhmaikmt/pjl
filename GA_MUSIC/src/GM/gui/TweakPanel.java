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
public class TweakPanel extends JPanel {
    Tweakables tweaks;

    int dcol=1;
    int drow=0;

    GridBagLayout gridBagLayout1 = new GridBagLayout();

    public TweakPanel(Tweakable t) {

        this.tweaks=new MyTweakables(t);

        try {
            jbInit();
        } catch (Exception exception) {
            exception.printStackTrace();
        }

    }

    public TweakPanel(Tweakables t) {


           this.tweaks=t;
           try {
               jbInit();
           } catch (Exception exception) {
               exception.printStackTrace();
           }

       }


    private void jbInit() throws Exception {

        setLayout(gridBagLayout1);

        Iterator <Tweakable> iter = tweaks.getTweaks().iterator();

        int row=0;
        int col=0;
        while(iter.hasNext()) {
            Tweakable t = iter.next();
            JLabel label = new JLabel(t.getLabel());
            JComponent tc=null;
            if (t instanceof TweakableList) {

                SpinListTweaker slider = new SpinListTweaker((TweakableList)t);
                tc=slider.getComponent();

            } else {
                SpinTweaker slider = new SpinTweaker(t);
                tc=slider.getComponent();
            }

            add(label,
                new GridBagConstraints(row ,col, 1, 1, 1.0, 0.0
                                       , GridBagConstraints.WEST,
                                       GridBagConstraints.NONE,
                                       new Insets(2, 2, 2, 2), 0, 0));

            add(tc,
                new GridBagConstraints(row+1, col, 1, 1, 1.0, 0.0
                                       , GridBagConstraints.CENTER,
                                       GridBagConstraints.BOTH,
                                       new Insets(2, 2, 2, 2), 0, 0));

            row = row + 2*drow;
            col= col+ dcol;
        }

        validate();
    }

    class MyTweakables implements Tweakables {

        Vector<Tweakable> list;

        MyTweakables(Tweakable t) {
            list=new Vector<Tweakable>();
            list.add(t);
        }
        public Vector<Tweakable> getTweaks() { return list;}
    }
}
