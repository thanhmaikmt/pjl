/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package uk.co.drpj.audio;


/*
 * Created on May 31, 2007
 *
 * Copyright (c) 2006-2007 P.J.Leonard
 *
 * http://www.frinika.com
 *
 * This file is part of Frinika.
 *
 * Frinika is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.

 * Frinika is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.

 * You should have received a copy of the GNU General Public License
 * along with Frinika; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */
import java.io.BufferedInputStream;
import java.io.DataInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.RandomAccessFile;

import java.net.URL;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.sound.sampled.AudioFormat;
import uk.org.toot.audio.core.AudioBuffer;
import uk.org.toot.audio.core.AudioProcess;

public class URLWavReader implements AudioProcess {

    protected static String sp = "     ";
    static String indent = sp + "     ";
    protected int bytecount = 0;
    protected int riffdata = 0;
    protected AudioFormat format;
    protected int nChannels;
    private byte[] byteBuff;
    private DataInputStream dis;
    private boolean eof=false;

    public URLWavReader(URL url) throws IOException {
        String sfield = "";

        InputStream is = url.openStream();
        dis = new DataInputStream(new BufferedInputStream(is));


        readChunkHeader(dis);   // 12 bytes



        while (bytecount < riffdata) { // check for chunks inside RIFF data
            // area.
            sfield = "";
            for (int i = 1; i <= 4; i++) {
                sfield += (char) dis.readByte();
            }

            int chunkSize = 0;
            for (int i = 0; i < 4; i++) {
                chunkSize += dis.readUnsignedByte() * (int) Math.pow(256, i);
            }

            if (sfield.equals("data")) {
                return;
            }

            bytecount += (8 + chunkSize);

            if (sfield.equals("fmt ")) { // extract info from "format"
                readFormat(dis, chunkSize);
            } else // if NOT the fmt chunk.
            {
                dis.skipBytes(chunkSize);
            }

        } 

    }

    // reads 12 bytes
    protected void readChunkHeader(DataInputStream fis) throws IOException {
        String sfield = "";

        int chunkSize = 0;

        /* -------- Get RIFF chunk header --------- */
        for (int i = 1; i <= 4; i++) {
            sfield += (char) fis.readByte();
        }
        if (!sfield.equals("RIFF")) {
            System.out.println(" ****  Not a valid RIFF file  ****");
            return;
        }

        for (int i = 0; i < 4; i++) {
            chunkSize += fis.readUnsignedByte() * (int) Math.pow(256, i);
        }
        sfield = "";
        for (int i = 1; i <= 4; i++) {
            sfield += (char) fis.readByte();
        }
        // S ystem.out.println(sp + " ----- form type: " + sfield + "\n");

        riffdata = chunkSize;
        /* --------------------------------------------- */

        bytecount = 4; // initialize bytecount to include RIFF form-type
        // bytes.

    }

//	public int getLengthInFrames() {
//		return lengthInFrames;
//	}
    protected void readFormat(DataInputStream fis, int chunkSize)
            throws IOException {
        // chunk.

        if (chunkSize < 16) {
            System.out.println(" ****  Not a valid fmt chunk  ****");
            return;
        }
        int wFormatTag = fis.readUnsignedByte();
        fis.skipBytes(1);
        // if (wFormatTag == 1)
        // System. out.println(indent + "wFormatTag: MS PCM format");
        // else
        // System. out.println(indent + "wFormatTag: non-PCM format");
        nChannels = fis.readUnsignedByte();
        fis.skipBytes(1);
        System.out.println("nChannels: " + nChannels);
        int nSamplesPerSec = 0;
        for (int i = 0; i < 4; i++) {
            nSamplesPerSec += fis.readUnsignedByte() * (int) Math.pow(256, i);
        }
        // System.out.println(indent + "nSamplesPerSec: " + nSamplesPerSec);
        int nAvgBytesPerSec = 0;
        for (int i = 0; i < 4; i++) {
            nAvgBytesPerSec += fis.readUnsignedByte() * (int) Math.pow(256, i);
        }
        // System.out.println(indent + "nAvgBytesPerSec: " + nAvgBytesPerSec);
        int nBlockAlign = 0;
        for (int i = 0; i < 2; i++) {
            nBlockAlign += fis.readUnsignedByte() * (int) Math.pow(256, i);
        }
        // System.out.println(indent + "nBlockAlign: " + nBlockAlign);
        int nBitsPerSample = 0;
        if (wFormatTag == 1) { // if MS PCM format
            nBitsPerSample = fis.readUnsignedByte();
            fis.skipBytes(1);
            // System.out.println(indent + "nBitsPerSample: " + nBitsPerSample);
        } else {
            fis.skipBytes(2);
        }
        fis.skipBytes(chunkSize - 16); // skip over any extra bytes
        // in format specific field.

        // Assume 16 bit signed little endian.
        format = new AudioFormat(nSamplesPerSec, nBitsPerSample, nChannels,
                true, false);
    }

