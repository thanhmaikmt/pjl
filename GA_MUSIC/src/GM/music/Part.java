package GM.music;

import java.util.*;
import java.sql.*;
import GM.jdbc.*;
import GM.genetic.*;
import java.util.*;
import GM.tweak.*;

public class Part extends Observable implements TableInfo, Observer, Tweakables {


    ArrayList<Rep> history = new ArrayList<Rep>();
    int ihist = 0;


    Vector<Tweakable> tweaks = new Vector<Tweakable>();
    long id;
    long mumId;
    long dadId;
    int ruleId;
    public Time start;

    Time len;
    Time dt;
    String name;
    Chord chordArray[];
    int nSlice;
    ChordList chords;
    Rep rep;
    Vector<Phrase> phrases;
    Song song;
    Scale scale=null;

    int nt;
  //  int scaleRepLocal=0;

    boolean solo;
    boolean killed = false;
    boolean selected = false;

    public TweakableInt chordsPerBeat;

    public TweakableInt length;


    private Part() {
        phrases = new Vector<Phrase>();
        solo = false;

    }

    private Part(Song perf) {
        this();
        this.song = perf;
    }

    public Vector<Phrase> getPhrases() {
        return phrases;
    }

    void makeTweaks() {
        length = new TweakableInt(1, 8, len.getBND()[0], "length");
        int r[] = dt.getBND();
        chordsPerBeat = new TweakableInt(1, 4, r[2], "Chords per beat");
        tweaks.add(chordsPerBeat);
        tweaks.add(length);
        chordsPerBeat.addObserver(this);
        length.addObserver(this);
    }

    public Part(Part cloneMe, Time start, Song song ) {
        this(song);
        this.start = start;
        this.dt = cloneMe.dt;
        this.len = cloneMe.len;
        this.scale= cloneMe.scale;
        rep = new Rep(cloneMe.rep);
        this.id = cloneMe.id;
        makeTweaks();
        build(true);
        Iterator<Phrase> iter = cloneMe.phrases.iterator();
        while (iter.hasNext()) {
            Phrase clonePhrase = iter.next();
            new Phrase(clonePhrase, this);
        }
    }


    void setFrom(Part cloneMe) {
        this.dt = cloneMe.dt;
        this.id = cloneMe.id;
        this.dt  = cloneMe.dt;
        this.len = cloneMe.len;
        this.scale =cloneMe.scale;
        nt = (int) (len.getTick() / dt.getTick());
        rep = new Rep(cloneMe.rep);

        build(true);
  //      interpret();
    }


    public Part(Time start, Song song) {
        this(song);
        this.start = start;
        this.dt = new Time(0,1,Defaults.chordsPerBeat);
        this.len = new Time(Defaults.partLength,0,1);

        nt = (int) (len.getTick() / dt.getTick());
        int nv = 2;
        rep = new Rep(nv, nt);
        makeTweaks();
        mutate();
    }

    private void resizeRep() {
        nt = (int) (len.getTick() / dt.getTick());
        int nv = 2;
        rep.expand(nv, nt);
    }


    public Part(ResultSet res) throws SQLException {
        this();
        int i = 1;
        id = res.getInt("id");
        mumId = res.getInt("mum");
        dadId = res.getInt("dad");
        ruleId = res.getInt("rule");
        len = new Time(res.getInt("len"));
        dt = new Time(res.getInt("dt"));
        int mode = res.getInt("mode");
        int key= res.getInt("root");

        if (mode != 0 ) {
            scale = new Scale(mode,key);
        } else {
            scale=null;
        }

        rep = new Rep(res.getString("rep"));
        makeTweaks();

    }


    public void update(Observable o, Object arg) {
   //     System.out.println("Part:update " + o + "  " + arg);
        len = new Time(length.intValue(), 0, 1);

        dt = new Time(0, 1, chordsPerBeat.intValue());
        build(false);

        if (o == length) {
            song.rePositionParts();
        }
    }


    public Vector<Tweakable> getTweaks() {
        return tweaks;
    }



    public synchronized void addPhrase(Phrase p) {
        //   perf.setId(0); //@TODO (think)
        addObserver(p);
        phrases.add(p);
    }

    synchronized void removePhrase(Phrase p) {
        song.setId(0);
        deleteObserver(p);
        phrases.remove(p);
    }


    public synchronized void mutate() {
        //    System.out.println(" SECTION MUTATE ");
        setId(0);
        song.setId(0);
        rep=new Rep(2,nt);
        rep.randFill();

        //  System.out.println(scaleRep);
        build(true);
        //  setChanged();
        //  notifyObservers("MODIFY");
    }

