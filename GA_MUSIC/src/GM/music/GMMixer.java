package GM.music;

import java.util.*;


/**
 * Write a description of class Mixer here.
 *
 * @author DR pJ
 * @version 1
 */

public abstract class GMMixer implements Observer {
    /**
     * Constructor for objects of class Mixer
     */

    protected Vector voices;
    boolean isDirty;

    public GMMixer() {
        voices = new Vector();
    }

    public void update(Observable o, Object arg) {
        if (o instanceof Voice) {
            // updateVoiceState();

        }
    }


    public abstract void rebuild(Vector players);


    public abstract void kill();


    public void setDirty() { isDirty=true; }

   // public Mixer createMixer() { return new Mixer();}

}
