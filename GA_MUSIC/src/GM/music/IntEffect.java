package GM.music;

/**
 * Note description.
 *
 * @author P.J.Leonard
 * @version (0.1)
 */
public class IntEffect implements Effect
{
    /**
     *
     */

    final static double dScale=1000.0;

    public IntEffect(IntEffect cm)
    {
        val = new long[cm.dim];
        for (int i=0;i< dim;i++) val[i]=cm.val[i];
    }

    public IntEffect(long i0,long i1,long i2,long i3)
    {
         val = new long[4];
         val[0] = i0;
         val[1] = i1;
         val[2] = i2;
         val[3] = i3;

    }

    public void mutate() {
        assert(false);
    }
    public void setInt(long i,int id) {
        this.val[id]=i;
    }

    public String toString() {
        String x="";
        for (int i=0;i< dim;i++) { x=x+" "+val[i];}
        return x;
    }

    public Object clone() {
        return new IntEffect(this);
    }

//     public IntEffect(GeneReader r) throws IOException {
//         dim=r.getInt();
//
//         for (int i=0; i< dim;i++) val[i]=r.getLong();
//     }
//
//     public void writeToGene(GeneWriter w)throws Exception {
// //
//         for (int i=0;i< dim;i++) w.write(val[i]," intEffect"+i);
//     }

    private int   dim;
    protected long  val[];
    public  long  getValAt(int id) { return val[id];}
//     public String getType() { return "Int";}
//     public String getName() { return "";}
//     public void setName(String name) {
//         assert(name.equals(getName()));
//     }
}
