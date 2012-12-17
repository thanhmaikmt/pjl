package GM.music;

import java.io.*;
import GM.genetic.*;
import GM.io.*;

/**
 * Mode of the scale. Set of intervals relative to root.
 *
 */

public class Scale {
    int notes[];
    int n;
    int root;
    int rep;

    static public final String[] types={"WHITENOTE","EASTERN","RANDOM"};

    public final static int WHITENOTE=1 + 4 + 16 + 32 * (1 + 4 + 16 + 64);
    public final static int EASTERN=1 + 2 + 16 + 32 * (1 + 4 + 8  + 64);

    public Scale(Scale cloneMe) {
        this.root=cloneMe.root;
        this.n=cloneMe.n;
        this.rep=cloneMe.rep;
        this.notes=cloneMe.notes;
    }

    public Scale(int rep,int key) {
        this.rep=rep;
        this.root=key;

        boolean f[] = new boolean[12];
        int noteTmp[] = new int[12];
        n = 0;
        noteTmp[n++] = 0;
        int pitch = 0;
        int iprev;
        int bit=1;
        while (pitch < 12) {

            if ((rep & bit) != 0 ) {
                noteTmp[n++] = pitch;
            }
             pitch++;
             bit=bit*2;
        }


        notes = new int[n];
        System.arraycopy(noteTmp,0, notes, 0, n);

    }

    public int getInt(int i) {
        return root + notes[i % n] + 12*(i/n);
    }

}
