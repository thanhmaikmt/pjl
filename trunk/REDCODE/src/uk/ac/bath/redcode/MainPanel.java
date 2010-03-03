/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

/*
 * MainPanel.java
 *
 * Created on 15-Feb-2010, 16:32:11
 */
package uk.ac.bath.redcode;

import java.awt.Color;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.MouseEvent;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.StringReader;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.Observable;
import java.util.Observer;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.JComponent;
import javax.swing.JMenuItem;
import javax.swing.JPopupMenu;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;
import javax.swing.text.BadLocationException;
import javax.swing.text.Caret;
import javax.swing.text.DefaultCaret;
import javax.swing.text.DefaultHighlighter;
import javax.swing.text.DefaultHighlighter.DefaultHighlightPainter;

/**
 *
 * @author pjl
 */
public class MainPanel extends javax.swing.JPanel {

    Machine mach;
    CodeTableModel codeModel;
    private Character inChar;
    //   String out = "";
    private final DefaultHighlighter hilit;
    private final DefaultHighlightPainter painter;
    final static Color HILIT_COLOR = Color.RED;
    private JPopupMenu popup;
      private final Caret caret;

    /** Creates new form MainPanel */
    public MainPanel(final Machine mach, URL codebase) {
        popup = makePopup(codebase);
        this.mach = mach;
        mach.setIO(new IO() {

            public void put(int x) {
                String c = "" + (char) x;
                int caretPos = ioTextArea.getCaretPosition();
                switch ((char)x) {
                    case '\n':
                        ioTextArea.insert("\n", caretPos);
                        ioTextArea.setCaretPosition(caretPos + 1);
                        break;
                    case '\b':
                        if (caretPos==0) break;
                        ioTextArea.replaceRange(null, caretPos-1, caretPos);
                        caretPos = Math.max(0, caretPos - 1);
                        break;
                    default:
                        ioTextArea.insert(c, caretPos);
                        ioTextArea.setCaretPosition(caretPos + 1);
                }
                 // caret.setVisible(true);
                //   System.out.println("OUT:>" + out + "<");
            }

            public Integer get() {
           //     ioTextArea.requestFocus();
                if (ioTextArea.hasFocus()) caret.setVisible(true);
                else caret.setVisible(false);
                // Don't block for input (we are on an event thread here)
                // Let the machine ask until there is a character.
                if (inChar == null) {
                    if (ioTextArea.hasFocus()) statusPanel.setText("Waiting for input . . .");
                    else statusPanel.setText("Click IO panel to gain focus for input . . .");
                    return null;
                } else {
                    Integer ret = new Integer((int) inChar);
                    inChar = null;
                    return ret;
                }
            }
        });

        codeModel = new CodeTableModel(mach);
        initComponents();
        codeTable.setModel(codeModel);
        mach.addObserver(new Observer() {

            public void update(Observable o, Object arg) {
                codeModel.fireTableDataChanged();
                int line = mach.getPC();
                codeTable.setRowSelectionInterval(line, line);
                codeTable.scrollRectToVisible(codeTable.getCellRect(line, line, true));
                if (!mach.isRunning()) {
                    statusPanel.setText("Halted");
                    runButton.setSelected(false);
                }
                //           ioTextArea.setText(out);
            }
        });


        codeTable.getColumn(codeModel.getColumnName(0)).setMinWidth(30);
        codeTable.getColumn(codeModel.getColumnName(1)).setMinWidth(220);
        sizeText.setText("" + mach.getSize());
        editPanel.setSelectionColor(Color.red);


        hilit = new DefaultHighlighter();
        painter = new DefaultHighlighter.DefaultHighlightPainter(HILIT_COLOR);
        editPanel.setHighlighter(hilit);
        editPanel.getDocument().addDocumentListener(new DocumentListener() {

            public void insertUpdate(DocumentEvent e) {
                hilit.removeAllHighlights();
            }

            public void removeUpdate(DocumentEvent e) {
                hilit.removeAllHighlights();
            }

            public void changedUpdate(DocumentEvent e) {
                hilit.removeAllHighlights();
            }
        });
        ioTextArea.setEditable(false);
        caret = ioTextArea.getCaret();
    }

