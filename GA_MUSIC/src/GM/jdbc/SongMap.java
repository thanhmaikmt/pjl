package GM.jdbc;

import java.sql.ResultSet;
import java.sql.SQLException;



class SongMap implements TableInfo {

    static String[] types = {"INT", "INT","INT", "INT","INT", "INT", "INT" };
    static String[] keys = {"SongID", "SectionID", "PartID","PhraseID", "TrackID","PlayerID","VoiceID"};

    static public final TableInfoData tableInfo = new TableInfoData(types, keys,
            "MAP", false);

    long perfID;
    long sectID;
    long partID;
    long phraseID;
    long trackID;
    long playerID;
    long voiceID;

    SongMap(long perfID, long sectID, long partID,long phraseID,long trackID, long playerID,long voiceID) {
        this.perfID = perfID;
        this.sectID = sectID;
        this.partID = partID;
        this.phraseID = phraseID;
        this.voiceID = voiceID;
        this.playerID = playerID;
        this.trackID=trackID;
    }

    SongMap(ResultSet res) throws SQLException {
        int i=1;
        perfID = res.getInt(i++);
        sectID = res.getInt(i++);
        partID = res.getInt(i++);
        phraseID = res.getInt(i++);
        trackID = res.getInt(i++);
        playerID = res.getInt(i++);
        voiceID = res.getInt(i++);
    }

    public String[] getValues() {
        String[] r = {String.valueOf(perfID),
                     String.valueOf(sectID),
                     String.valueOf(partID),
                     String.valueOf(phraseID),
                     String.valueOf(trackID),
                     String.valueOf(playerID),
                     String.valueOf(voiceID)
        };
        return r;
    }


    public long getId() {
        return 0;
    }

    public void setId(long id) {}


}
