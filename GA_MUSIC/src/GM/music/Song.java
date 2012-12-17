package GM.music;


import java.sql.*;
import GM.jdbc.*;
import java.util.*;

import GM.tweak.*;
import GM.genetic.GmRandom;
import GM.gui.SimphoneyApp;
import GM.gui.TopFrame;
//import GM.gui.TopFrame;


/**
 * Messages to observers
 *
 *     this       AddPart   section
 *                AddPlayer    player
 *                Kill
 *
 *    (focus)     SetFocus
 *                ReleaseFocus
 *
 * @author (your name)
 * @version (a version number or a date)
 */

public class Song extends Observable implements Observer, TableInfo {

    long mum;
    long dad;
    int rule;
    long id = -1;
    long playTime;
   // int scaleRep;
    Scale scale;
    Phrase dragPhrase;

    public final double bpm;
    Band band = new Band(this);
    protected Part playSection = null;
    protected Vector<Part> parts;

    boolean killed = false;
    boolean idLock=false;

    Vector<Part> partClip = new Vector<Part>();


    public String scaleType = Scale.types[0];

    public final TweakableList scaleTweak = new TweakableList(Scale.types, Scale.types[0],
                                                 "Scale types");

    public final TweakableInt rootTweak = new TweakableInt(0,12,1,"root");


    String title = "NewSong";
    String artist = SimphoneyApp.the().getUser();
    String genre = "";

    SongSequencer seq;
    boolean loopSelected;

    public Song() {

        parts = new Vector<Part>();
        makeTweaks();

        if (Conductor.the() != null) {
            Conductor.the().addObserver(this);
        }
        bpm = 60+new GmRandom().nextInt(120);

        int  scaleRep = Scale.WHITENOTE;
        int key = (int)new GmRandom().nextInt(12);
        scale = new Scale(scaleRep,key);
    }

    public Song(ResultSet res) throws SQLException {
        parts = new Vector<Part>();
        int i = 1;
        id = res.getInt("id");
        mum = res.getInt("mum");
        dad = res.getInt("dad");
        rule = res.getInt("rule");
        bpm = res.getDouble("tempo");

        int scaleRep = res.getInt("mode");
        int key = res.getInt("root");
        scale = new Scale(scaleRep,key);
        title = res.getString("title");
        artist = res.getString("artist");
        genre = res.getString("genre");
        playTime = res.getLong("playtime");
        makeTweaks();
    }

    public Song(Song song) {
        parts = new Vector<Part>();
        id = song.id;
        mum = song.mum;
        dad = song.dad;
        rule = song.rule;
        title = song.title;
        artist = song.artist;
        scale = song.scale;
        genre = song.genre;
        bpm = song.bpm;
        playTime = 0;
        makeTweaks();
    }


    void makeTweaks() {
        scaleTweak.addObserver(this);
    }

/*
    public String getScaleType() {
        return scaleType;
    }
*/

    public Vector<Part> getParts() {
        return parts;
    }

    public synchronized void rePositionParts() {
        Vector<Part> secL = null;
        try {
            secL = (Vector<Part>) parts.clone();
        } catch (Exception e) {
            e.printStackTrace();
        }

        Iterator<Part> iter = secL.iterator();
        Time t = new Time(0);
        while (iter.hasNext()) {
            Part sec = iter.next();
            if (sec.killed) {
                parts.removeElement(sec);
            } else {
                sec.start = t;
                t = t.add(sec.len);
            }
        }
        setChanged();
        notifyObservers(new Message("Modified"));
    }


    synchronized public void appendClippedParts() {
        Part lastSection = parts.elementAt(parts.size() - 1);
        Time start = lastSection.getEnd();
        Iterator<Part> iter = partClip.iterator();
        while (iter.hasNext()) {
            Part newSect = iter.next();
            newSect.start = start;
            start = start.add(newSect.len);
            parts.add(newSect);
            setChanged();
            notifyObservers(new Message("AddPart", newSect));
        }
    }


    public void newPart() {
        Time start;
        Part newPart;
        if (parts.size() == 0) {
            start = new Time(0);
        } else {
            Part lastPart = parts.elementAt(parts.size() - 1);
            start = lastPart.getEnd();
        }

        newPart = new Part(start, this);

        synchronized (band) {
            Iterator<Player> iter = band.getPlayers().iterator();

            while (iter.hasNext()) {
                Player player = iter.next();
                Phrase phrase = new Phrase(newPart, player);
                phrase.mutate();
                player.addPhrase(phrase);

            }
        }

        parts.add(newPart);
        setChanged();
        notifyObservers(new Message("AddPart", newPart));

        setId(0);
    }

