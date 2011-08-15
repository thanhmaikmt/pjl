
/*
 *
 * Copyright (c) 2006 P.J.Leonard
 * 
 * http://www.frinika.com
 * 
 * This file is part of Frinika.
 * 
 * Frinika is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.

 * Frinika is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.

 * You should have received a copy of the GNU General Public License
 * along with Frinika; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */
package uk.co.drpj.audio.gui;

import java.awt.Color;
import java.awt.Graphics;
import java.awt.event.ActionEvent;
import javax.swing.AbstractAction;
import javax.swing.ButtonGroup;
import javax.swing.JMenu;
import javax.swing.JMenuItem;
import javax.swing.JPanel;
import javax.swing.JRadioButtonMenuItem;
import uk.co.drpj.audio.CycliclyBufferedAudio;

/**
 *
 * @author pjl
 */
public class ScopePanel extends JPanel {

    CycliclyBufferedAudio buffer;
    float x[];
    private int nSamp;
    int padX = 10;
    JMenu menu;

    private boolean isOn=true;

    public ScopePanel(CycliclyBufferedAudio buffer, int nnSamp) {
        this.buffer = buffer;
        this.nSamp = nnSamp;
        setBackground(null);
        
        menu = new JMenu("Scope");
        final float Fs = 44100;
        ButtonGroup group = new ButtonGroup();

        JMenuItem item = new JRadioButtonMenuItem(new AbstractAction("2 Sec") {

            public void actionPerformed(ActionEvent e) {
                nSamp = (int) (2 * Fs);
            }
        });
        menu.add(item);
    
        group.add(item);

        item = new JRadioButtonMenuItem(new AbstractAction("1 Sec") {

            public void actionPerformed(ActionEvent e) {
                nSamp = (int) (1 * Fs);
            }
        });
        menu.add(item);
        group.add(item);

        item = new JRadioButtonMenuItem(new AbstractAction("500 mS") {

            public void actionPerformed(ActionEvent e) {
                nSamp = (int) (.5 * Fs);
            }
        });
        menu.add(item);
        group.add(item);
        item.setSelected(true);


        item = new JRadioButtonMenuItem(new AbstractAction("200 mS") {

            public void actionPerformed(ActionEvent e) {
                nSamp = (int) (.2 * Fs);
            }
        });
        menu.add(item);
        group.add(item);



        item = new JRadioButtonMenuItem(new AbstractAction("100 mS") {

            public void actionPerformed(ActionEvent e) {
                nSamp = (int) (.1 * Fs);
            }
        });
        menu.add(item);
        group.add(item);



        item = new JRadioButtonMenuItem(new AbstractAction("50 mS") {

            public void actionPerformed(ActionEvent e) {
                nSamp = (int) (.05 * Fs);
            }
        });
        menu.add(item);
        group.add(item);


    }

    @Override
    public void paintComponent(Graphics g) {
        super.paintComponent(g);
        if (!isOn) return;
       
        if (x == null || x.length != nSamp);

        x = new float[nSamp];

        buffer.grabEnd(x, nSamp);
        int midY = getHeight() / 2;

        int iy1 = midY;
        float x1 = padX;
        float dx = (getWidth() - 2.0f * padX) / nSamp;
        float scaleY = getHeight();
        int ix1 = (int) x1;
        g.setColor(Color.BLACK);

        for (int i = 0; i < nSamp; i++) {
            x1 += dx;
            int ix2 = (int) x1;
            // if (ix2 == ix1 ) continue;
            int iy2 = (int) (midY + scaleY * x[i]);
            if (ix1 == ix2 && iy1 == iy2) {
                continue;
            }
            g.drawLine(ix1, iy1, ix2, iy2);
            ix1 = ix2;
            iy1 = iy2;
        }
    }
    
    public JMenu  getMenu() {
        return menu;
    }

    public void setOn(boolean enabled) {
        isOn=enabled;
    }

   
}
