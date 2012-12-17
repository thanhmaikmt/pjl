package GM.gui;

import GM.music.*;
import GM.jdbc.*;
import java.awt.*;

import javax.swing.*;
import java.awt.event.*;

public class SongSaveFrame extends JFrame implements ActionListener{
    GridBagLayout gridBagLayout1 = new GridBagLayout();
    JTextField titleWidget = new JTextField();
    JTextField artistWidget = new JTextField();
    JTextField genreWidget = new JTextField();
    JLabel artistLab = new JLabel();
    JLabel titleLab = new JLabel();
    JLabel genreLab = new JLabel();
    JButton cancelBut = new JButton();
    JButton saveBut = new JButton();
    Song perf;
    DataBase db;
    public SongSaveFrame(Song p,DataBase db) {
        perf=p;
        this.db=db;
        try {
            jbInit();
        } catch (Exception exception) {
            exception.printStackTrace();
        }
        pack();
        doLayout();
    }

    private void jbInit() throws Exception {
//        setPreferredSize(new Dimension(600,800));
  //      setMinimumSize(new Dimension(600,800));
        getContentPane().setLayout(gridBagLayout1);
        genreWidget.setColumns(80);
        titleWidget.setColumns(80);
        artistWidget.setColumns(80);
        artistLab.setText("Artist:");
        titleLab.setText("Title:");
        genreLab.setText("Genre:");


        artistWidget.setText(perf.getArtist());
        artistWidget.setEnabled(false);
        genreWidget.setText(perf.getGenre());
        titleWidget.setText(perf.getTitle());
        cancelBut.setText("cancel");
        saveBut.setText("save");
        saveBut.addActionListener(this);
        this.getContentPane().add(titleWidget,
                                  new GridBagConstraints(1, 0, 2, 1, 0.1, 0.0
                , GridBagConstraints.CENTER, GridBagConstraints.HORIZONTAL,
                new Insets(0, 0, 0, 0), 0, 0));
        this.getContentPane().add(artistWidget,
                                  new GridBagConstraints(1, 1, 2, 1, 0.1, 0.0
                , GridBagConstraints.CENTER, GridBagConstraints.HORIZONTAL,
                new Insets(0, 0, 0, 0), 0, 0));
        this.getContentPane().add(genreWidget,
                                  new GridBagConstraints(1, 2, 2, 1, 0.1, 0.0
                , GridBagConstraints.CENTER, GridBagConstraints.HORIZONTAL,
                new Insets(0, 0, 0, 0), 0, 0));
        this.getContentPane().add(titleLab,
                                  new GridBagConstraints(0, 0, 1, 1, 0.1, 0.0
                , GridBagConstraints.CENTER, GridBagConstraints.NONE,
                new Insets(0, 0, 0, 0), 0, 0));
        this.getContentPane().add(genreLab,
                                  new GridBagConstraints(0, 2, 1, 1, 0.1, 0.0
                , GridBagConstraints.CENTER, GridBagConstraints.NONE,
                new Insets(0, 0, 0, 0), 0, 0));
        this.getContentPane().add(artistLab,
                                  new GridBagConstraints(0, 1, 1, 1, 0.1, 0.0
                , GridBagConstraints.CENTER, GridBagConstraints.NONE,
                new Insets(0, 0, 0, 0), 0, 0));
        this.getContentPane().add(cancelBut,
                                  new GridBagConstraints(2, 3, 1, 1, 0.1, 0.0
                , GridBagConstraints.CENTER, GridBagConstraints.NONE,
                new Insets(0, 0, 0, 0), 0, 0));
        this.getContentPane().add(saveBut,
                                  new GridBagConstraints(1, 3, 1, 1, 0.1, 0.0
                , GridBagConstraints.CENTER, GridBagConstraints.NONE,
                new Insets(0, 0, 0, 0), 0, 0));
    }

    public void actionPerformed(ActionEvent e){
        Object src=e.getSource();


        if (src == saveBut) {


            try{
                perf.setHeaders(titleWidget.getText(),artistWidget.getText(),genreWidget.getText());
                new SimphoneySaver(db).saveSong(perf);
            } catch( Exception ee) {
                ee.printStackTrace();
            }
        } else if (src == cancelBut) {
            this.setVisible(false);
        }
        this.dispose();
    }
}
