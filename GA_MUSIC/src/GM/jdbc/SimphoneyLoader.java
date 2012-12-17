package GM.jdbc;


import GM.music.Voice;
import java.sql.SQLException;
import java.sql.ResultSet;
import GM.music.Song;
import java.util.*;
import GM.music.Part;
import GM.music.Phrase;
import java.sql.Statement;
import GM.music.Player;
import GM.music.Band;
import java.lang.reflect.InvocationTargetException;

import java.io.*;
import GM.music.GMPatch;
import GM.music.Hub;
import GM.music.NullPhrase;

/**
 * A <code> SimphoneyLoader </code> loads osng components and builds a song
 * from the <code> DataBase </code>
 *
 * @author Dr PJ
 * @version 0.1
 */
public class SimphoneyLoader {
    DataBase db;

    /**
     *
     * @param db <code> DataBase </code>
     */
    public SimphoneyLoader(DataBase db) {
        this.db = db;
    }

    /**
     * Fetch list of songs from the DataBase
     *
     * @return Vector
     */
    public Vector<Song> getSongs() {
        Vector<Song> perfs = new Vector<Song>();
        Statement stat = null;
        try {
            stat = db.conn.createStatement();

            ResultSet res = null;
            res = stat.executeQuery(
                    "SELECT * FROM SongTABLE order by -id");
            while (res.next()) {
                Song song = new Song(res);
                perfs.add(song);
            }

        } catch (SQLException ex) {
            ex.printStackTrace();
        }

        return perfs;

    }

    public Part loadPart(long id) throws SQLException {
        Statement stat = db.conn.createStatement();
        String cmd = "SELECT * FROM  PartTABLE WHERE id = " +
                     String.valueOf(id);
        //     System.out.println(cmd);
        ResultSet res = stat.executeQuery(cmd);
        res.next();
        return new Part(res);

    }


    public Phrase loadPhrase(long id) throws SQLException {

        if (id == 0) {
            return new NullPhrase();
        }

        Statement stat = db.conn.createStatement();
        ResultSet res = stat.executeQuery(
                "SELECT * FROM  PhraseTABLE WHERE id = " + String.valueOf(id));
        res.next();
        return new Phrase(res);
    }


    public Player loadPlayer(long id, Band band, Voice v) throws SQLException,
            ClassNotFoundException,
            SecurityException, NoSuchMethodException, InvocationTargetException,
            IllegalArgumentException, IllegalAccessException,
            InstantiationException, IOException {
        Statement stat = db.conn.createStatement();
        String cmd = "SELECT * FROM  PlayerTABLE WHERE id = " +
                     String.valueOf(id);

        System.out.println(cmd);
        ResultSet res = stat.executeQuery(cmd);
        res.next();

        return (new Player(res, band, v));

    }

    public void loadSong(Song song) throws Exception {

        song.lockId(true);
        Part part = null;
        Band band = song.getBand();

        long partID = 0;
        long songId = song.getId();
        Map<Long, Player> trackPlayerMap = new TreeMap<Long, Player>(); // loadPlayers(song);

        Statement stat = db.conn.createStatement();
        ResultSet res = stat.executeQuery(
                "SELECT * FROM  MAP WHERE SongID = " +
                String.valueOf(songId));

        while (res.next()) {
            SongMap map = new SongMap(res);

            //@TODO sections

            Phrase phrase = null;
            if (map.partID != partID) {
                part = loadPart(map.partID);
                song.appendPart(part);
                partID = map.partID;
            }

            phrase = loadPhrase(map.phraseID);
            phrase.setPart(part);

            Player player = trackPlayerMap.get(map.trackID);

            if (player == null) {
                System.out.println(" Creating player for track " + map.trackID);
                Voice voice = Hub.the().createVoice(new GMPatch(map.voiceID));

                if (map.playerID > 0) {
                    player = loadPlayer(map.playerID, band, voice);
                    trackPlayerMap.put(map.trackID, player);
                } else {
                    assert (map.playerID == -1);
                    player = new Player(voice, band);
                    trackPlayerMap.put(map.trackID, player);
                    //player.setId(-1);
                }

                // player.setVoice(voice);
            }

            phrase.setPlayer(player);
        }
        song.rebuild();
        song.lockId(false);
    }

}
