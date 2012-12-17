package GM.music;
//import gm.*;
//import java.io.*;

/**
 * Note description.
 *
 * @author P.J.Leonard
 * @version (0.1)
 */
public class Note extends IntEffect
{
    /**
     *
     */


    public Note(Time l,int i,double vel)
    {
        super(l.getTick(),i,i,(long)(vel*IntEffect.dScale));
    }

    public void mutate() {
        assert(false);
    }
    public void setPitch(int p) {
        val[2]=p;
    }
   public void setInt(int p) {
        val[1]=p;
    }

    public Time   getLength() { return new Time(val[0]);}
    public long   getLengthInTicks() { return val[0];}
    public int    getPitch() { return (int)val[2];}
    public int    getInt() { return (int)val[1];}
    public double getFrequency() { return Midi.midiNumberToFrequency(getPitch());}
    public double getVelocity() { return getValAt(3)/IntEffect.dScale;}
    public String toString() {
        return "Note: "+getPitch()+" "+getVelocity()+" " + getLength().toString();
    }

    public String getName() { return Midi.midiNumberToName((int)val[2]);}


}
