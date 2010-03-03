/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package uk.ac.bath.redcode;

/**
 *
 * @author pjl
 */
class RedCodeParseException extends Exception {
    private final String mess;
    int line;
    RedCodeParseException(String mess,int line) {
         this.line=line;
         this.mess=mess;
    }
    String userString() {
        return mess;
    }

    int getLine() {
        return line;
    }
}