    public SongSequencer getSequencer() {
        return seq;
    }

    public void play() {
        seq = new SongSequencer(this);
        seq.start();
    }


    public void rebuild() {
        Iterator<Part> iter = parts.iterator();

        while (iter.hasNext()) {
            iter.next().build(false);
        }

    }

    public void createPlayer(VoicePatch pat) {
        try {
            Voice v;
            Player p=createPlayer(v=Hub.the().createVoice(pat));
            v.allocate(true);
            p.updateAllCtrl(true);
            //p.setId(-1);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    /**
     * TODO is GMPatch really the way to do this
     *
     * @param o Observable
     * @param arg Object
     */
    public void update(Observable o, Object arg) {
        //   System.out.println(this +" update " + o + " " + arg);
        if (arg instanceof VoicePatch) {
            try {
                Player player = band.getSelectedPlayer();
                if (player == null) {
                    return;
                }
                VoicePatch p = (VoicePatch) arg;
                Voice voice = Hub.the().createVoice(p);
                player.setVoice(voice);
            } catch (Exception e) {
                e.printStackTrace();
            }
        } else if (arg == Conductor.tempoBPM) {
            setId(0);
        } else if (o == scaleTweak) {
            Object so = scaleTweak.getObject();
            String scaleType = (String) so;
            long scaleRep;
            if (scaleType.equals("WHITENOTE")){
                scaleRep = Scale.WHITENOTE;
            } else if (scaleType.equals("EASTERN")){
                scaleRep = Scale.EASTERN;
            } else {
                scaleRep=new GmRandom().nextLong();
            }
            scale=new Scale((int)scaleRep,rootTweak.intValue());
            //     System.out.println(scaleType);
            rebuild();
        } else if (o instanceof Tweakable) {
            //        defChord = new Time(0, 1, defChordT.intValue());
            //        defDT = new Time(0, 1, pulsesPerBeat.intValue());
            //        defLen = new Time(defLenT.intValue(), 0, 1);
        }
    }

    public Band getBand() {
        return band;
    }

    public Player createPlayer(Voice voice) throws Exception {
        Player player = new Player(voice, band);
        synchronized (this) {
            Iterator<Part> iter = parts.iterator();
            while (iter.hasNext()) {
                Part part = iter.next();
                Phrase phrase = new Phrase(part, player);
                synchronized (player) {
                    player.addPhrase(phrase);
                }
                phrase.mutate();
    //            phrase.setSelected(true);
            }
        }
        setChanged();
        notifyObservers(new Message("AddPlayer", player));
        player.lockId(true);
        band.setSelectedPlayer(player);
        player.lockId(false);
        setId(0);
        return player;
    }



    public boolean selectAllPhrases(boolean yes) {
        boolean changed = false;
        synchronized (this) {
            Iterator<Part> iter = parts.iterator();
            while (iter.hasNext()) {
                Part part = iter.next();
                changed = part.selectAllPhrases(yes) || changed;
            }
        }

        if (changed) {
            setChanged();
            notifyObservers(Message.SELECTION_CHANGE);
        }
        return changed;
    }

    public boolean selectAllParts(boolean yes) {
        boolean changed = false;
        synchronized (this) {
            Iterator<Part> iter = parts.iterator();
            while (iter.hasNext()) {
                Part part = iter.next();
                changed = part.setSelected(yes) || changed;
            }
        }

        if (changed) {
            setChanged();
            notifyObservers(Message.SELECTION_CHANGE);
        }
        return changed;
    }

    private boolean selectPhrases(Vector<Phrase> vec, boolean yes) {
        boolean changed = false;
        synchronized (this) {
            Iterator<Phrase> iter = vec.iterator();
            while (iter.hasNext()) {
                Phrase phrase = iter.next();
                changed = phrase.setSelected(yes) || changed;
            }
        }
        return changed;
    }



    private boolean selectParts(Vector<Part> vec, boolean yes) {
        boolean changed = false;
        synchronized (this) {
            Iterator<Part> iter = vec.iterator();
            while (iter.hasNext()) {
                Part part = iter.next();
                changed = part.setSelected(yes) || changed;
            }
        }
        return changed;
    }

    public void notifySelectionChange() {
        setChanged();
        notifyObservers(Message.SELECTION_CHANGE);
    }

    public synchronized void appendPart(Part part) {

        Part lastSect = null;

        if (parts.size() != 0) {
            lastSect = parts.elementAt(parts.size() - 1);
        }
        if (lastSect == null) {
            part.setStartTime(new Time(0));
        } else {
            part.setStartTime(lastSect.getEnd());
        }
        parts.add(part);

        part.setSong(this);
        setId(0);
    }

    public long getId() {
        return id;
    }

    public void lockId(boolean yes) {
        idLock=yes;
    }

    public void setId(long id) {
        //      assert (this.id == 0);
        //    System.out.println("Song.setId() " + id + "  " + this.id);

        if (idLock) return;
        if (this.id != 0) {
            if (this.id != id) {
                mum = this.id;
            }
        }

        if (id > 0) {
            this.id = id;
            setChanged();
            notifyObservers(new Message("Saved"));
        } else if (id == 0 && this.id != 0) {
            if (this.id != -1) {
                DataBase db = DataBase.the();
                if (db != null)
                    db.addPlayTime(this,
                                   SimphoneyApp.the().getUser());
                this.id = id;
                artist=SimphoneyApp.the().getUser();
                TopFrame.the().setFrameTitle();
            }
            this.id = id;

            //setChanged();
            //notifyObservers(new Message("Modified"));
        }
    }

    public String getTitle() {
        return title;
    }

    public String getArtist() {
        return artist;
    }

    public String getGenre() {
        return genre;
    }

    public void setHeaders(String title, String artist, String genre) {
        this.title = title;
        this.artist = artist;
        this.genre = genre;
    }

    public String toString() {
        return title + " / " + artist + " / " + genre + String.valueOf(playTime);
    }

    static String[] types = {"INT", "INT", "INT", "INT", "INT", "INT","TEXT",
                            "TEXT","TEXT","INT"};
    static String[] info = {"mum", "dad", "rule", "tempo", "mode","root","title",
                           "artist", "genre","playtime"};
    static String[] xtraType = {"INT"};
    static String[] xtraInfo = {"playTime"};
    static public final TableInfoData tableInfo = new TableInfoData(types, info,
             "SongTABLE", true);

    public String[] getValues() {
        String[] r = {
                     String.valueOf(mum),
                     String.valueOf(dad),
                     String.valueOf(rule),
                     Conductor.tempoBPM.toString(),
                     String.valueOf(scale.rep),
                     String.valueOf(scale.root),
                     '"' + title + '"',
                     '"' + artist + '"',
                     '"' + genre + '"',
                     "0"
        };
        return r;
    }

    public synchronized void kill() {
        Iterator<Part> iter = parts.iterator();
        while (iter.hasNext()) {
            Part sect = iter.next();
            sect.deleteObservers();
            sect.song = null;
            sect.kill();
        }
        band.kill();
        setChanged();
        notifyObservers(Message.KILLED);
    }

    synchronized Part nextPartToPlay() {
        if (parts.size() == 0) {
            return null;
        }

        int ip = 0;
        int n = parts.size();
        if (playSection == null) {
            playSection = parts.elementAt(0);
            ip = 0;
        } else {
            ip = parts.indexOf(playSection);
            ip = (ip + 1) % n;
            playSection = parts.elementAt(ip);
        }

        if (loopSelected && !playSection.isSelected()) {
            for (int ip1 = ip + 1; ip1 < n; ip1++) {
                Part pppp = parts.elementAt(ip1);
                if (pppp.isSelected()) {
                    playSection = pppp;
                    return pppp;
                }
            }
            for (int ip1 = 0; ip1 < ip; ip1++) {
                Part pppp = parts.elementAt(ip1);
                if (pppp.isSelected()) {
                    playSection = pppp;
                    return playSection;
                }
            }
        }
        return playSection;
    }

    public Time getStart() {
        return parts.elementAt(0).start;
    }

    public Time getEnd() {
        return parts.elementAt(parts.size() - 1).getEnd();
    }

    public void setLoopSelected(boolean yes) {
        loopSelected = yes;
    }

    public Vector<Part> getSections() {
        return parts;
    }

    public int countSections() {
        return parts.size();
    }

    public synchronized void copySelectedPartsToClip() {

        partClip.removeAllElements();

        Iterator<Part> hiter = parts.iterator();
        while (hiter.hasNext()) {
            Part part = hiter.next();
            if (part.isSelected()) {
                Part npart = new Part(part, Time.ZERO, this);
                partClip.add(npart);
            }
        }
    }

    public synchronized int posOfPart(Part part) {
        return parts.indexOf(part);
    }

    public synchronized int[] posOfPhrase(Phrase phrase) {
        return new int[] {posOfPart(phrase.part),
                band.posOfPlayer(phrase.player)};
    }

    synchronized Phrase phraseAt(int x,int y) {
        return parts.elementAt(x).phrases.elementAt(y);

    }

    public Phrase dragPhrase() {
        SongPhraseIterator iter = new SongPhraseIterator(this);
        while (iter.hasNext()) {
            Phrase phrase = iter.next();
            if (phrase.isSelected()) {
                return phrase;
            }
        }
        return null;
    }


    public Part dragPart() {
         Iterator<Part> iter = parts.iterator();
         while (iter.hasNext()) {
             Part part = iter.next();
             if (part.isSelected()) {
                 return part;
             }
         }
         return null;
    }
    public synchronized void pasteSelectedPhrases() {

        //      phraseClip.removeAllElements();
        int xMin = Integer.MAX_VALUE;
        int xMax = Integer.MIN_VALUE;
        int yMin = Integer.MAX_VALUE;
        int yMax = Integer.MIN_VALUE;

        Vector<Phrase> phraseClip = new Vector<Phrase>();
        SongPhraseIterator iter = new SongPhraseIterator(this);
        while (iter.hasNext()) {
            Phrase phrase = iter.next();
            if (phrase.isSelected()) {
                int loc[] = posOfPhrase(phrase);
                xMin = Math.min(xMin, loc[0]);
                xMax = Math.max(xMax, loc[0]);
                yMin = Math.min(yMin, loc[1]);
                yMax = Math.max(yMax, loc[1]);
                //      phraseClip.add(phrase);
            }
        }
        // Hack to put just after selected.

        int xDiff = (xMax - xMin) + 1;

        for (int i = xMin; i <= xMax; i++) {
            int dst = i + xDiff;
            Part srcPart = parts.elementAt(i);
            Iterator<Phrase> srcIter = srcPart.phrases.iterator();
            Iterator<Phrase> dstIter;
            Part dstPart;

            if (dst >= parts.size()) {

                dstPart = new Part(parts.elementAt(i), getEnd(), this);
                appendPart(dstPart);
                dstIter = dstPart.phrases.iterator();

                int jy = 0;
                while (dstIter.hasNext()) {
                    Phrase dstPhrase = dstIter.next();
                    Phrase srcPhrase = srcIter.next();
                    if (!srcPhrase.isSelected()) {
                        dstPhrase.setMute(true);
                    } else {
                        phraseClip.add(dstPhrase);
                    }
                }
                setChanged();
                notifyObservers(new Message("AddPart", dstPart));
            } else {
                dstPart = parts.elementAt(dst);
                dstIter = dstPart.phrases.iterator();
                while (dstIter.hasNext()) {
                    Phrase dstPhrase = dstIter.next();
                    Phrase srcPhrase = srcIter.next();
                    if (srcPhrase.isSelected()) {
                        dstPhrase.setFrom(srcPhrase);
                        phraseClip.add(dstPhrase);
                    }
                }
            }
        }
        selectAllPhrases(false);
        selectPhrases(phraseClip, true);
        setChanged();
        notifyObservers(Message.SELECTION_CHANGE);
    }

    public synchronized void copySelectedPhrasesTo(int x, int y) {

        //      phraseClip.removeAllElements();
        int xMin = Integer.MAX_VALUE;
        int xMax = Integer.MIN_VALUE;
        int yMin = Integer.MAX_VALUE;
        int yMax = Integer.MIN_VALUE;

        SongPhraseIterator iter = new SongPhraseIterator(this);
        while (iter.hasNext()) {
            Phrase phrase = iter.next();
            if (phrase.isSelected()) {
                int loc[] = posOfPhrase(phrase);
                xMin = Math.min(xMin, loc[0]);
                xMax = Math.max(xMax, loc[0]);
                yMin = Math.min(yMin, loc[1]);
                yMax = Math.max(yMax, loc[1]);
                //      phraseClip.add(phrase);
            }
        }

        if (x == xMin && y == yMin) return;

        int newPartCount = x + xMax - xMin - parts.size()+1;

        /* Create new parts if need be */

        if (newPartCount > 0) {
            for (int i = 0; i < newPartCount; i++) {
                Part dstPart = new Part(parts.elementAt(i + xMin), getEnd(), this);
                appendPart(dstPart);
                setChanged();
                notifyObservers(new Message("AddPart", dstPart));
                Iterator<Phrase> dstIter = dstPart.phrases.iterator();
                while (dstIter.hasNext()) {
                    Phrase dstPhrase = dstIter.next();
                    dstPhrase.setMute(true);
                }

            }
        }

        int newPlayerCount = y + yMax - yMin - band.players.size()+1;

        if (newPlayerCount > 0) {
            for (int i = 0; i < newPlayerCount; i++) {

                Player player = null;
                try {
                    Voice v =
                            Hub.the().createDefaultVoice();
                    v.allocate(true);
                    player = createPlayer(v);
                    player.updateAllCtrl(true);
                } catch (Exception ex) {
                    Simphoney.displayException(ex);
                }
                synchronized(player) {
                    Iterator<Phrase> piter = player.getPhrases().iterator();
                    while (piter.hasNext()) {
                        piter.next().setMute(true);
                    }
                }
            }
        }

        Vector<Phrase> phraseClip = new Vector<Phrase>();

        boolean copyLeft = x > xMin;
        boolean copyDown = y > yMin;

        int x1, x2, dx;
        int y1, y2, dy;

        if (copyLeft) {
            x1 = xMax;
            x2 = xMin;
            dx = -1;
        } else {
            x1 = xMin;
            x2 = xMax;
            dx = 1;
        }

        if (copyDown) {
            y1 = yMax;
            y2 = yMin;
            dy = -1;
        } else {
            y1 = yMin;
            y2 = yMax;
            dy = 1;
        }

        int xOff = x - xMin;
        int yOff = y - yMin;

        for (int is = x1; is != x2 + dx; is += dx) {
            for (int js = y1; js != y2 + dy; js += dy) {
                int id = is + xOff;
                int jd = js + yOff;
                Phrase src = phraseAt(is, js);
                Phrase dst = phraseAt(id, jd);
                dst.setFrom(src);
                phraseClip.add(dst);

            }
        }

        selectAllPhrases(false);
        selectPhrases(phraseClip, true);
        setChanged();
        notifyObservers(Message.SELECTION_CHANGE);
    }

    public synchronized void copySelectedPartsTo(int x) {

          //      phraseClip.removeAllElements();
          int xMin = Integer.MAX_VALUE;
          int xMax = Integer.MIN_VALUE;

          Iterator<Part> iter = parts.iterator();
          while (iter.hasNext()) {
              Part part = iter.next();
              if (part.isSelected()) {
                  int loc = posOfPart(part);
                  xMin = Math.min(xMin, loc);
                  xMax = Math.max(xMax, loc);
              }
          }

          if (x == xMin ) return;

          int oldSize = parts.size();
          int newPartCount = x + xMax - xMin - parts.size()+1;

          /* Create new parts if need be */

          if (newPartCount > 0) {
              for (int i = 0; i < newPartCount; i++) {
                  Part dstPart = new Part(parts.elementAt(i + xMin), getEnd(), this);
                  appendPart(dstPart);
                  setChanged();
                  notifyObservers(new Message("AddPart", dstPart));
              }
          }

          Vector<Phrase> phraseClip = new Vector<Phrase>();

          boolean copyLeft = x > xMin;

          int x1, x2, dx;
          int y1, y2, dy;

          if (copyLeft) {
              x1 = xMax;
              x2 = xMin;
              dx = -1;
          } else {
              x1 = xMin;
              x2 = xMax;
              dx = 1;
          }

          int xOff = x - xMin;

          for (int is = x1; is != x2 + dx; is += dx) {
                  int id = is + xOff;
                  Part dst = parts.elementAt(id);
                  if (id < oldSize) {
                      Part src = parts.elementAt(is);
                      dst.setFrom(src);
                  }
                  partClip.add(dst);

          }

          selectAllParts(false);
          selectParts(partClip, true);
          setChanged();
          notifyObservers(Message.SELECTION_CHANGE);
      }

}
