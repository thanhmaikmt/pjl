package GM.javasound;

import javax.sound.midi.MidiDevice;
import javax.sound.midi.MidiDevice.Info;
import javax.sound.midi.spi.MidiDeviceProvider;

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
public class GMMidiDeviceProvider extends MidiDeviceProvider {



    static MyFilter filt = new MyFilter();

    public GMMidiDeviceProvider() {
    }

    /**
     * Obtains an instance of the device represented by the info object.
     *
     * @param info an info object that describes the desired device
     * @return device instance
     * @todo Implement this javax.sound.midi.spi.MidiDeviceProvider method
     */
    public MidiDevice getDevice(Info info) {
        return new MyFilter();
    }

    /**
     * Obtains the set of info objects representing the device or devices
     * provided by this <code>MidiDeviceProvider</code>.
     *
     * @return set of device info objects
     * @todo Implement this javax.sound.midi.spi.MidiDeviceProvider method
     */
    public Info[] getDeviceInfo() {
        Info [] ret= {filt.getDeviceInfo()};
        return ret;
    }
}
