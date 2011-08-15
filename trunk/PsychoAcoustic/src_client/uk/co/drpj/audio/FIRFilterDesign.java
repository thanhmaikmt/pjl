package uk.co.drpj.audio;

import uk.co.drpj.util.Graphs;
import java.awt.GridLayout;
import javax.swing.JFrame;
import javax.swing.JPanel;

/**
 *  Taken from toot software.
 *
 * @author pjl
 */
public class FIRFilterDesign {

    private int order = -1; // estimated by design()
//    private float transitionBandwidth;
    private float attenuation = -60.0f;
    private float alpha;
    private final int winType;
    private final float bw;

    public float getAlpha() {
        return alpha;
    }
    private float[] a;
    //   private float sampleRate;
    public static final int LPF = 0;
    public static final int HPF = 1;
    public static final int BPF = 2;
    private float frequency;
    float[] win;
    private float[] aRaw;
    private final float fNyquist;
    public static final int RECT = 0;
    public static final int KAISER = 1;

    public FIRFilterDesign(float alpha,
            float sampleRate, float frequency, int type,
            int order, int winType, float bw) {
    
        //      this.sampleRate = sampleRate;
       // this.attenuation = attenuation;
        this.frequency = frequency;
        fNyquist = sampleRate / 2f;
        this.winType = winType;
        this.order = (order / 2) * 2;
        this.bw = bw;
        this.alpha=alpha;
        design(type);
    }

    public int getOrder() {
        return order;
    }

   
    public float getAttenuation() {
        return attenuation;
    }

    public void design(int type) {

        // window function values
        float I0alpha = I0(alpha);
        int m = order / 2;
        win = new float[order + 1];

        switch (winType) {
            case KAISER:

                for (int n = 1; n <= m; n++) {
                    win[n] = I0(alpha * (float) Math.sqrt(1.0f - sqr((float) n / m))) / I0alpha;
                }
                break;

            case RECT:

                for (int n = 1; n <= m; n++) {
                    win[n] = 1.0f;
                }
                break;

        }

     //   float ft = getTransitionBandwidth();
        float w0 = 0.0f;
        float w1 = 0.0f;
        switch (type) {
            case LPF:
                w0 = 0.0f;
                w1 = (float) Math.PI * (frequency) / fNyquist;
                break;
            case HPF:
                w0 = (float) Math.PI;
                w1 = (float) Math.PI * (1.0f - (frequency) / fNyquist);
                break;
            case BPF:
//                w0 = 0.5f * (float)Math.PI * (fl + fh) / fNyquist;
                w0 = (float) Math.PI * frequency / fNyquist;
               // float fb = frequency / 4; // !!!
                w1 =  0.5f*(float) Math.PI * (bw) / fNyquist;
                break;
        }
        // filter coefficients (NB not normalised to unit maximum gain)
        a = new float[order + 1];
        a[0] = w1 / (float) Math.PI;
        aRaw = new float[order + 1];
        aRaw[0] = w1 / (float) Math.PI;

        for (int n = 1; n <= m; n++) {
            a[n] = (float) Math.sin(n * w1) * (float) Math.cos(n * w0) * win[n] / (n * (float) Math.PI);
            aRaw[n] = (float) Math.sin(n * w1) * (float) Math.cos(n * w0) / (n * (float) Math.PI);
        }
        // shift impulse response to make filter causal
        for (int n = m + 1; n <= order; n++) {
            a[n] = a[n - m];
            aRaw[n] = aRaw[n - m];
            win[n] = win[n - m];
        }
        for (int n = 0; n <= m - 1; n++) {
            a[n] = a[order - n];
            aRaw[n] = aRaw[order - n];
            win[n] = win[order - n];
        }
        a[m] = w1 / (float) Math.PI;
        aRaw[m] = w1 / (float) Math.PI;
        win[m] = 1.0f;
    }

//    protected int estimatedOrder(float fNyquist) {
//        // estimate filter order
//        int o = 2 * (int) ((getAttenuation() - 7.95) / (14.36 * getTransitionBandwidth() / fNyquist) + 1.0f);
//        //System.out.println("KF: order="+o+" fN="+fN) ;
//        return o;
//    }

    /**
     * Calculate the zero order Bessel function of the first kind
     */
    protected float I0(float x) {
        float eps = 1.0e-6f; // accuracy parameter
        float fact = 1.0f;
        float x2 = 0.5f * x;
        float p = x2;
        float t = p * p;
        float s = 1.0f + t;
        for (int k = 2; t > eps; k++) {
            p *= x2;
            fact *= k;
            t = sqr(p / fact);
            s += t;
        }
        return s;
    }

    protected float sqr(float x) {
        return x * x;
    }

    public float[] getCoefficients() {
        return a;
    }

    public float[] getRawCoefficients() {
        return aRaw;
    }

    public float[] getWin() {
        return win;
    }

    public static void main(String args[]) {


        float transitionBandwidth = 500.0f;
        float sampleRate = 44100.0f;
        float frequency = sampleRate / 4 - transitionBandwidth;
        float attenuation = 60f;
        int type = FIRFilterDesign.LPF;
        int order = 100;
        float alpha = 5;
        float bw = 50;

        FIRFilterDesign filt = new FIRFilterDesign(attenuation, sampleRate, frequency, type, order, KAISER, bw);

        float coeffs[] = filt.getCoefficients();
        float w[] = new float[coeffs.length];

        float sum = 0.0f;
        for (float a : coeffs) {
            System.out.println(a);
            sum += a;
        }
        // shift impulse response to make filter causal

        //       int order = filt.getOrder();
//        System.out.println(" Sum = " + sum + " Order: " + filt.getOrder()  + "  " + coeffs.length);
//
//        assert(coeffs.length == order);


        JFrame frame = new JFrame();

        JPanel panel = new JPanel();
        panel.setLayout(new GridLayout(3, 2));

        panel.add(Graphs.timePanel(filt.getRawCoefficients(), sampleRate, "Time [s]", "h(t)", "Ideal Impulse response"));
        panel.add(Graphs.fftDBPanel(filt.getRawCoefficients(), sampleRate, "Frequency [Hz]", "Attenuation [dB]", "Attenuation"));
        panel.add(Graphs.timePanel(filt.getWin(), sampleRate, "Time [s]", "w(t)", "Window"));
        panel.add(Graphs.fftDBPanel(filt.getWin(), sampleRate, "Frequency [Hz]", "Attenuation [dB]", "Attenuation (rect window)"));
        panel.add(Graphs.timePanel(coeffs, sampleRate, "Time [s]", "h(t)", "Weighted Impulse response"));
        panel.add(Graphs.fftDBPanel(coeffs, sampleRate, "Frequency [Hz]", "Attenuation [dB]", "Filter Attenuation"));



        frame.setContentPane(panel);
        frame.pack();
        frame.setVisible(true);

    }
}


