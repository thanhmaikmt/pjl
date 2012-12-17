package GM.gui;

//package uk.ac.bath.pjl.soundTest;


import java.awt.image.*;
import javax.swing.*;
import java.util.*;


import java.util.*;
import java.io.*;
import java.awt.*;

import javax.swing.*;


public class Spectrogram extends JPanel implements Observer  {

    int NBYTE=4;
    private MemoryImageSource  srcImage;
    private Image  image;
    private int w, h;
    private int   pixel[];
    int col=0;
    double vLast[];

    public Spectrogram(int w,int h) throws IOException  {
	setBackground(Color.black);
        this.w=w;
        this.h=h;

	resizeImage();
    }


    public Dimension getPreferredSize() {
        return new Dimension(w,h);
    }

    public Dimension getMinumumSize() {
        return getPreferredSize();
    }

    public Dimension getMaximumSize() {
        return getPreferredSize();
    }


    public void update(Observable o,Object args) {


        //     System.out.println("UPDATE");
     //   if(true) return;

     double[] v = (double[]) args;


     col = (col+1)%w;
   //  else System.arraycopy(pixel,1,pixel,0,pixel.length-1);



     for(int row=0;row<h;row++) {


            int red = (int)(Math.abs(v[row])*255);
            int blue= red;
            int  green =red;

            pixel[col + (h-row-1) * w] = (int) (
                    (blue) |
                    (red << 8) |
                    (green << 16) |
                    (0xffff << 24) );

        }
        newPixels();
        repaint();
    }




     void newPixels() {
         srcImage.newPixels();
         if (isShowing()) repaint();
     }



    public void paint(Graphics g) {
      //  System.out.println(" PAINT ");

      System.out.println(col);
	if ( pixel == null) return;

        if (col != w)
            g.drawImage(image,
                        0,  0, w-2-col,h-1 ,
                        col+1,0, w-1,h-1,          null);

        g.drawImage(image,
                    w-col-1, 0, w-1,h-1 ,
                    0,   0 ,col,h-1,
                    null);
	return;
    }





    private void resizeImage() {

	pixel = new int[w*h];
        vLast = new double[h];

	srcImage = new MemoryImageSource(w,h,pixel,0,w);

	// ANIM VERSION
 	srcImage.setAnimated(true);
	image  = createImage(srcImage);
	image.flush();
    }



}


