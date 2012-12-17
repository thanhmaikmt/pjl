package GM.util;

public class MyMath {
    public MyMath() {
    }

    static public double halfLifeToLambda(double halfLifeInTicks) {
        // N=halfLifeInTicks
        // decay^N = 0.5
        // N ln(decay)= ln(0.5)
        // decay = e^(ln(0.5)/N)

        return Math.exp(Math.log(0.5)/halfLifeInTicks);


    }

}
