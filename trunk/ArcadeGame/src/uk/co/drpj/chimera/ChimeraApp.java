package uk.co.drpj.chimera;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.GraphicsConfiguration;
import java.awt.Image;
import java.awt.MediaTracker;
import java.awt.Rectangle;
import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.io.File;
import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.Random;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.swing.JApplet;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.Timer;
import javazoom.jl.decoder.JavaLayerException;
import uk.co.drpj.audio.AudioEngine;
import uk.co.drpj.audio.ClipResource;
//import uk.org.toot.audio.core.AudioBuffer;

/**************************************/
public class ChimeraApp extends JFrame {

    private Image backGroundImage;
    private Image foreGroundImage;
    private Image waveImage;
    Image oopsImage;
    private Image[] waterShipImages;
    private MediaTracker mediaTracker;
    int animationDelay = 100;
    ArrayList<MySprite> sprites = new ArrayList<MySprite>();
    //   private int spritesLength = 0;
    static GraphicsConfiguration graphicConf;
    Image cursorImage;
    int xCursor;
    int yCursor;
    //  private float yShipWaterLine;
//    private SpriteMover targetMover;
    private float dt = (float) (1e-3 * animationDelay);
    int height;
    int width;
    int cnt = 0;
    int ammo;
    int timeLimit = 60;
    int timeLeft;
    float bonusTime;
    private AudioEngine audioEngine;
    private ClipResource backgroundMusic;
    private ClipResource applause;
    boolean gameOver = false;
    Image gameOverImage;
    private ClipResource[] shot = new ClipResource[1];
    private ClipResource laughter;
    private ClipResource reward;
    int score;
    ArrayList<MySprite> targetSprites = new ArrayList<MySprite>();
    ArrayList<MySprite> waveSprites = new ArrayList<MySprite>();
    GameOverPanel gameOverPanel;
    private int hiScoreThreshOld = -1;
    HighScoreDialog hiScoreDialog;
    JButton newGameBut;
    Font font = new Font("Lucida Typewriter Bold", Font.BOLD, 24);
    Color opaqueBackGround = new Color(255, 255, 255, 180);
    private Image[] waterMonsterImages;
    private Image[] airShipImages;
    private Image[] roadShipImages;
    private Image[] numberImages;
    private Image[] airMonsterImages;
    private int nTarget = 6;
    private Image bonusImage;
    private ClipResource penalty;
    private boolean bonus = false;
    private boolean oops;
    int xCent, yCent, xTen, yTen, xUnit, yUnit;

    public ChimeraApp() {
        init();
        setUndecorated(true);
        setSize(width, height);
        setVisible(true);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    }

    void makeSprites() {

        int waveSep = 30;
        int yShipWaterLine = height - 200;
        int yMonsterWaterLine = height - 100;
        int yRoadWaterLine = height - 120;

        int yAirLine = 250;

//        spritesLength = 0;

        int yWave = 8 * (height) / 9;
        int waveAmp = waveSep / 5;
        float waveSpeed = 5.0f;   // rads  per sec


        TargetSpriteMover mover = new TargetSpriteMover(yAirLine);

        for (Image i : airShipImages) {
            MySprite sprite = new MySprite(i, yAirLine, mover, this, -5);
            sprites.add(sprite);
            targetSprites.add(sprite);
            //       spritesLength = spritesLength + i.getWidth(this) + 100;
        }




        for (Image i : airMonsterImages) {
            mover = new TargetSpriteMover(yAirLine, 160.0f, 2f, (float) (rand.nextDouble() * Math.PI));
            MySprite sprite = new MySprite(i, yAirLine, mover, this, 1);
            sprites.add(sprite);
            targetSprites.add(sprite);
            //        spritesLength = spritesLength + i.getWidth(this) + 100;
        }


        int iWave = 2;
        WaveSpriteMover waveMover =
                new WaveSpriteMover(waveSpeed, (float) (iWave * Math.PI * 2.0 / 3.0), waveAmp, 0, (float) yWave - iWave * waveSep, this);

        MySprite sprite = new MySprite(waveImage, 0, waveMover, this, 0);

        sprites.add(sprite);
        waveSprites.add(sprite);




        mover = new TargetSpriteMover(yShipWaterLine);

        for (Image i : waterShipImages) {
            sprite = new MySprite(i, yShipWaterLine, mover, this, -5);
            sprites.add(sprite);
            targetSprites.add(sprite);
            //           spritesLength = spritesLength + i.getWidth(this) + 100;
        }


        iWave = 1;
        waveMover =
                new WaveSpriteMover(waveSpeed, (float) (iWave * Math.PI * 2.0 / 3.0), waveAmp, 0, (float) yWave - iWave * 3.0f * waveAmp, this);

        sprite = new MySprite(waveImage, 0, waveMover, this, 0);

        sprites.add(sprite);
        waveSprites.add(sprite);

// Sea monsters

        for (Image i : waterMonsterImages) {
            mover = new TargetSpriteMover(yMonsterWaterLine, 60.0f, 5f, (float) (rand.nextDouble() * Math.PI));
            sprite = new MySprite(i, (int) yMonsterWaterLine, mover, this, 1);
            sprites.add(sprite);
            targetSprites.add(sprite);
            //        spritesLength = spritesLength + i.getWidth(this) + 100;
        }


        iWave = 0;
        waveMover =
                new WaveSpriteMover(waveSpeed, (float) (iWave * Math.PI * 2.0 / 3.0), waveAmp, 0, (float) yWave - iWave * 3.0f * waveAmp, this);

        sprite = new MySprite(waveImage, 0, waveMover, this, 0);

        sprites.add(sprite);
        waveSprites.add(sprite);


        mover = new TargetSpriteMover(yRoadWaterLine);

        for (Image i : roadShipImages) {
            sprite = new MySprite(i, (int) yRoadWaterLine, mover, this, -5);
            sprites.add(sprite);
            targetSprites.add(sprite);
            //        spritesLength = spritesLength + i.getWidth(this) + 100;
        }

    }

