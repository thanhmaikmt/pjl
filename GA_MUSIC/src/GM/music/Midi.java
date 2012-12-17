package GM.music;

/**
 * Midi description.
 *
 * @author P.J.Leonard
 * @version (0.1)
 */
public class Midi {
    /**
     *
     */

    static double pitch[];
    static int noteAt[] = {0, 2, 3, 5, 7, 8, 10};
    static String names[] = {"C", "C#", "D", "D#", "E", "F", "F#", "G", "G#",
                            "A", "A#", "B"};
    final static int N_MIDI_NOTE = 256;
    static public class Controller {

        Controller(int val, String name, int defVal) {
            cntrl = val;
            this.defVal = defVal;
            this.name = name;
        }

        public int cntrl;
        public int defVal;
        public String name;
    }


    final public static
            Controller[]
            cntrlTable = {
                         new Controller(1,
                                        "Modulation", 0),
                         //     new Controller(2, "Breath",0),
                         //     new Controller(5, "Portamento Time",0),
                         new Controller(7, "Volume",100),
                         //      new Controller(8, "Balance",64),
                         new Controller(10, "Pan", 64),
                         new Controller(91, "Reverb",0)
                        // new Controller(92, "Tremolo(depth)",0),
                        // new Controller(76, "Tremolo(rate)",0),
                        // new Controller(93, "Chorus",0)
    };



    public static void init() {
        pitch = new double[N_MIDI_NOTE];
        pitch[21] = 27.5;
        double fact = Math.pow(2.0, 1.0 / 12.0);
        for (int i = 22; i < N_MIDI_NOTE; i++) {
            pitch[i] = pitch[i - 1] * fact;
        }
    }

    static double midiNumberToFrequency(int i) {
        if (pitch == null) {
            init();
        }
        return pitch[i];
    }

    static String midiNumberToName(int n) {
        int flav = n % 12;
        int nOct = n / 12;
        return names[flav] + nOct;
    }


    static int nameToMidiNumber(String name) {
        byte b[] = name.getBytes();
        int note = b[0] - ("A".getBytes())[0];
        int sharp = 0;
        int octave = 0;

        if (b.length > 1) {
            if (b[1] == "#".getBytes()[0]) {
                sharp = +1;
            } else if (b[1] == "b".getBytes()[0]) {
                sharp = -1;
            }
        }

        if (sharp != 0 && b.length > 2) {
            octave = b[2] - "0".getBytes()[0];
        } else if (b.length > 1) {
            octave = b[1] - "0".getBytes()[0];
        }

        System.out.println("n:" + note + "(" + sharp + ")" + " o:" + octave);

        return noteAt[note] + octave * 12 + sharp;
    }

    /**
     * Test code
     */
    public static void main(String args[]) {

        for (int i = 0; i < N_MIDI_NOTE; i++) {
            System.out.println(i + " " + midiNumberToFrequency(i));
        }

    }

    // private data
}
