package GM.music;

public class VoicePatch implements SynthNode {
    int ids[];
    String name;
    SynthNode parent;

    public VoicePatch(SynthNode parent, String name, int prog) {
        this.name = name;
        this.parent = parent;

        int count = 1;
        SynthNode n = parent;
        while (n.getParent() != null) {
            n = n.getParent();
            count++;
        }
        ids = new int[count + 1];

        ids[0] = prog;
        int ii = 1;
        n = parent;
        do {
            ids[ii++] = n.index();
            n = n.getParent();
        } while (n != null);
    }

    public String toDebug() {
        StringBuffer buff=new StringBuffer(name+"("+ids[0]+")");
        SynthNode n=this;
        while( (n = n.getParent())!= null) {
            buff.append("|" + n.getName()+"("+n.index()+")");
        }
        return buff.toString();
    }

    public String toString() {
        return getName();
    }

    public SynthNode getParent() {
        return parent;
    }

    public int getProg() {
        return ids[0];
    }

    public int getBank() {
        return ids[1];
    }

    public int idAt(int i) {
        return ids[i];
    }

    public String getName() {
        return name;
    }

    public int size() {
        return 0;
    }

    public SynthNode nodeAt(int i) {
        return null;
    }

    public int index() {
        return ids[0];
    }

    public Voice createVoice(VoicePatch pat) {
        assert (false); return null;
    }

}

