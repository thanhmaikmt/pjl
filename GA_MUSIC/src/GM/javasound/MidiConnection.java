package GM.javasound;


import java.util.Vector;
import javax.sound.midi.Transmitter;
import javax.sound.midi.Receiver;
import javax.sound.midi.MidiUnavailableException;
import java.util.*;



class MidiConnection {
    static Vector<MidiConnection> connections= new Vector<MidiConnection>();


    public MidiHub.DeviceHandle transDev;
    Transmitter trans;
    public MidiHub.DeviceHandle recvDev;
    Receiver recv;
    boolean connected=false;


     MidiConnection(MidiHub.DeviceHandle transDev,MidiHub.DeviceHandle recvDev) {
         assert(recvDev.dev.getMaxReceivers() != 0);
         assert(transDev.dev.getMaxTransmitters() != 0);
         this.transDev = transDev;
         this.recvDev = recvDev;
         synchronized(connections) {
             connections.add(this);
         }
     }

     public void connect() {


//         info(" before connect ");

         if (connected) return;

         try {
             if (!recvDev.dev.isOpen()) recvDev.dev.open();
             recv = recvDev.dev.getReceiver();
             if (!transDev.dev.isOpen()) transDev.dev.open();
             trans= transDev.dev.getTransmitter();
             trans.setReceiver(recv);
             connected = true;
         } catch (MidiUnavailableException ex) {
             ex.printStackTrace();
         }

  //       info(" after connect ");

    }


    public void disconnect() {

        if (!connected) return;
        info(" before disconnect ");
        trans.setReceiver(null);
        trans.close();
        recv.close();
        info(" after disconnect ");
        connected=false;
    }

    static void remove(MidiConnection con) {
        con.disconnect();
        synchronized(connections){
            connections.remove(con);
        }
    }

    public void info(String str) {

        System.out.println(str);
        List<Transmitter> tl = transDev.dev.getTransmitters();
        List<Receiver> rl = recvDev.dev.getReceivers();

        System.out.println(transDev.dev.getDeviceInfo().getName() + "  used =" + tl.size());
        System.out.println(recvDev.dev.getDeviceInfo().getName() + "  used =" + rl.size());

   }


}

