package GM.gui;

import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

import GM.jdbc.*;
import GM.music.*;
import java.util.*;
import GM.javasound.ConnectFrame;
import org.jsresources.apps.mixer.SystemMixerFrame;
import GM.tweak.TweakableList;


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


public class TopFrame extends JFrame implements Observer {


    TweakableList scaleTweak = new TweakableList(Scale.types, Scale.types[0],
                                                 "Scale types");

    /** elemental panels */
     VoiceSelectPanel voiceSelectPanel;
     PlayerCntrl voiceCntrl;
     TweakPanel scaleTweakPanel;

     PartCntrl   partCntrl;
     PhraseCntrl phraseCntrl;
     PianoRoll   pianoRoll;
     TransportPanel transportPanel;
     AbstractAction songSaveAction;

     /** Contianers */

    JSplitPane splitPanel = new JSplitPane();

    RightPanel rightPanel;
    LeftMiddlePanel leftMiddlePanel;
    JFrame openFrame;
    ConnectFrame connectFrame;
    SystemMixerFrame mixerFrame;
    FFTFrame    fftFrame;

    Song song;

    static TopFrame the;

    static public TopFrame the() {
        return the;
    }

    static public void displayException(Exception ex) {
        int ans = JOptionPane.showConfirmDialog(TopFrame.the(),
                                                ex.getMessage(),
                                                " Java Exceptioin",
                                                JOptionPane.OK_OPTION);
    }

    public TopFrame() {

        assert(the==null);
        the=this;

        try {
            if (!SimphoneyApplet.isApplet) setDefaultCloseOperation(EXIT_ON_CLOSE);
            jbInit();

        } catch (Exception exception) {
            exception.printStackTrace();
        }

        openFrame = new JFrame();
        openFrame.setContentPane(new SongSelectPanel());
        openFrame.pack();
        connectFrame = new ConnectFrame();
        new PlayTimer();

     //   mixerFrame = new SystemMixerFrame();
      //  fftFrame = new FFTFrame();
      //  fftFrame.pack();
      //  fftFrame.setVisible(true);

    }


    private void makeMenus() {

        JMenuBar menuBar = new JMenuBar();

        JMenuItem item;
        // FILE items
        JMenu menu = new JMenu("file");
        menuBar.add(menu);

        item = new JMenuItem(new NewSongAction());
        menu.add(item);

        item = new JMenuItem(songSaveAction=new SaveSongAction());
        menu.add(item);

        item = new JMenuItem(new OpenAction());
        menu.add(item);

        item = new JMenuItem(new AbstractAction("Connect"){
            public void actionPerformed(ActionEvent e) {
                SimphoneyApp.connectToDataBase();
            }
        } );
        menu.add(item);

        item = new JMenuItem("Exit");
        item.addActionListener(new ExitAction());
        menu.add(item);


        menu = new JMenu("Midi/Audio");
        menuBar.add(menu);

        item=new JMenuItem(new ConnectAction());
        menu.add(item);

        item=new JMenuItem(new MixerAction());
        menu.add(item);

        DataBase db = DataBase.the();
        if (db != null) {
            if (db.mysqlUser().equals("simphoneyadmin")) {
                menu = new JMenu("admin");
                menuBar.add(menu);
                item = new JMenuItem(new ClearDBAction());
                menu.add(item);
            }
        }

        setJMenuBar(menuBar);

    }

    void makeElementalPanels() {
        voiceSelectPanel = new VoiceSelectPanel(); // VoiceCntrlPanel();
        voiceSelectPanel.voiceTree.setToolTipText("Set voice of selected player");

        voiceCntrl = new PlayerCntrl();
        voiceCntrl.setBorder(BorderFactory.createTitledBorder("Voice parameters"));

        scaleTweak.addObserver( new Observer(){
            public void update(Observable o,Object arg) {
                Simphoney.getSong().scaleTweak.set(scaleTweak.getObject().toString());
            }
        });


        scaleTweakPanel=new TweakPanel(scaleTweak);

        pianoRoll = new PianoRoll();
        phraseCntrl = new PhraseCntrl();
        partCntrl = new PartCntrl();
        transportPanel= new TransportPanel();
    }


    private void jbInit() throws Exception {
        makeElementalPanels();

        setSize(Layout.width,Layout.height);

        rightPanel = new RightPanel();
        leftMiddlePanel = new LeftMiddlePanel();

        setTitle("GM");

        makeMenus();

        splitPanel.add(leftMiddlePanel, JSplitPane.LEFT);
        splitPanel.add(rightPanel, JSplitPane.RIGHT);

        splitPanel.setDividerSize(2);
        setContentPane(splitPanel);
    }



    public void kill() {
          this.invalidate();
          the=null;
      }


      /**
       *
       * @param perf Song
       *
       * Responsible for ensuring connections to the GUI
       *
       */
      public void setSong(Song perf) {

          if (this.song != perf) {
              if (this.song != null) {
                  song.deleteObservers();
                  song.getBand().deleteObservers();
                  voiceSelectPanel.voiceTree.agent.deleteObserver(song);
                  /*
                                   song.deleteObserver(this);
                                   song.deleteObserver(pianoRoll);
                                   song.deleteObserver(playerListPanel);
                   */
               //   leftMiddlePanel.leftPanel.voiceSelectPanel.voiceTree.agent.deleteObserver(song);
              }
          }


          this.song = perf;
          //voiceSelectPanel.voiceTree.agent.deleteObservers();
          song.addObserver(this);
          voiceSelectPanel.voiceTree.agent.addObserver(song);
          pianoRoll.playerView.rebuild(song.getBand());
          pianoRoll.rebuild(song);
          scaleTweak.set(song.scaleType);
          song.addObserver(pianoRoll);
          song.addObserver(pianoRoll.playerView);
          song.addObserver(phraseCntrl);
          song.addObserver(partCntrl);
          song.getBand().addObserver(voiceCntrl);
          PlayTimer.reset();

    //      cntrls.setSong(song);
      }


