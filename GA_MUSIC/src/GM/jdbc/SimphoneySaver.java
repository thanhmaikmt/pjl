package GM.jdbc;

import GM.music.Voice;
import java.sql.SQLException;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import GM.music.Song;
import java.util.Iterator;
import GM.music.Part;
import GM.music.Phrase;
import GM.music.Player;

public class SimphoneySaver {

    DataBase db;
    public SimphoneySaver(DataBase db) {
        this.db=db;
    }

    void savePlayer(Player player) throws SQLException {
        if (player.getId() != 0) {
            return;
        }
        Player.tableInfo.save(db.conn,player);
    }


    public void saveSong(Song perf) throws Exception {

        //@TODO


        synchronized(perf) {
            Song.tableInfo.save(db.conn, perf);

            long perfId = perf.getId();
            int sectId=1;

            for(Part part: perf.getSections()) {
                savePart(part, perfId , sectId);
            }
        }
    }

    void savePart(Part part, long perfId,long sectId) {
        long partId = part.getId();

        //@TODO do we want to do this
        //      (save partly created songs ? )
        if (partId != 0 && perfId == 0) {
            return;
        }

        if (partId == 0) {
            Part.tableInfo.save(db.conn, part);
            partId = part.getId();
        }

        //SongMap ps = new SongMap(perfId, sectId, partId, 0, 0,0,0);
        //ps.tableInfo.save(db.conn, ps);

        int trackId=1;

        synchronized (part) {
            for (Phrase phrase:part.getPhrases()) {
                long phraseId = phrase.getId();
                if (!phrase.isMute()) {
                    if (phraseId == 0) {
                        Phrase.tableInfo.save(db.conn, phrase);
                        phraseId = phrase.getId();
                    }
                } else {
                    phraseId=0;
                }

                Player player = phrase.getPlayer();
                long playerId = player.getId();
                if (playerId == 0) {
                    //Voice.tableInfo.save(db.conn, voice);
                    try {
                        savePlayer(player);
                    } catch (SQLException ex) {
                        ex.printStackTrace();
                    }
                    playerId = player.getId();
                }

                SongMap ps = new SongMap(perfId, sectId, partId, phraseId, trackId++, playerId,
                                 player.getVoice().getId());
                ps.tableInfo.save(db.conn, ps);
            }
        }
    }

}
