package GM.music;

import java.sql.*;
import GM.genetic.*;
import GM.jdbc.*;
import GM.*;
import GM.tweak.*;
import java.util.*;

/**
 * Write a description of class Phrase here.
 *
 * @author DR pJ
 * @version 1
 */
public class Phrase extends Observable implements Observer, TableInfo , Tweakables {


    ArrayList<Rep> history= new ArrayList<Rep>();
    int ihist=0;

    final EventList eventList = new EventList();


    long id;
    long mumId;
    long dadId;
    int ruleId;
    Time dt;
    //  Time len;
    Rep rep=null;
    Player player;
    int nt;

    Part part;
    boolean killed = false;
    boolean mute = false;
    boolean selected=false;

    public static long muteBit=0x1;
    public static long selectedBit=0x2;

    Vector<Tweakable> tweaks = new Vector<Tweakable>();

    public TweakableInt pulsePerBeat;
    public TweakableInt multiplier;

    protected Phrase() {
        id=0;
        pulsePerBeat = new TweakableInt(1, 4, Defaults.pulsesPerBeat, "Pulses per beat");
        multiplier = new TweakableInt(1, 4, Defaults.pulsesPerBeatMult, "Multiplier");
        this.dt = new Time(0,Defaults.pulsesPerBeatMult,Defaults.pulsesPerBeat);
        tweaks.add(multiplier);
        tweaks.add(pulsePerBeat);
        pulsePerBeat.addObserver(this);
        multiplier.addObserver(this);
        mute=true;
    }

    public Phrase(ResultSet res) throws SQLException {

        int i = 1;
        id = res.getInt("id");
        mumId = res.getInt("mum");
        dadId = res.getInt("dad");
        ruleId = res.getInt("rule");
        //        res.getInt("res");
        //   len = new Time(res.getInt(i++));

        long flags = res.getLong("flags");

        setFlags(flags);
        dt = new Time(res.getInt("dt"));
        rep = new Rep(res.getString("rep"));
        pulsePerBeat = new TweakableInt(1, 4, dt.getND()[1], "Pulses per beat");
        multiplier = new TweakableInt(1, 4, dt.getND()[0], "Multiplier");
        tweaks.add(multiplier);
        tweaks.add(pulsePerBeat);
        pulsePerBeat.addObserver(this);
        multiplier.addObserver(this);

    }

    public Phrase(Phrase cloneMe, Part part) {
        part.addPhrase(this);
        this.player = cloneMe.player;
        player.addPhrase(this);
        //  assert (player.getConductor() != null);
        this.dt = cloneMe.dt;
        this.id = cloneMe.id;
        this.part = part;
        nt = (int) (part.len.getTick() / dt.getTick());
        rep = new Rep(cloneMe.rep);
        createTweaks();
        build(true);
        interpret();
        killed = false;
    }

    public Phrase(Part part, Player player) {

        part.addPhrase(this);
        part.setId(0);

        this.player = player;
        this.dt = new Time(0,Defaults.pulsesPerBeatMult,Defaults.pulsesPerBeat);
        this.id = 0;
        this.part = part;
        createTweaks();
        nt = (int) (part.len.getTick() / dt.getTick());
        int nv = 4;
        killed = false;
    }

    void setFrom(Phrase cloneMe) {
        this.dt = cloneMe.dt;
        this.id = cloneMe.id;
        this.dt  = cloneMe.dt;
        this.mute = cloneMe.mute;
        nt = (int) (part.len.getTick() / dt.getTick());
        rep = new Rep(cloneMe.rep);

        build(true);
        interpret();
    }


    private void createTweaks() {
        pulsePerBeat = new TweakableInt(1, 4, dt.getND()[1], "Pulses per beat");
        multiplier = new TweakableInt(1, 4, dt.getND()[0], "Multiplier");

        tweaks.add(multiplier);
        tweaks.add(pulsePerBeat);
        pulsePerBeat.addObserver(this);
        multiplier.addObserver(this);

    }

    public Vector<Tweakable>  getTweaks() { return tweaks; }

    public void setMute(boolean yes) {
        if (mute == yes) return;
        this.mute = yes;
        setChanged();
        notifyObservers(Message.MODIFIED);
    }

    public boolean isMute() {
        return mute;
    }

    public Voice getVoice() {
        return player.getVoice();
    }

    private synchronized void resizeRep() {
        nt = (int) (part.len.getTick() / dt.getTick());
        if (rep == null) {
            rep=new Rep(4,nt);
            rep.randFill();
        } else {
            int nv = rep.nv;
            rep.expand(nv, nt);
        }
    }

    public void update(Observable o, Object a) {

      //  System.out.println(" Phrase update " + o + " " + a );
        if (o == part) {
            build(false);
        } else if (o instanceof Tweakable) {
            dt = new Time(0,multiplier.intValue(),pulsePerBeat.intValue());
      //      System.out.println(" DT = " + dt);
            build(false);
        }

    }

