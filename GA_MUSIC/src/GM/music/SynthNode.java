package GM.music;

public interface SynthNode {
    public SynthNode getParent();
    public int size();
    public SynthNode nodeAt(int i);
    public String getName();
    public Voice createVoice(VoicePatch vn)throws Exception ;
    public int index();
}
