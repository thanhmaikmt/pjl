package GM.music;

import java.util.*;

public class Band extends Observable  {

    Vector<Player> players = new Vector<Player>();

    Song song;
    Player selectedPlayer=null;

    boolean updates=true; // avoid recursion
    public Band(Song song) {
        this.song = song;
    }

    public Song getSong() {
        return song;
    }

    public void setSelectedPlayer(Player p) {
        if (selectedPlayer == p) return;
        if (selectedPlayer != null ) selectedPlayer.setSelected(false);
        selectedPlayer = p;
        selectedPlayer.setSelected(true);
        setChanged();
        notifyObservers(Message.SELECTION_CHANGE);
    }

    public Player getSelectedPlayer() {
        return selectedPlayer;
    }

    public synchronized void addPlayer(Player p) {
        players.add(p);
        setChanged();
        notifyObservers(Message.ADD_PLAYER);
    }

    public synchronized Player lastPlayer() {
        if (players.size()==0) return null;
        return players.elementAt(players.size()-1);
    }

    public synchronized void removePlayer(Player p) {
        players.remove(p);
        p.kill();
    }

    synchronized void kill() {
        Iterator<Player> iter = players.iterator();
        while (iter.hasNext()) {
            Player player=iter.next();
            player.band=null;
            player.kill();
        }
        players.removeAllElements();
        players = null;
    }


    public Vector<Player> getPlayers() {
        return players;
    }

    public synchronized int posOfPlayer(Player p) {
        return players.indexOf(p);
    }

    public int countPlayers() {
        return players.size();
    }


    public synchronized void silenceAll() {
        Iterator iter = players.iterator();
        while (iter.hasNext()) {
            Player v = ((Player) iter.next());
            v.setSilent(true);
        }
    }

    public synchronized boolean soloistExists() {

        boolean isSoloist = false;
        Iterator<Player> iter = players.iterator();
        while (iter.hasNext()) {
            Player v = iter.next();
            if (v.isSolo()) return true;

        }
        return false;
    }


    public synchronized void updatePlayerState() {
        if (!updates) return;
        boolean isSoloist=soloistExists();

        Iterator<Player> iter = players.iterator();

        while (iter.hasNext()) {
            Player v = ((Player) iter.next());

            if (v.isMute() || (isSoloist && (!v.isSolo()))) {
              //  System.out.println(v.getName() + " muting ");
                v.setSilent(true);
            } else {
              //  System.out.println(v.getName() + " unmuting ");
                v.setSilent(false);
            }
        }
    }

    public synchronized void unMuteAll() {

        updates=false;
        Iterator<Player> iter = players.iterator();

       while (iter.hasNext()) {
           Player v = iter.next();
           v.mute.setOn(false);
       }
       updates=true;

       updatePlayerState();
    }


    public synchronized void unSoloAll() {

        updates=false;

        Iterator<Player> iter = players.iterator();

        while (iter.hasNext()) {
            Player v = iter.next();
            v.solo.setOn(false);
        }
        updates=true;

        updatePlayerState();
    }


    public synchronized void allocate(boolean yes) {

        for(Player p: players) {
            Voice  v = p.getVoice();
            v.allocate(yes);
            p.updateAllCtrl(true);
        }


    }

}
