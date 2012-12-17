package GM.music;

/**
 * <p>Title: </p>
 *
 * <p>Description: </p>
 *
 * <p>Copyright: Copyright (c) 2005</p>
 *
 * <p>Company: </p>
 *
 * @author not attributable
 * @version 1.0
 */


public class GMPatch {

    final public int synth;
    final public int bank;
    final public int prog;

    public GMPatch(long id) {
        prog = (int) (id & 0xFF);
        bank = (int) ((id >> 8) & 0xFFFF);
        synth = (int) (id >> 24);
    }

    public long getId() {
        long ret1 = synth;
        ret1 = ret1 << 24;
        long ret2 = bank;
        ret2 = ret2 << 8;
        return ret1 + ret2 + prog;

    }


    public GMPatch(int synth,int bank,int prog) {
        this.synth=synth;
        this.bank=bank;
        this.prog=prog;
    }

    public String toString() {
        return synth+" "+bank+" "+prog;
    }

    public static void main(String args[] ) {
        GMPatch  p1 = new GMPatch(13,1567,127);

        GMPatch  p2 = new GMPatch(p1.getId());
        System.out.println(String.format("%o  %o ",p1.getId(), p2.getId()));


    }
}
