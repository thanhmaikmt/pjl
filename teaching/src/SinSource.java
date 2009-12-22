/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */



/**
 *
 * @author pjl
 */
public class SinSource implements Source {

 
    private final double wid;
   
    int type;
    private double tFire=Double.NEGATIVE_INFINITY;

    SinSource(double wid) {
        this.wid=wid;
       
    }

    public void fireAt(double tFire) {
        this.tFire=tFire;
    }
    
    public double getValue(double t) {
        t=t - tFire;
        if (t > wid || t < 0 ) return 0;
        return 0.5 * (1.0 - Math.cos(2 * Math.PI * t / wid));
    }

    public static void main(String arg[]) {

        double period=100.0;
        PulseSource b= new PulseSource( 10.0);

        double dt=.31;

        for (double t=0.0;t<period*10;t+=dt) {
            System.out.println(b.getValue(t));
        }


    }


  
}
