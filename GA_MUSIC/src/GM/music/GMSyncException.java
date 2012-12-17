package GM.music;

public class GMSyncException extends Exception{
    public long ticksLost;
    public GMSyncException(long ticks) {
        ticksLost=ticks;
    }
}
