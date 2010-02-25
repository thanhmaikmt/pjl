/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package redcode;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.StreamTokenizer;
import java.io.StringReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author pjl
 */
public class Prism {

    ArrayList<String> lines = new ArrayList<String>();
    HashMap<String, Integer> tokens = new HashMap<String, Integer>();

    void load(BufferedReader reader) {


        //   String parseLine;

        String str1 = null;
        int loc = 0;
        while (true) {
            try {
                str1 = reader.readLine();
                if (str1 == null) {
                    break;
                }
                str1 = str1.trim();
                System.out.println(str1);
            } catch (IOException ex) {
                break;
            }
            lines.add(str1);
            int ii = str1.indexOf(":");
            if (ii > 0) {
                String tok = str1.substring(0, ii);
                tokens.put(tok, loc);
                str1 = str1.substring(ii + 1);
            }
            lines.add(str1);
            loc++;
        }

        loc = 0;
        for (String line : lines) {
            line = line.trim();
            String toks[] = line.split("[ \t]+");

            toks[1] = crackOp(toks[1]);

            line = toks[0] + " " + toks[1];
            if (toks.length > 2) {
                toks[2] = crackOp(toks[2]);
                line = line + " " + toks[2];
            }
            loc++;
        }

    }

    private String crackOp(String str) {
        String ret = "";
        str = str.trim();
        StreamTokenizer toker = new StreamTokenizer(new StringReader(str));

        int sign = 1;
        Integer val = null;
        // boolean first = true;

        toker.ordinaryChar('-');
        try {
            while (toker.nextToken() != StreamTokenizer.TT_EOF) {
                if (toker.ttype == StreamTokenizer.TT_EOL) {
                    break;
                }
                if (toker.ttype == StreamTokenizer.TT_WORD) {
                    String lab = toker.sval;
//                    if (first) {
//                        ret = ret + lab + " ";
//                        first = false;
//                    } else {
                    int lineNo = tokens.get(lab);
                    System.out.println("WORD:" + toker.sval + " line: " + lineNo);
                    //        }
                } else if (toker.ttype == StreamTokenizer.TT_NUMBER) {
                    System.out.println("NUMBER:" + toker.nval);
                } else {
                    char c = (char) (toker.ttype);

                    switch (c) {
                        case '+':
                            break;
                        case '-':
                            sign = -1;
                            break;
                        case '#':
                            ret
                    
                    }
                    System.out.println("XX:" + c);

                    if (val == null) {
                        }

            }
        } catch (IOException ex) {
            Logger.getLogger(Prism.class.getName()).log(Level.SEVERE, null, ex);
        }
        return "null";


    }

    public static void main(String args[]) {
        String str = "X: DAT 0\n  MOV #1 X";
        BufferedReader reader = new BufferedReader(new StringReader(str));

        new Prism().load(reader);

//        StreamTokenizer toker = new StreamTokenizer(new StringReader(str));
//        int type;
//        toker.ordinaryChar('-');
//        try {
//            while (toker.nextToken() != StreamTokenizer.TT_EOF) {
//                System.out.println(toker);
//            }
//        } catch (IOException ex) {
//            Logger.getLogger(Prism.class.getName()).log(Level.SEVERE, null, ex);
//        }

    }
}
