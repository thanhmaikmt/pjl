package GM.music;

import java.io.*;
import GM.util.*;

public class Time implements Comparable {

    long bit;

    public final static long bitsPerBeat = 2 * 2 * 2 * 3 * 5 ;
    public final static Time ZERO = new Time(0, 0, 1);
    public final static Time INF = new Time(10000000, 0, 1);

    static int allFactors[] = Factorize.factor((int) bitsPerBeat, null);


    //   public static Type timeType=new Type("Time");


    /*
        public Time(GeneReader s) throws IOException {
            bit=s.getLong();
        }

        public void writeToGene(GeneWriter g) throws Exception  {
            g.write(bit, " time");
        }
     */

    public Time(long bit) {
        this.bit = bit;
    }

    public void mutate() {
        assert (false);
    }

    public Time(double beat) {
        this.bit = (long) (beat * bitsPerBeat);
    }


//     public Time(int beat,long bit) {
//         //  bar  = barA;
//         this.bit = beat*bitsPerBeat + bit;
//     }


    public Time(Time t) {
        this.bit = t.bit;
    }


    public int[] getBND() {
        long r[] = new long[3];
        r[0] = (long) (bit / bitsPerBeat);
        int rem = (int) (bit - r[0] * bitsPerBeat);
        if (rem == 0) {
            r[1] = 0;
            r[2] = 1;
        } else {
            long nbot = bitsPerBeat;

            for (int itop = 0; itop < allFactors.length; itop++) {
                int fact = allFactors[itop];
                if (rem % fact == 0) {
                    nbot = nbot / fact;
                    rem = rem / fact;
                    if (rem <= 1) {
                        break;
                    }
                }
            }

            r[1] = rem;
            r[2] = nbot;
        }
        int r2[] = {(int) r[0], (int) r[1], (int) r[2]};
        return r2;
    }


    public int[] getND() {
        long r[] = new long[2];

        int beats = (int) (bit / bitsPerBeat);
        int rem = (int) (bit - beats * bitsPerBeat);

        if (rem == 0) {
            r[0] = beats;
            r[1] = 1;
        } else {
            long nbot = bitsPerBeat;
            for (int itop = 0; itop < allFactors.length; itop++) {
                int fact = allFactors[itop];
                if (rem % fact == 0) {
                    nbot = nbot / fact;
                    rem = rem / fact;
                    if (rem <= 1) {
                        break;
                    }
                }
            }

            r[0] = rem + nbot*beats;
            r[1] = nbot;
        }
        int r2[] = {(int) r[0], (int) r[1] };
        return r2;
    }


    public Time(int beat, int num, int dom) {
        //  bar  = barA;
        assert (dom != 0);
        this.bit = (long) beat * bitsPerBeat +
                   ((long) num * bitsPerBeat / (long) dom);
    }


    public long getBit() {
        return bit % bitsPerBeat;
    }

    public double getBeat() {
        return (double) bit / (double) bitsPerBeat;
    }

    public long getTick() {
        return bit;
    }

    public Time add(Time t) {
        return (new Time(bit + t.bit));
    }

    public static int getPPQ() {
        return (int) bitsPerBeat;
    }

    public Time times(double f) {

        return (new Time((long) (bit * f)));
    }


    public Time subtract(Time t) {
        return (new Time(bit - t.bit));
    }

    public Object clone() {
        return new Time(bit);
    }

    public int compareTo(Object b) {
        Time bt = (Time) b;
        return (int) (bit - bt.bit);
    }

    public String toString() {
        return bit / bitsPerBeat + ":" + bit % bitsPerBeat;
    }

    public String getName() {
        return String.valueOf(bit);
    }


    static public void main(String arg[]) {
        Time t = new Time(18, 5, 7);
        int b[] = t.getBND();
        System.out.println(b[0] + ":" + b[1] + ":" + b[2] + "   ---- " + t);

    }

}
