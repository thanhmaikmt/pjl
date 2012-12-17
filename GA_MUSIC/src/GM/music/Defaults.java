package GM.music;

import GM.genetic.GmRandom;

public class Defaults {
    static GmRandom r=new GmRandom();

    public static int chordsPerBeat=1;
    public static int partLength=r.nextInt(2)+3;
    public static int pulsesPerBeat= r.nextInt(3)+2;
    public static int pulsesPerBeatMult=1;
    public static String user="anonymous";

    public static void randomInit() {
        partLength=r.nextInt(2)+3;
        pulsesPerBeat= r.nextInt(3)+2;
    }

}
