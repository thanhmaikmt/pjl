/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package uk.ac.bath.redcode;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.StreamTokenizer;
import java.io.StringReader;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author pjl
 */
class Pretty {

    static String makePretty(String inText) {
        BufferedReader reader = new BufferedReader(new StringReader(inText));
        String redCode = "";

        while (true) {

            String inLine = null;
            try {
                inLine = reader.readLine();
            } catch (IOException ex) {
                Logger.getLogger(Pretty.class.getName()).log(Level.SEVERE, null, ex);
            }

            if (inLine == null) {
                break;
            }

            inLine = inLine.trim();

            String toks[] = inLine.split("[ \t]+");

            String line;

            int cnt = 0;

            if (!toks[0].contains(":")) {
                line = String.format("%-6s ", " ");
            } else {
                line = String.format("%-6s ", toks[0]);
                cnt = 1;
            }

            if (toks.length > cnt) {
                line = line + String.format("%-3s ", toks[cnt]);
                cnt++;
            }

            for (; cnt < toks.length; cnt++) {
                line = line + String.format("%6s ", toks[cnt]);
            }

            redCode = redCode + line + "\n";


        }
        return redCode;
    }
}
