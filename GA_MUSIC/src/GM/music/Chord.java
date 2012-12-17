package GM.music;

import GM.io.*;
import GM.genetic.*;


/**
 * A Chord takes an index and returns a note.
 *
 *
 */

public class Chord implements Effect {


    int rep;
    int root;
//    private Scale scale;
//    private int   root=0;    //
    private int note[]; // root+note[i] --->index into scale
    int n;
    /**
     * @param scale  to base chord on.
     *
     * @param root   note relative to root of scale to base chord.
     *               root is like the I II IV  notation
     */
    public Chord(int rep,int root) {
        //      this.scale    = scale;
        this.rep = rep;
        this.root =root;
        boolean f[] = new boolean[12];
        int noteTmp[] = new int[12];
        n = 0;
        noteTmp[n++] = 0;
        int pitch = 1;
        int bit = 1;
        while (pitch < 12) {

            if ((rep & bit) != 0) {
                noteTmp[n++] = pitch;
            }
            pitch++;
            bit = bit * 2;
        }

        note = new int[n];
        System.arraycopy(noteTmp, 0, note, 0, n);
    }

    public int getPitch(int pos, Scale scale) {
        int ic = root + note[( pos)%n] + scale.n*((pos)/n);
        return scale.getInt(ic);
    }

    public int getN() {
        return n;
    }

    public Object clone() {
        assert (false); return this;
    }

    /**
     * @param pos position in chord
     * @return scale note number
     */
/*
    public int getScaleNumberAt(int pos) {
        return note[pos];
    }
*/

//    public Scale getScale() {
    //       return scale;
    //   }


    public String toString() {
        String tmp = String.valueOf(rep);
//        for (int i=0 ; i < note.length ; i++) {
//            tmp = tmp + scale.getInt(note[i]) + " ";
//        }
        return tmp;
    }


    public String getName() {
        String s = new String();
        s = s + "_" + note.length;
        for (int i = 0; i < note.length; i++) {
            s = s + "_" + note[i];
        }
        return s;
    }

    public String getType() {
        return "Chord";
    }

    public void setName(String name) {
        assert (name.equals(getName()));
    }

    private void jbInit() throws Exception {
    }
    //public Genetic create(String name) {assert(false);return null;}
}