    synchronized void build(boolean push) {

        resizeRep();
        if (push) history.add(ihist++, rep);

        nSlice = (int) (len.getTick() / dt.getTick());
        chords = new ChordList();
        chords.add(new Event(len, null));
        chordArray = new Chord[nSlice];
  //      if (scaleRep == null)
  //      scale = new Scale(song.scaleRep, song.getScaleType());

        Time t = new Time(0);
        int iChord = 0;
        while (t.compareTo(len) < 0) {
            Chord chord = new Chord(rep.at(0)[iChord], rep.at(1)[iChord]); // scale,r.nextInt(8));
            chords.add(new Event(t, chord));
            chordArray[iChord++] = chord;
            t = t.add(dt);
        }
        setChanged();
        notifyObservers(Message.MODIFIED);
        // return new Score(song,scName,start,end,dChord,dt,chords,chordArray);
    }

    public Scale getScale() {
        if (scale == null) return song.scale;
        else return scale;
    }

    public EventList getChords() {
        return chords;
    }

    public String getName() {
        return name;
    }

    public String getType() {
        return "Score";
    }

    public Chord chordAt(Time t) {
        // t=t.subtract(start);
        int i = (int) ((t.getTick() / dt.getTick()) % nSlice);
        return chordArray[i];
    }

    public Time getEnd() {
        return start.add(len);
    }

    public void setPhrasesSelected(boolean yes) {

        synchronized (this) {
            Iterator<Phrase> iter = phrases.iterator();
            while (iter.hasNext()) {
                Phrase phrase = iter.next();
                phrase.setSelected(yes);
            }
        }
    }

    public synchronized void kill() {
        Iterator<Phrase> iter = phrases.iterator();
        while (iter.hasNext()) {
            Phrase phrase = iter.next();
            phrase.part = null;
            phrase.kill();
        }
        phrases.removeAllElements();
        killed = true;
        setChanged();
        notifyObservers(Message.KILLED);
        if (song != null) {
            //          song.removePhrase
            song.rePositionParts();
        }

        /* Nothing yet ? */

    }


    public boolean selectAllPhrases(boolean yes) {
        boolean changed = false;
        synchronized (this) {
            Iterator<Phrase> iter = phrases.iterator();
            while (iter.hasNext()) {
                changed =  iter.next().setSelected(yes) || changed ;
            }
        }
        return changed;
    }

    public void setName(String name) {
        assert (name.equals(getName()));
    }


    /*    public Vector<Phrase> getPhrases() {
            return phrases;
        }
     */

    public long getId() {
        return id;
    }

    public void setId(long id) {
        //    assert (this.id == 0);
        this.id = id;
    }


    static String[] types = {"INT", "INT", "INT", "INT", "INT", "INT", "INT","TEXT"};
    static String[] keys = {"mum", "dad", "rule", "len", "dt", "mode", "root", "rep"};

    static public final TableInfoData tableInfo = new TableInfoData(types, keys,
            "PartTABLE", true);

    public String[] getValues() {
;

        if (scale != null) {
            String[] r = {
                         // String.valueOf(perf.getId()),
                         String.valueOf(mumId),
                         String.valueOf(dadId),
                         String.valueOf(ruleId),
                         String.valueOf(len.getTick()),
                         String.valueOf(dt.getTick()),
                         String.valueOf(scale.rep),
                         String.valueOf(scale.root),
                         "\"" + rep.toString() + "\""
            };
            return r;
        }

        String[] r = {
                     // String.valueOf(perf.getId()),
                     String.valueOf(mumId),
                     String.valueOf(dadId),
                     String.valueOf(ruleId),
                     String.valueOf(len.getTick()),
                     String.valueOf(dt.getTick()),
                     String.valueOf(0),
                     String.valueOf(0),
                     "\"" + rep.toString() + "\""
        };
        return r;
    }


    public void setChanged() {
        super.setChanged();
    }

    void setSolo(boolean yes) {
        if (solo == yes) {
            return;
        }
        solo = yes;
        setChanged();
        if (yes) {
            notifyObservers(Message.SOLO_ON);
        } else {
            notifyObservers(Message.SOLO_OFF);
        }
//        song.setSoloSection(this, yes);
    }

    public boolean isSolo() {
        return solo;
    }

    public void setStartTime(Time s) {
        start = s;
        // end=s.add(len);
    }


    public Time getStart() {
        return start;
    }

    public Time getLength() {
        return len;
    }

    //  public Time getEnd() { return start.add(len); }

    public void setSong(Song song) {
        this.song = song;
        build(false);
        /*
                 setChanged();
                 notifyObservers(Message.MODIFIED);
         */
    }

    public Song getSong() {
        return song;
    }

    public int colorHashCode() {
        return rep.colorHashCode();
    }


    public boolean isSelected() {
        return selected;
    }

    public boolean setSelected(boolean yes) {
        if (selected == yes) {
            return false;
        }
        selected = yes;
        setChanged();
        notifyObservers(Message.SELECT_CHANGE);
        return true;
    }

    public boolean canUndo() {
        return ihist > 1;
    }

    public boolean canRedo() {
        return ihist < history.size();
    }

    public void redo() {
        if (!canRedo()) {
            return;
        }
        rep = history.get(ihist++);
        build(false);
    }

    public void undo() {
        if (!canUndo()) {
            return;
        }
        ihist -= 2;
        rep = history.get(ihist++);
        build(false);
    }
}
