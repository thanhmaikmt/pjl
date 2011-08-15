/*
 * Created on May 3, 2007
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

import uk.org.toot.audio.core.AudioProcess;

public abstract class FiniteAudioProcess implements AudioProcess {


	Thread waiter=null;
	
	
	protected void wakeUpSleepers(){
		if (waiter != null) waiter.interrupt();
		waiter=null;
	}
	
	public synchronized void waitTillDone() {
		waiter=Thread.currentThread();
		try {
			wait();
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			// e.printStackTrace();
		}	
	}
	
	public void open() {
	}

	public void close() {
	}
	
}
