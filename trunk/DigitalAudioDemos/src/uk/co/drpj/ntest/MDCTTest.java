/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package uk.co.drpj.ntest;

import mediaframe.mpeg4.audio.AAC.MDCT;

/**
 *
 * @author pjl
 */
public class MDCTTest {

    public static void main(String args[]) {
        test2();
    }

    static void test1() {
        int N = 4;
        int nHalf = N / 2;
        int nFrame = 4;
        float in[] = new float[N * nFrame];
        float out[] = new float[N * nFrame];
        float buff[] = new float[N];
        int pos = nFrame * N / 2;
        in[pos] = 1.0f;
        int b = N/2;





        for (int i = 0; i < nFrame * 2 - 2; i++) {
            int i1 = i * nHalf;
            System.arraycopy(in, i1, buff, 0, N);
            MDCT.Transform(buff, N, b);
            MDCT.ITransform(buff, N, b);
            for (int j = 0; j < N ; j++) {
                out[i1 + j] += buff[j]*0.5;
            }
        }


        for (float x : out) {
            System.out.println(x);
        }


    }

    static void test2() {
        int N = 8;

        for (int i = 0; i < N; i++) {

            float buff[] = new float[N];
            buff[i] = 1.0f;
            MDCT.ITransform(buff, N, N/2);
            for (int k = 0; k < N; k++) {
                System.out.print(buff[k] + " ");
            }
            System.out.println();
        }
    }

    static void test3() {
        int N = 8;



        for (int i = 0; i < N; i++) {

            float buff[] = new float[N];
            buff[i] = 1.0f;
            MDCT.ITransform(buff, N, N/2);
            for (int k = 0; k < N; k++) {
                System.out.print(buff[k] + " ");
            }
            System.out.println();
        }
    }


}
