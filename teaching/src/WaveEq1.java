/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author pjl
 */
public class WaveEq1 implements WaveEq {

    int N;
    double s0, s1;
    double u2[];
    double u1[];
    double u[];
    double dt;
    double dx;
    Boundary boundL;
    Boundary boundR;
    private double t;

    WaveEq1(double vel, double dt, double dx, int N) {

        //  double lambda=100*vel*dt;
        //  dx = lambda/100.0;
        this.N = N;
        this.dt = dt;
        this.dx = dx;

////

        // See sadiku page 147
        double r = (vel * dt / dx);

        System.out.println(" Courant number = "+ r);
        r = r * r;

        s0 = 2 * (1 - r);
        s1 = r;




        u2 = new double[N];
        u1 = new double[N];
        u = new double[N];

    }

    public void setLeftBoundary(Boundary bL) {
        boundL = bL;
    }

    public void setRightBoundary(Boundary bR) {
        boundR = bR;
    }

    void setup() {

        double ctr = 0.7, wid = 0.1;             // center location/width of excitation

        double u0 = 1, v0 = 0;                   // maximum initial displacement/velocity

        double xax[] = new double[N];
        double ind[] = new double[N];
        double rc[] = new double[N];

        for (int i = 0; i < N; i++) {
            xax[i] = ((float) i) / N;
            ind[i] = Math.signum(Math.max(-(xax[i] - ctr - wid / 2) * (xax[i] - ctr + wid / 2), 0));
            rc[i] = 0.5 * ind[i] * (1.0 + Math.cos(2 * Math.PI * (xax[i] - ctr) / wid));
            u2[i] = u0 * rc[i];
            u1[i] = (u0 + dt * v0) * rc[i];
        }

    }

    public void step() {


        for (int i = 1; i < N - 1; i++) {
            u[i] = -u2[i] + s0 * u1[i] + s1 * (u1[i - 1] + u1[i + 1]);           
        }


        Double imp = boundL.imp;

      
        if (imp == Double.POSITIVE_INFINITY) {
            u[0] = -u2[0] + s0 * u1[0] + 2 * s1 * u1[1];
        }    else if (imp <= 1.0) {
            u[0] =  boundL.getValue(t)+u1[0] - imp * s1 * (u1[0] - u1[1]);
        } else if (imp > 1.0) {
            double nimp=1.0/imp;
            u[0] = (1.0-nimp)*(-u2[0] + s0 * u1[0] + 2 * s1 * u1[1])
            + nimp*(u1[0] -  s1 * (u1[0] - u1[1]));
        }

        //u[0] = boundL.getValue(t);


        imp = boundR.imp;

        if (imp == Double.POSITIVE_INFINITY) {
            u[N - 1] = -u2[N - 1] + s0 * u1[N - 1] + 2 * s1 * u1[N - 2];
        } else if (imp <= 1.0) {
            u[N - 1] = u1[N - 1] - imp * s1 * (u1[N - 1] - u1[N - 2]);
        } else if (imp > 1.0) {
            double nimp=1.0/imp;
            u[N - 1] = (1.0-nimp)*(-u2[N - 1] + s0 * u1[N - 1] + 2 * s1 * u1[N - 2])
            + nimp*(u1[N - 1] -  s1 * (u1[N - 1] - u1[N - 2]));
        }


        double tmp[] = u2;
        u2 = u1;
        u1 = u;
        u = tmp;
        t += dt;
    }

    public double[] getState() {
        return u1;
    }

    public double getTime() {
        return t;
    }
}
