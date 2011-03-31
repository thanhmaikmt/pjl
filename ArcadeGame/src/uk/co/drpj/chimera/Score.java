/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package uk.co.drpj.chimera;

/**
 *
 * @author pjl
 */
class Score implements Comparable<Score> {

    String name;
    int score;
    Score(String name, int score) {
        this.name=name;
        this.score=score;
    }

    public int compareTo(Score arg0) {
        if (score > arg0.score) return -1;
        return 1;
    }

}
