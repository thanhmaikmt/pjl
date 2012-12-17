package GM.jdbc;

import GM.music.*;
import java.util.*;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.io.*;
import java.net.InetAddress;
import java.net.*;
import GM.util.Mangler;


public class DataBase {

    Connection conn;

    String user;

    static DataBase the = null;

    public static class MySqlHost {

        public MySqlHost(String name, String server, byte IP[], String user,
                         String passwd,boolean xxx) {
            this.name = name;
            this.server = server;
            this.IP = IP;
            this.user = user;
            this.passwd = passwd;
            this.port = 3306;
            this.xxx=xxx;
        }

        public MySqlHost(String name, String server, byte IP[], String user,
                         String passwd,
                         int port,boolean xxx) {
            this.name = name;
            this.server = server;
            this.IP = IP;
            this.user = user;
            this.passwd = passwd;
            this.port = port;
            this.xxx=xxx;
        }

        public String toString() {
            return name;
        }

        String name;
        String server;
        byte IP[];
        String user;
        String passwd;
        int port;
        String dbName = "PROJsimphoney";
        boolean xxx=false;
    }

    static String xxx=new String(new char[]{92,21,66,78,20,23,7});

    static MySqlHost hosts[]
            = {



              new MySqlHost("138.38.66.197", "138.38.66.197",
                            new byte[] {(byte)138,38,66, (byte) 197},
                            "simphoneyuser", xxx , 6306 , true),

              new MySqlHost("datachase.net", "datachase.net",
                            new byte[] {66,(byte) 197,(byte) 155, (byte) 183},
                            "simphoneyuser", xxx , true ),


              new MySqlHost("localhost", "", new byte[] {(byte) 127, (byte) 0,
                            (byte) 0, (byte) 1}, "simphoneyuser", xxx,true),


              new MySqlHost("localhost", "", new byte[] {(byte) 127, (byte) 0,
                            (byte) 0, (byte) 1}, "simphoneyadmin", xxx,true),

              new MySqlHost("datachase.net(IP)", "66.197.155.183",
                     new byte[] {66,(byte) 197,(byte) 155, (byte) 183},
                     "simphoneyuser", xxx, true ),

        //      new MySqlHost("bath.ac.uk", "mysqlhost.bath.ac.uk",
        //                    new byte[] {(byte) 138, 38,
        //                    32, 52}, "simphoneyuser", "EmmS6d52",false),

              new MySqlHost("emd0007", "eepc-emd0007",
                            new byte[] {(byte) 138, (byte) 38,
                            (byte) 64, (byte) 115}, "simphoneyadmin", xxx,true)

    };


    MySqlHost host = null;



    public MySqlHost getHost() {
        return host;
    }

    static public DataBase the() {
        return the;
    }

    static public void  kill() {
        if (the == null) return;
        the.close();
        the=null;

    }

    static public int n() {
        return hosts.length;
    }

    boolean isServerReachable(int timeout) {
        InetAddress addr = null;
        try {
            addr = InetAddress.getByAddress(host.IP);
        } catch (UnknownHostException ex) {
            System.out.println(" Unknown Host "
                               + host.IP[3] + "."
                               + host.IP[2] + "."
                               + host.IP[1] + "."
                               + host.IP[0]);
            return false;
        }

        try {
            if (addr.isReachable(timeout)) {
                return true;
            } else {
                System.out.println("Server is not reachable");
                return false;
            }
        } catch (IOException ex1) {
            ex1.printStackTrace();
            return false;
        }
    }

    public DataBase(int id, int timeout) throws Exception {
        this(hosts[id]);
    }

