package GM.music;

import java.util.*;

public class Message {
    public String str;
    public Object o = null;

    public Message(String str,Object o) {
        this.str=str;
        this.o=o;
    }
    public Message(String str) {
        this.str=str;
    }
    public String toString() {
        return str + " " + o;
    }

    public void unhandled(Observer ob,Observable o,Object arg) {
        System.out.println(str + " Unhandled message in " + ob.getClass().getName() + " " + o);

    }
    final static public Message MODIFIED= new Message("MODIFIED");
    final static public Message KILLED = new Message("KILLED");
    final static public Message CREATEGUI = new Message("CREATEGUI");
    final static public Message SOLO_OFF = new Message("SOLO_OFF");
    final static public Message SOLO_ON = new Message("SOLO_ON");
    final static public Message SELECT_CHANGE = new Message("SELECT_CHANGE");
    final static public Message SELECTION_CHANGE = new Message("SELECTION_CHANGE");
    final static public Message ENABLE = new Message("ENABLE");
    final static public Message DISABLE = new Message("DISABLE");
    final static public Message ADD_PLAYER = new Message("ADD_PLAYER");

}