    void newGame() {
        ammo = 6000;
        cnt = 0;
        score = 0;
        timeLeft = timeLimit;
        gameOver = false;
        bonus = false;
        oops = false;

        for (MySprite s : targetSprites) {
            s.dead = true;
        }

        if (gameOverPanel != null) {
            gameOverPanel.setVisible(false);
            hiScoreDialog.setVisible(false);
            newGameBut.setVisible(false);
        }
    }

    void gameOver() {
        audioEngine.playClip(applause, false);
        gameOver = true;
        //    gameOverPanel.setVisible(true);
        bonus = false;
        oops = false;
//        if (score > hiScoreThreshOld) {
//            int y = gameOverPanel.getY();// +
//            y += gameOverPanel.yName;
//            int x = gameOverPanel.getX() + 30;
//            hiScoreDialog.setLocation(y, x);
//            hiScoreDialog.setHighScore();
//        }
//        gameOverPanel.setVisible(true);
        newGameBut.setVisible(true);
    }

    Image[] loadSet(String names[]) {

        Image images[] = new Image[names.length];

        for (int i = 0; i < names.length; i++) {

            URL urlB = ChimeraApp.class.getResource("images/" + names[i] + ".png");
            File file = new File(urlB.getFile());
            if (!file.exists()) {
                System.out.println(" NOT FOUND" + file);
            }


            images[i] =
                    Toolkit.getDefaultToolkit().
                    getImage(urlB);
            mediaTracker.addImage(
                    images[i], 0);
        }
        return images;
    }

    void loadImages() {
        mediaTracker =
                new MediaTracker(this);

        URL urlC = ChimeraApp.class.getResource("images/crosshairsRed.png");

        cursorImage =
                Toolkit.getDefaultToolkit().
                getImage(urlC);
        mediaTracker.addImage(
                cursorImage, 0);


        URL url = ChimeraApp.class.getResource("images/BACKGROUNDnight.png");
        backGroundImage =
                Toolkit.getDefaultToolkit().
                getImage(url);
        mediaTracker.addImage(
                backGroundImage, 0);

        url = ChimeraApp.class.getResource("images/Bonus.png");
        bonusImage =
                Toolkit.getDefaultToolkit().
                getImage(url);
        mediaTracker.addImage(
                bonusImage, 0);

        url = ChimeraApp.class.getResource("images/oops.png");
        oopsImage =
                Toolkit.getDefaultToolkit().
                getImage(url);
        mediaTracker.addImage(
                oopsImage, 0);

        url = ChimeraApp.class.getResource("images/WAVES.png");
        waveImage =
                Toolkit.getDefaultToolkit().
                getImage(url);
        mediaTracker.addImage(
                waveImage, 0);


        url = ChimeraApp.class.getResource("images/BRIDGEframe2.png");
        foreGroundImage =
                Toolkit.getDefaultToolkit().
                getImage(url);
        mediaTracker.addImage(
                foreGroundImage, 0);

        url = ChimeraApp.class.getResource("images/game_over.png");
        gameOverImage =
                Toolkit.getDefaultToolkit().
                getImage(url);

        mediaTracker.addImage(
                gameOverImage, 0);


        numberImages = loadSet(new String[]{"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"});



        waterShipImages = loadSet(new String[]{"SHIP04"});


        roadShipImages = loadSet(new String[]{"SHIP03"});


        airShipImages = loadSet(new String[]{"SHIP01", "SHIP02"});

        waterMonsterImages = loadSet(new String[]{"monsterGREEN", "monsterRED"});

        airMonsterImages = loadSet(new String[]{"monsterPurple", "monsterORANGE"});

        try {
            mediaTracker.waitForID(0);
        } catch (InterruptedException e) {
            System.out.println(e);
        }

    }