    public synchronized void setPart(Part sect) {
        part = sect;
        part.addPhrase(this);
    }

    public synchronized void setPlayer(Player player) {

        if (player == this.player) {
            return;
        }

        if (player != null) {
            player.removePhrase(this);
        }

        this.player = player;
        player.addPhrase(this);
        interpret();
        //    seq=new LoopingSequencer(this);
        //    seq.start();
        //  Conductor.the().addObserver(seq);
    }

    public synchronized void kill() {
        killed = true;
        //   if (seq != null) seq.kill();
        //   seq=null;
        if (part != null) {
            part.removePhrase(this);
            part = null;
        }
        if (player != null) {
            player.removePhrase(this);
            player=null;
        }
        setChanged();
        notifyObservers(Message.KILLED);

    }


    public synchronized void interpret() {
        System.out.println("Phrase.interpret");
        if (player.getVoice().isMelodic()) {
            int high = player.highest();
            int low = player.lowest();
            assert (high - low >= 12);
            Iterator iter = eventList.iterator();
            while (iter.hasNext()) {
                Event e = (Event) iter.next();
                Note n = (Note) e.getEffect();
                Time on = (Time) e.getTime();
                Chord c = part.chordAt(on);
                int p = c.getPitch(n.getInt(), part.getScale());
                while (p <= low) {
                    p += 12;
                }

                while (p >= high) {
                    p -= 12;
                }
                n.setPitch(p);
            }
        }
        setChanged();
        notifyObservers(Message.MODIFIED);
    }



    public boolean canUndo() {
        return ihist > 1;
    }

    public boolean canRedo() {
        return ihist < history.size();
    }

    public void redo() {
        if (!canRedo()) return;
        rep=history.get(ihist++);
        build(false);
    }

    public void undo() {
        if (!canUndo() ) return;
        ihist -= 2;
        rep=history.get(ihist++);
        build(false);
    }


    public synchronized void mutate() {
        setId(0);
        part.song.setId(0);
        rep= new Rep(4,nt);
        rep.randFill();
        build(true);
    }

    public synchronized void build(boolean push) {
        resizeRep();
        if (push) history.add(ihist++,rep);
        eventList.clear();
        Time t = new Time(0);
        int index = 0;

        while (t.compareTo(part.len) < 0) {
            double vel = Math.sqrt(rep.at(0)[index] / 127.0);
            if (vel < 0.5) {
                vel = 0.0;
            }
            int ivert = rep.at(1)[index];
            Time nlen = dt.times((rep.at(2)[index] %  3 + 1) );
            Time dur;
            int dkey = rep.at(3)[index] % 10;
            if (dkey == 0) {
                dur = dt.times(0.3);
            } else if (dkey == 1) {
                dur = nlen.subtract(dt.times(0.3));
            } else if (dkey == 2)  {
                nlen=nlen.times(2);
                dur = nlen;
            } else {
                dur = nlen;
            }

            eventList.add(new Event(t, new Note(dur, ivert, vel)));
            t = t.add(nlen);
            index++;
        }

        interpret();
        setChanged();
        notifyObservers(Message.MODIFIED);
    }

    public long getId() {
        return id;
    }

    public void setId(long id) {
        //    assert (this.id == 0);
        this.id = id;
    }

    static String[] types = {"INT", "INT", "INT", "INT", "INT", "INT", "TEXT"};
    static String[] keys = {"mum", "dad", "rule", "len", "dt", "flags","rep"};

    static public final TableInfoData tableInfo = new TableInfoData(types, keys,
            "PhraseTABLE", true);



    public long getFlags() {
        long flags=0;
        if (mute) flags=flags| muteBit;
        if (selected) flags=flags| selectedBit;
        return flags;
    }

    public void setFlags(long flags) {
        mute = (flags & muteBit) != 0;
        selected = (flags & selectedBit) != 0;
    }

    public String[] getValues() {
        String[] r = {
                     String.valueOf(mumId),
                     String.valueOf(dadId),
                     String.valueOf(ruleId),
                     String.valueOf(part.len.getTick()),
                     String.valueOf(dt.getTick()),
                     String.valueOf(getFlags()),
                     "\"" + rep.toString() + "\""};

        return r;
    }

    public String getName() {
        return player.getName();
    }

    public Player getPlayer() {
        return player;
    }

    public Time getStart() {
        return part.start;
    }


    public Time getEnd() {
        return part.getEnd();
    }

    public boolean isKilled() {
        return killed;
    }

    public int colorHashCode() {
        return rep.colorHashCode();
    }

    public boolean isSelected() {
        return selected;
    }

    public boolean setSelected(boolean yes) {
        if (selected == yes) return false;
        selected = yes;
        setChanged();
        notifyObservers(Message.SELECT_CHANGE);
        return true;
    }

}
