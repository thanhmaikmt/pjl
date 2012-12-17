package GM.music;

//import gm.*;

public class Event implements Comparable{


    Time time;
    Effect effect;

    public Event(Time time) {
        this.time = time;
        this.effect = null;
    }

    public void mutate() {
        assert(false);
    }
    public Event(Time time,Effect effect) {
        this.time   = time;
        this.effect = effect;
    }

//     public void writeToGene(GeneWriter g) throws Exception {
//         time.writeToGene(g);
//         effect.writeToGene(g);
//     }

    public Time getTime() {
       return time;
    }

    public void setTime(Time time) {
        this.time=time;
    }

    public int compareTo(Object b) {
        Event e=(Event)b;
        return time.compareTo(e.getTime());
    }

    public Effect getEffect() {
        return effect;
    }


    public void setEffect(Effect effect) {
        this.effect = effect;
    }

    public String toString() {
        if (effect != null)
            return "At:" + time.toString() +" "+ effect.toString();
        else
            return "At:" + time.toString() +" null ";
    }

    public Object clone() {
    return new Event((Time)(time.clone()),(Effect)(effect.clone()));
    }

    public String getName(){ return "";}
  //  final public Type getType(){ return eventType;}
}
