package GM.tweak;

import java.util.*;

public class TweakableInt extends Tweakable {


    public TweakableInt(int min,int max,int val,String label) {
	super(label,new Integer(val),new Integer(min),new Integer(max),new Integer(1));
    }


/*
    public TweakableInt(Collection c,int min,int max,int val,String label) {
	super(c,label,new Integer(val),new Integer(min),new Integer(max),new Integer(1));
    }

*/

    public void   set(String s) {
	try {
	    n = new Integer(s);
	} catch(Exception e) {
	} // TODO
        setChanged();
        notifyObservers();
    }

}
