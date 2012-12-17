package GM.gui;

//import GM.javasound.JavaSoundSynth;
import GM.music.*;
import javax.swing.tree.*;
import javax.swing.*;
import java.util.*;
import GM.music.IdString;
import javax.swing.event.TreeSelectionListener;
import javax.swing.event.TreeSelectionEvent;
import java.awt.*;
import GM.javasound.*;

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
 *
 */

public class VoiceTree extends JTree implements Observer  {

    final public Agent agent;

    class Agent extends Observable implements TreeSelectionListener {


        public void valueChanged(TreeSelectionEvent e) {
            DefaultMutableTreeNode node = (DefaultMutableTreeNode)
                                          getLastSelectedPathComponent();
            if (node == null) {
                return;
            }

            Object nodeInfo = node.getUserObject();

            if (node.isLeaf()) {
              //  System.out.println(nodeInfo);
               // int vid =((IdString)nodeInfo).id;
                DefaultMutableTreeNode bnode=(DefaultMutableTreeNode)node.getParent();
              //  IdString bid = (IdString)bnode.getUserObject();
              //  int bankId = bid.id;
              //  System.out.println(bankId);
                /* Hope that someone is listening (Performance?) */
                setChanged();
                notifyObservers(node.getUserObject());
            }
        }
    }


    public void update(Observable o,Object arg) {
        Player player=((Band)o).getSelectedPlayer();
        if (player == null) return;
        Voice voice = player .getVoice();


    }

    public VoiceTree() {
        super(myTreeRoot());
     //   setRootVisible(false);

        jbInit();
        addTreeSelectionListener(agent=new Agent());
    }

    /*
    public GMPatch getSelectedPatch() {

        DefaultMutableTreeNode node = (DefaultMutableTreeNode)
                                      getLastSelectedPathComponent();
        if (node == null) return null;

        Object nodeInfo = node.getUserObject();

        if (node.isLeaf()) {
            //  System.out.println(nodeInfo);

            //int vid = ((IdString) nodeInfo).id;
            DefaultMutableTreeNode bnode = (DefaultMutableTreeNode) node.getParent();
          //  IdString bid = (IdString) bnode.getUserObject();
          //  int bankId = bid.id;
           // System.out.println(bankId);
           Object o=bnode.getUserObject();
           assert(o instanceof VoicePatch);
            return o;
        }

        return null;
    }

*/

    public void jbInit() {
        this.setMinimumSize(new Dimension(0, 0));

    }

    /**
     * My stuff
     *
     */


    static private void visit(SynthNode node,DefaultMutableTreeNode parent) {



      //  if (node.size() == 0) return;



        for(int i=0;i< node.size();i++) {
            SynthNode child = node.nodeAt(i);
            DefaultMutableTreeNode childNode = new DefaultMutableTreeNode(child);
            parent.add(childNode);
            visit(child,childNode);
        }


    }

    static private DefaultMutableTreeNode myTreeRoot() {

        SynthNode root = Hub.the();

       // while(root.size() == 1)

       root=root.nodeAt(0);

       /*
        Vector<DefaultMutableTreeNode> vec = new Vector<DefaultMutableTreeNode>();


        for(int i=0;i<root.size();i++) {
            SynthNode n=root.nodeAt(i);
            DefaultMutableTreeNode tn = new DefaultMutableTreeNode(n);
            vec.add(tn);
            visit(n,tn);
        }
*/

       DefaultMutableTreeNode tn = new DefaultMutableTreeNode(root);
       visit(root,tn);
       return tn;
   }
}
