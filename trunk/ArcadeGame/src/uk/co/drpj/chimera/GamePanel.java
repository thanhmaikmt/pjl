package uk.co.drpj.chimera;

import java.awt.Color;
import java.awt.Cursor;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Image;
import java.awt.Point;
import java.awt.Toolkit;
import java.awt.image.BufferedImage;
import javax.swing.JPanel;

public class GamePanel extends JPanel {

    ChimeraApp outer;
 private Image offScreenImage;
  private Graphics offScreenGraphicsCtx;
    private Dimension screenSize;
    
    public GamePanel(ChimeraApp outer) {
        super();
        this.outer = outer;
          Point hot = new Point(0, 0);
        Image ii = new BufferedImage(1, 1, BufferedImage.TYPE_INT_ARGB);
        Cursor cc = Toolkit.getDefaultToolkit().createCustomCursor(ii,
                hot,
                "gun");
        setCursor(cc);

    }

    @Override
    public void paint(Graphics g) {
        if (offScreenGraphicsCtx == null || !getSize().equals(screenSize)) {
            screenSize = new Dimension(getSize());
            offScreenImage = createImage(getSize().width, getSize().height);
            offScreenGraphicsCtx = offScreenImage.getGraphics();
        }
        //end if
        outer.drawScene(offScreenGraphicsCtx);
//        offScreenGraphicsCtx.setFont(outer.font);
//        outer.timeLeft = outer.timeLimit - outer.cnt * outer.animationDelay / 1000;
//        if (outer.timeLeft > 0) {
//            String time = "Time Left: " + outer.timeLeft;
//            offScreenGraphicsCtx.setColor(Color.white);
//            offScreenGraphicsCtx.drawString(time, 20, 30);
//        } else {
//            if (!outer.gameOver) {
//                outer.gameOver();
//            }
//        }
////        String scoreStr = " Score: " + outer.score;
//        offScreenGraphicsCtx.setColor(Color.white);
//        offScreenGraphicsCtx.drawString(scoreStr, outer.width - 150, 30);
//        String ammoStr = " Ammo: " + outer.ammo;
//        offScreenGraphicsCtx.setColor(Color.white);
//        offScreenGraphicsCtx.drawString(ammoStr, outer.width / 2 - 75, 30);
        offScreenGraphicsCtx.drawImage(outer.cursorImage, outer.xCursor - 75, outer.yCursor - 75, this);
        if (outer.gameOver) {
            offScreenGraphicsCtx.drawImage(outer.gameOverImage, (outer.width - outer.gameOverImage.getWidth(null)) / 2, (outer.height - outer.gameOverImage.getHeight(null)) / 2, this);
        }
        if (offScreenImage != null) {
            g.drawImage(offScreenImage, 0, 0, this);
        }
    }
}
