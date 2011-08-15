/*
 * Created on Mar 6, 2007
 *
 * Copyright (c) 2006 P.J.Leonard
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

package uk.co.drpj.psycho.experiment;

import java.awt.BorderLayout;
import java.awt.Component;
import java.awt.Container;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Observable;
import java.util.Observer;
import java.util.Vector;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextArea;
import javax.swing.Spring;
import javax.swing.SpringLayout;


import uk.ac.bath.gui.SpinTweaker;
import uk.ac.bath.gui.SpinTweakerPanel;
import uk.ac.bath.gui.TweakerPanel;
import uk.ac.bath.util.Tweakable;
import uk.ac.bath.util.TweakableDouble;
import uk.org.toot.audio.core.AudioBuffer;


public class LowFreqQExperiment extends ThreeChoiceExperiment {

//	LowFreqQProcess ping;

	final double fs;

	JPanel panel = new JPanel();
	
	Vector<Tweakable> tweaks=new Vector<Tweakable>();
	final TweakableDouble dur    = new TweakableDouble(tweaks,50 , 1000, 500, 1, " length [mS]");
	final TweakableDouble period = new TweakableDouble(tweaks,0 , 200, 50, 1, " period [mS]");
	final TweakableDouble pulselen    = new TweakableDouble(tweaks,0, 200, 10, 1, " pulse length [mS]");
	final TweakableDouble amp    = new TweakableDouble(tweaks,0.0, 1.0, 1.0, .1, "Amp");

	// private double tolHigh=0.2;
	double tolNow = 0.1;

	// private double tolLow=0.0;
	private double damp = 0.2;

	public LowFreqQExperiment(final MyAudioClient client) {
		super(client);

	
//		JFrame frame = new JFrame();
//		frame.setLocationRelativeTo(null);
//		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
//
//		SpringLayout layout=new SpringLayout();
		
	
	
		JPanel tw=makeTweakPanel(tweaks);
		audioProcess = new LowFreqQProcess(client);

		pulselen.addObserver(new Observer() {
			public void update(Observable arg0, Object arg1) {
				((LowFreqQProcess)audioProcess).makePulse(pulselen.doubleValue());
						}		
		});
		
		((LowFreqQProcess)audioProcess).makePulse(pulselen.doubleValue());
		
		
		JPanel cntrlPanel = new JPanel();

		cntrlPanel.setLayout(new BorderLayout());
		cntrlPanel.add(tw, BorderLayout.NORTH);
		this.fs = client.getSampleRate();

		client.addInput(audioProcess);

		panel.add(threeChoicePanel(), BorderLayout.SOUTH);
		panel.add(cntrlPanel);
//		frame.setContentPane(panel);
//		frame.pack();
//		frame.setVisible(true);
		try {
			Thread.sleep(1000);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	private JPanel makeTweakPanel(Vector<Tweakable> tweaks) {
		JPanel panel=new JPanel(new SpringLayout());
		int n=tweaks.size();
	
		for(Tweakable t:tweaks) {
			SpinTweaker spin=new SpinTweaker(t);
			JLabel label=new JLabel(t.getLabel());
			panel.add(label);
			panel.add(spin);
		}
		SpringUtilities.makeCompactGrid(panel,2,n,2,2,2,2);
		return panel;
	}

	protected void setResults() {
		results.setText(String.format(" Acrruracy estimate %4.3f%%  ",
				tolNow * 100));
	}

	
	
	
	protected void fire(boolean key) {
		double periodMs=period.doubleValue();			
		int nPulse= (int) (dur.doubleValue()/periodMs);
		((LowFreqQProcess)audioProcess).fire(periodMs, nPulse, key);
	}
	/**
	 * decrease tolerance if we guess correctly.
	 * 
	 */
	@Override
	protected void correctResultAction(int guess) {
	//
	}

	@Override
	protected void incorrectResultAction(int guess, int real) {
	}

	@Override
	protected void passAction(int real) {
	}

	@Override
	public JPanel getGUIPanel() {
		return panel;
	}

}

/**
 * A 1.4 file that provides utility methods for
 * creating form- or grid-style layouts with SpringLayout.
 * These utilities are used by several programs, such as
 * SpringBox and SpringCompactGrid.
 */
