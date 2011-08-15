package tests;

import java.util.Date;

import rasmus.interpreter.sampled.util.FFT;

import edu.cornell.lassp.houle.RngPack.Ranlux;

public class RandomTest {

	static Ranlux r = new Ranlux(4, new Date());

	public static void main(String args[]) {
		int fftlen = 512;
		double in[] = new double[2 * fftlen];

		FFT fft = new FFT(fftlen);

		for (int i = 0; i < fftlen; i++) {
			in[2*i] = 2*(0.5-r.raw());
			in[2*i+1]=0;
		}

		fft.calc(in, -1);

		for (int i = 0; i < fftlen; i++) {
			System.out.println(in[2 * i] + "  " + in[2 * i + 1]);
		}

	}
}
