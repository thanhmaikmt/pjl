package GM.music;

import java.util.concurrent.locks.Lock;

/***
 * Plays the sequence at an offset time
 */
class PhraseSequencer extends Thread {

    final static boolean monitor = false;
    EventList eventList;
    Voice voice;
    boolean stop;
    Player player;
    Phrase phrase;
    Conductor conductor;
    Time offset;
    Time end;
    boolean alive=true;

    PhraseSequencer(Phrase phrase, Time offset) {
        // super(phrase);
        this.offset = offset;
        this.end = offset.add(phrase.part.len);
        this.player = phrase.getPlayer();
        this.phrase = phrase;
        this.voice = player.getVoice();
        this.conductor = player.getVoice().getConductor();
        assert(conductor != null);
        eventList = new EventList(phrase.eventList); // player.getPhrase())
        if (PhraseSequencer.monitor) {
            System.out.println(" Offsetplayer " + offset);
        }
    }


    public void run() {


        setPriority(Thread.MAX_PRIORITY);

        //    System.out.println(" OS 1 ---");

        EventIterator iter = new EventIterator(eventList);

        while (iter.hasNext() && conductor != null && ! phrase.isKilled() ) {

            Event event = iter.next();
            try {
                play(event, offset);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    synchronized public void play(Event event, Time offset) throws Exception {
        if (monitor) {
            System.out.println("Player - Playing (offset)" + offset + " -> " +
                               event.toString());
        }

        Time on = event.getTime().add(offset);
        try {
            //   System.out.print(" > ");
            if (conductor == null) return;
            conductor.sleepUntilJustBefore(on);
            //  System.out.print(" < ");
            if (player != null && !player.isSilent()  && !phrase.isMute()) {
                Effect effect = event.getEffect();
                if (!alive) return;
                voice.play(effect, conductor.getTickAt(on), conductor);
            }
        } catch (GMSyncException ex) {
            System.err.println(" Lost sync " + ex.ticksLost +
                               " in Sequencer.play --- increase latency");
        }
    }

    public void kill() {
        alive=false;
    }

    public Voice getVoice() {
        return voice;
    }

    public void setVoice(Voice voice) {
        this.voice = voice;
    }

}