    /** This method is called from within the constructor to
     * initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is
     * always regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        jScrollPane1 = new javax.swing.JScrollPane();
        editPanel = new javax.swing.JTextArea();
        stepBut = new javax.swing.JButton();
        codeTableScroll = new javax.swing.JScrollPane();
        codeTable = new javax.swing.JTable();
        loadBut = new javax.swing.JButton();
        runButton = new javax.swing.JToggleButton();
        statusPanel = new javax.swing.JLabel();
        machSizelabel = new javax.swing.JLabel();
        sizeText = new javax.swing.JTextField();
        speedSplider = new javax.swing.JSlider();
        jLabel3 = new javax.swing.JLabel();
        fileButton = new javax.swing.JButton();
        jScrollPane2 = new javax.swing.JScrollPane();
        ioTextArea = new javax.swing.JTextArea();
        prettyButton = new javax.swing.JButton();

        jScrollPane1.setBorder(javax.swing.BorderFactory.createTitledBorder("Editor"));

        editPanel.setColumns(4);
        editPanel.setFont(new java.awt.Font("Courier New", 1, 14)); // NOI18N
        editPanel.setRows(500);
        editPanel.setToolTipText("Type in redcode or load file(right mouse)");
        editPanel.setWrapStyleWord(true);
        editPanel.setAutoscrolls(true);
        editPanel.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mousePressed(java.awt.event.MouseEvent evt) {
                editPanelMousePressed(evt);
            }
        });
        jScrollPane1.setViewportView(editPanel);

        stepBut.setText("Step");
        stepBut.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                stepActionPerformed(evt);
            }
        });

        codeTableScroll.setBorder(javax.swing.BorderFactory.createTitledBorder("Machine"));

        codeTable.setModel(new javax.swing.table.DefaultTableModel(
            new Object [][] {
                {null, null, null, null},
                {null, null, null, null},
                {null, null, null, null},
                {null, null, null, null}
            },
            new String [] {
                "Title 1", "Title 2", "Title 3", "Title 4"
            }
        ));
        codeTable.setEnabled(false);
        codeTableScroll.setViewportView(codeTable);

        loadBut.setText("Compile/Load");
        loadBut.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                loadButActionPerformed(evt);
            }
        });

        runButton.setText("Run/Stop");
        runButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                runButtonActionPerformed(evt);
            }
        });

        statusPanel.setBorder(new javax.swing.border.SoftBevelBorder(javax.swing.border.BevelBorder.LOWERED));

        machSizelabel.setText("Machine Size");

        sizeText.setText("100");
        sizeText.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                sizeTextActionPerformed(evt);
            }
        });

        speedSplider.setMajorTickSpacing(1);
        speedSplider.setMaximum(10);
        speedSplider.setMinimum(1);
        speedSplider.setMinorTickSpacing(1);
        speedSplider.setPaintLabels(true);
        speedSplider.setPaintTicks(true);
        speedSplider.setSnapToTicks(true);
        speedSplider.setValue(1);
        speedSplider.addChangeListener(new javax.swing.event.ChangeListener() {
            public void stateChanged(javax.swing.event.ChangeEvent evt) {
                speedSpliderStateChanged(evt);
            }
        });

        jLabel3.setText("speed");

        fileButton.setText("File");
        fileButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                fileButtonActionPerformed(evt);
            }
        });

        ioTextArea.setColumns(20);
        ioTextArea.setRows(5);
        ioTextArea.setBorder(javax.swing.BorderFactory.createTitledBorder("IO"));
        ioTextArea.addKeyListener(new java.awt.event.KeyAdapter() {
            public void keyPressed(java.awt.event.KeyEvent evt) {
                ioTextAreaKeyPressed(evt);
            }
        });
        jScrollPane2.setViewportView(ioTextArea);

        prettyButton.setText("Pretty");
        prettyButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                prettyButtonActionPerformed(evt);
            }
        });

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(this);
        this.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING)
                            .addGroup(javax.swing.GroupLayout.Alignment.LEADING, layout.createSequentialGroup()
                                .addGap(6, 6, 6)
                                .addComponent(jLabel3)
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                .addComponent(speedSplider, javax.swing.GroupLayout.DEFAULT_SIZE, 482, Short.MAX_VALUE))
                            .addGroup(layout.createSequentialGroup()
                                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING)
                                    .addGroup(layout.createSequentialGroup()
                                        .addComponent(fileButton, javax.swing.GroupLayout.PREFERRED_SIZE, 131, javax.swing.GroupLayout.PREFERRED_SIZE)
                                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                        .addComponent(prettyButton, javax.swing.GroupLayout.DEFAULT_SIZE, 94, Short.MAX_VALUE))
                                    .addComponent(machSizelabel))
                                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                                    .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                        .addComponent(loadBut, javax.swing.GroupLayout.PREFERRED_SIZE, 165, javax.swing.GroupLayout.PREFERRED_SIZE)
                                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED))
                                    .addGroup(layout.createSequentialGroup()
                                        .addGap(36, 36, 36)
                                        .addComponent(sizeText, javax.swing.GroupLayout.PREFERRED_SIZE, 76, javax.swing.GroupLayout.PREFERRED_SIZE)
                                        .addGap(77, 77, 77)))
                                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING)
                                    .addComponent(runButton, javax.swing.GroupLayout.Alignment.LEADING, javax.swing.GroupLayout.PREFERRED_SIZE, 113, javax.swing.GroupLayout.PREFERRED_SIZE)
                                    .addComponent(stepBut, javax.swing.GroupLayout.Alignment.LEADING, javax.swing.GroupLayout.PREFERRED_SIZE, 112, javax.swing.GroupLayout.PREFERRED_SIZE))
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED))
                            .addComponent(jScrollPane1, javax.swing.GroupLayout.DEFAULT_SIZE, 539, Short.MAX_VALUE))
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING)
                            .addComponent(codeTableScroll, javax.swing.GroupLayout.DEFAULT_SIZE, 422, Short.MAX_VALUE)
                            .addComponent(jScrollPane2, javax.swing.GroupLayout.Alignment.LEADING, javax.swing.GroupLayout.DEFAULT_SIZE, 422, Short.MAX_VALUE)))
                    .addComponent(statusPanel, javax.swing.GroupLayout.DEFAULT_SIZE, 961, Short.MAX_VALUE)))
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING)
                    .addComponent(jScrollPane1, javax.swing.GroupLayout.DEFAULT_SIZE, 394, Short.MAX_VALUE)
                    .addComponent(codeTableScroll, javax.swing.GroupLayout.DEFAULT_SIZE, 394, Short.MAX_VALUE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createSequentialGroup()
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                            .addComponent(fileButton)
                            .addComponent(prettyButton)
                            .addComponent(loadBut)
                            .addComponent(stepBut))
                        .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING, false)
                            .addGroup(layout.createSequentialGroup()
                                .addGap(8, 8, 8)
                                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                                    .addComponent(machSizelabel)
                                    .addComponent(sizeText, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                                    .addComponent(runButton))
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
                                .addComponent(speedSplider, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                            .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                                .addComponent(jLabel3)
                                .addGap(29, 29, 29))))
                    .addComponent(jScrollPane2, javax.swing.GroupLayout.PREFERRED_SIZE, 149, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(statusPanel, javax.swing.GroupLayout.PREFERRED_SIZE, 27, javax.swing.GroupLayout.PREFERRED_SIZE))
        );
    }// </editor-fold>//GEN-END:initComponents

    private void loadButActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_loadButActionPerformed

        String blueCode = editPanel.getText();
        Prism prism = new Prism();

        try {
            String redCode = prism.compile(blueCode);

//            System.out.println("----------------");
//            System.out.println(redCode);
//            System.out.println("----------------");
            BufferedReader reader = new BufferedReader(new StringReader(redCode));
            ioTextArea.setText("");
            hilit.removeAllHighlights();
            mach.load(reader);
            statusPanel.setText("LOADED OK");
        } catch (RedCodeParseException ex) {

            //
            try {

                int errorLine = ex.getLine();
                int i1 = editPanel.getLineStartOffset(errorLine);
                int i2 = editPanel.getLineEndOffset(errorLine);
                hilit.addHighlight(i1, i2, painter);
            } catch (BadLocationException ex1) {
                Logger.getLogger(MainPanel.class.getName()).log(Level.SEVERE, null, ex1);
            }

            statusPanel.setText("Error at line " + mach.getParseLine() + "  :  " + ex.userString());
        }

    }//GEN-LAST:event_loadButActionPerformed

    private void stepActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_stepActionPerformed
        resetStatusPanel();
        try {
            mach.step();
        } catch (RedCodeParseException ex) {
            Logger.getLogger(MainPanel.class.getName()).log(Level.SEVERE, null, ex);
        }
        statusPanel.setText(mach.getStatus());
    }//GEN-LAST:event_stepActionPerformed

    private void runButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_runButtonActionPerformed
        if (runButton.isSelected()) {
            statusPanel.setText("Running");
            mach.run();
        } else {
            statusPanel.setText("Stopped");
            mach.stop();
        }
    }//GEN-LAST:event_runButtonActionPerformed

    private void sizeTextActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_sizeTextActionPerformed
        int size = Integer.parseInt(sizeText.getText());
        mach.setSize(size);
    }//GEN-LAST:event_sizeTextActionPerformed

    private void speedSpliderStateChanged(javax.swing.event.ChangeEvent evt) {//GEN-FIRST:event_speedSpliderStateChanged
        mach.setSpeed(speedSplider.getValue()*speedSplider.getValue());
    }//GEN-LAST:event_speedSpliderStateChanged

    private void fileButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_fileButtonActionPerformed
        System.out.println(evt);
        JComponent c = (JComponent) evt.getSource();
        int x = c.getX() + c.getWidth() / 2;
        int y = c.getY() + c.getHeight() / 2;

        popup.show(this, x, y);
    }//GEN-LAST:event_fileButtonActionPerformed

    private void editPanelMousePressed(java.awt.event.MouseEvent evt) {//GEN-FIRST:event_editPanelMousePressed
        if (evt.getButton() != MouseEvent.BUTTON3) {
            return;
        }
        popup.show(this, evt.getX(), evt.getY()); // TODO add your handling code here:
    }//GEN-LAST:event_editPanelMousePressed

    private void prettyButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_prettyButtonActionPerformed
        String prettyCode = Pretty.makePretty(editPanel.getText());
        editPanel.setText(prettyCode);
    }//GEN-LAST:event_prettyButtonActionPerformed

    private void ioTextAreaKeyPressed(java.awt.event.KeyEvent evt) {//GEN-FIRST:event_ioTextAreaKeyPressed
        if (!Character.isDefined(evt.getKeyChar())) {
            return;
        }
        inChar = evt.getKeyChar();
    }//GEN-LAST:event_ioTextAreaKeyPressed
    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JTable codeTable;
    private javax.swing.JScrollPane codeTableScroll;
    private javax.swing.JTextArea editPanel;
    private javax.swing.JButton fileButton;
    private javax.swing.JTextArea ioTextArea;
    private javax.swing.JLabel jLabel3;
    private javax.swing.JScrollPane jScrollPane1;
    private javax.swing.JScrollPane jScrollPane2;
    private javax.swing.JButton loadBut;
    private javax.swing.JLabel machSizelabel;
    private javax.swing.JButton prettyButton;
    private javax.swing.JToggleButton runButton;
    private javax.swing.JTextField sizeText;
    private javax.swing.JSlider speedSplider;
    private javax.swing.JLabel statusPanel;
    private javax.swing.JButton stepBut;
    // End of variables declaration//GEN-END:variables

    private void resetStatusPanel() {
        statusPanel.setText("");
    }

    void setEditText(String str) {
        editPanel.setText(str);
    }

    void loadFromURL(URL name) throws IOException {
        String str = "";
        BufferedReader in = new BufferedReader(
                new InputStreamReader(
                name.openStream()));

        String inputLine;

        while ((inputLine = in.readLine()) != null) {
            //   System.out.println(inputLine);
            str = str + inputLine + "\n";
        }

        in.close();
        setEditText(str);

    }

    JPopupMenu makePopup(final URL urlBase) {

        JPopupMenu menu = new JPopupMenu();


        //  String fna = codeBase + "/prog";

        //  final URL url;
        try {
            URL url = new URL(urlBase + "list.txt");


            System.out.println(url);

            java.net.URLConnection con;
            con = url.openConnection();

            con.connect();

            java.io.BufferedReader in = new java.io.BufferedReader(new java.io.InputStreamReader(con.getInputStream()));
            String line;

            while ((line = in.readLine()) != null) {

                System.out.println(line);
                final JMenuItem item = new JMenuItem(line);
                menu.add(item);
                item.addActionListener(new ActionListener() {

                    public void actionPerformed(ActionEvent e) {
                        String fna = item.getActionCommand();
                        System.out.println(item.getActionCommand());
                        try {
                            URL url = getClass().getResource("/prog/" + fna);

                            loadFromURL(url);// new URL(urlBase + "/" + fna));
                        } catch (IOException ex) {
                            Logger.getLogger(RedcodeApplet.class.getName()).log(Level.SEVERE, null, ex);
                        }
                    }
                });
            }

        } catch (MalformedURLException ex) {
            Logger.getLogger(RedcodeApplet.class.getName()).log(Level.SEVERE, null, ex);
        } catch (IOException ex) {
            Logger.getLogger(RedcodeApplet.class.getName()).log(Level.SEVERE, null, ex);
        }
        // TODO overwrite start(), stop() and destroy() methods
        return menu;

    }
}
