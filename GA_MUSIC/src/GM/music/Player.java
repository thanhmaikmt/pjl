package GM.music;


import java.util.*;
import GM.*;
import GM.tweak.*;
import GM.jdbc.TableInfoData;
import GM.jdbc.TableInfo;
import java.io.StreamTokenizer;
import java.io.IOException;
import java.sql.ResultSet;
import java.sql.SQLException;

/**
 * <p>Title: </p>
 *
 * <p>Description: </p>
 *
 * <p>Copyright: Copyright (c) 2005</p>
 *
 * <p>Company: </p>
 *
 * @author not attributable
 * @version 1.0
 */


public class Player extends Observable implements TableInfo, Observer,
        Tweakables {

    long id = -1;
    int high = 65;
    int low = 45;
    int vol = 100;

    TweakableInt lowT = new TweakableInt(10, 120, low, "Lowest");
    TweakableInt rangeT = new TweakableInt(12, 100, high - low, "Range");

    protected Vector<Tweakable> tweaks = new Vector<Tweakable>();

    //   public final ReentrantLock lock= new ReentrantLock();
    //  public final Condition condition = lock.newCondition();

    Voice voice;
    // Conductor conductor;

    public final TweakableBool solo = new TweakableBool(false, "S");
    public final TweakableBool mute = new TweakableBool(false, "M");
    private boolean silent = false;
    private final Vector<Phrase> phrases = new Vector<Phrase>(); //@TODO
    Band band;
    boolean selected = false;
    boolean idLock=false;
    static long soloBit=0x1;
    static long muteBit=0x2;
    static long selectedBit=0x4;

    public Player() {
        tweaks.add(lowT);
        tweaks.add(rangeT);
        addMidiTweaks();
        lowT.addObserver(this);
        rangeT.addObserver(this);
        solo.addObserver(this);
        mute.addObserver(this);
    }

    public Player(Voice v, Band band) {
        this();
        voice = v;
        this.band = band;
        band.addPlayer(this);
    }



    public Player(ResultSet res,Band band,Voice v) throws SQLException, IOException {
        this(new StreamTokenizer(res.getBinaryStream("data")),band);
        id=res.getInt("id");
        long flags=res.getLong("flags");
        setFlags(flags);
        // if (selected) band.setSelectedPlayer(this);
        selected=false;
        this.voice=v;
    }

    public Player(StreamTokenizer st,Band band) throws IOException {
        this();
        joinBand(band);
        st.nextToken();
        int low = (int) st.nval;

        st.nextToken();
        int high = (int) st.nval;

        while (st.nextToken() != StreamTokenizer.TT_EOF) {
            String tn = st.sval;
            st.nextToken();
            int val = (int) st.nval;
            setMidiTweak(tn, val);
        }
        lowT.setNumber(new Integer(low));
        rangeT.setNumber(new Integer(high - low));
        this.low=low;
        this.high=high;
    }

    public Vector<Tweakable> getTweaks() {
        return tweaks;
    }

    public void joinBand(Band b) {
        assert (band == null);
        this.band = b;
        band.addPlayer(this);
    }

    public Band getBand() {
        return band;
    }

    void setSelected(boolean yes) {
        if (selected == yes) {
            return;
        }
        selected = yes;
        setChanged();
        notifyObservers(Message.SELECT_CHANGE);
    }

    public boolean isSelected() {
        return selected;
    }

    public synchronized void addPhrase(Phrase phrase) {
        phrases.add(phrase);
    }

    public synchronized void removePhrase(Phrase phrase) {
        phrases.remove(phrase);
    }

    /**
     *
     * @param o Observable  should be a tweakable
     * @param arg Object
     */
    public void update(Observable o, Object arg) {

        //    System.out.println("Player update:"+ o );
        Tweakable tweak = (Tweakable) o;
        if (tweak == lowT ||
            tweak == rangeT) {
            int low = lowT.intValue();
            int range = rangeT.intValue();
            setRange(low, low + range);
            setId(0);
        } else if (tweak == mute ||
                   tweak == solo) {
            band.updatePlayerState();
        } else if (o instanceof TweakableMidiCtrl) {
            TweakableMidiCtrl t = (TweakableMidiCtrl) o;
            int ctrl = t.ctrl;
            int val = t.intValue();
            if (voice != null) {
                voice.tweakCtrl(ctrl, val);
            }
            setId(0);
        }

    }

    public void lockId(boolean yes) {
        idLock=yes;

    }

    public Voice getVoice() {
        return voice;
    }

    public void setVoice(Voice voice) {
        //   System.out.println("SET VOICE" + voice.getName());
        if (this.voice != null) {
            this.voice.kill();
        }
        this.voice = voice;
        voice.allocate(true);
      //  lowT.addObserver(this);
     //   rangeT.addObserver(this);
        updateAllCtrl(true);
        setChanged();
        notifyObservers(Message.MODIFIED);
        Simphoney.getSong().setId(0);
    }


    public synchronized void kill() {

        for (Phrase phrase : phrases) {
            phrase.player = null;
            phrase.kill();
        }

        phrases.removeAllElements();
        if (voice != null) {
            voice.kill();
        }
        voice = null;
        if (band != null) {
            band.players.removeElement(this);
        }
        band = null;

        setChanged();
        notifyObservers(Message.KILLED);
        deleteObservers();
        //     conductor = null;
        Tweakable.deleteObservers(this);
    }


    /*
        public Conductor getConductor() {
            return voice.getConductor();
        }
     */


    public Vector<Phrase> getPhrases() {
        return phrases;
    }


    public String getName() {
        return voice.getName();
    }


    public boolean isMute() {
        return mute.isOn();
    }

    public boolean isSolo() {
        return solo.isOn();
    }

    public boolean isSilent() {
        return silent;
    }

    void setSilent(boolean f) {
        //    assert (!(solo && f));
        silent = f;
        if (voice!= null) voice.setSilent();
    }

    public int lowest() {
        return low;
    }

    public int highest() {
        return high;
    }

    public void setRange(int low, int high) {
        //    System.out.println(" set Range ");
        if (this.high == high && this.low == low) {
            return;
        }
        this.high = high;
        this.low = low;
        //   voice.setId(0);
        synchronized (this) {
            Iterator iter = phrases.iterator();

            while (iter.hasNext()) {
                Phrase phrase = (Phrase) iter.next();
                phrase.interpret();
            }
        }
    }

    void setMidiTweak(String tn, int val) {
        Iterator<Tweakable> iter = tweaks.iterator();
        while (iter.hasNext()) {
            Tweakable t = iter.next();
            if (t.getLabel().equals(tn)) {
                t.setNumber(val);
                return;
            }
        }
        System.out.println(" Unknown controller label " + tn);
    }


    void addMidiTweaks() {
        Midi.Controller[] ctrl = Midi.cntrlTable;

        for (int i = 0; i < ctrl.length; i++) {
            TweakableMidiCtrl c = new TweakableMidiCtrl(ctrl[i].cntrl,
                    ctrl[i].defVal, ctrl[i].name);

            tweaks.add(c);
            c.addObserver(this);
            //     System.out.println(this +" observers " + c.hashCode());
        }

    }


    public void updateAllCtrl(boolean idLock) {
        boolean tmp=this.idLock;
        this.idLock=idLock;
        Iterator<Tweakable> iter = tweaks.iterator();
        while (iter.hasNext()) {
            Tweakable t = iter.next();
            if (t instanceof TweakableMidiCtrl) {
                update(t, null);
            }
        }
        this.idLock=tmp;
    }

    static String[] types = {"INT","BLOB"};
    static String[] keys = {"flags","data"};

    static public final TableInfoData tableInfo = new TableInfoData(types, keys,
            "PlayerTABLE", true);


    public long getId() {
        return id;
    }

    public void setId(long id) {
        if (idLock) return;
     //   setChanged();
     //   notifyObservers(Message.MODIFIED);
     //    System.out.println(" PLAYER ID SET =" + id);
        this.id = id;
        Simphoney.getSong().setId(0);
    }

    public String getData() {

        StringBuffer buf = new StringBuffer(low + " " + high);

        Iterator<Tweakable> iter = tweaks.iterator();

        while (iter.hasNext()) {
            Tweakable t = iter.next();
            if (t instanceof TweakableMidiCtrl) {
                buf.append(" " + t.getLabel() + " " + t.intValue());
            }
        }
        return buf.toString();
    }

    public String[] getValues() {
        String[] r = {String.valueOf(getFlags()),"\"" + getData() + "\""};
        return r;
    }


    public long getFlags() {
        long flags=0;
        if (mute.isOn()) flags=flags| muteBit;
        if (solo.isOn()) flags=flags| soloBit;
        if (selected) flags=flags| selectedBit;
        return flags;
    }

    public void setFlags(long flags) {
        mute.setOn((flags & muteBit) != 0);
        solo.setOn((flags & soloBit) != 0);
        selected = (flags & selectedBit) != 0;
    }

}
