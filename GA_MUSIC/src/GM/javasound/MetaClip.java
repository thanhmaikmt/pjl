package GM.javasound;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import javax.sound.sampled.*;
import javax.sound.midi.*;
import com.sun.media.sound.DataPusher;

public class MetaClip implements MetaEventListener {
    private int sampleSizeInBits = 16;
    private float sampleRate = 44100;
    private int nBufferSize = 4096*4;
    private boolean bBigEndian = false;


    public MetaClip() {

    }

    public MetaClip(int bits, float rate, float
                    bufferMilliseconds) {
        sampleSizeInBits = bits;
        sampleRate = rate;
        nBufferSize = (int) (sampleRate * sizeInBytes() *
                             bufferMilliseconds / 1000);
    }

    private int sizeInBytes() {
        return (int) ((sampleSizeInBits + 7) / 8);
    }

    static long ref;
    public void meta(MetaMessage msg) {
        if (msg.getType() != 127 ) return;
        byte[] data = msg.getData(); // all data after META
        long t=System.nanoTime();

        System.out.println(0.5-(t-ref)/1e9);
        ref=t;
        //  System.out.println(" HELLO FROM META ");
        String sampleName = new String(data);
        play(getFileForSample(sampleName));

    }

    protected File getFileForSample(String sampleName) {
        return new File("/home/pjl/jbproject/GM/samples/", sampleName + ".wav");
    }

    public void play(File file) {
        try {
            AudioInputStream audioInputStream =
                    AudioSystem.getAudioInputStream(file);
            AudioFormat sourceFormat = audioInputStream.getFormat();
            // our audioformat has the resolution and sample rate of the hardware
            // but otherwise matches the sourceFormat
            AudioFormat targetFormat =
                    new AudioFormat(
                            AudioFormat.Encoding.PCM_SIGNED,
                            sampleRate,
                            sampleSizeInBits,
                            sourceFormat.getChannels(),
                            sourceFormat.getChannels() * sizeInBytes(),
                            sampleRate,
                            bBigEndian);
            SourceDataLine line = getSourceDataLine(targetFormat,
                    nBufferSize);
            DataPusher player = new DataPusher(line, audioInputStream);
            player.start();
        } catch (UnsupportedAudioFileException uafe) {
            uafe.printStackTrace();
        } catch (IOException ioe) {
            ioe.printStackTrace();
        }
    }

    protected SourceDataLine getSourceDataLine(AudioFormat audioFormat,
                                               int nBufferSize) {
        SourceDataLine line = null;
        DataLine.Info info = new DataLine.Info(SourceDataLine.class,
                                               audioFormat, nBufferSize);
        try {
            line = (SourceDataLine) AudioSystem.getLine(info);
            line.open(audioFormat, nBufferSize);
        } catch (LineUnavailableException lue) {
            lue.printStackTrace();
        }
        return line;
    }
}
