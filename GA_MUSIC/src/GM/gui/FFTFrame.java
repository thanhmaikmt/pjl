package GM.gui;
import javax.swing.*;
import java.awt.Container;
import GM.audio.*;
import GM.javasound.JavaSoundHub;
import java.io.*;


public class FFTFrame extends JFrame {
    public FFTFrame() {
        Container c= getContentPane();
        try {
            Spectrogram spect;
            FFTAnalyst fft=FFTAnalyst.the();
            c.add(spect = new Spectrogram(500,
                                  fft.size()));
            fft.addObserver(spect);

        } catch (IOException ex) {
            ex.printStackTrace();
        }

    }
};
