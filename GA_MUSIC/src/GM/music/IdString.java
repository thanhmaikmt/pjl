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
public class IdString  {
    final public String name;
    final public int id;
    public IdString(int id,String string) {
        this.id=id;
        this.name=string;
    }
    public String toString() { return name;}

    public int size() { return 0; }
    public SynthNode nodeAt(int i) { return null; }
    public String getName() { return name;}
   // public String getName() { return name;}
}
