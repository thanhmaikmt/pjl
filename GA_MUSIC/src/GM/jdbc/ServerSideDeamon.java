package GM.jdbc;


import java.sql.Statement;


/**
 * <p>Title: </p>
 *
 * <p>Description: </p>
 *
 * <p>Copyright: Copyright (c) Dr PJ Leonard 2005</p>
 *
 * <p>Company: </p>
 *
 * @author Dr PJ
 * @version 0.1
 */
public class ServerSideDeamon {


    DataBase db;
    javax.swing.Timer    timer;
    ServerSideDeamon(DataBase db) throws InterruptedException {
        this.db = db;
//          wait();
    }

    synchronized void start() {
        while(true) {
            doit();
            try {
                wait(10000);
            }catch (InterruptedException ex) {

            }
        }
    }

    class S {
        S(long p) { time=p; }
        long time=0;
    }


    public void doit() {


   //     System.out.println("HELLO");


        try {
            Statement stat = db.conn.createStatement();
            String cmd =
            "UPDATE SongTABLE,PlayTimeTABLE "+
            "SET SongTABLE.playTime=SongTABLE.playTime+PlayTimeTABLE.playTime "+
            "WHERE SongTABLE.id=PlayTimeTABLE.songID";
            stat.execute(cmd);
            cmd = "DELETE from PlayTimeTABLE";
            stat.execute(cmd);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }



    public static void main(String argts[]) throws Exception {

        String xxx=new String(new char[]{83,20,88,67,13,18,1});
        DataBase.MySqlHost host=new DataBase.MySqlHost("138.38.66.197", "138.38.66.197",
                                              new byte[] {(byte)138, 38,(byte) 66, (byte) 197},
                                              "simphoneyadmin", xxx , 6306 , true);
        ServerSideDeamon d=new ServerSideDeamon(new DataBase(host));
        d.start();
    }
}