    //   @Override
    public void init() {
        newGame();
        setLayout(null);
        audioEngine = new AudioEngine();
        hiScoreDialog = new HighScoreDialog(this);


        loadImages();





        while (width == -1 || height == -1) {
            System.out.println(
                    "Waiting for image");
            width = backGroundImage.getWidth(this);
            height = backGroundImage.getHeight(this);
        }

        width = backGroundImage.getWidth(this);
        height = backGroundImage.getHeight(this);

        yCent = yTen = yUnit = 30; //numberImages[0].getHeight(this);

        int wid0 = numberImages[0].getWidth(this);
        xCent = (int) (width / 2.0 - wid0 * 2.0);
        xTen = (int) (width / 2.0 - wid0 * 1.0);
        xUnit = (int) (width / 2.0);

        makeSprites();
        setMinimumSize(new Dimension(width, height));
        setPreferredSize(new Dimension(width, height));


        Timer t = new Timer(animationDelay, new ActionListener() {

            public void actionPerformed(ActionEvent e) {
                cnt++;
                if (durInMillis() - bonusTime > 800) {
                    bonus = false;
                    oops = false;
                }
                animate();
                repaint();
            }
        });

        t.start();
        t.setCoalesce(false);


        addMouseListener(new MouseAdapter() {

            @Override
            public void mousePressed(MouseEvent e) {
                if (ammo <= 0 || timeLeft <= 0) {
                    return;
                }

                //System.out.println("BANG");
                // boolean hit = false;

                audioEngine.playClip(shot[0], false);

                int x = e.getX();
                int y = e.getY();
                int scoreBit = 0;

                int fact = 0;

                for (MySprite s : sprites) {
                    if (s.dead) {
                        continue;
                    }
                    if (s.shoot(x, y)) {

                        scoreBit += s.score;

                    }
                }

                if (scoreBit == 2) {
                    scoreBit = 10;
                }
                if (scoreBit == 3) {
                    scoreBit = 50;
                }


                if (scoreBit > 0) {
                    audioEngine.playClip(reward, false);
                    if (scoreBit > 1) {
                        bonus = true;
                        bonusTime = durInMillis();
                    }
                } else if (scoreBit < 0) {
                    bonus = false;
                    oops = true;
                    bonusTime = durInMillis();
                    audioEngine.playClip(penalty, false);
                } else {
                    audioEngine.playClip(laughter, false);
                }

                score += scoreBit;
                if (score < 0) {
                    score = 0;
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


        try {
            backgroundMusic = audioEngine.loadClip(getClass().getResource("/uk/co/drpj/chimera/images/background.mp3"));
            applause = audioEngine.loadClip(getClass().getResource("/uk/co/drpj/chimera/images/applause.mp3"));
            shot[0] = audioEngine.loadClip(getClass().getResource("/uk/co/drpj/chimera/images/uzi.mp3"));
            //  shot[1] = audioEngine.loadClip(getClass().getResource("/uk/co/drpj/chimera/images/gunshot.mp3"));
            laughter = audioEngine.loadClip(getClass().getResource("/uk/co/drpj/chimera/images/laughter.mp3"));
            penalty = audioEngine.loadClip(getClass().getResource("/uk/co/drpj/chimera/images/sploosh.mp3"));
            reward = audioEngine.loadClip(getClass().getResource("/uk/co/drpj/chimera/images/reward.mp3"));
        } catch (JavaLayerException ex) {
            Logger.getLogger(ChimeraApp.class.getName()).log(Level.SEVERE, null, ex);
        } catch (MalformedURLException ex) {
            Logger.getLogger(ChimeraApp.class.getName()).log(Level.SEVERE, null, ex);
        } catch (IOException ex) {
            Logger.getLogger(ChimeraApp.class.getName()).log(Level.SEVERE, null, ex);
        }

        audioEngine.configureAudio();
        if (backgroundMusic != null) {
            audioEngine.playClip(backgroundMusic, true);
        }

        JPanel main = new GamePanel(this);



        newGameBut = new JButton("NEW GAME");
        int borderX = 250;
        int borderY = 60;

        Rectangle bounds = new Rectangle(borderX, height - 2 * borderY, width - 2 * borderX, borderY);

        newGameBut.setBounds(bounds);
        add(newGameBut);
        newGameBut.setFont(font);
        newGameBut.setBackground(opaqueBackGround);
        newGameBut.setVisible(false);
        newGameBut.addActionListener(new ActionListener() {

            public void actionPerformed(ActionEvent arg0) {
                newGame();
            }
        });

        //    hiScoreDialog.setOpaque(false);

        borderX = 260;
        borderY = 80;
        bounds = new Rectangle(borderX, borderY, width - 2 * borderX, borderY);
        hiScoreDialog.setBounds(bounds);
        add(hiScoreDialog);
        hiScoreDialog.setVisible(false);

        gameOverPanel = new GameOverPanel(this);

        // gameOverPanel.setBackground(Color.pink);
        gameOverPanel.setOpaque(true);
        borderX = 250;
        bounds = new Rectangle(borderX, borderY, width - 2 * borderX, height - 2 * borderY);
        gameOverPanel.setBounds(bounds);
        add(gameOverPanel);

        add(main);
        main.setBounds(new Rectangle(0, 0, width, height));
        gameOverPanel.setVisible(false);

    }

    void drawScene(Graphics g) {

        g.drawImage(
                backGroundImage, 0, 0, this);


        for (MySprite s : sprites) {
            if (onScreen(s)) {
                s.draw(g);
            }
        }

        if (bonus) {
            g.drawImage(
                    bonusImage, (int) ((width - bonusImage.getWidth(this)) / 2.0), (int) ((height - bonusImage.getHeight(this)) / 2.0), this);
        }

        if (oops) {
            g.drawImage(
                    oopsImage, (int) ((width - oopsImage.getWidth(this)) / 2.0), (int) ((height - oopsImage.getHeight(this)) / 2.0), this);
        }

        g.drawImage(
                foreGroundImage, 0, 0, this);

        int cents = score / 100;

        int tens = (score % 100) / 10;

        int units = (score % 10);

        if (cents > 0) {
            g.drawImage(
                    numberImages[cents], xCent, yCent, this);
        }

        if (cents > 0 || tens > 0) {
            g.drawImage(
                    numberImages[tens], xTen, yTen, this);
        }

        g.drawImage(
                numberImages[units], xUnit, yUnit, this);


    }

    private void animate() {


        int count = 0;
        for (MySprite s : targetSprites) {

            s.mover.move(s, dt);
            if (onScreen(s)) {
                count++;
            } else {
                if (s.x > width * 2 || s.x + s.width < -width) {
                    s.dead = true;
                }
            }
        }

        if (count < nTarget) {

            int i = 0;
            i = rand.nextInt(targetSprites.size());
            MySprite ss = ss = targetSprites.get(i);

            if (ss.dead && !onScreen(ss)) {


                ss.y = ss.mover.getbase();
                ss.dydt = 0;
                ss.dead = false;

                float vel = (float) (10.0f * (rand.nextDouble() + 0.4) * Math.max(4, Math.min(score + 4, 40)));


                if (rand.nextBoolean()) {
                    ss.x = width + width * rand.nextFloat() / 2;
                    ss.dxdt = -vel;
                } else {
                    ss.x = -ss.width - width * rand.nextFloat() / 2;
                    ss.dxdt = vel;
                }
            }
        }



        for (MySprite s : waveSprites) {
            s.mover.move(s, dt);

        }
    }
    Random rand = new Random();

    private boolean onScreen(MySprite s) {
        return s.intersects(0, 0, width, height);
    }

    long durInMillis() {
        return cnt * animationDelay;

    }

    public static void main(String args[]) {
        new ChimeraApp();

    }
}
