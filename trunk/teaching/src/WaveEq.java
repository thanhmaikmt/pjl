/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author pjl
 */
public class WaveEq {

    int N;
    double s0, s1;
    double u2[];
    double u1[];
    double u[];
    double dt;
    double dx;

    WaveEq() {
      
    
        double vel=1000.0;
        double dt = 1.0e-5;                           // time step

        N=100;

        double dx = 1.0 / N;

        double courrant = vel * dt / dx;

        s0 = 2 * (1 - courrant * courrant);
        s1 = courrant * courrant;



    
        u2 = new double[N];
        u1 = new double[N];
        u = new double[N];

    }



    void setup(){

    double ctr = 0.7, wid = 0.1;             // center location/width of excitation

        double u0 = 1, v0 = 0;                   // maximum initial displacement/velocity

            double xax[] = new double[N];
        double ind[] = new double[N];
        double rc[] = new double[N];

        for (int i = 0; i < N; i++) {
            xax[i] = i * dx;
            ind[i] = Math.signum(Math.max(-(xax[i] - ctr - wid / 2) * (xax[i] - ctr + wid / 2), 0));
            rc[i] = 0.5 * ind[i] * (1.0 + Math.cos(2 * Math.PI * (xax[i] - ctr) / wid));
            u2[i] = u0 * rc[i];
            u1[i] = (u0 + dt * v0) * rc[i];
        }
    }

    
    void step() {
        for (int i = 1; i < N - 1; i++) {
            u[i] = -u2[i] + s0 * u1[i] + s1 * (u1[i - 1] + u1[i + 1]);
            // out[n] = (1 - rp_frac) * u[rp_int] + rp_frac * u[rp_int + 1];     // readout
        }
        double tmp[]=u2;
        u2 = u1;
        u1 = u;
        u=tmp;
    }

    public double[] getState() {
        return u1;
    }
}