class SpringUtilities {
    /**
     * A debugging utility that prints to stdout the component's
     * minimum, preferred, and maximum sizes.
     */
    public static void printSizes(Component c) {
        System.out.println("minimumSize = " + c.getMinimumSize());
        System.out.println("preferredSize = " + c.getPreferredSize());
        System.out.println("maximumSize = " + c.getMaximumSize());
    }

    /**
     * Aligns the first <code>rows</code> * <code>cols</code>
     * components of <code>parent</code> in
     * a grid. Each component is as big as the maximum
     * preferred width and height of the components.
     * The parent is made just big enough to fit them all.
     *
     * @param rows number of rows
     * @param cols number of columns
     * @param initialX x location to start the grid at
     * @param initialY y location to start the grid at
     * @param xPad x padding between cells
     * @param yPad y padding between cells
     */
    public static void makeGrid(Container parent,
                                int rows, int cols,
                                int initialX, int initialY,
                                int xPad, int yPad) {
        SpringLayout layout;
        try {
            layout = (SpringLayout)parent.getLayout();
        } catch (ClassCastException exc) {
            System.err.println("The first argument to makeGrid must use SpringLayout.");
            return;
        }

        Spring xPadSpring = Spring.constant(xPad);
        Spring yPadSpring = Spring.constant(yPad);
        Spring initialXSpring = Spring.constant(initialX);
        Spring initialYSpring = Spring.constant(initialY);
        int max = rows * cols;

        //Calculate Springs that are the max of the width/height so that all
        //cells have the same size.
        Spring maxWidthSpring = layout.getConstraints(parent.getComponent(0)).
                                    getWidth();
        Spring maxHeightSpring = layout.getConstraints(parent.getComponent(0)).
                                    getWidth();
        for (int i = 1; i < max; i++) {
            SpringLayout.Constraints cons = layout.getConstraints(
                                            parent.getComponent(i));

            maxWidthSpring = Spring.max(maxWidthSpring, cons.getWidth());
            maxHeightSpring = Spring.max(maxHeightSpring, cons.getHeight());
        }

        //Apply the new width/height Spring. This forces all the
        //components to have the same size.
        for (int i = 0; i < max; i++) {
            SpringLayout.Constraints cons = layout.getConstraints(
                                            parent.getComponent(i));

            cons.setWidth(maxWidthSpring);
            cons.setHeight(maxHeightSpring);
        }

        //Then adjust the x/y constraints of all the cells so that they
        //are aligned in a grid.
        SpringLayout.Constraints lastCons = null;
        SpringLayout.Constraints lastRowCons = null;
        for (int i = 0; i < max; i++) {
            SpringLayout.Constraints cons = layout.getConstraints(
                                                 parent.getComponent(i));
            if (i % cols == 0) { //start of new row
                lastRowCons = lastCons;
                cons.setX(initialXSpring);
            } else { //x position depends on previous component
                cons.setX(Spring.sum(lastCons.getConstraint(SpringLayout.EAST),
                                     xPadSpring));
            }

            if (i / cols == 0) { //first row
                cons.setY(initialYSpring);
            } else { //y position depends on previous row
                cons.setY(Spring.sum(lastRowCons.getConstraint(SpringLayout.SOUTH),
                                     yPadSpring));
            }
            lastCons = cons;
        }

        //Set the parent's size.
        SpringLayout.Constraints pCons = layout.getConstraints(parent);
        pCons.setConstraint(SpringLayout.SOUTH,
                            Spring.sum(
                                Spring.constant(yPad),
                                lastCons.getConstraint(SpringLayout.SOUTH)));
        pCons.setConstraint(SpringLayout.EAST,
                            Spring.sum(
                                Spring.constant(xPad),
                                lastCons.getConstraint(SpringLayout.EAST)));
    }

    /* Used by makeCompactGrid. */
    private static SpringLayout.Constraints getConstraintsForCell(
                                                int row, int col,
                                                Container parent,
                                                int cols) {
        SpringLayout layout = (SpringLayout) parent.getLayout();
        Component c = parent.getComponent(row * cols + col);
        return layout.getConstraints(c);
    }

