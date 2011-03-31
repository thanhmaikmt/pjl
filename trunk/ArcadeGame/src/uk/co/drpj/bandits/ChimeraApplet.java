package uk.co.drpj.bandits;

import java.awt.Color;
import java.awt.Cursor;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.GraphicsConfiguration;
import java.awt.Image;
import java.awt.MediaTracker;
import java.awt.Point;
import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.Random;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.JApplet;
import javax.swing.Timer;
import javazoom.jl.decoder.JavaLayerException;
import uk.co.drpj.audio.AudioEngine;
import uk.co.drpj.audio.ClipResource;
//import uk.org.toot.audio.core.AudioBuffer;

/**************************************/
public class ChimeraApplet extends JApplet {

    private Image offScreenImage;
    private Image backGroundImage;
    private Image[] headImages;
    private Graphics offScreenGraphicsCtx;
    private MediaTracker mediaTracker;
    private int animationDelay = 10;
    ArrayList<MySprite> sprites = new ArrayList<MySprite>();
    private int spritesLength = 0;
    static GraphicsConfiguration graphicConf;
    private Dimension screenSize;
    private Image cursorImage;
    private int xCursor;
    private int yCursor;
    private float yEquilibrium;
    private SpriteMover mover;
    private float dt = (float) (1e-3 / animationDelay);
    private int height;
    private int width;
    int cnt = 0;
    private int ammo;
    int timeLimit = 60;
    int timeLeft;
    private AudioEngine audioEngine;
    private ClipResource backgroundMusic;
    private ClipResource applause;
    boolean gameOver = false;
    private Image gameOverImage;
    private ClipResource[] shot = new ClipResource[1];
    private ClipResource laughter;
    private ClipResource reward;
    private int score;

    void newGame() {
        ammo = 60;
        cnt = 0;
        score = 0;
        timeLeft = timeLimit;
        gameOver = false;
    }

    @Override
    public void init() {
        newGame();

        audioEngine = new AudioEngine();


        mediaTracker =
                new MediaTracker(this);

        URL urlC = ChimeraApplet.class.getResource("images/crosshairsRed.png");

        cursorImage =
                Toolkit.getDefaultToolkit().
                getImage(urlC);
        mediaTracker.addImage(
                cursorImage, 0);


        URL url = ChimeraApplet.class.getResource("images/abbey.png");
        backGroundImage =
                Toolkit.getDefaultToolkit().
                getImage(url);
        mediaTracker.addImage(
                backGroundImage, 0);

        url = ChimeraApplet.class.getResource("images/game_over.png");
        gameOverImage =
                Toolkit.getDefaultToolkit().
                getImage(url);
        mediaTracker.addImage(
                backGroundImage, 0);


        String heads[] = {"bandits_2.png", "bandits_3.png",
            "bandits_5.png", "bandits_4.png", "bandits_1.png"};

        headImages = new Image[heads.length];
        for (int i = 0; i < heads.length; i++) {
            URL urlB = ChimeraApplet.class.getResource("images/" + heads[i]);
            headImages[i] =
                    Toolkit.getDefaultToolkit().
                    getImage(urlB);
            mediaTracker.addImage(
                    headImages[i], 0);

        }


        try {
            mediaTracker.waitForID(0);
        } catch (InterruptedException e) {
            System.out.println(e);
        }



        width = backGroundImage.getWidth(this);
        height = backGroundImage.getHeight(this);
        while (width == -1 || height == -1) {
            System.out.println(
                    "Waiting for image");
            width = backGroundImage.getWidth(this);
            height = backGroundImage.getHeight(this);
        }

        yEquilibrium = (height) / 2;
        spritesLength = 0;

        float dxdt = 20000.0f * (rand.nextFloat() - 0.5f);
        float dydt = 1000.0f;

        for (Image i : headImages) {

            sprites.add(new MySprite(i, spritesLength, (int) yEquilibrium, dxdt, dydt));
            spritesLength = spritesLength + i.getWidth(this) + 100;

        }


        setMinimumSize(new Dimension(width, height));
        setPreferredSize(new Dimension(width, height));


        Timer t = new Timer(animationDelay, new ActionListener() {

            public void actionPerformed(ActionEvent e) {
                cnt++;
                animate();
                repaint();
            }
        });

        t.start();
        t.setCoalesce(false);

        Point hot = new Point(0, 0);
        Image ii = new BufferedImage(1, 1, BufferedImage.TYPE_INT_ARGB);
        Cursor cc = Toolkit.getDefaultToolkit().createCustomCursor(ii,
                hot,
                "gun");
        setCursor(cc);

        addMouseListener(new MouseAdapter() {

            @Override
            public void mousePressed(MouseEvent e) {
                if (ammo <= 0 || timeLeft <= 0) {
                    return;
                }
                //System.out.println("BANG");
                // boolean hit = false;

                audioEngine.playClip(shot[0],false);
                boolean hit = false;
                int x = e.getX();
                int y = e.getY();
                for (MySprite s : sprites) {
                    hit = hit | s.shoot(x, y);

                }
                if (hit) {
                    audioEngine.playClip(reward,false);
                } else {
                    audioEngine.playClip(laughter,false);
                }
                ammo--;
            }
        });

        addMouseMotionListener(new MouseAdapter() {

            @Override
            public void mouseMoved(MouseEvent e) {
                xCursor = (int) e.getX();
                yCursor = (int) e.getY();
            }
        });
        xCursor = width / 2;
        yCursor = height / 2;

        mover = new SpriteMover();

        try {
        //    backgroundMusic = audioEngine.loadClip(getClass().getResource("/uk/co/drpj/chimera/images/Coinssilver.mp3"));
            applause = audioEngine.loadClip(getClass().getResource("/uk/co/drpj/chimera/images/applause.mp3"));
            shot[0] = audioEngine.loadClip(getClass().getResource("/uk/co/drpj/chimera/images/uzi.mp3"));
          //  shot[1] = audioEngine.loadClip(getClass().getResource("/uk/co/drpj/chimera/images/gunshot.mp3"));
            laughter = audioEngine.loadClip(getClass().getResource("/uk/co/drpj/chimera/images/laughter.mp3"));
            reward = audioEngine.loadClip(getClass().getResource("/uk/co/drpj/chimera/images/reward.mp3"));
        } catch (JavaLayerException ex) {
            Logger.getLogger(ChimeraApplet.class.getName()).log(Level.SEVERE, null, ex);
        } catch (MalformedURLException ex) {
            Logger.getLogger(ChimeraApplet.class.getName()).log(Level.SEVERE, null, ex);
        } catch (IOException ex) {
            Logger.getLogger(ChimeraApplet.class.getName()).log(Level.SEVERE, null, ex);
        }

        audioEngine.configureAudio();
        if (backgroundMusic!= null) audioEngine.playClip(backgroundMusic,false);
    }

