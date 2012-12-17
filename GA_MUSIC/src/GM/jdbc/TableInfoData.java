package GM.jdbc;

import java.sql.*;
import GM.music.Phrase;
import GM.music.Player;

public class TableInfoData {
    String[] types;
    String[] keys;
    String[] xtypes;
    String[] xkeys;
    String name;
    boolean autoKey;


    public TableInfoData(String[] types, String[] keys,String[] xTy,String [] xInfo,String name,
                         boolean autoKey) {
        this.xtypes=xTy;
        this.xkeys=xInfo;
        this.types = types;
        this.keys = keys;
        this.name = name;
        this.autoKey = autoKey;


    }

    public TableInfoData(String[] types, String[] keys, String name,
                         boolean autoKey) {
        assert (types.length == keys.length);
        this.types = types;
        this.keys = keys;
        this.name = name;
        this.autoKey = autoKey;
    }

    public void createTable(Connection conn) throws Exception {
        Statement stat = conn.createStatement();

        StringBuffer buf = new StringBuffer();
        buf.append("CREATE TABLE " + name + " ( ");
        if (autoKey) {
            buf.append(" id INT NOT NULL AUTO_INCREMENT,");
        }
        for (int i = 0; i < keys.length; i++) {
            if (i == 0) buf.append(keys[i] + " " + types[i] );
            else  buf.append(","+keys[i] + " " + types[i]);
        }

        if (xkeys != null) {
            for (int i = 0; i < xkeys.length; i++) {
                buf.append(","+xkeys[i] + " " + xtypes[i]);
            }
        }



        if (autoKey) {
            buf.append(", PRIMARY KEY (id))");
        }else {
            buf.append(")");
        }
     //   System.out.println(buf);
        stat.execute(buf.toString());
    }


    String makeList(String[] a) {
        String ret = "(" + a[0];

        for (int i = 1; i < a.length; i++) {
            ret += "," + a[i];
        }

        ret += ")";
        return ret;
    }


    public String getStatement() {
        return "INSERT INTO "+name+" "+makeList(keys)+" values(?, ?)";
    }

    public void save(Connection conn, TableInfo info) {

        try {
            Statement stat = conn.createStatement();
            String cmd = "INSERT INTO " + name + " " +
                         makeList(keys) +
                         " VALUES " +
                         makeList(info.getValues());
            System.out.println(cmd);
            stat.execute(cmd);
            if (autoKey) {
                ResultSet res = stat.executeQuery("SELECT LAST_INSERT_ID()");
                res.next();
                info.setId((int) (res.getLong(1)));

            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

}
