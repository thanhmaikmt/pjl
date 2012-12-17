package GM.music;

public class Calibrator implements Runnable {
    Player player;
    boolean running;

    public Calibrator(Player player) {
        this.player=player;
    }

    public void run() {
        running=true;
        doit();
    }

    public void halt() {
        running=false;
    }

    private synchronized void doit() {
        Voice voice = player.getVoice();
        boolean doit = true;
        Conductor c = player.getVoice().getConductor();
        try {
            System.out.println(" Wait a tick for buffers to clear");
            wait(2000);
            System.out.println(" Starting calibrationg. Toggle button to quit ");
        }catch(Exception e) {
            e.printStackTrace();
        }

        double ticksTPS=Conductor.masterRate();
        long  period = (long)ticksTPS*2;


        while (running) {

            long tNow = Conductor.getTickNow();

            long tPlay = tNow + period;
            long millisPlay=(long)((tPlay*1000.0)/ticksTPS);
            Time len = new Time(0, 1, 8);
            Note note = new Note(len, 64, .8);

           try {
                c.sleepUntilJustBefore(tPlay);
                voice.play(note, tPlay, c);
                long millis=PeakAnalyst.the().waitForPulse(4000);
                System.out.println(
            " now=" + millisPlay/1000.0 + " pulseAt="+ millis/1000.0 + " diff(ms)=" +(millisPlay-millis));
       //    } catch (GMSyncException ex) {
            //    System.err.println(" Sync err of " + ex.ticksLost + " [ticks] ");

            } catch (Exception ex) {
                ex.printStackTrace();
            }
        }
       System.out.println(" Exited calibrator ");
    }



}
