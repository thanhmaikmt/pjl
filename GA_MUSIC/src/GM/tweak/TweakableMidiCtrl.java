package GM.tweak;
import java.util.*;


public class TweakableMidiCtrl extends TweakableInt {


    public TweakableMidiCtrl(int ctrl,int val,String label) {
	super(0,127,val,label);
        this.ctrl=ctrl;
    }

    public final int ctrl;



}
