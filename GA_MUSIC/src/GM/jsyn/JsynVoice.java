package GM.jsyn;

import GM.music.*;
import GM.io.*;
import com.softsynth.jsyn.*;
import com.softsynth.jsyn.circuits.*;

public class JsynVoice extends Voice {


    public SynthNote note;
    boolean melodicFlag=false;

    public boolean isMelodic() { return melodicFlag; }



    public long getId() { return 0; }

    JsynVoice(SynthNote note,String name,int index) {

        // @TODO make me work
        super(name);
        this.note=note;
        melodicFlag=note.frequency != null;
    }

    public void play(Effect effect, long on, Conductor c) {
        int tick=(int)on;
        try {
            if (effect == null) {
                note.noteOff(tick);
            } else {
          //      System.out.println(" PLAYING " + note);
          //      note.setStage(tick,0);
                Note myNote = (Note) effect;
                double ampval = .7 * myNote.getVelocity();
                double freq = myNote.getFrequency();

                note.noteOn(tick,freq,ampval);

                Time dur=myNote.getLength();
                int tickL=(int)Conductor.durationToTicks(dur);
               // System.out.println(tickL);
                note.noteOff(tick+tickL);

            }
        } catch (SynthException e) {
            e.printStackTrace();
        }


    }

    public void setSilent() {
        note.noteOff(0);
    }

    public Conductor getConductor() {
        return JsynConductor.the();
    }

    public void allocate(boolean yes) {
        assert(false);

    }

    public SynthNode getParent() { return null; }



}
