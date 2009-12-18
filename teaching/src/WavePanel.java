
import java.awt.Color;
import java.awt.Graphics;
import java.awt.Graphics2D;
import javax.swing.JPanel;

/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
/**
 *
 * @author pjl
 */
class WavePanel extends JPanel {

    private final WaveEq eq;

    public WavePanel(WaveEq eq) {
        this.eq = eq;
        setBackground(Color.BLACK);
    }

    public void paintComponent(Graphics g1) {
        super.paintComponent(g1);
        Graphics2D g = (Graphics2D) g1;

        double s[] = eq.getState();
        int n = s.length;
        int w = getWidth();
        int h = getHeight();
        g.clearRect(0, 0, w, h);

        g.setColor(Color.red);

        float yZero = h / 2;
        float dx = ((float) w) / n;
        float x0 = 0.0f;
        float yScale = yZero;

        float y0 = (float) (yZero + s[0] * yScale);
        float x1;
        float y1;

        for (int i = 1; i < n; i++) {
            x1 = i*dx;
            y1 = (float) (yZero + s[i] * yScale);
            g.drawLine((int) x0, (int) y0, (int) x1, (int) y1);
            x0=x1;
            y0=y1;
        }
    }
}
