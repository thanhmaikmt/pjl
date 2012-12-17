package GM.javasound;


import javax.sound.midi.MidiDevice;
import javax.sound.midi.MidiDevice.Info;
import javax.sound.midi.MidiSystem;
import java.util.Vector;
import javax.sound.midi.MidiUnavailableException;
import javax.sound.midi.Synthesizer;
import javax.sound.midi.Sequencer;
import GM.gui.SimphoneyApp;
import GM.gui.SimphoneyApplet;

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
public class MidiHub {

    static DeviceHandle[] recvHandle;
    static DeviceHandle[] transHandle;


    static MidiDevice defaultMidiOut = null;
    static Sequencer sequencer = null;

    static {

        //    String defSynth = System.getProperty("javax.sound.midi.Synthesizer");

        System.out.println(" HI HI HI ");
        MidiDevice[] recvList;
        MidiDevice[] transList;
        Info info[] = MidiSystem.getMidiDeviceInfo();

        Vector<MidiDevice> recV = new Vector<MidiDevice>();
        Vector<MidiDevice> transV = new Vector<MidiDevice>();

        for (int i = 0; i < info.length; i++) {
         //   System.out.println("---------------------------------------------");
            MidiDevice dev = null;
            try {
                dev = MidiSystem.getMidiDevice(info[i]);
            } catch (MidiUnavailableException ex1) {
                ex1.printStackTrace();
            }

            Synthesizer synth = null;
            if (dev.getMaxReceivers() != 0) {
                recV.add(dev);
             //   System.out.println("#  " + dev.getDeviceInfo().getName());
                if (dev.getDeviceInfo().toString().equals(
                        "SW1000 #1 Synthesizer")) {
                    ;

                    defaultMidiOut = dev;
                }
            }
            if (dev instanceof javax.sound.midi.Synthesizer) {
                if (defaultMidiOut == null) {
                    defaultMidiOut = (Synthesizer) dev;
                }

            }

            if (dev.getMaxTransmitters() != 0) {
                transV.add(dev);
                if (dev instanceof javax.sound.midi.Sequencer) {
                    sequencer = (Sequencer) dev;
                }
            }
        }

        System.out.println("Synthesizer: " + defaultMidiOut);

        MyFilter filt= new MyFilter();
        recV.add(filt);
        recvList = new MidiDevice[recV.size()];
        recV.toArray(recvList);


        recvHandle = makeHandles(recvList);
        transV.add(filt);
        transList = new MidiDevice[transV.size()];
        transV.toArray(transList);

        transHandle = makeHandles(transList);

        System.out.println(" Trans devices ------------------------------ ");

        for (int i = 0; i < transList.length; i++) {
            System.out.println(transList[i].getDeviceInfo());

        }
        System.out.println(" Recv  devices ------------------------------- ");

        for (int i = 0; i < recvList.length; i++) {
            System.out.println(recvList[i].getDeviceInfo());
        }

        if( !SimphoneyApplet.isApplet) {
            Thread hook = new ExitHandler();
            Runtime.getRuntime().addShutdownHook(hook);
        }
    }


    static public DeviceHandle transHandleOf(MidiDevice dev) {
        for (DeviceHandle h : transHandle) {
            //  System.out.println(dev + "    " + h.dev);
            if (dev == h.dev) {
                return h;
            }
        }

        System.err.println(" Device not in list " + dev);
        return null;

    }

    static public DeviceHandle recvHandleOf(MidiDevice dev) {
        for (DeviceHandle h : recvHandle) {
            if (dev == h.dev) {
                return h;
            }
        }
        System.err.println(" Device not in  list " + dev);
        return null;

    }

    static DeviceHandle[] makeHandles(MidiDevice[] l) {
        DeviceHandle[] ret = new DeviceHandle[l.length + 1];
        ret[0] = new DeviceHandle(null);
        for (int i = 0; i < l.length; i++) {
            ret[i + 1] = new DeviceHandle(l[i]);
        }
        return ret;
    }

    static class DeviceHandle {
        MidiDevice dev;
        DeviceHandle(MidiDevice dev) {
            this.dev = dev;
        }

        public String toString() {
            if (dev == null) {
                return "NULL";
            }
            return dev.getDeviceInfo().toString() +
                    "|" + dev.getMaxReceivers() +
                    "|" + dev.getMaxTransmitters() +
                    "|" + dev.getReceivers().size() +
                    "|" + dev.getTransmitters().size();
        }
    }


    public static class ExitHandler extends Thread {
        public void run() {
            System.out.println(" Closing midi devices ");
            for (MidiConnection c : MidiConnection.connections) {
                c.disconnect();
            }
            for (DeviceHandle r : recvHandle) {
                if (r.dev != null) {
                    r.dev.close();
                }
            }
            for (DeviceHandle t : transHandle) {
                if (t.dev != null) {
                    t.dev.close();
                }
            }
        }
    }
}
