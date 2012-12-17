
package GM.tweak;
import java.util.*;

public class TweakableDouble extends Tweakable {


    public TweakableDouble(double min,double max,double val,double step,String label) {
	super(label,new Double(val),new Double(min),new Double(max),new Double(step));
    }

/*
    public TweakableDouble(Collection c,double min,double max,double val,double step,String label) {
	super(c,label,new Double(val),new Double(min),new Double(max),new Double(step));
    }
*/

    public void   set(String s) {
	try {
	    n = new Double(s);
	} catch(Exception e) {
	} // TODO
    }

}
