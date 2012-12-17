package GM.tweak;

import java.util.*;

public class TweakableList extends Tweakable {

   // Vector list = new Vector();
    Object[] arg;
    Object val;

    public TweakableList(Object[] arg, String val, String label) {
        super(label, new Integer(0), new Integer(0), new Integer(arg.length),
              new Integer(1));
        this.arg = arg;
     //   list.addArray(arg);
        set(val);
    }


    /*
     public TweakableInt(Collection c,int min,int max,int val,String label) {
     super(c,label,new Integer(val),new Integer(min),new Integer(max),new Integer(1));
        }

     */

    public Object[] getList() {
        return arg;

    }

    public int indexOf(Object o) {
        for(int i=0;i< arg.length; i++) {
            if (o == arg[i]) return i;
        }
        System.err.println(" CULD NT FIND " + o);
        return -1;
    }
    private void setObject(Object o) {

        int i = indexOf(o);

        if (i == -1) {
            System.err.println(this +" OooPS not in list " + o);
            try {
             //   System.out.println( o );
                throw new Exception(" OOOOOOOOOOOOOOPS ");
            } catch (Exception ex) {
                ex.printStackTrace();
            }
        } else {
            val=o;
            setNumber(new Integer(i));
         //   System.err.println(this +" OK " + o);
        }

    }

    public Object getObject() { return val;}
    public String toString() {if (val==null) return "null";
        return val.toString();}

    public void set(String str) {
     //   System.out.println(this + " set " + str);

        for(int i=0;i<arg.length;i++) {
            Object o = arg[i];
           // System.out.println(o.toString());
            if (o.toString().equals(str)) {
                setObject(o);
            //    System.out.println(" OK OK OK ");
            }
        }
        //setChanged();
        //notifyObservers();
    }


}
