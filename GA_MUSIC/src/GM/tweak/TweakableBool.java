package GM.tweak;
import java.util.*;
public class TweakableBool extends TweakableInt {


    public TweakableBool(boolean val,String label) {
	super(new Integer(0),new Integer(1),val?1:0,label);
    }

    public void setOn(boolean val) {
        if (val) setNumber(new Integer(1));
        else setNumber(new Integer(0));
    }

}
