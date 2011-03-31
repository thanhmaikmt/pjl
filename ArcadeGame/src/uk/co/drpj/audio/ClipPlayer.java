/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package uk.co.drpj.audio;

import uk.org.toot.audio.core.AudioProcess;

/**
 *
 * @author pjl
 */
public interface ClipPlayer extends AudioProcess {

    void setLooping(boolean yes);
}
