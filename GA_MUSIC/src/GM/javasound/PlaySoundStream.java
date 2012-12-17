// Example 17-4. PlaySoundStream.java

package GM.javasound;

import GM.jsyn.*;
import javax.sound.sampled.*;


/**
 * This class plays sounds streaming from a URL: it does not have to preload
 * the entire sound into memory before playing it. It is a command-line
 * application with no gui. It includes code to convert ULAW and ALAW
 * audio formats to PCM so they can be played. Use the -m command-line option
 * before MIDI files.
 */
public class PlaySoundStream extends Thread {


    boolean dummy = false;
    JsynMixer mixer;
    /** Read sampled audio data from the specified URL and play it */


    public PlaySoundStream(JsynMixer mixer) {
        this.mixer = mixer;
    }

    public void run() {
//
        SourceDataLine line = null; // And write it here.
        int maxFrames = mixer.getMaxFramesPerRead();
        int nChannel = mixer.getNChannel();
        int bytesPerFrame = mixer.getFrameSizeInBytes();

        int bufSize = maxFrames * 16 * bytesPerFrame;

        try {
            // Get an audio input stream from the URL
            //          ain = AudioSystem.getAudioInputStream(url);

            // Get information about the format of the stream
            //        AudioFormat format = ain.getFormat();

            AudioFormat pcm =
                    new AudioFormat(44100, 16, 2, true, false);

            DataLine.Info info = new DataLine.Info(SourceDataLine.class, pcm,
                    bufSize);

            // Open the line through which we'll play the streaming audio.
            line = (SourceDataLine) AudioSystem.getLine(info);

            line.open(pcm);

            // Allocate a buffer for reading from the input stream and writing
            // to the line.  Make it large enough to hold 4k audio frames.
            // Note that the SourceDataLine also has its own internal buffer.
            int framesize = line.getBufferSize();
          //  System.out.println(framesize + "frameSize");



            short[] sbuff = new short[maxFrames * nChannel];

            byte[] buffer = new byte[maxFrames * nChannel * 2];


            // We haven't started the line yet.
            boolean started = false;

            for (; ; ) { // We'll exit the loop when we reach the end of stream

                int nread = mixer.read(sbuff, 0, maxFrames);
                assert (nread == maxFrames);

                int nShort = maxFrames * bytesPerFrame / 2;
                for (int i = 0; i < nShort; i++) {
                    buffer[2 * i] = (byte) (sbuff[i] & 0xff);
                    buffer[2 * i + 1] = (byte) ((sbuff[i] & 0xff00) >> 8);
                }

                int bytesread = nShort * 2;
                // If there were no more bytes to read, we're done.
                if (bytesread == -1) {
                    break;
                }

                // Now that we've got some audio data to write to the line,
                // start the line, so it will play that data as we write it.
                if (!started) {
                    line.start();
                    started = true;
                }

                // Now write the bytes. The line will buffer them and play
                // them. This call will block until all bytes are written.
                // System.out.println(" Writting "+bytestowrite+" bytes");


               int n= line.write(buffer, 0, bytesread);
               assert(n == bytesread);

                // If we didn't have an integer multiple of the frame size,
                // then copy the remaining bytes to the start of the buffer.
            }

            // Now block until all buffered sound finishes playing.
            line.drain();
            if (line != null) {
                line.close();
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