    public AudioFormat getFormat() {
        return format;
    }

    public int getChannels() {
        return nChannels;
    }

    /**
     *
     *
     * Read from file into byte buffer and advance the fPtrBytes pointer it is
     * OK to read before/after start/end of the file you'll just get zeros.
     * fPtrBytes is advanced by appropriate byte count.
     *
     * @param byteBuffer
     *            buffer to fill
     * @param offSet
     *            offset into byteBuffer
     * @param n
     *            number of bytes to be read
     * @throws IOException
     */
    public int processAudio(AudioBuffer buffer) {

        if (eof) {
            return AudioProcess.AUDIO_DISCONNECT;
        }

        int nBytes = nChannels * 2 * buffer.getSampleCount();

        //  boolean realTime = buffer.isRealTime();

        if (byteBuff == null || byteBuff.length != nBytes) {
            byteBuff = new byte[nBytes];
        }

        try {
            // portion of
            dis.readFully(byteBuff);
        } catch (IOException ex) {
            eof=true;
            
//            Logger.getLogger(URLWavReader.class.getName()).log(Level.SEVERE, null, ex);
        }

        processAudioImp(buffer, 0, nBytes);



        return AUDIO_OK;

    }

    protected void processAudioImp(AudioBuffer buffer, int startChunk,
            int endChunk) {
        fill(buffer, startChunk, endChunk);
    }

    /**
     *
     *
     * @param buffer
     * @param startChunk
     * @param endChunk
     * @param gain1
     * @param gain2
     */
    protected void fillLinearInterpolate(AudioBuffer buffer, int startChunk,
            int endChunk, double gain1, double gain2) {

        double dG = (gain2 - gain1) / (endChunk - startChunk) / nChannels / 2.0;
        if (nChannels == 2) {
            float[] left = buffer.getChannel(0);

            float[] right = buffer.getChannel(1);
            for (int n = startChunk / 2; n < endChunk / 2; n++) {
                float sample = ((short) ((0xff & byteBuff[(n * 2) + 0]) + ((0xff & byteBuff[(n * 2) + 1]) * 256)) / 32768f);
                sample *= gain1;
                if (n % 2 == 0) {
                    left[n / 2] += sample;
                } else {
                    right[n / 2] += sample;
                }
                gain1 += dG;
            }
        } else {
            float[] left = buffer.getChannel(0);

            for (int n = startChunk; n < endChunk; n += 2) {
                float val = ((short) ((0xff & byteBuff[n]) + ((0xff & byteBuff[n + 1]) * 256)) / 32768f);
                left[n / 2] += val * gain1;
                gain1 += dG;
            }
        }
    }

    protected void fillConstantGain(AudioBuffer buffer, int startChunk,
            int endChunk, double gain) {
        if (nChannels == 2) {
            float[] left = buffer.getChannel(0);

            float[] right = buffer.getChannel(1);
            for (int n = startChunk / 2; n < endChunk / 2; n++) {
                float sample = ((short) ((0xff & byteBuff[(n * 2) + 0]) + ((0xff & byteBuff[(n * 2) + 1]) * 256)) / 32768f);
                sample *= gain;
                if (n % 2 == 0) {
                    left[n / 2] += sample;
                } else {
                    right[n / 2] += sample;
                }
            }
        } else {
            float[] left = buffer.getChannel(0);

            for (int n = startChunk; n < endChunk; n += 2) {
                float val = ((short) ((0xff & byteBuff[n]) + ((0xff & byteBuff[n + 1]) * 256)) / 32768f);
                left[n / 2] += val * gain;
            }
        }
    }

    protected void fill(AudioBuffer buffer, int startChunk, int endChunk) {
        if (nChannels == 2) {
            float[] left = buffer.getChannel(0);

            float[] right = buffer.getChannel(1);
            for (int n = startChunk / 2; n < endChunk / 2; n++) {
                float sample = ((short) ((0xff & byteBuff[(n * 2) + 0]) + ((0xff & byteBuff[(n * 2) + 1]) * 256)) / 32768f);
                if (n % 2 == 0) {
                    left[n / 2] += sample;
                } else {
                    right[n / 2] += sample;
                }
            }
        } else {
            float[] left = buffer.getChannel(0);

            for (int n = startChunk; n < endChunk; n += 2) {
                float val = ((short) ((0xff & byteBuff[n]) + ((0xff & byteBuff[n + 1]) * 256)) / 32768f);
                left[n / 2] += val;
            }
        }
    }

    public void open() throws Exception {
//        throw new UnsupportedOperationException("Not supported yet.");
    }

    public void close() throws Exception {
  //      throw new UnsupportedOperationException("Not supported yet.");
    }
}
