/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author pjl
 */
interface WaveEq {

    public void setLeftBoundary(Boundary boundL);

    public void setRightBoundary(Boundary boundR);

    public double[] getState();

    public void step();

    public double getTime();

}
