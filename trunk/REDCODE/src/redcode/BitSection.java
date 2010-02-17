/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package redcode;

/**
 *
 * @author pjl
 */
public class BitSection {

    Value val;
    int low;
    int n;
    int mask;
    int sign;
    int maskL;

    BitSection(Value val,int low, int n) {
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
        sign=bit/2;
        maskL=mask >> low;
  //      System.out.println(" mask =" +mask);
    }

    void put(int x) {
        if (x < 0 ) {
            x= -x;
            x = ~x;
            x = x+1;
        }

        int xx = x << low;
        val.x = (val.x & (~mask)) | (xx & mask);
   //     System.out.println( x +  "    "  + val.x);
    }

    int get() {
        int xx= ((val.x & mask) >> low);

        if ( (sign & val.x) != 0 ) {
            xx= xx-1;
            xx= ((~xx) & maskL);
            return -xx;
        }
        return xx;
        
    }


    static public void main(String args[]) {

        Value val=new Value();
        int nBit=6;
        BitSection a=new BitSection(val,0,nBit);
        BitSection b=new BitSection(val,nBit,nBit);


        a.put(-24);
        b.put(-15);
        System.out.println(val.x + " " + a.get() +" " + b.get());


        a.put(-25);
        b.put(1);
        System.out.println(val.x + " " + a.get() +" " + b.get());

//
//
//        a.put(3);
//
//       b.put(-2);
//
//        System.out.println(val.x + " " + a.get() +" " + b.get());

    }
 }