    @Override
    public void paint(Graphics g) {

        if (offScreenGraphicsCtx == null || !getSize().equals(screenSize)) {
            screenSize = new Dimension(getSize());
            offScreenImage =
                    createImage(getSize().width,
                    getSize().height);
            offScreenGraphicsCtx =
                    offScreenImage.getGraphics();
        }//end if

        drawScene(offScreenGraphicsCtx);

        Font font = new Font("Lucida Typewriter Bold", Font.BOLD, 24);
        offScreenGraphicsCtx.setFont(font);
        timeLeft = timeLimit - cnt * animationDelay / 1000;

        if (timeLeft > 0) {
            String time = "Time Left: " + timeLeft;

            offScreenGraphicsCtx.setColor(Color.white);

            offScreenGraphicsCtx.drawString(time, 20, 30);
        } else {
            if (!gameOver) {
                audioEngine.playClip(applause,false);
                gameOver = true;
            }

        }


        String scoreStr = " Score: " + score;

        offScreenGraphicsCtx.setColor(Color.white);

        offScreenGraphicsCtx.drawString(scoreStr, width - 150, 30);


        String ammoStr = " Ammo: " + ammo;

        offScreenGraphicsCtx.setColor(Color.white);

        offScreenGraphicsCtx.drawString(ammoStr, width / 2 - 75, 30);



        offScreenGraphicsCtx.drawImage(
                cursorImage, xCursor - 75, yCursor - 75, this);

        if (gameOver) {
            offScreenGraphicsCtx.drawImage(
                    gameOverImage, (width - gameOverImage.getWidth(null)) / 2, (height - gameOverImage.getHeight(null)) / 2, this);


        }

        if (offScreenImage != null) {
            g.drawImage(
                    offScreenImage, 0, 0, this);
        }



    }

    private void drawScene(Graphics g) {

        g.drawImage(
                backGroundImage, 0, 0, this);


        for (MySprite s : sprites) {
            s.draw(g);
        }

    }

    private void animate() {


        for (MySprite s : sprites) {
            mover.move(s, dt);
            while (s.x + s.w > spritesLength) {
                s.x = s.x - spritesLength;
            }

            while (s.x + s.w < 0) {
                s.x = s.x + spritesLength;
            }

            if (s.y > height * 2) {
                s.y = yEquilibrium;
                s.dead = false;
                s.x = width;
                s.dxdt = 20000.0f * (rand.nextFloat() - 0.5f) * Math.min(score + 2, 25);
            }
        }
    }

    class MySprite {

        Image img;
        float x;
        float y;
        float dxdt;
        float dydt;
        int w;
        int h;
        private boolean dead;

        MySprite(Image img, int x, int y, float dxdt, float dydt) {
            this.img = img;
            this.x = x;
            this.y = y;
            this.dxdt = dxdt;
            this.dydt = dydt;
            this.w = img.getWidth(ChimeraApplet.this);
            this.h = img.getHeight(ChimeraApplet.this);
        }

        boolean shoot(int xf, int yf) {

            if (xf < (x + w / 10.0)) {
                return false;
            }

            if (xf > (x + (9 * w) / 10.0)) {
                return false;
            }

            if (yf < (y - h / 2.0)) {
                return false;
            }

            if (yf > (y + h / 2.0)) {
                return false;
            }


            if (!dead) {

                score++;
            }

            dead = true;
            return true;

        }

        void draw(Graphics g) {

            g.drawImage(
                    img, (int) x, (int) y - img.getHeight(null) / 2, ChimeraApplet.this);

        }
    }
    Random rand = new Random();

    class SpriteMover {

        private float accelFactX = 500.0f;
        private float accelFactY = 5000.0f;
        private float damp = 0.1f;

        void move(MySprite s, float dt) {


            s.x = s.x + s.dxdt * dt;
            s.y = s.y + s.dydt * dt;

            s.dxdt = s.dxdt + accelFactX * (rand.nextFloat() - 0.5f);

            if (s.dead) {
                s.dydt = s.dydt + accelFactY * 0.3f;
            } else {
                s.dydt = s.dydt + accelFactY * ((rand.nextFloat() - 0.5f) + (yEquilibrium - s.y)) - damp * s.dydt;
            }
        }
    }
}
