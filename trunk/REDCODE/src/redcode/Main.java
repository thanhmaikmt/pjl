/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package redcode;

import java.io.BufferedReader;
import java.io.StringReader;

/**
 *
 * @author pjl
 */
public class Main {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) throws RedCodeParseException {

        Machine mach = new Machine(10);

        String str = " MOV 0 1\n SUB #1 @3\nADD @7 @9\nMOV @-3 -1\n";

        BufferedReader reader = new BufferedReader(new StringReader(str));
        // TODO code application logic here

        System.out.println(mach.toString());

        mach.load(reader);

        System.out.println(mach.toString());

        mach.step();

        System.out.println(mach.toString());
        mach.step();

        System.out.println(mach.toString());

    }
}
