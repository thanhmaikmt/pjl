/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package uk.co.drpj.chimera;

import java.awt.Color;
import java.awt.Graphics;
import java.util.Iterator;
import javax.swing.BoxLayout;
import javax.swing.JPanel;

/**
 *
 * @author pjl
 */
class GameOverPanel extends JPanel {
 
    int yName;
    int dyName=30;
    int yNameTop=60;
    ChimeraApp outer;
    public GameOverPanel(ChimeraApp aThis) {

        setOpaque(true);
        setBackground(aThis.opaqueBackGround);

        setLayout(new BoxLayout(this, BoxLayout.Y_AXIS));
        outer=aThis;
        yName=yNameTop+dyName;
    }

    
    @Override
    public void paintComponent(Graphics g) {
        super.paintComponent(g);

        setFont(outer.font);
        Iterator<Score> iter =outer.hiScoreDialog.highScore.iterator();
        g.setColor(Color.BLACK);
        int xName=(int) (getWidth() * .1);
        int xScore=(int) (getWidth() * .7);
        g.drawString("HI SCORES",xName , 30);

        for (int i=1;i<=10;i++) {

            int y=yNameTop+i*dyName;
            String name="_ _ _ _ _ _ _ _ _ _ ";
            String pts=" _ _ _";
            if (iter.hasNext()) {
                Score sc=iter.next();
                name=sc.name;
                pts=String.format("%3d", sc.score);
                yName=y;
            }
            g.drawString(name, xName, y);

            g.drawString(pts, xScore, y);
        }

        
    }

}
