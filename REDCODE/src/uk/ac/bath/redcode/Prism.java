package uk.ac.bath.redcode;

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
    int parseLine;

    String load(BufferedReader reader) throws RedCodeParseException {

        String redCode="";

        String line = null;

        while (true) {
            try {
                line = reader.readLine();
                if (line == null) {
                    break;
                }
                line = line.trim();
         //       System.out.println(line);
            } catch (IOException ex) {
                break;
            }
            int ii = line.indexOf(":");
            if (ii > 0) {
                String tok = line.substring(0, ii);
                if (tokens.containsKey(tok)) {
                    throw new RedCodeParseException(" Label : "+tok+ "  already defined on line "+tokens.get(tok), parseLine);
                }
                tokens.put(tok, parseLine);
                line = line.substring(ii + 1);
            }
            lines.add(line);
            parseLine++;
        }

        parseLine = 0;
        for (String inLine : lines) {
            inLine = inLine.trim();
            System.out.println(":" + inLine);
            String toks[] = inLine.split("[ \t]+");
            line = toks[0];
            if (toks.length > 1) {
                toks[1] = crackOp(toks[1]);
                line = line + " " + toks[1];

            }

            if (toks.length > 2) {
                toks[2] = crackOp(toks[2]);
                line = line + " " + toks[2];
            }
            parseLine++;
            System.out.println(">" + line);
            redCode = redCode + line +"\n";
        }
        return redCode;
    }

    private String crackOp(String str) throws RedCodeParseException {
        System.out.println(" Cracking op:" + str);
        String ret = "";
        str = str.trim();
        StreamTokenizer toker = new StreamTokenizer(new StringReader(str));

        int sign = 1;

        //Integer val = null;
        // boolean first = true;

        int val = 0;
        toker.ordinaryChar('-');
        toker.wordChars('\'', '\'');
        try {
            while (toker.nextToken() != StreamTokenizer.TT_EOF) {


                if (toker.ttype == StreamTokenizer.TT_EOL) {
                    break;
                }
                if (toker.ttype == StreamTokenizer.TT_WORD) {
                    String lab = toker.sval;
                    if (lab.charAt(0) =='\'') return ret+lab;
                        

                    if (!tokens.containsKey(lab))
                        throw new RedCodeParseException("no value for symmbol: "+lab,parseLine);
                    int lineNo = tokens.get(lab);
                    System.out.println("WORD:" + toker.sval + " line: " + lineNo);
                    val += sign * (lineNo - parseLine);
                } else if (toker.ttype == StreamTokenizer.TT_NUMBER) {
                   System.out.println("NUMBER:" + toker.nval);
                    val += sign * (int) toker.nval;

                } else {
                    char c = (char) (toker.ttype);

                    switch (c) {
                        case '+':
                            break;
                        case '-':
                            sign = -1;
                            break;
                        case '#':
                            ret = "#";
                            break;
                        case '@':
                            ret = "@";
                            break;


                    }
                    System.out.println("XX:" + c);

                }
            }
        } catch (IOException ex) {
            Logger.getLogger(Prism.class.getName()).log(Level.SEVERE, null, ex);
        }
        return ret + val;


    }

    public static void main(String args[]) throws RedCodeParseException {
        String str = "MOV  #'Q'  1\n";
        //str = "CMP -5 #-1";
        Prism prism=new Prism();
        System.out.print(prism.compile(str));
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

    String compile(String inText) throws RedCodeParseException {
        BufferedReader reader = new BufferedReader(new StringReader(inText));
        return load(reader);
       
    }
}
