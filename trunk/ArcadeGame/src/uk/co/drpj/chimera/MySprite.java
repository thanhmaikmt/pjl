package uk.co.drpj.chimera;

import java.awt.Component;
import java.awt.Graphics;
import java.awt.Image;
import java.awt.Rectangle;
import javax.swing.JComponent;

class MySprite extends Rectangle.Float {

    Image img;
    float dxdt;
    float dydt;
    boolean dead;
    SpriteMover mover;
    ChimeraApp outer;
    float initY;
    boolean dormant;
    final int score;

    MySprite(Image img, int yBase, SpriteMover mover, ChimeraApp outer, int score) {
        super();
        this.outer = outer;
        this.img = img;
        this.width = img.getWidth(outer);
        this.height = img.getHeight(outer);
        this.mover = mover;
        initY = yBase;
        dead = true;
        this.score = score;
    }
//
//    MySprite(Image i, int yAirLine, TargetSpriteMover mover, ChimeraApp aThis, int i0) {
//        throw new UnsupportedOperationException("Not yet implemented");
//    }

    void setState(float x, float y, float dxdt, float dydt) {
        this.x = x;
        this.y = y;
        this.dxdt = dxdt;
        this.dydt = dydt;
        this.dead = false;
    }

    boolean shoot(int xf, int yf) {
        if (xf < (x + width / 10.0)) {
            return false;
        }
        if (xf > (x + (9 * width) / 10.0)) {
            return false;
        }
        if (yf < (y - height / 2.0)) {
            return false;
        }
        if (yf > (y + height / 2.0)) {
            return false;
        }
//        if (!dead) {
//            outer.score++;
//        }
        dead = true;
//        this.dormant=true;
        return true;
    }

    void draw(Graphics g) {
        g.drawImage(img, (int) x, (int) y - img.getHeight(null) / 2, outer);
    }
}
