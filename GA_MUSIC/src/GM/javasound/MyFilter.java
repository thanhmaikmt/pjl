package GM.javasound;

import javax.sound.midi.*;
import java.util.*;

/**
 * <p>Title: </p>
 *
 * <p>Description: </p>
 *
 * <p>Copyright: Copyright (c) 2005</p>
 *
 * <p>Company: </p>
 *
 * @author not attributable
 * @version 1.0
 */
public class MyFilter implements MidiDevice {


    List<Transmitter> trans=new Vector();
    List<Receiver> recvs=new Vector();

    class MyDeviceInfo extends MidiDevice.Info {
        MyDeviceInfo() {
            super("MyFilt", "DrPJ", "Whatever", "0.1a");
        }
    }

    boolean isOpen;

    class Rec implements Receiver {



        public void close() {
            recvs.remove(this);

        }

        byte filtMe=(byte)0xFE;

        public void send(MidiMessage mess,long timeStamp) {
            byte a[] = mess.getMessage();
            StringBuffer buff=new StringBuffer(" MESS: ");

              if (a[0] != filtMe) {
                  for (byte b:a) buff.append(String.format("%2X |",b));

                  System.out.println(buff + " @ " + timeStamp);
                  for (Transmitter t : trans)
                      ((Trans) t).recv.send(mess, -1);
              }
          }

    }

    class Trans implements Transmitter {

        Receiver recv;

        public void close() {
            trans.remove(this);
            if (recv !=null) recv.close();
            recv=null;
        }


        public Receiver getReceiver() {
            return recv;
        }

        public void setReceiver(Receiver recv) {
            this.recv = recv;
        }
    }

    public MyFilter() {

    }

    public long getMicrosecondPosition() {
        return -1;
    }
    public List<Transmitter> getTransmitters() { return trans; }
    public List<Receiver> getReceivers() { return recvs; }



    public void close(){}


    public Transmitter getTransmitter() {
        Trans t=new Trans();
        trans.add(t);
        return t;
    }

    public Receiver getReceiver() {
         Rec r=new Rec();
         recvs.add(r);
         return r;
     }


    public int getMaxTransmitters() { return -1; }
    public int getMaxReceivers() { return -1; }

    public MidiDevice.Info getDeviceInfo() {
        return new MyDeviceInfo();
    }




    public void open() {
        isOpen=true;
    }

    public boolean isOpen() {
        return isOpen;
    }


}
