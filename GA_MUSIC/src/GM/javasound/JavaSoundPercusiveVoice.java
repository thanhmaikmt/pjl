package GM.javasound;

import GM.music.*;

import GM.io.*;
import javax.sound.midi.*;
import java.io.BufferedReader;
import java.io.InputStream;
import java.io.StreamTokenizer;
import java.io.InputStreamReader;

public class JavaSoundPercusiveVoice extends JavaSoundVoice {



    int note;
    //   GMPatch patch;


    public JavaSoundPercusiveVoice(long id,String name) {
        super(id,name);
        channel=9;
        note=patch.getProgram();

    }



    public void play(Effect effect, long tick, Conductor conductor) {
        Note note = (Note) effect;
        assert (conductor != null);
        ((JavaSoundConductor) conductor).addEvent(this.note,
                                                  tick, note.getLengthInTicks(),
                                                  channel,
                                                  (int) (vol * note.getVelocity()));

    }

    public void setSilent() {
        //@TODO
    }

    public boolean isMelodic() {
        return false;
    }

    public void allocate(boolean yes) {
        channel=9;
      //     JavaSoundConductor.the().setPatch(channel, patch);
      //  updateAllCtrl();
    }

}
