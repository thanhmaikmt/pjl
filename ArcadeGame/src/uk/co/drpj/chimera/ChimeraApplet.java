//package uk.co.drpj.chimera;
//
//import java.awt.Color;
//import java.awt.Dimension;
//import java.awt.Font;
//import java.awt.Graphics;
//import java.awt.GraphicsConfiguration;
//import java.awt.Image;
//import java.awt.MediaTracker;
//import java.awt.Rectangle;
//import java.awt.Toolkit;
//import java.awt.event.ActionEvent;
//import java.awt.event.ActionListener;
//import java.awt.event.MouseAdapter;
//import java.awt.event.MouseEvent;
//import java.io.IOException;
//import java.net.MalformedURLException;
//import java.net.URL;
//import java.util.ArrayList;
//import java.util.Random;
//import java.util.logging.Level;
//import java.util.logging.Logger;
//import javax.swing.JApplet;
//import javax.swing.JButton;
//import javax.swing.JPanel;
//import javax.swing.Timer;
//import javazoom.jl.decoder.JavaLayerException;
//import uk.co.drpj.audio.AudioEngine;
//import uk.co.drpj.audio.ClipResource;
////import uk.org.toot.audio.core.AudioBuffer;
//
///**************************************/
//public class ChimeraApplet extends JApplet  {
//
//    private Image backGroundImage;
//    private Image foreGroundImage;
//    private Image waveImage;
//    private Image[] waterShipImages;
//    private MediaTracker mediaTracker;
//    int animationDelay = 100;
//    ArrayList<MySprite> sprites = new ArrayList<MySprite>();
//    private int spritesLength = 0;
//    static GraphicsConfiguration graphicConf;
//    Image cursorImage;
//    int xCursor;
//    int yCursor;
//    //  private float yShipWaterLine;
////    private SpriteMover targetMover;
//    private float dt = (float) (1e-3 * animationDelay);
//    int height;
//    int width;
//    int cnt = 0;
//    int ammo;
//    int timeLimit = 200;
//    int timeLeft;
//    private AudioEngine audioEngine;
//    private ClipResource backgroundMusic;
//    private ClipResource applause;
//    boolean gameOver = false;
//    Image gameOverImage;
//    private ClipResource[] shot = new ClipResource[1];
//    private ClipResource laughter;
//    private ClipResource reward;
//    int score;
//    ArrayList<MySprite> targetSprites = new ArrayList<MySprite>();
//    ArrayList<MySprite> waveSprites = new ArrayList<MySprite>();
//    GameOverPanel gameOverPanel;
//    private int hiScoreThreshOld = -1;
//    HighScoreDialog hiScoreDialog;
//    JButton newGameBut;
//    Font font = new Font("Lucida Typewriter Bold", Font.BOLD, 24);
//    Color opaqueBackGround = new Color(255, 255, 255, 180);
//    private Image[] waterMonsterImages;
//    private Image[] airShipImages;
//    private Image[] roadShipImages;
//    private Image[] airMonsterImages;
//    private int nTarget = 6;
//
//    void makeSprites() {
//
//        int waveSep = 30;
//        int yShipWaterLine = height - 200;
//        int yMonsterWaterLine = height - 160;
//        int yRoadWaterLine = height - 120;
//
//        int yAirLine = 250;
//
//        spritesLength = 0;
//        int yWave = 8 * (height) / 9;
//        int waveAmp = waveSep / 5;
//        float waveSpeed = 5.0f;   // rads  per sec
//
//
//        TargetSpriteMover mover = new TargetSpriteMover(yAirLine);
//
//        for (Image i : airShipImages) {
//            MySprite sprite = new MySprite(i, yAirLine, mover, this,-5);
//            sprites.add(sprite);
//            targetSprites.add(sprite);
//            spritesLength = spritesLength + i.getWidth(this) + 100;
//        }
//
//
//
//
//        for (Image i : airMonsterImages) {
//            MySprite sprite = new MySprite(i, yAirLine, mover, this,1);
//            sprites.add(sprite);
//            targetSprites.add(sprite);
//            spritesLength = spritesLength + i.getWidth(this) + 100;
//        }
//
//
//        int iWave = 2;
//        WaveSpriteMover waveMover =
//                new WaveSpriteMover(waveSpeed, (float) (iWave * Math.PI * 2.0 / 3.0), waveAmp, 0, (float) yWave - iWave * waveSep, this);
//
//        MySprite sprite = new MySprite(waveImage, 0, waveMover, this,0);
//
//        sprites.add(sprite);
//        waveSprites.add(sprite);
//
//
//
//
//        mover = new TargetSpriteMover(yShipWaterLine);
//
//        for (Image i : waterShipImages) {
//            sprite = new MySprite(i, yShipWaterLine, mover, this,-5);
//            sprites.add(sprite);
//            targetSprites.add(sprite);
//            spritesLength = spritesLength + i.getWidth(this) + 100;
//        }
//
//
//        iWave = 1;
//        waveMover =
//                new WaveSpriteMover(waveSpeed, (float) (iWave * Math.PI * 2.0 / 3.0), waveAmp, 0, (float) yWave - iWave * 3.0f * waveAmp, this);
//
//        sprite = new MySprite(waveImage, 0, waveMover, this,0);
//
//        sprites.add(sprite);
//        waveSprites.add(sprite);
//
//// Sea monsters
//
//
//        mover = new TargetSpriteMover(yMonsterWaterLine);
//
//        for (Image i : waterMonsterImages) {
//            sprite = new MySprite(i, (int) yMonsterWaterLine, mover, this,1);
//            sprites.add(sprite);
//            targetSprites.add(sprite);
//            spritesLength = spritesLength + i.getWidth(this) + 100;
//        }
//
//
//        iWave = 0;
//        waveMover =
//                new WaveSpriteMover(waveSpeed, (float) (iWave * Math.PI * 2.0 / 3.0), waveAmp, 0, (float) yWave - iWave * 3.0f * waveAmp, this);
//
//        sprite = new MySprite(waveImage, 0, waveMover, this,0);
//
//        sprites.add(sprite);
//        waveSprites.add(sprite);
//
//
//        mover = new TargetSpriteMover(yRoadWaterLine);
//
//        for (Image i : roadShipImages) {
//            sprite = new MySprite(i, (int) yRoadWaterLine, mover, this,-5);
//            sprites.add(sprite);
//            targetSprites.add(sprite);
//            spritesLength = spritesLength + i.getWidth(this) + 100;
//        }
//
////        for (MySprite s : sprites) {
////
////            float dxdt;
////            do {
////                dxdt = (float) (200.0 * (rand.nextDouble() - 0.5)); // Pixels per sec.
////            } while (Math.abs(dxdt) < 5);
////            float dydt = 0.0f;
////            float x = (float) (rand.nextDouble() * spritesLength / 4);
////
////            s.setState(x, s.initY, dxdt, dydt);
////
////        }
//
//
//
//
//    }
//
//    void newGame() {
//        ammo = 60;
//        cnt = 0;
//        score = 0;
//        timeLeft = timeLimit;
//        gameOver = false;
//        if (gameOverPanel != null) {
//            gameOverPanel.setVisible(false);
//            hiScoreDialog.setVisible(false);
//            newGameBut.setVisible(false);
//        }
//    }
//
//    void gameOver() {
//        audioEngine.playClip(applause);
//        gameOver = true;
//        gameOverPanel.setVisible(true);
//
//        if (score > hiScoreThreshOld) {
//            int y = gameOverPanel.getY();// +
//            y += gameOverPanel.yName;
//            int x = gameOverPanel.getX() + 30;
//            hiScoreDialog.setLocation(y, x);
//            hiScoreDialog.setHighScore();
//
//        }
//        gameOverPanel.setVisible(true);
//        newGameBut.setVisible(true);
//    }
//
//    Image[] loadSet(String names[]) {
//
//        Image images[] = new Image[names.length];
//
//        for (int i = 0; i < names.length; i++) {
//            URL urlB = ChimeraApplet.class.getResource("images/" + names[i]);
//            images[i] =
//                    Toolkit.getDefaultToolkit().
//                    getImage(urlB);
//            mediaTracker.addImage(
//                    images[i], 0);
//        }
//        return images;
//    }
//
//    void loadImages() {
//        mediaTracker =
//                new MediaTracker(this);
//
//        URL urlC = ChimeraApplet.class.getResource("images/crosshairsRed.png");
//
//        cursorImage =
//                Toolkit.getDefaultToolkit().
//                getImage(urlC);
//        mediaTracker.addImage(
//                cursorImage, 0);
//
//
//        URL url = ChimeraApplet.class.getResource("images/BACKGROUNDnight.png");
//        backGroundImage =
//                Toolkit.getDefaultToolkit().
//                getImage(url);
//        mediaTracker.addImage(
//                backGroundImage, 0);
//
//
//        url = ChimeraApplet.class.getResource("images/WAVES.png");
//        waveImage =
//                Toolkit.getDefaultToolkit().
//                getImage(url);
//        mediaTracker.addImage(
//                waveImage, 0);
//
//
//        url = ChimeraApplet.class.getResource("images/BRIDGEframe2.png");
//        foreGroundImage =
//                Toolkit.getDefaultToolkit().
//                getImage(url);
//        mediaTracker.addImage(
//                foreGroundImage, 0);
//
//        url = ChimeraApplet.class.getResource("images/game_over.png");
//        gameOverImage =
//                Toolkit.getDefaultToolkit().
//                getImage(url);
//
//        mediaTracker.addImage(
//                gameOverImage, 0);
//
//
//
//
//        waterShipImages = loadSet(new String[]{"SHIP04.png"});
//
//
//        roadShipImages = loadSet(new String[]{"SHIP03.png"});
//
//
//        airShipImages = loadSet(new String[]{"SHIP01.png", "SHIP02.png"});
//
//        waterMonsterImages = loadSet(new String[]{"monsterGREEN.png", "monsterRED.png"});
//
//        airMonsterImages = loadSet(new String[]{"monsterPurple.png", "monsterORANGE.png"});
//
//        try {
//            mediaTracker.waitForID(0);
//        } catch (InterruptedException e) {
//            System.out.println(e);
//        }
//
//    }
//
//    @Override
//    public void init() {
//        newGame();
//        setLayout(null);
//        audioEngine = new AudioEngine();
//        hiScoreDialog = new HighScoreDialog(this);
//
//
//        loadImages();
//
//
//        width = backGroundImage.getWidth(this);
//        height = backGroundImage.getHeight(this);
//        while (width == -1 || height == -1) {
//            System.out.println(
//                    "Waiting for image");
//            width = backGroundImage.getWidth(this);
//            height = backGroundImage.getHeight(this);
//        }
//
//
//        makeSprites();
//        setMinimumSize(new Dimension(width, height));
//        setPreferredSize(new Dimension(width, height));
//
//
//        Timer t = new Timer(animationDelay, new ActionListener() {
//
//            public void actionPerformed(ActionEvent e) {
//                cnt++;
//                animate();
//                repaint();
//            }
//        });
//
//        t.start();
//        t.setCoalesce(false);
//
//
//        addMouseListener(new MouseAdapter() {
//
//            @Override
//            public void mousePressed(MouseEvent e) {
//                if (ammo <= 0 || timeLeft <= 0) {
//                    return;
//                }
//                //System.out.println("BANG");
//                // boolean hit = false;
//
//                audioEngine.playClip(shot[0]);
//                boolean hit = false;
//                int x = e.getX();
//                int y = e.getY();
//                for (MySprite s : sprites) {
//                    if (s.dead) {
//                        continue;
//                    }
//                    if (s.shoot(x, y)) {
//                        score++;
//                    }
//                    hit = true;
//                }
//                if (hit) {
//                    audioEngine.playClip(reward);
//                } else {
//                    audioEngine.playClip(laughter);
//                }
//                ammo--;
//            }
//        });
//
//        addMouseMotionListener(new MouseAdapter() {
//
//            @Override
//            public void mouseMoved(MouseEvent e) {
//                xCursor = (int) e.getX();
//                yCursor = (int) e.getY();
//            }
//        });
//        xCursor = width / 2;
//        yCursor = height / 2;
//
//
//        try {
//            //    backgroundMusic = audioEngine.loadClip(getClass().getResource("/uk/co/drpj/chimera/images/Coinssilver.mp3"));
//            applause = audioEngine.loadClip(getClass().getResource("/uk/co/drpj/chimera/images/applause.mp3"));
//            shot[0] = audioEngine.loadClip(getClass().getResource("/uk/co/drpj/chimera/images/uzi.mp3"));
//            //  shot[1] = audioEngine.loadClip(getClass().getResource("/uk/co/drpj/chimera/images/gunshot.mp3"));
//            laughter = audioEngine.loadClip(getClass().getResource("/uk/co/drpj/chimera/images/laughter.mp3"));
//            reward = audioEngine.loadClip(getClass().getResource("/uk/co/drpj/chimera/images/reward.mp3"));
//        } catch (JavaLayerException ex) {
//            Logger.getLogger(ChimeraApplet.class.getName()).log(Level.SEVERE, null, ex);
//        } catch (MalformedURLException ex) {
//            Logger.getLogger(ChimeraApplet.class.getName()).log(Level.SEVERE, null, ex);
//        } catch (IOException ex) {
//            Logger.getLogger(ChimeraApplet.class.getName()).log(Level.SEVERE, null, ex);
//        }
//
//        audioEngine.configureAudio();
//        if (backgroundMusic != null) {
//            audioEngine.playClip(backgroundMusic);
//        }
//
//        JPanel main = new GamePanel(this);
//
//
//
//        newGameBut = new JButton("NEW GAME");
//        int borderX = 250;
//        int borderY = 60;
//
//        Rectangle bounds = new Rectangle(borderX, height - 2 * borderY, width - 2 * borderX, borderY);
//
//        newGameBut.setBounds(bounds);
//        add(newGameBut);
//        newGameBut.setFont(font);
//        newGameBut.setBackground(opaqueBackGround);
//        newGameBut.setVisible(false);
//        newGameBut.addActionListener(new ActionListener() {
//
//            public void actionPerformed(ActionEvent arg0) {
//                newGame();
//            }
//        });
//
//        //    hiScoreDialog.setOpaque(false);
//
//        borderX = 260;
//        borderY = 80;
//        bounds = new Rectangle(borderX, borderY, width - 2 * borderX, borderY);
//        hiScoreDialog.setBounds(bounds);
//        add(hiScoreDialog);
//        hiScoreDialog.setVisible(false);
//
//        gameOverPanel = new GameOverPanel(this);
//
//        // gameOverPanel.setBackground(Color.pink);
//        gameOverPanel.setOpaque(true);
//        borderX = 250;
//        bounds = new Rectangle(borderX, borderY, width - 2 * borderX, height - 2 * borderY);
//        gameOverPanel.setBounds(bounds);
//        add(gameOverPanel);
//
//        add(main);
//        main.setBounds(new Rectangle(0, 0, width, height));
//        gameOverPanel.setVisible(false);
//
//    }
//
//    void drawScene(Graphics g) {
//
//        g.drawImage(
//                backGroundImage, 0, 0, this);
//
//
//        for (MySprite s : sprites) {
//            if (onScreen(s)) {
//                s.draw(g);
//            }
//        }
//
//        g.drawImage(
//                foreGroundImage, 0, 0, this);
//
//    }
//
//    private void animate() {
//
//
//        int count = 0;
//        for (MySprite s : targetSprites) {
//
//            s.mover.move(s, dt);
//            if (onScreen(s)) {
//                count++;
//            } else {
//                s.dead=true;
//            }
//        }
//
//        if (count < nTarget) {
//
//            int i = 0;
//            MySprite ss = null;
//            do {
//                i = rand.nextInt(targetSprites.size());
//            } while ((!(ss = targetSprites.get(i)).dead) || onScreen(ss));
//
//            ss.y = ss.mover.getbase();
//            ss.dydt = 0;
//            ss.dead = false;
//
//            float vel = (float) (20.0f * (rand.nextDouble() + 0.4) * Math.min(score + 4, 20));
//
//
//            if (rand.nextBoolean()) {
//                ss.x = width;
//                ss.dxdt = -vel;
//            } else {
//                ss.x = -ss.width;
//                ss.dxdt = vel;
//            }
//        }
//
//
//
//
//        for (MySprite s : waveSprites) {
//            s.mover.move(s, dt);
//
//        }
//    }
//    Random rand = new Random();
//
//    private boolean onScreen(MySprite s) {
//        return s.intersects(0, 0, width, height);
//    }
//}
