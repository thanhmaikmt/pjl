package uk.co.drpj.psycho.experiment;

import java.awt.BorderLayout;
import java.awt.Component;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Random;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextArea;

public abstract class ThreeChoiceExperiment {

	protected FiniteAudioProcess audioProcess;

	private final JPanel panel = new JPanel();

	protected final JButton startStop = new JButton("start");

	protected final JButton guess[] = new JButton[4];

	protected JLabel feedback;

	protected boolean isRunning = false;

	protected int idiff;

	protected final Random random = new Random();

	JTextArea instructions;

	JLabel results = new JLabel();
	protected MyAudioClient client;

	public ThreeChoiceExperiment(final MyAudioClient client) {
	

		this.client = client;

		panel.add(startStop);

		startStop.addActionListener(new ActionListener() {

			public void actionPerformed(ActionEvent e) {
				if (!isRunning) {
					isRunning = true;
					startStop.setText("Stop");
					playAudio();
				} else {
					isRunning = false;
					startStop.setText("Start");
				}

			}
		});
		instructions = new JTextArea(
				"  Press start "
						+ " to hear 3 sounds \n"
						+ " tPress the button corrresponding to the sound you think is different");

		feedback = new JLabel(" wait for the clicks ");

		// panel.add(instructions);
		// panel.add(play);

		for (int i = 0; i < 4; i++) {
			if (i < 3)
				guess[i] = new JButton("" + (i + 1));
			else
				guess[i] = new JButton("pass");

			final double fs = client.getSampleRate();
			guess[i].addActionListener(new MyListener(i));
			guess[i].setEnabled(false);
			panel.add(guess[i]);
		}

		panel.add(feedback);
		panel.add(results);
		setResults();

	}

	protected Component threeChoicePanel() {
		// TODO Auto-generated method stub
		return panel;
	}

	abstract protected void setResults();
	
        abstract protected void fire(boolean key);

	abstract protected void correctResultAction(int guess);

	abstract protected void incorrectResultAction(int guess, int real);

	abstract protected void passAction(int real);
        
        
        protected void setResultText(String message) {
           results.setText(message); 
        }
	class MyListener implements ActionListener {
		int key;

		MyListener(int key) {
			this.key = key;
		}

		public void actionPerformed(ActionEvent e) {

			if (key == idiff) {
				correctResultAction(key); // tolNow = (1.0 - damp) * tolNow;
				feedback.setText(" Correct !!");
			} else if (key == 3) {
				passAction(idiff + 1);
				feedback.setText(" it was " + (idiff + 1));
			} else {
				incorrectResultAction(key, idiff + 1);
				feedback.setText(" wrong " + (idiff + 1));
			}
			setResults();
			if (isRunning)
				playAudio();
		}

	}


	
	protected void playAudio() {
		Thread t = new Thread(new Runnable() {

			public void run() {

				for (int i = 0; i < 4; i++) {
					guess[i].setEnabled(false);
				}
			
				idiff = random.nextInt(3);
				
				for (int i = 0; i < 3; i++) {
				
					fire(idiff == i);
					audioProcess.waitTillDone();
					
					try {
						Thread.sleep(200);
					} catch (InterruptedException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
				}

				for (int i = 0; i < 4; i++)
					guess[i].setEnabled(true);
			}

		});
		
		t.start();

	}


	public abstract JPanel getGUIPanel();
	
}
