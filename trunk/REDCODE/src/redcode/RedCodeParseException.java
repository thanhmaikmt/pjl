/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package redcode;

/**
 *
 * @author pjl
 */
class RedCodeParseException extends Exception {
    private final String line;

    RedCodeParseException(String line,String mess) {
        super(mess);
        this.line=line;
    }
}
