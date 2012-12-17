package GM.jdbc;


class PlayTime implements TableInfo {

    static String[] types = {"INT", "INT","TEXT"};
    static String[] keys = {"songID", "playtime","user"};

    static public final TableInfoData tableInfo = new TableInfoData(types, keys,
            "PlayTimeTABLE", false);

    long songID;
    long playTime;
    String user;

    PlayTime(long songId, long time,String user) {
        this.songID = songId;
        this.playTime = time;
        this.user=user;
    }


    public String[] getValues() {
        String[] r = {String.valueOf(songID), String.valueOf(playTime),
                     "\"" + user + "\""
        };
        return r;
    }

    public void setId(long id) {}

    public long getId() {
        return 0;
    }
}
