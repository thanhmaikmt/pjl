/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package uk.ac.bath.redcode;

/**
 *
 * @author pjl
 */
public class UBitSection {

    Machine.Value val;
    int low;
    int n;
    int mask;
    //int sign;
    int maskL;

    UBitSection(Machine.Value val,int low, int n) {
        this.val=val;
        this.n = n;
        int bit = 1;
        this.low=low;

        for (int i = 0; i < low; i++) {
            bit *= 2;
        }

        mask = 0;
        for (int i = 0; i < n; i++) {
            mask += bit;
            bit *= 2;
        }
      //  sign=bit/2;
        maskL=mask >> low;
  //      System.out.println(" mask =" +mask);
    }

    void put(int x) {
        int xx = x << low;
        val.x = (val.x & (~mask)) | (xx & mask);
   //     System.out.println( x +  "    "  + val.x);
    }

    int get() {
        int xx= ((val.x & mask) >> low);
        return xx;
        
    }


    
 }