    /**
     * Aligns the first <code>rows</code> * <code>cols</code>
     * components of <code>parent</code> in
     * a grid. Each component in a column is as wide as the maximum
     * preferred width of the components in that column;
     * height is similarly determined for each row.
     * The parent is made just big enough to fit them all.
     *
     * @param rows number of rows
     * @param cols number of columns
     * @param initialX x location to start the grid at
     * @param initialY y location to start the grid at
     * @param xPad x padding between cells
     * @param yPad y padding between cells
     */
    public static void makeCompactGrid(Container parent,
                                       int rows, int cols,
                                       int initialX, int initialY,
                                       int xPad, int yPad) {
        SpringLayout layout;
        try {
            layout = (SpringLayout)parent.getLayout();
        } catch (ClassCastException exc) {
            System.err.println("The first argument to makeCompactGrid must use SpringLayout.");
            return;
        }

        //Align all cells in each column and make them the same width.
        Spring x = Spring.constant(initialX);
        for (int c = 0; c < cols; c++) {
            Spring width = Spring.constant(0);
            for (int r = 0; r < rows; r++) {
                width = Spring.max(width,
                                   getConstraintsForCell(r, c, parent, cols).
                                       getWidth());
            }
            for (int r = 0; r < rows; r++) {
                SpringLayout.Constraints constraints =
                        getConstraintsForCell(r, c, parent, cols);
                constraints.setX(x);
                constraints.setWidth(width);
            }
            x = Spring.sum(x, Spring.sum(width, Spring.constant(xPad)));
        }

        //Align all cells in each row and make them the same height.
        Spring y = Spring.constant(initialY);
        for (int r = 0; r < rows; r++) {
            Spring height = Spring.constant(0);
            for (int c = 0; c < cols; c++) {
                height = Spring.max(height,
                                    getConstraintsForCell(r, c, parent, cols).
                                        getHeight());
            }
            for (int c = 0; c < cols; c++) {
                SpringLayout.Constraints constraints =
                        getConstraintsForCell(r, c, parent, cols);
                constraints.setY(y);
                constraints.setHeight(height);
            }
            y = Spring.sum(y, Spring.sum(height, Spring.constant(yPad)));
        }

        //Set the parent's size.
        SpringLayout.Constraints pCons = layout.getConstraints(parent);
        pCons.setConstraint(SpringLayout.SOUTH, y);
        pCons.setConstraint(SpringLayout.EAST, x);
    }
}

class LowFreqQProcess extends FiniteAudioProcess {

	private double amp;

	private MyAudioClient sync;

	private boolean isDone = true;
	private int pulseSize;
	private float[] pulse;
	private int pulseSamplePtr;

	private long period;

	

	private int pulsePtr;
	private int nPulse;

	private int ssign;
	private boolean sign;


	
	LowFreqQProcess(MyAudioClient sync) {
		this.sync = sync;
	}

	public int processAudio(AudioBuffer buffer) {
		if (isDone)
			return AUDIO_OK;
		buffer.makeSilence();
		int n = buffer.getSampleCount();
	
		
		float buffL[] = buffer.getChannel(0);
		float buffR[] = buffer.getChannel(1);

				
		for (int i = 0 ; i < n; i++,pulseSamplePtr++) {
			if (pulseSamplePtr == period) {
				pulsePtr++;
				System.out.println(pulsePtr);
				if (pulsePtr == nPulse) {
					isDone=true;
					wakeUpSleepers();
					return AUDIO_OK;
				}
				pulseSamplePtr=0;
				if (sign) ssign = -ssign;
			}
			if (pulseSamplePtr < pulseSize) {
				buffL[i]=buffR[i] = ssign*pulse[pulseSamplePtr];
			//	System.out.println(buffL[i]);
			} 
		}
		return AUDIO_OK;

	}

	public void fire(double period,int nPulse,boolean sign) {
		System.out.println("fire");
		this.period=sync.milliToSamples(period);
		this.isDone = false;
		this.pulsePtr=0;
		this.nPulse=nPulse;
		this.ssign=1;
		this.sign=sign;
		this.pulseSamplePtr=0;
	//	this.armed=true;
	}

	
	public void makePulse(double pulseWidth) {
	
		pulseSize=(int) sync.milliToSamples(pulseWidth);
		System.out.println(" Size = " + pulseSize);
		pulse=new float[pulseSize];
		for (int i=0;i<pulseSize;i++) {
			double z=i/(double)(pulseSize-1);
			double w=Math.sin(Math.PI*z);
			pulse[i]=(float) (w*w);		
		}
	}
	
	
	public void open() {
		// TODO Auto-generated method stub

	}

	public void close() {
		// TODO Auto-generated method stub

	}

	public boolean isDone() {
		return isDone;
	}
	

}