      public void update(Observable o, Object arg) {
          Message mess = (Message) arg;
          //  System.out.println("TopFrame.update " + mess);

          if (mess.str.equals("Modified")) {
              setTitle(song.getTitle() + "*");
          }
          if (mess.str.equals("Saved")) {
              setTitle(song.getTitle());
          }

      }


    //**********************  Actions **************************************
     class AboutAction extends AbstractAction {
         public void actionPerformed(ActionEvent actionEvent) {
             TopFrame_AboutBox dlg = new TopFrame_AboutBox(TopFrame.this);
             Dimension dlgSize = dlg.getPreferredSize();
             Dimension frmSize = getSize();
             Point loc = getLocation();
             dlg.setLocation((frmSize.width - dlgSize.width) / 2 + loc.x,
                             (frmSize.height - dlgSize.height) / 2 + loc.y);
             dlg.setModal(true);
             dlg.pack();
             dlg.setVisible(true);
         }
     }

    class ExitAction extends AbstractAction {
           public void actionPerformed(ActionEvent actionEvent) {
               if (SimphoneyApplet.isApplet) setVisible(false);
               else System.exit(0);
           }
       };



      class LoopSongAction extends AbstractAction {

          LoopSongAction() {
              super("LoopSong");
          }

          public void actionPerformed(ActionEvent ee) {

              Vector<Part> s = song.getSections();
              Part f = s.elementAt(0);
              Part e = s.elementAt(s.size() - 1);
              //      Conductor.setLoop(f.start, e.end);
          }
      }


      public class SaveSongAction extends AbstractAction {

          SaveSongAction() {
              super("save", new ImageIcon(GM.gui.TopFrame.class.getResource(
                      "openFile.png")));
          }

          public void actionPerformed(ActionEvent e) {
              try {
                  if (song.getId() != 0) {
                      JOptionPane.showMessageDialog(TopFrame.this,
                                                    " Song has not been edited. I won't save duplicate songs.",
                                                    " Edit song before trying to save!",
                                                    JOptionPane.
                                                    INFORMATION_MESSAGE);
                      return;
                  }

                  JFrame f = new SongSaveFrame(song,DataBase.the());
                  f.setVisible(true);
              } catch (Exception ex) {
                  ex.printStackTrace();
              }
          }
      }


      /** **************************************************************************/

      class ClearDBAction extends AbstractAction {

          ClearDBAction() {
              super("clear", new ImageIcon(GM.gui.TopFrame.class.getResource(
                      "openFile.png")));
          }

          public void actionPerformed(ActionEvent e) {
              try {
                  DataBase.the().initialize();
              } catch (Exception ex) {
                  ex.printStackTrace();
              }
          }
      }


      /*******************************************************************************************/

      class NewSongAction extends AbstractAction {

          NewSongAction() {
              super("new", new ImageIcon(GM.gui.TopFrame.class.getResource(
                      "openFile.png")));
          }

          public void actionPerformed(ActionEvent e) {

              try {
                  Simphoney.setSong(new Song());
              } catch (Exception ex) {
                  ex.printStackTrace();
              }
          }
      }


      /*******************************************************************************************/

      class OpenAction extends AbstractAction {

          OpenAction() {
              super("open", new ImageIcon(GM.gui.TopFrame.class.getResource(
                      "openFile.png")));
          }

          public void actionPerformed(ActionEvent e) {

              try {
                  openFrame.setVisible(true);
              } catch (Exception ex) {
                  ex.printStackTrace();
              }
          }
      }



      class ConnectAction extends AbstractAction {

          ConnectAction() {
              super("connections", new ImageIcon(GM.gui.TopFrame.class.getResource(
                      "openFile.png")));
          }

          public void actionPerformed(ActionEvent e) {

              try {
                  connectFrame.setVisible(true);
              } catch (Exception ex) {
                  ex.printStackTrace();
              }
          }
      }


      class MixerAction extends AbstractAction {

          MixerAction() {
              super("mixer", new ImageIcon(GM.gui.TopFrame.class.getResource(
                      "openFile.png")));
          }

          public void actionPerformed(ActionEvent e) {

              try {
                  mixerFrame.setVisible(true);
              } catch (Exception ex) {
                  ex.printStackTrace();
              }
          }
      }


      /****************************************************************/


      /*
      class MutateSectionAction extends AbstractAction {

          MutateSectionAction() {
              super("Mutate", null);
          }

          public void actionPerformed(ActionEvent e) {
              song.getFocus().mutate();
          }
      }
*/

    public void setFrameTitle() {
        Song song = Simphoney.getSong();
        String user ="["+SimphoneyApp.the().getUser()+"]    ";
        if (song.getId() > 0) {
            Long t = PlayTimer.getPlayTime();
            setTitle(user + song + " " + t);
        } else {
            setTitle(user + song + " (modified)");

        }
    }


}
