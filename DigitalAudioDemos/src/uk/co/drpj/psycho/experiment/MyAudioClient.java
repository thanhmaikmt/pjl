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

import java.util.Vector;


import uk.org.toot.audio.core.AudioBuffer;
import uk.org.toot.audio.core.AudioProcess;
import uk.org.toot.audio.server.AudioClient;



public class MyAudioClient implements AudioClient, SyncSource {

	long framePos = 0;

	private int frameSize;

	private AudioBuffer buffer;

	private AudioProcess out;

	Vector<AudioProcess> inputs = new Vector<AudioProcess>();

	private double rate;

	public MyAudioClient(AudioProcess out,double rate) {
		this.out = out;
		this.rate=rate;

	}

	public void work(int size) {
		if (buffer == null || size != frameSize) {
			this.frameSize = size;
			this.buffer =  new AudioBuffer(null, 2, size, 44100.0f);
		}
		this.buffer.makeSilence();
		for (AudioProcess in : this.inputs) {
			in.processAudio(this.buffer);
		}
		this.out.processAudio(this.buffer);
		this.framePos += this.frameSize;

	}

	public long getFramePos() {
		return (long) this.framePos;
	}

	public void addInput(AudioProcess input) {
		this.inputs.add(input);
	}

	public int getFrameSize() {
		return this.frameSize;
	}

	public double getSampleRate() {
		return rate;
	}
	
	public long milliToSamples(double ms) {
		return (long) ((rate*ms)/1000.0);
	}

    public void setEnabled(boolean arg0) {
        // throw new UnsupportedOperationException("Not supported yet.");
    }
}
