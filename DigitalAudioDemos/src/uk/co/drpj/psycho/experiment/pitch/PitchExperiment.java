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

package uk.co.drpj.psycho.experiment.pitch;

import uk.co.drpj.psycho.experiment.FiniteAudioProcess;
import uk.co.drpj.psycho.experiment.MyAudioClient;
import uk.co.drpj.psycho.experiment.ThreeChoiceExperiment;
import java.awt.BorderLayout;

import javax.swing.JPanel;


import uk.ac.bath.gui.TweakerPanel;
import uk.ac.bath.util.TweakableDouble;
import uk.org.toot.audio.core.AudioBuffer;

public class PitchExperiment extends ThreeChoiceExperiment {

	
	private JPanel panel = new JPanel();
	final double fs;

	final TweakableDouble freq = new TweakableDouble(10, 10000, 500, 5,
			"frequency");

	final TweakableDouble len10 = new TweakableDouble(-3, 1, -1, 0.1, "10**");

	final TweakableDouble amp = new TweakableDouble(0.0, 1.0, .5, .1, "Amp");

	// private double tolHigh=0.2;
	double tolNow = 0.1;

	// private double tolLow=0.0;
	private double damp = 0.2;

	public PitchExperiment(final MyAudioClient client) {
		super(client);



		TweakerPanel tw = new TweakerPanel(1, 3);
		tw.addSpinTweaker(freq);
		tw.addSpinTweaker(len10);

		JPanel cntrlPanel = new JPanel();

		cntrlPanel.setLayout(new BorderLayout());
		cntrlPanel.add(tw, BorderLayout.NORTH);
		this.fs = client.getSampleRate();

		PingProcess ping = new PingProcess(client);
		client.addInput(ping);
		audioProcess=ping;
		panel.add(threeChoicePanel(), BorderLayout.SOUTH);
		panel.add(cntrlPanel);
	}

	protected void setResults() {
		setResultText(String.format(" Acrruracy estimate %4.3f%%  ",
				tolNow * 100));
	}

	protected void fire(boolean key) {

		double f = freq.doubleValue();
		double l = Math.pow(10, len10.doubleValue());
		double a = amp.doubleValue();
		if (key)
			f *= (1.0 + tolNow);
		doPing(f, l, a);

	}
	
	void doPing(double freq, double l, double amp) {
		double tNext = (client.getFramePos() + client.getFrameSize())
		/ fs + l;
		
		((PingProcess)audioProcess).fire(tNext, freq, l, amp);

	}
	
	/**
	 * decrease tolerance if we guess correctly.
	 * 
	 */
	@Override
	protected void correctResultAction(int guess) {
		tolNow = (1.0 - damp) * tolNow;
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

 class PingProcess extends FiniteAudioProcess {

	private double w;
//
//	private double len;

	private double wQ;
	
	private double tOnInSamples;

	private double tOffInSamples;

	private double tCenterInSamples;

	private double amp;

	private double fs;


	private MyAudioClient sync;

	private boolean isDone = true;

	PingProcess(MyAudioClient sync) {
		this.fs = sync.getSampleRate();
		this.sync = sync;

	}

	public int processAudio(AudioBuffer buffer) {
		if (this.isDone)
			return AUDIO_OK;
		double t1 = this.sync.getFramePos();
		int n = buffer.getSampleCount();
		float buffL[] = buffer.getChannel(0);
		float buffR[] = buffer.getChannel(1);

		if ((t1 + n) < this.tOnInSamples)
			return AUDIO_OK;
		if (t1 > this.tOffInSamples)
			return AUDIO_OK;

		for (int i = 0; i < n; i++) {
			double t = t1 + i;
			if (t > this.tOffInSamples) {
				this.isDone = true;
				wakeUpSleepers();
				break;
			}

			if (t < this.tOnInSamples)
				continue;
			double a = this.tCenterInSamples - t;
			double win = (float) ((1 + Math.cos(this.wQ * a)) * 0.5);
			double s = Math.cos(this.w * a);
		//	 System.out.println(a + " " + win + " " + s);
			buffL[i]=buffR[i] = (float) (win * s * amp);
		}

		return AUDIO_OK;

	}

	public void fire(double tcenter, double freq, double len, double amp) {
		this.w = Math.PI * 2.0 * freq / this.fs;
		double halfT = len / 2;
		this.wQ = Math.PI / halfT / this.fs;

		this.tOnInSamples = (tcenter - halfT) * this.fs;
		this.tOffInSamples = (tcenter + halfT) * this.fs;
		this.tCenterInSamples = tcenter * this.fs;
		this.amp = amp;
		this.isDone = false;
//		System.out.println((this.tCenterInSamples - this.sync.getFramePos() - this.sync
//				.getFrameSize()));
	}

	

	public boolean isDone() {
		return this.isDone;

	}
}