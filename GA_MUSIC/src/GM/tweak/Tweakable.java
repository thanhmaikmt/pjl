package GM.tweak;
import java.util.*;
import GM.music.Message;

abstract public class Tweakable extends Observable {
    Number  n;
    Comparable min;
    Comparable max;
    String  label;
    Number stepSize;
    boolean enabled=true;

    Tweakable(String label,Number n,Comparable min,Comparable max,Number stepSize) {
	this.label= label;
	this.n = n;
	this.stepSize = stepSize;
	this.min = min;
	this.max = max;
    }

/*
    Tweakable(Collection c,String label,Number n,Comparable min,Comparable max,Number step) {
	this(label,n,min,max,step);
	c.add(this);
    }
*/
    public String getLabel() {return label;}
    public Number getNumber() { return n; }
    public int   intValue() { return n.intValue(); }
    public double  doubleValue(){ return n.doubleValue(); }
    public Comparable getMinimum() { return min;}
    public Comparable getMaximum() { return max;}
    public Number getStepSize() {return stepSize; }
    public boolean isOn() { return !(intValue() == 0);}
    public abstract void   set(String s);

    public void   setNumber(Number n) {
	this.n=n;
        setChanged();
        notifyObservers();
    }

    public String toString() {
	return n.toString();
    }

    public void setEnabled(boolean yes) {
        if (yes == enabled) return;
        setChanged();
        enabled=yes;
        if (yes) notifyObservers(Message.ENABLE);
        else notifyObservers(Message.DISABLE);
    }

    public boolean isEnabled() {
        return enabled;
    }

    static public Tweakable getTweak(String label,Tweakables ts) {
        Iterator<Tweakable> iter=ts.getTweaks().iterator();
        while(iter.hasNext()){
            Tweakable tt=iter.next();
            if (tt.getLabel().equals(label)) return tt;
        }
        assert(false);
        return null;
    }


    static public void deleteObservers(Tweakables ts) {
         Iterator<Tweakable> iter=ts.getTweaks().iterator();
         while(iter.hasNext()){
             iter.next().deleteObservers();
         }
     }

}
