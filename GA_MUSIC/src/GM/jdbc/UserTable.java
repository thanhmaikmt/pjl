package GM.jdbc;

//import com.mysql.*;
import java.sql.Statement;
import java.sql.ResultSet;
import java.sql.SQLException;


class UserTable implements TableInfo {

    static String[] types = {"TEXT", "TEXT"};
    static String[] keys = {"username", "password"};

    static public final TableInfoData tableInfo = new TableInfoData(types, keys,
            "UserTABLE", false);

    String user;
    String passwd;

    UserTable(String user, String passwd) {
        this.user = user;
        this.passwd = passwd;
    }


    public String[] getValues() {
        String[] r = {"\"" + user + "\"", "\"" + passwd + "\""
        };
        return r;
    }

    static public boolean exists(String name) throws SQLException {
        String cmd="SELECT * from "+ tableInfo.name +" where username="+"\"" +name + "\"";
        Statement stat = DataBase.the().conn.createStatement();
        ResultSet res = stat.executeQuery(cmd);
        return res.next();
    }

    public void setId(long id) {}

    public long getId() {
        return 0;
    }
}
