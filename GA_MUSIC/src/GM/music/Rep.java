package GM.music;

import GM.genetic.*;
import java.util.StringTokenizer;

public class Rep {


    static GmRandom random = new GmRandom();
    int rep[][];
    int nv;
    int nt;
    //  int key;

    public Rep(Rep clone) {
        nv = clone.nv;
        nt = clone.nt;
        //    key=clone.key;
        rep = new int[nv][nt];
        for (int i=0;i<nv;i++) {
            for(int j=0;j< nt;j++) {
                rep[i][j]=clone.rep[i][j];
            }
        }
    }

    public Rep(int nv, int nt) {
        rep = new int[nv][nt];
        this.nv = nv;
        this.nt = nt;
//        this.key=0;
    }

    public Rep(String str) {
        StringTokenizer st = new StringTokenizer(str);
        //  key=new Integer(st.nextToken()).intValue();
        nv = new Integer(st.nextToken()).intValue();
        nt = new Integer(st.nextToken()).intValue();

        rep = new int[nv][nt];

        for (int i = 0; i < nv; i++) {
            for (int j = 0; j < nt; j++) {
                rep[i][j] = new Integer(st.nextToken()).intValue();
            }

        }

    }


    public void expand(int nvNew,int ntNew) {

      //  System.out.println(ntNew+" " + nt + " | " + nvNew + " " + nv);
        if (ntNew <= nt && nvNew <= nv) return;
        assert( ntNew>=nt && nvNew >=nv);

        int newrep[][] = new int[nvNew][ntNew];

       // Rep nr=new Rep(nvNew,ntNew);

       // nr.randFill();
        for (int i = 0; i < nvNew; i++) {
            int v[]=newrep[i];
            for (int j = 0; j < ntNew; j++) {
                if (i>=nv || j>=nt) v[j] = random.nextInt(127);
                else                v[j] = rep[i][j];
            }
        }
        nt=ntNew;
        nv=nvNew;
        rep=newrep;
    }

    public int[] at(int i) {
        return rep[i];
    }

    public void randFill() {
        for (int i = 0; i < nv; i++) {
            int v[] = at(i);
            for (int j = 0; j < nt; j++) {
                v[j] = random.nextInt(127);
            }
        }

    }

    public String toString() {
        StringBuffer buf = new StringBuffer();
        buf.append(nv);
        buf.append(" ");
        buf.append(nt);
        buf.append(" ");

        for (int i = 0; i < nv; i++) {
            int v[] = at(i);
            for (int j = 0; j < nt; j++) {
                if (i > 0 || j > 0) {
                    buf.append(" ");
                }
                buf.append(v[j]);

            }
            //  buf.append("\n");

        }
        return buf.toString();
    }

    public int colorHashCode() {
        long hash = 0;
        for (int i = 0; i < nv; i++) {
            int v[] = at(i);
            for (int j = 0; j < nt; j++) {
                long vv=v[j]*3621291;
                if ((hash & 0x80000000) != 1) {
                    hash =  0xffffffff & (1 + (hash*2) ^ vv);
                } else {
                    hash =  0xffffffff & ((hash*2) ^ vv );
                }
            }
        }
        return (int) hash;
    }


}
