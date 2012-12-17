package GM.javasound;

import GM.music.*;

import javax.sound.midi.*;
import java.io.BufferedReader;
import java.io.InputStream;
import java.io.StreamTokenizer;
import java.io.InputStreamReader;

public class JavaSoundMelodicVoice extends JavaSoundVoice {


/*
        JavaSoundMelodicVoice(String name,Patch patch,String sb,String synthName) {
        super(name,patch,sb,synthName);
    }

    public JavaSoundMelodicVoice(InputStream str) {
        super(new StreamTokenizer(new BufferedReader(new InputStreamReader(str))));
     //   allocate(true);
    }

*/
    public JavaSoundMelodicVoice(long id,String name) {
        super(id,name);
    }

    public void play(Effect effect, long tick,Conductor conductor) {
        if (channel < 0) return; // must have been deallocated
        Note note=(Note)effect;
        assert(conductor != null);
        ((JavaSoundConductor)conductor).addEvent(note.getPitch(),
                                                 tick,note.getLengthInTicks(),
                                                 channel,(int)(127*note.getVelocity()));

    }

    public void setSilent() {
        //@TODO
    }

    public boolean isMelodic() { return true;}

    public final void allocate(boolean yes) {

        // @ TODO count the number of allocates

        if (yes) {
            if (channel != -1) return;
            try {
                channel = JavaSoundSynth.the().allocateChannel();
              //  System.out.println(" ALLOCATE " + channel);
                JavaSoundConductor.the().setPatch(channel, patch);
             //   updateAllCtrl();
            } catch (Exception ex) {
                ex.printStackTrace();
            }
        } else {
            try {
             //   System.out.println(" RELEASE " + channel);
             JavaSoundSynth.the().releaseChannel(channel);
             channel=-1;
            } catch (Exception ex1) {
                ex1.printStackTrace();
            }
        }
    }
}
