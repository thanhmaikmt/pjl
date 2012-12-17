package GM.music;

import java.util.*;
import GM.jdbc.*;
import java.io.*;
import GM.tweak.*;

abstract public class Voice extends Observable { // implements TableInfo  {

  //  int index;
//    long id;


    private String name;
  //  private String bankName;
  //  private String synthName;



    boolean killed = false;


    protected Voice(String name) {
        this.name = name;

    }

/*
    public Voice(StreamTokenizer st) {
        this();
        try {
            st.nextToken();
            name = st.sval;
            st.nextToken();
            bankName = st.sval;
            st.nextToken();
            synthName = st.sval;

        } catch (IOException ex) {
            ex.printStackTrace();
        }


    }


    public Voice(String name,int index,String bankName,String synthName) {
        this();
        this.name=name;
        this.bankName=bankName;
        this.synthName=synthName;
        this.index=index;
    }

*/
    /*
    public void update(Observable o, Object arg) {
        Tweakable t=(Tweakable) o;
        System.out.println(" Hi! You should probably override update() in your subclass of Voice !!!!");
    }
*/

    public void tweakCtrl(int ctrl,int val) {
        System.out.println(" Hi! You should probably override update() in your subclass of Voice !!!!");
    }

    /**
     * if you have really finished with this voice.
     * should release all resources
     */
    public void kill() {
        if (killed) return;
        allocate(false);
      //  System.out.println(" Killing " + getName());
        killed = true;
        setSilent();


        //@TODO Kill the voice
    }


    /**
     * concrete class must provide a method to play the effect at the given time
     * @param effect Effect
     * @param tickOn int
     */
    abstract public void play(Effect effect, long tick,Conductor c) ;
    public boolean isAlive() {
        return!killed;
    }

    abstract public boolean isMelodic();
    abstract public Conductor getConductor();

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }



    public String getType() {
        return "Melodic";
    }

    public abstract void setSilent();

/*
    public long getId() {     return id;    }

     public void setId(long id) {
         this.id = id;
     }



     static String[] types = {"TEXT", "BLOB"};
     static String[] keys = {"className", "binData"};

     static public final TableInfoData tableInfo = new TableInfoData(types, keys,
             "VoiceTABLE",true);


     public BinaryData  getBinaryData() {
         return new BinaryData(getData());
   }

    public String[] getValues() {
        String[] r = { "\""+getClass().getName()+"\"", "\""+getData()+"\"" };
        return r;
    }

    public String getData() { return "\""+name +"\" \""+ bankName + "\" \""+ synthName + "\"  " ; }

*/


     abstract public void allocate(boolean yes);

     public abstract long getId();

}