    public DataBase(MySqlHost host) throws Exception {

        this.host = host;
        String x;

        if (host.xxx) {
    //        System.out.println(" DEMANGLE " +host.passwd.toCharArray());
            x = new String(Mangler.spin(host.passwd.toCharArray()));

        } else x = host.passwd;

        String jdbcStr;
        
        
        if (host.port != 3306) {
            jdbcStr = "jdbc:mysql://" + host.server + ":" + host.port +
                      "/?user=" + host.user +
                      "&password=" + x; //+"&connectTimeOut="+timeout+"&socketTimeOut="+timeout;
        } else {
            jdbcStr = "jdbc:mysql://" + host.server +
                      "/?user=" + host.user +
                      "&password=" + x ; //+"&connectTimeOut="+timeout+"&socketTimeOut="+timeout;
        }
        jdbcStr = "jdbc:mysql://localhost;"+
                "user=" + host.user +
                ";password=" + x ; //+"&connectTimeOut="+timeout+"&socketTimeOut="+timeout;
      System.out.println(jdbcStr);


        /*
                 if (!isServerReachable(timeout)) {
            throw new  Exception(" Service unreachable ");
                 }
         */

        if (the == null) {
            Class.forName("com.mysql.jdbc.Driver").newInstance();
        }

        try {
        	//conn = DriverManager.getConnection(jdbcStr);
        	conn = DriverManager.getConnection("jdbc:mysql://localhost/PROJsimphony","simphonyadmin","m0llusc");
        } catch (SQLException ex) {
            jdbcStr=null;
            // handle any errors
            System.err.println("SQLException: " + ex.getMessage());
            System.err.println("SQLState: " + ex.getSQLState());
            System.err.println("VendorError: " + ex.getErrorCode());
            throw ex;

        } finally {
            jdbcStr=null;
        }

        System.out.println(" Connected OK  . . . Now opening database " +
                           host.dbName);

        open();

        the = this;
    }


    public void close() {
        try {
            conn.close();
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    void open() throws SQLException {
        Statement stat = conn.createStatement();
        stat.execute("USE " + host.dbName);
        stat.close();
    }

    public void scub() throws Exception {
        Statement stat = conn.createStatement();
        stat.execute("DROP DATABASE PROJsimphoney");

    }

    public void initialize() throws Exception {
        Statement stat = conn.createStatement();
      //  stat.execute("DROP DATABASE PROJsimphoney");
      //   stat.execute("CREATE DATABASE PROJsimphoney");
        stat.execute("USE PROJsimphoney");
        stat.close();

        Song.tableInfo.createTable(conn);
        Part.tableInfo.createTable(conn);
        SongMap.tableInfo.createTable(conn);
        Phrase.tableInfo.createTable(conn);
        Player.tableInfo.createTable(conn);
        PlayTime.tableInfo.createTable(conn);
        createUserTable();
    }

    public String getUser() {
        return user;
    }

    public boolean logon(char passwd[], String name) throws
            Exception {
        Statement stat = conn.createStatement();
        String cmd = "SELECT password FROM  UserTABLE WHERE username = \"" +
                     name + "\"";
        ResultSet res = stat.executeQuery(cmd);
        if (!res.next()) {
            throw new Exception(" Username " + name + " not found");
        }
        String passwdStr = res.getString(1);
        String passwdStr1 = new String(passwd);
        if (passwdStr.equals(passwdStr1)) {
            user=name;
            return true;
        }
        throw new Exception("Invalid password");
      }

      public void addUser(String name, String passwd) {
          UserTable ut = new UserTable(name, passwd);
          ut.tableInfo.save(conn, ut);
      }


      public boolean userExists(String name) throws Exception {
          return UserTable.exists(name);
      }



    public void addPlayTime(Song song,String user) {
        PlayTime pt=new PlayTime(song.getId(),PlayTimer.getPlayTime(),user);
        PlayTime.tableInfo.save(conn,pt);
    }

    void createUserTable() throws Exception {
        UserTable.tableInfo.createTable(conn);
        addUser(Defaults.user, "");
    }

    public String mysqlUser() { return host.user; }


    public static void main(String[] args) throws Exception {


        JDBCConnectDialog dialog= new JDBCConnectDialog(false);

        dialog.setVisible(true);


        DataBase db=dialog.getDataBase();

        //  db.createUserTable();

        db.initialize();

        System.exit(0);
        //      db.createTables();

    }
}



