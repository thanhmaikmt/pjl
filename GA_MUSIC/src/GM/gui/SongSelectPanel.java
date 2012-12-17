package GM.gui;

import GM.music.*;
import java.util.*;
import java.awt.*;

import javax.swing.*;
import GM.jdbc.*;
import java.awt.event.*;

public class SongSelectPanel extends JPanel implements ActionListener {
    BorderLayout borderLayout1 = new BorderLayout();
    JList list;
    JButton open;
    JButton cancel;
    JButton refresh;
    JButton append;
    JButton save;



    public SongSelectPanel() {
        list = new JList();

     //   Container panel = getContentPane();
     setLayout(borderLayout1);
     Container panel=this;
     panel.add(new JScrollPane(list));

        refresh();

        list.addMouseListener(new MouseAdapter() {
            public void mouseClicked(MouseEvent e) {
                if (DataBase.the()==null) return;
                if (e.getClickCount() == 2) {
                    int index = list.locationToIndex(e.getPoint());
                    Song song = (Song) (list.getModel().getElementAt(index));
                  //  System.out.println("Double clicked on Item " + song);
                    try {
                        Simphoney.setSong(song);
                        new SimphoneyLoader(DataBase.the()).loadSong(song);
                      //  song.setId(song.getId()); // @TODO hmmm dee dum (forcing TopFrame to see new title)
                    } catch (Exception ex) {
                        ex.printStackTrace();
                    }
                }
            }
        });

        JPanel buts = new JPanel();
        panel.add(buts, BorderLayout.SOUTH);
        buts.setLayout(new FlowLayout());

        open = new JButton("Open");
        buts.add(open);

        open.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                if (DataBase.the() == null) return ;
                Simphoney.getSong().setId(0);
                Song song = new Song((Song) list.getSelectedValue());

                try {
                    new SimphoneyLoader(DataBase.the()).loadSong(song);
                    Simphoney.setSong(song);
                  //  setVisible(false);
                } catch (Exception ex) {
                    ex.printStackTrace();
                 }

            }
        });


        cancel = new JButton("Cancel");
        buts.add(cancel);

        cancel.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                setVisible(false);
            }
        }
        );


        append = new JButton("Append");
      //  buts.add(append);

        append.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                if (DataBase.the() == null) return;
                Song song = new Song((Song) list.getSelectedValue());
                try {
                    new SimphoneyLoader(DataBase.the()).loadSong(song);
                    System.out.println(" OK SO FAR");
                } catch (Exception ex) {
                    ex.printStackTrace();
                }
                //Simphoney.setSong(song);
            }
        });


        save = new JButton(TopFrame.the().songSaveAction);
        buts.add(save);

        refresh = new JButton("Refresh");
        buts.add(refresh);

        refresh.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                refresh();
            }
        });

        validate();
      //  new javax.swing.Timer(2000,this).start();

    }


    public void actionPerformed(ActionEvent e) {
        refresh();
    }

    void refresh() {
        Vector<Song> songs = null;
        DataBase db = DataBase.the();

        if (db == null) return;

        try {
            songs = new SimphoneyLoader(db).getSongs();
        } catch (Exception ex) {
            ex.printStackTrace();
        }

        list.setListData(songs);
        list.validate();
    }

}
