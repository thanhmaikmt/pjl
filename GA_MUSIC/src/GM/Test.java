package GM;

import javax.sound.midi.*;
import java.util.*;


class Test extends TimerTask {

  Track track;
  Sequence sequence;

  final int NOTEON = 144;
  final int NOTEOFF = 128;

  Sequencer sequencer;

  long time=50;       /** events are add 50ms before sequencer plays them */

  int  interval =100; /**  play notes every (in ms) */
  long dur     = 10;  /** length of the note */
  long startTime;     /** system time when we start sequencer */

  int count    = 0;

  /** IMPORTANT make a tick a milli second for this test */

  float tempoMPQ=100000; /** ms per quarter note */
  int ticksPQ=100;       /** ticks per quarter note */

  Random r=new Random();

  public Test() {
    try {


      Synthesizer synth=MidiSystem.getSynthesizer();
      System.out.println(synth);

      sequencer = MidiSystem.getSequencer();
      System.out.println(sequencer);

      System.out.println(sequencer.getMasterSyncMode());

      sequencer.open();
      synth.open();

      Soundbank sb = synth.getDefaultSoundbank();

      synth.loadAllInstruments(sb);
      //      if (sb != null) {
      //	  Instrument instruments[] = synth.getDefaultSoundbank().getInstruments();
      //	  synth.loadInstrument(instruments[0]);
      //      }

      sequence = new Sequence(Sequence.PPQ, ticksPQ);
      track = sequence.createTrack();
      sequencer.setTempoInMPQ(tempoMPQ);
      sequencer.setSequence(sequence);

      /** IMPORTANT  add an event a long time into the future */

      addEvent(0,1000000,50,1);
      sequencer.start();
      startTime = System.currentTimeMillis();

      new java.util.Timer().scheduleAtFixedRate(this,interval,interval);

    }catch(Exception e) {
      e.printStackTrace();
    }
  }


  public void run() {

    long  tick = sequencer.getTickPosition();
    time += interval;
    long stime = System.currentTimeMillis()-startTime;

    if (r.nextInt(8) > 1) addEvent(60+r.nextInt(12),time,dur,r.nextInt(16));

    System.out.println(" stamp  systemTime-sequencerTime  stamp-sequencerTime = " + time + " " + (stime - tick) + "  " + (time - tick) );

  }


  /** add a note on at when of length dur */

  void addEvent(int pitch,long when,long dur,int ch) {

    try {

      ShortMessage message = new ShortMessage();
      message.setMessage(NOTEON, ch, pitch, 127);
      MidiEvent event = new MidiEvent(message, when);
      track.add(event);

      message = new ShortMessage();
      message.setMessage(NOTEOFF, ch, pitch, 0);
      event = new MidiEvent(message, (when+dur));
      track.add(event);

    } catch (Exception ex) { ex.printStackTrace(); }
  }

  public static void main(String args[]) {
    new Test();
  }

}
