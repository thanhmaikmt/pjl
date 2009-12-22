/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author pjl
 */
public class WaveEq2 { // implements WaveEq {

    int N;
    double s0, s1;
    double V[];
    double DVDT[];
    double I[];
    double DIDT[];
    double dt;
    double dx;
    Boundary boundL;
    Boundary boundR;
    private double t;
    private double L;
    private double C;

    WaveEq2(double C, double L, double dt, double dx, int N) {

        //  double lambda=100*vel*dt;
        //  dx = lambda/100.0;
        this.N = N;
        this.dt = dt;
        this.dx = dx;
        this.L = L;
        this.C = C;

////
        DVDT = new double[N];
        V = new double[N];
        I = new double[N];
        DIDT = new double[N];
    }

    public  void setLeftBoundary(Boundary bL) {
        boundL = bL;
    }

    public void setRightBoundary(Boundary bR) {
        boundR = bR;
    }
//
//    void setup() {
//
//        double ctr = 0.7, wid = 0.1;             // center location/width of excitation
//
//        double u0 = 1, v0 = 0;                   // maximum initial displacement/velocity
//
//        double xax[] = new double[N];
//        double ind[] = new double[N];
//        double rc[] = new double[N];
//
//        for (int i = 0; i < N; i++) {
//            xax[i] = ((float) i) / N;
//            ind[i] = Math.signum(Math.max(-(xax[i] - ctr - wid / 2) * (xax[i] - ctr + wid / 2), 0));
//            rc[i] = 0.5 * ind[i] * (1.0 + Math.cos(2 * Math.PI * (xax[i] - ctr) / wid));
//            u2[i] = u0 * rc[i];
//            u1[i] = (u0 + dt * v0) * rc[i];
//        }
//
//    }

   public  void step() {


        DIDT[0] = -(V[1] - V[0]) / L / dx;

        for (int i = 1; i < N - 2; i++) {
            DVDT[i] = -(I[i] - I[i-1]) / C / dx;
            DIDT[i] = -(V[i+1] - V[i]) / L / dx ;
            // out[n] = (1 - rp_frac) * u[rp_int] + rp_frac * u[rp_int + 1];     // readout
        }

        for (int i = 0; i < N - 1; i++) {
            V[i] += dt*DVDT[i];
            I[i] += dt*DIDT[i];
        }


//        if (boundL != null) {
//            switch (boundL.getType()) {
//                case OPEN:
//                   // u[0] = -u2[0] + s0 * u1[0] + 2 * s1 * u1[1];
//                    break;
//                case FIXED:
//                    V[0] = ((PulseSource) boundL).getValue(t);
//            }
//        }
//
//
//        if (boundR != null) {
//            switch (boundR.getType()) {
//
//                case OPEN:
//                //    u[N - 1] = -u2[N - 1] + s0 * u1[N - 1] + 2 * s1 * u1[N - 2];
//                    break;
//                case FIXED:
//                    V[N - 1] = ((PulseSource) boundR).getValue(t);
//            }
//        }

        t += dt;
    }

    public double[] getState() {
        return V;
    }

   public  double getTime() {
        return t;
    }

    public void setLeftBoundary(PulseSource boundL) {
        throw new UnsupportedOperationException("Not supported yet.");
    }
}
