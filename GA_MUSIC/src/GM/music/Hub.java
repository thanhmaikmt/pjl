package GM.music;

import GM.javasound.*;
import GM.audio.FramedFeed;

abstract public class Hub implements SynthNode {

    protected static Hub the;

    static public Hub the() {
        return the;
    }

    // abstract public void init();
    abstract public FramedFeed getFeed();

    abstract public Voice createVoice(VoicePatch pat) throws Exception;

    abstract public Voice createVoice(GMPatch pat) throws Exception;

    //  abstract public SynthNodes[] getSynths();
    abstract public Voice createDefaultVoice() throws Exception ;

}
